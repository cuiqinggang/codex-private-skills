import json
import os
from pathlib import Path

import requests

from feishu_hermes_bridge import load_credentials


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "feishu-api-diagnostics.json"
BASE = "https://open.feishu.cn/open-apis"


def call(method: str, path: str, **kwargs) -> dict:
    resp = requests.request(method, BASE + path, timeout=20, **kwargs)
    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text[:500]}
    return {"http_status": resp.status_code, "body": body}


def main() -> int:
${REDACTED_SECRET}
    token_resp = call(
        "POST",
        "/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
    )
    result = {
        "app_id": app_id,
        "tenant_token_http_status": token_resp["http_status"],
        "tenant_token_code": token_resp["body"].get("code"),
        "tenant_token_msg": token_resp["body"].get("msg"),
        "bot_info": None,
        "chat_list": None,
        "target_chat_members": None,
    }
    token = token_resp["body"].get("tenant_access_token")
    if not token:
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    headers = {"Authorization": f"Bearer {token}"}
    bot_info = call("GET", "/bot/v3/info", headers=headers)
    result["bot_info"] = {
        "http_status": bot_info["http_status"],
        "code": bot_info["body"].get("code"),
        "msg": bot_info["body"].get("msg"),
        "app_name": (bot_info["body"].get("bot") or {}).get("app_name"),
        "open_id": (bot_info["body"].get("bot") or {}).get("open_id"),
    }
    chats = call("GET", "/im/v1/chats?page_size=20", headers=headers)
    items = ((chats["body"].get("data") or {}).get("items") or [])
    result["chat_list"] = {
        "http_status": chats["http_status"],
        "code": chats["body"].get("code"),
        "msg": chats["body"].get("msg"),
        "count": len(items),
        "items": [
            {
                "chat_id": item.get("chat_id"),
                "name": item.get("name"),
                "chat_type": item.get("chat_type"),
                "external": item.get("external"),
            }
            for item in items
        ],
    }
    target = next((item for item in items if item.get("name") == "爱马仕ai测试群"), None)
    if target and target.get("chat_id"):
        members = call("GET", f"/im/v1/chats/{target.get('chat_id')}/members?page_size=50", headers=headers)
        member_items = ((members["body"].get("data") or {}).get("items") or [])
        result["target_chat_members"] = {
            "http_status": members["http_status"],
            "code": members["body"].get("code"),
            "msg": members["body"].get("msg"),
            "count": len(member_items),
            "member_ids": [
                {
                    "member_id": item.get("member_id"),
                    "member_id_type": item.get("member_id_type"),
                    "name": item.get("name"),
                }
                for item in member_items
            ],
        }
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
