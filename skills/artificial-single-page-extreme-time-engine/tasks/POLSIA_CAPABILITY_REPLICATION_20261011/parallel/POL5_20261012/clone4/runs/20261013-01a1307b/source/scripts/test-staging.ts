// Real loopback HTTP + PostgreSQL acceptance. No model, cloud, payment, or replay.
import assert from "node:assert/strict";
import { writeFileSync } from "node:fs";

const base = process.env.POLSIA_TEST_URL || "http://127.0.0.1:55437";
assert.equal(new URL(base).hostname, "127.0.0.1");
const checks: { name: string; pass: boolean }[] = [];
const started = new Date().toISOString();
function check(name: string, action: () => void) { action(); checks.push({ name, pass: true }); }
async function call(path: string, method = "GET", body?: unknown, company = "demo", headers: Record<string, string> = {}) {
  const url = new URL(path, base); url.searchParams.set("company", company);
  const response = await fetch(url, { method, headers: { ...(body ? { "content-type": "application/json" } : {}), ...headers },
    body: body ? JSON.stringify(body) : undefined, signal: AbortSignal.timeout(15000) });
  const value = await response.json() as any; return { status: response.status, value };
}

async function main() {
  const runtime = await call("/api/runtime");
  check("local staging and no worker/model authorization", () => {
    assert.equal(runtime.value.mode, "LOCAL_TEST"); assert.equal(runtime.value.workerAllowed, false);
    assert.ok(["NOT_ENABLED_IN_LOCAL_TEST","LOCAL_CODEX_JOBS_ENABLED"].includes(runtime.value.modelExecution));
  });
  const catalog = await call("/api/capabilities");
  check("nine evidence categories, honest scope", () => {
    assert.equal(catalog.status, 200); assert.equal(catalog.value.capabilities.length, 9);
    assert.equal(catalog.value.functionalIntegrated, false);
  });
  const company = await call("/api/companies", "POST", { name: "独立真实验收 " + Date.now(), goal: "核验只读证据闭环及持久化" });
  check("company creation persisted", () => assert.equal(company.status, 201));
  const companyId: string = company.value.id;
  const taskIds: string[] = [];
  for (const capability of catalog.value.capabilities) {
    const created = await call("/api/tasks", "POST", { title: capability.title + "资料核验", capabilityId: capability.id }, companyId);
    check(capability.id + " task created as todo", () => { assert.equal(created.status, 201); assert.equal(created.value.task.status, "todo"); });
    const taskId = created.value.task.id; taskIds.push(taskId);
    const executed = await call("/api/tasks/" + taskId + "/execute", "POST", undefined, companyId);
    check(capability.id + " actual evidence task completed", () => {
      assert.equal(executed.status, 200); assert.equal(executed.value.task.status, "completed");
      assert.equal(executed.value.modelCalled, false);
      assert.equal(executed.value.task.events.filter((e: { type: string }) => e.type === "tool_result").length, 1);
    });
    const artifact = executed.value.task.result.artifacts[0];
    const report = await call(artifact.ref, "GET", undefined, companyId);
    const document = JSON.parse(report.value.content);
    check(capability.id + " persisted real file and SHA", () => {
      assert.equal(document.capabilityId, capability.id); assert.equal(document.sha256, document.expectedSha256);
      assert.equal(document.integrity, "PINNED_SHA256_MATCH"); assert.ok(document.content.length > 0);
    });
  }
  const repeat = await Promise.all(Array.from({ length: 4 }, () => call("/api/tasks/" + taskIds[0] + "/execute", "POST", undefined, companyId)));
  check("completed task is not replayed", () => { repeat.forEach(r => assert.equal(r.value.replayed, false)); });
  const state = await call("/api/state", "GET", undefined, companyId);
  check("single report per task and worker off", () => { assert.equal(state.value.reports.length, 9); assert.equal(state.value.worker, false); });
  const privateTask = await call("/api/tasks/" + taskIds[0], "GET", undefined, "demo");
  check("company task isolation", () => assert.equal(privateTask.status, 404));
  const invalid = await call("/api/tasks", "POST", { title: "bad", capabilityId: "../../finance" }, companyId);
  check("nonallowlisted evidence cannot create task", () => assert.equal(invalid.status, 400));
  const empty = await call("/api/companies", "POST", { name: "", goal: "" });
  check("invalid company rejected", () => assert.equal(empty.status, 400));
  const foreign = await call("/api/companies", "POST", { name: "forbidden", goal: "forbidden" }, companyId, { origin: "https://untrusted.invalid" });
  check("foreign browser origin cannot mutate loopback", () => assert.equal(foreign.status, 403));
  for (const [path, method] of [["/api/worker?on=true", "POST"], ["/api/reset", "POST"], ["/api/onboard", "POST"],
    ["/api/chat", "POST"], ["/api/cron", "POST"], ["/api/proxy/llm", "POST"], ["/run/" + taskIds[0], "GET"]]) {
    const blocked = await call(path, method);
    check(path + " is fail-closed", () => { assert.equal(blocked.status, 409); assert.equal(blocked.value.modelCalled, false); });
  }
  const receipt = { result: "PASS_LOCAL_EVIDENCE_FLOW_ONLY", fullPolsiaParity: false, startedAt: started, completedAt: new Date().toISOString(),
    base, companyId, taskIds, checks, modelCalls: 0, historicalBusinessReplays: 0, reportPersistence: "REAL_POSTGRES" };
  if (process.env.POLSIA_TEST_RECEIPT) writeFileSync(process.env.POLSIA_TEST_RECEIPT, JSON.stringify(receipt, null, 2) + "\n");
  console.log(JSON.stringify({ result: receipt.result, checks: checks.length, companyId, taskIds, fullPolsiaParity: false }));
}

main().catch(error => {
  if (process.env.POLSIA_TEST_RECEIPT) writeFileSync(process.env.POLSIA_TEST_RECEIPT, JSON.stringify({ result: "FAILED", startedAt: started, completedAt: new Date().toISOString(), checks, error: error instanceof Error ? error.message : String(error), fullPolsiaParity: false }, null, 2));
  console.error(error); process.exitCode = 1;
});
