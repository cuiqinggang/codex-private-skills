#!/usr/bin/env python3
"""Exercise real Louez UI mutations on dedicated local synthetic data.

No database writes, auth fabrication, browser cookie extraction, or automatic retries.
Prefers its existing native oRPC HTTP client; Next-Action is a guarded fallback.
HTTP 200 is not success: the decoded business result must contain success:true.
The report separately requires database readback before a business-integrity verdict.

Examples (run against dedicated synthetic orders only):
  python louez-concurrency.py --source C:\\AI\\Rental-N001-20261028\\Louez --discover-only
  python louez-concurrency.py --source ... --cookie-file test-cookie.json \
    --reservation-id ORDER --mode deposit-refund --amount 100.00 --report refund.json
  python louez-concurrency.py --source ... --cookie-file test-cookie.json \
    --reservation-ids ORDER_A,ORDER_B --mode checkout --report pickup.json
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
from decimal import Decimal, InvalidOperation
import hashlib
import http.client
from http.cookies import SimpleCookie
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import time
from urllib.parse import urlsplit

ACTION_NAMES = ("recordPayment", "returnDeposit", "deletePayment", "updateReservationStatus", "createManualReservation")
HASH_RE = re.compile(r"^[0-9a-f]{40,64}$")
ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,80}$")

ORPC_NAMES = {"recordPayment": "recordPayment", "returnDeposit": "returnDeposit",
              "deletePayment": "deletePayment", "updateReservationStatus": "updateStatus",
              "createManualReservation": "createManualReservation"}


def discover_orpc(source):
    web = source / "apps" / "web" if (source / "apps" / "web").is_dir() else source
    route = web / "app" / "api" / "rpc" / "[...path]" / "route.ts"
    client = web / "lib" / "orpc" / "client.ts"
    router = web.parents[1] / "packages" / "api" / "src" / "routers" / "dashboard" / "reservations.ts"
    if not all(path.is_file() for path in (route, client, router)):
        return {}, {"verified": False, "reason": "Required existing oRPC source files were not found"}
    route_text, client_text, router_text = (path.read_text(encoding="utf-8") for path in (route, client, router))
    required = ('prefix: "/api/rpc"', 'dashboardReservationActions:',
                'from "@/app/(dashboard)/dashboard/reservations/actions"')
    valid = (all(marker in route_text for marker in required) and 'new RPCLink' in client_text and
             all(f"context.dashboardReservationActions?.{name}" in router_text for name in ORPC_NAMES) and
             all(f"const {procedure} =" in router_text for procedure in ORPC_NAMES.values()))
    procedures = {name: "dashboard.reservations." + procedure for name, procedure in ORPC_NAMES.items()} if valid else {}
    return procedures, {"verified": valid, "web_root": str(web), "prefix": "/api/rpc",
                        "route": str(route), "client": str(client), "router": str(router),
                        "call_chain": "existing UI -> native oRPC RPCLink HTTP -> router -> injected original actions.ts"}


ORPC_RUNNER = r'''
import {createORPCClient} from '@orpc/client';
import {RPCLink} from '@orpc/client/fetch';
let inputText=''; for await (const chunk of process.stdin) inputText += chunk;
const input=JSON.parse(inputText);
const http={attempted_requests:0,status_counts:{}};
const link=new RPCLink({url:new URL('/api/rpc', input.base).toString(),
  headers:()=>({Cookie:input.cookie, Origin:new URL(input.base).origin}),
  fetch:async (request,init)=>{
    http.attempted_requests++;
    const response=await fetch(request,{...init,signal:AbortSignal.timeout(input.timeoutMs)});
    http.status_counts[response.status]=(http.status_counts[response.status]??0)+1;
    return response;
  }});
const client=createORPCClient(link);
let release; const gate=new Promise(resolve=>release=resolve);
const pending=input.tasks.map(async (task,index)=>{
  await gate; const started=performance.now();
  try {
    let fn=client; for(const part of task.procedure.split('.')) fn=fn[part];
    const result=await fn(task.input);
    const outcome=result?.success===true && !result.error ? 'success' :
      typeof result?.error==='string' ? 'business_error' : 'unexpected';
    return {request:index,reservation_id:task.reservation_id,outcome,result,
      seconds:Number(((performance.now()-started)/1000).toFixed(4))};
  } catch(error) {
    const business=error?.code==='BAD_REQUEST' && typeof error?.message==='string' && error.message.startsWith('errors.');
    return {request:index,reservation_id:task.reservation_id,
      outcome:business?'business_error':(error?.code?'unexpected':'unknown'),
      result:business?{error:error.message}:undefined,
      error:business?undefined:String(error?.code??error?.name??'NetworkError'),
      seconds:Number(((performance.now()-started)/1000).toFixed(4)),automatic_retry:false};
  }
});
release(); const results=await Promise.all(pending);
process.stdout.write(JSON.stringify({results,http,transport:'existing_native_orpc_RPCLink_HTTP'}));
'''


def invoke_orpc_batch(base, cookie, tasks, web_root, timeout, node="node"):
    executable = shutil.which(node)
    if not executable:
        raise ValueError("Installed Node runtime is required for the existing native oRPC client")
    payload = {"base": base, "cookie": cookie, "tasks": tasks, "timeoutMs": int(timeout * 1000)}
    try:
        completed = subprocess.run([executable, "--input-type=module", "-e", ORPC_RUNNER],
                                   input=json.dumps(payload), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding="utf-8", errors="replace", cwd=str(web_root),
                                   timeout=timeout + 30, shell=False)
        if completed.returncode:
            # An unexpected child termination can follow committed writes.
            return ([{"request": index, "reservation_id": task["reservation_id"], "outcome": "unknown",
                      "error": "Native_oRPC_child_exit_" + str(completed.returncode), "automatic_retry": False}
                     for index, task in enumerate(tasks)], {"child_exit_code": completed.returncode})
        data = json.loads(completed.stdout)
        return data["results"], data["http"]
    except (subprocess.TimeoutExpired, ValueError, KeyError):
        return ([{"request": index, "reservation_id": task["reservation_id"], "outcome": "unknown",
                  "error": "Native_oRPC_child_result_unknown", "automatic_retry": False}
                 for index, task in enumerate(tasks)], {"child_result": "unknown"})


def discover_actions(source: Path) -> tuple[dict, dict]:
    roots = [source / "apps" / "web" / ".next", source / ".next", source]
    next_root = next((p for p in roots if (p / "server" / "server-reference-manifest.json").is_file()), None)
    if next_root is None:
        raise ValueError("No completed .next/server/server-reference-manifest.json under --source")
    manifest_path = next_root / "server" / "server-reference-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidates = {name: set() for name in ACTION_NAMES}
    known_ids = set()
    provenance = {}
    for runtime in ("node", "edge"):
        for action_id, entry in manifest.get(runtime, {}).items():
            if not HASH_RE.fullmatch(action_id):
                continue
            known_ids.add(action_id)
            name = entry.get("exportedName")
            filename = str(entry.get("filename", "")).replace("\\", "/")
            if name in candidates and (not filename or "reservations/actions" in filename):
                candidates[name].add(action_id)
                provenance.setdefault(name, []).append({"kind": "manifest", "file": str(manifest_path)})
    missing = [name for name, ids in candidates.items() if not ids]
    if missing:
        # Fifth createServerReference argument is the exported name. Restrict the
        # preceding window to that call, and cross-check IDs against this build.
        for chunk in (next_root / "static" / "chunks").rglob("*.js"):
            text = chunk.read_text(encoding="utf-8", errors="replace")
            for name in missing:
                for match in re.finditer(r'["\']' + re.escape(name) + r'["\']', text):
                    if not text[match.end():match.end() + 100].lstrip().startswith(")"):
                        continue  # An export-map name is not the call's fifth argument.
                    window = text[max(0, match.start() - 1800):match.end()]
                    ref_pos = window.rfind("createServerReference")
                    if ref_pos < 0:
                        continue
                    call = window[ref_pos:]
                    if ";" in call:
                        continue  # Do not associate a name with a previous statement.
                    hashes = re.findall(r'["\']([0-9a-f]{40,64})["\']', call)
                    if len(hashes) == 1 and hashes[0] in known_ids:
                        candidates[name].add(hashes[0])
                        provenance.setdefault(name, []).append({"kind": "client_chunk", "file": str(chunk)})
    result = {}
    problems = []
    for name, ids in candidates.items():
        if len(ids) == 1:
            result[name] = next(iter(ids))
        elif len(ids) > 1:
            problems.append(f"Ambiguous action {name}: {len(ids)} IDs; do not guess")
    return result, {"next_root": str(next_root), "manifest": str(manifest_path),
                    "provenance": provenance, "problems": problems,
                    "missing": [name for name in ACTION_NAMES if name not in result]}


def read_cookie(path: Path) -> str:
    raw = path.read_text(encoding="utf-8-sig").strip()
    try:
        value = json.loads(raw)
    except ValueError:
        value = raw
    if isinstance(value, dict):
        value = value.get("cookie", value.get("cookieHeader", value.get("cookies")))
    if isinstance(value, list):
        if all(isinstance(c, dict) and "name" in c and "value" in c for c in value):
            value = "; ".join(f'{c["name"]}={c["value"]}' for c in value)
        elif all(isinstance(c, str) for c in value):
            jar = SimpleCookie()
            for item in value:
                jar.load(item.removeprefix("Set-Cookie:").strip())
            value = "; ".join(f"{name}={morsel.value}" for name, morsel in jar.items())
    if not isinstance(value, str) or not value:
        raise ValueError("Cookie file must contain a Cookie header string or JSON cookie/cookies")
    value = value.removeprefix("Cookie:").strip()
    if "\n" in value or "\r" in value:
        raise ValueError("Cookie header must be a single line; never paste a full response")
    if "=" not in value:
        raise ValueError("Cookie file does not contain a cookie pair")
    return value


def parse_action_result(body: str) -> dict:
    """Decode just plain JSON action results, following root.a Flight references.

    Deliberately rejects unsupported Flight forms instead of mistaking rendered
    page strings, HTTP 200, redirects, or an error digest for action success.
    """
    rows = {}
    server_errors = {}
    for line in body.splitlines():
        match = re.match(r"^([0-9a-f]+):(.*)$", line)
        if not match:
            continue
        row_id, payload = match.groups()
        if payload.startswith("E"):
            try:
                server_errors[row_id] = json.loads(payload[1:])
            except ValueError:
                server_errors[row_id] = {"message": "Unparsed server exception"}
            continue
        try:
            rows[row_id] = json.loads(payload)
        except ValueError:
            # Flight module, debug, resource, and binary records are irrelevant
            # to this narrow plain-object action-result decoder.
            continue
    root = rows.get("0")
    if not isinstance(root, dict) or "a" not in root:
        raise ValueError("RSC root has no action result (a); authentication/route/protocol must be checked")
    value = root["a"]
    seen = set()
    while isinstance(value, str) and re.fullmatch(r"\$(?:@|L)?[0-9a-f]+", value):
        row_id = re.sub(r"^\$(?:@|L)?", "", value)
        if row_id in seen:
            raise ValueError("Cyclic Flight action reference")
        seen.add(row_id)
        if row_id in server_errors:
            error = server_errors[row_id]
            raise ValueError("Server action exception; digest=" + str(error.get("digest", "unknown")))
        if row_id not in rows:
            raise ValueError("Missing Flight result row " + row_id)
        value = rows[row_id]
    if not isinstance(value, dict):
        raise ValueError("Action returned an unsupported non-object result")
    if value.get("success") is True and "error" not in value:
        return {"outcome": "success", "result": value}
    if isinstance(value.get("error"), str) and value["error"]:
        return {"outcome": "business_error", "result": value}
    raise ValueError("Action object contains neither explicit success:true nor error:string")


def invoke(base, cookie, action_id, reservation_id, args, route_template, timeout):
    route = route_template.format(reservation_id=reservation_id)
    if not route.startswith("/") or route.startswith("//") or "\r" in route or "\n" in route:
        raise ValueError("--route must be a same-origin absolute path")
    connection_type = http.client.HTTPSConnection if base.scheme == "https" else http.client.HTTPConnection
    connection = connection_type(base.hostname, base.port, timeout=timeout)
    origin = f"{base.scheme}://{base.netloc}"
    started = time.monotonic()
    try:
        # React encodeReply for these plain JSON arguments is the JSON string.
        connection.request("POST", route, json.dumps(args, separators=(",", ":")).encode("utf-8"), {
            "Accept": "text/x-component", "Content-Type": "text/plain;charset=UTF-8",
            "Next-Action": action_id, "Origin": origin, "Referer": origin + route, "Cookie": cookie,
        })
        response = connection.getresponse()
        raw = response.read()
        body = raw.decode("utf-8", errors="replace")
        result = {"reservation_id": reservation_id, "http_status": response.status,
                  "content_type": response.getheader("Content-Type", ""),
                  "response_sha256": hashlib.sha256(raw).hexdigest(),
                  "seconds": round(time.monotonic() - started, 4)}
        if response.getheader("x-action-redirect"):
            return result | {"outcome": "unexpected", "error": "Action redirected; verify authenticated dedicated account"}
        if response.status != 200 or not result["content_type"].startswith("text/x-component"):
            return result | {"outcome": "unexpected", "error": "Invalid action status/content type; no success inferred"}
        try:
            return result | parse_action_result(body)
        except ValueError as exc:
            return result | {"outcome": "unexpected", "error": str(exc)}
    except Exception as exc:
        # A lost response can follow a committed write. Never blindly retry.
        return {"reservation_id": reservation_id, "outcome": "unknown", "error": type(exc).__name__,
                "seconds": round(time.monotonic() - started, 4), "automatic_retry": False}
    finally:
        connection.close()


def self_test():
    assert parse_action_result('0:{"a":"$@1","f":[]}\n1:{"success":true,"paymentId":"test"}\n')["outcome"] == "success"
    assert parse_action_result('1:{"error":"errors.amountExceedsDeposit"}\n0:{"a":"$@1"}\n')["outcome"] == "business_error"
    assert parse_action_result('0:{"a":{"success":true}}\n')["outcome"] == "success"
    for body in ('0:{"f":[]}\n', '0:{"a":"$@1"}\n1:E{"digest":"123"}\n', '0:{"a":{"success":false}}\n'):
        try:
            parse_action_result(body)
        except ValueError:
            continue
        raise AssertionError("Parser accepted unsupported/error body")
    print("6 synthetic protocol-parser assertions passed; no live Louez test was run.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="http://localhost:4399")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--transport", choices=("auto", "orpc", "next-action"), default="auto")
    parser.add_argument("--node", default="node")
    parser.add_argument("--cookie-file", type=Path)
    parser.add_argument("--reservation-id")
    parser.add_argument("--reservation-ids", help="Comma-separated dedicated confirmed orders for physical checkout competition")
    parser.add_argument("--mode", choices=("deposit-refund", "checkout", "booking"))
    parser.add_argument("--payload-file", type=Path, help="Existing-customer, one-product quantity-1 booking input JSON")
    parser.add_argument("--amount", help="Full remaining refundable deposit, decimal currency units; required for deposit-refund")
    parser.add_argument("--method", choices=("cash", "card", "transfer", "check", "other"), default="cash")
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--route", default="/dashboard/reservations/{reservation_id}")
    parser.add_argument("--check-delete-payment-id", help="After refund, attempt deletion of its original deposit receipt; must be rejected")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--discover-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    options = parser.parse_args()
    if options.self_test:
        self_test()
        return 0
    if not options.source:
        parser.error("--source is required")
    base = urlsplit(options.base)
    if base.scheme not in ("http", "https") or base.hostname not in ("localhost", "127.0.0.1", "::1") or base.username or base.password:
        parser.error("This acceptance script only operates on an explicit local loopback service")
    actions, discovery = discover_actions(options.source)
    procedures, orpc_discovery = discover_orpc(options.source)
    discovery["orpc"] = orpc_discovery
    transport = "orpc" if options.transport == "auto" and procedures else (
        "next-action" if options.transport == "auto" else options.transport)
    if options.discover_only:
        print(json.dumps({"transport": transport, "actions": actions, "procedures": procedures,
                          "discovery": discovery}, ensure_ascii=False, indent=2))
        return 0
    if not options.cookie_file or not options.mode:
        parser.error("--cookie-file and --mode are required for a real mutation")
    if not 2 <= options.workers <= 64:
        parser.error("--workers must be in 2..64")
    booking_input = None
    if options.mode == "booking":
        if transport != "orpc" or not options.payload_file:
            parser.error("booking requires verified native oRPC and --payload-file")
        booking_input = json.loads(options.payload_file.read_text(encoding="utf-8-sig"))
        if isinstance(booking_input, dict) and "payload" not in booking_input:
            booking_input = {"payload": booking_input}
        payload = booking_input.get("payload") if isinstance(booking_input, dict) else None
        if not isinstance(payload, dict) or not isinstance(payload.get("customerId"), str) or len(payload["customerId"]) != 21:
            parser.error("booking requires a dedicated existing 21-character customerId")
        if "newCustomer" in payload or payload.get("customItems") or any(payload.get(key) for key in
                ("sendConfirmationEmail", "sendAsQuote", "allowOverbooking", "tulipInsuranceOptIn")):
            parser.error("booking prohibits new customers, custom lines, external email/insurance, quotes and overbooking")
        items = payload.get("items")
        if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict) or items[0].get("quantity") != 1:
            parser.error("booking must target exactly one dedicated product, quantity 1")
        product_id = items[0].get("productId")
        if not isinstance(product_id, str) or len(product_id) != 21 or not ID_RE.fullmatch(product_id):
            parser.error("booking productId must be a valid dedicated 21-character ID")
        try:
            dates = [dt.datetime.fromisoformat(payload[key].replace("Z", "+00:00")) for key in ("startDate", "endDate")]
            dates = [value.replace(tzinfo=dt.timezone.utc) if value.tzinfo is None else value for value in dates]
            if dates[0] >= dates[1]:
                raise ValueError()
        except (KeyError, AttributeError, TypeError, ValueError):
            parser.error("booking requires ordered ISO startDate/endDate strings")
        for key in ("sendConfirmationEmail", "sendAsQuote", "allowOverbooking", "tulipInsuranceOptIn"):
            payload[key] = False
        ids = [product_id]  # Used only to group requests by their explicit test target.
    else:
        ids = [x.strip() for x in (options.reservation_ids or options.reservation_id or "").split(",") if x.strip()]
        if not ids or any(not ID_RE.fullmatch(value) for value in ids):
            parser.error("Provide valid dedicated --reservation-id or --reservation-ids")
    ids = list(dict.fromkeys(ids))
    if options.mode == "deposit-refund" and len(ids) != 1:
        parser.error("deposit-refund uses exactly one dedicated order")
    if options.check_delete_payment_id and (options.mode != "deposit-refund" or not ID_RE.fullmatch(options.check_delete_payment_id)):
        parser.error("--check-delete-payment-id requires deposit-refund and a valid dedicated original deposit receipt ID")
    name = "createManualReservation" if options.mode == "booking" else (
        "returnDeposit" if options.mode == "deposit-refund" else "updateReservationStatus")
    mapping = procedures if transport == "orpc" else actions
    if name not in mapping or (options.check_delete_payment_id and "deletePayment" not in mapping):
        raise ValueError("Required action is missing/ambiguous: " + json.dumps(discovery, ensure_ascii=False))
    amount = None
    if options.mode == "deposit-refund":
        try:
            amount = Decimal(options.amount or "")
            if not amount.is_finite() or amount <= 0 or amount * 100 != (amount * 100).to_integral_value():
                raise InvalidOperation()
        except (InvalidOperation, ValueError):
            parser.error("--amount must be a positive amount with at most two decimal places")
    cookie = read_cookie(options.cookie_file)
    barrier = threading.Barrier(options.workers)
    started_at = dt.datetime.now(dt.timezone.utc).isoformat()
    started = time.monotonic()
    def compete(index):
        reservation_id = ids[index % len(ids)]
        args = [reservation_id, {"amount": float(amount), "method": options.method,
                                 "notes": "N001 dedicated concurrency acceptance"}] if amount is not None else [reservation_id, "ongoing"]
        barrier.wait(timeout=30)
        return {"request": index} | invoke(base, cookie, actions[name], reservation_id, args, options.route, options.timeout)
    protocol_stats = None
    if transport == "orpc":
        tasks = []
        for index in range(options.workers):
            reservation_id = ids[index % len(ids)]
            data = booking_input if booking_input is not None else ({"reservationId": reservation_id, "payload": {"amount": float(amount), "method": options.method,
                     "notes": "N001 dedicated concurrency acceptance"}} if amount is not None else
                    {"reservationId": reservation_id, "status": "ongoing"})
            tasks.append({"reservation_id": reservation_id, "procedure": procedures[name], "input": data})
        results, protocol_stats = invoke_orpc_batch(options.base, cookie, tasks, Path(orpc_discovery["web_root"]), options.timeout, options.node)
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=options.workers) as pool:
            results = list(pool.map(compete, range(options.workers)))
    allowed_errors = ({"errors.insufficientCapacity"} if options.mode == "booking" else
                      {"errors.amountExceedsDeposit"} if options.mode == "deposit-refund" else
                      {"errors.reservationStatusChanged", "errors.productNoLongerAvailable"})
    successes = [r for r in results if r["outcome"] == "success"]
    explicit_rejections = [r for r in results if r["outcome"] == "business_error" and r["result"].get("error") in allowed_errors]
    unexpected = [r for r in results if r not in successes and r not in explicit_rejections]
    grouped = {value: {"successes": sum(r["outcome"] == "success" for r in results if r["reservation_id"] == value),
                       "errors": [r.get("result", {}).get("error", r.get("outcome")) for r in results
                                  if r["reservation_id"] == value and r["outcome"] != "success"]} for value in ids}
    http_pass = len(successes) == 1 and len(explicit_rejections) == options.workers - 1 and not unexpected
    if transport == "orpc":
        http_pass = http_pass and protocol_stats.get("attempted_requests") == options.workers
    physical_competition = options.mode == "checkout" and len(ids) >= 2
    if physical_competition:
        # At least one other reservation must lose on actual custody, not only
        # duplicate-state checks against the already winning reservation.
        http_pass = http_pass and any(r.get("result", {}).get("error") == "errors.productNoLongerAvailable" for r in results)
    delete_check = None
    if options.check_delete_payment_id and http_pass:
        if transport == "orpc":
            checked, _ = invoke_orpc_batch(options.base, cookie, [{"reservation_id": ids[0],
                "procedure": procedures["deletePayment"], "input": {"paymentId": options.check_delete_payment_id}}],
                Path(orpc_discovery["web_root"]), options.timeout, options.node)
            delete_check = checked[0]
        else:
            delete_check = invoke(base, cookie, actions["deletePayment"], ids[0], [options.check_delete_payment_id], options.route, options.timeout)
        http_pass = http_pass and delete_check.get("outcome") == "business_error" and delete_check.get("result", {}).get("error") == "errors.amountExceedsDeposit"
    business_ids = [row["result"]["reservationId"] for row in successes] if options.mode == "booking" else ids
    if any(not isinstance(value, str) or not ID_RE.fullmatch(value) for value in business_ids):
        raise ValueError("Unexpected created reservation ID; no database query will be guessed")
    sql_ids = ", ".join("'" + value + "'" for value in business_ids) or "NULL"
    report = {"started_at": started_at, "seconds": round(time.monotonic() - started, 4),
              "mode": options.mode, "physical_checkout_competition": physical_competition,
              "reservation_ids": business_ids, "booking_target_product_id": ids[0] if options.mode == "booking" else None,
              "requests": options.workers, "action_name": name,
              "transport": transport, "procedure_or_action_id": mapping[name], "protocol_stats": protocol_stats,
              "amount": str(amount) if amount is not None else None,
              "http_assertions_passed": http_pass, "successes": len(successes),
              "expected_business_rejections": len(explicit_rejections), "unexpected_or_unknown": len(unexpected),
              "grouped_by_reservation": grouped, "delete_receipt_guard": delete_check, "results": results,
              "business_integrity_verdict": "REQUIRES_INDEPENDENT_DATABASE_READBACK",
              "database_readback_sql": [
                  f"SELECT id, status, picked_up_at, returned_at FROM reservations WHERE id IN ({sql_ids});",
                  "SELECT reservation_id, type, status, COUNT(*) AS rows_count, SUM(amount) AS amount "
                  f"FROM payments WHERE reservation_id IN ({sql_ids}) GROUP BY reservation_id, type, status;",
                  "SELECT reservation_id, activity_type, COUNT(*) AS rows_count FROM reservation_activity "
                  f"WHERE reservation_id IN ({sql_ids}) GROUP BY reservation_id, activity_type;"] + ([
                  "SELECT r.id, r.status, r.start_date, r.end_date, ri.product_id, ri.quantity FROM reservations r "
                  "JOIN reservation_items ri ON ri.reservation_id=r.id "
                  f"WHERE ri.product_id='{ids[0]}';"] if options.mode == "booking" else []),
              "discovery": discovery,
              "limitations": ["No automatic retries after unknown outcomes", "No claim of production high availability",
                              "Checkout physical test requires distinct non-overlapping confirmed test orders for the same capacity-1 quantity returnable product"]}
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if options.report:
        options.report.parent.mkdir(parents=True, exist_ok=True)
        options.report.write_text(output, encoding="utf-8")
    print(output)
    return 0 if http_pass else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        raise SystemExit(2)
