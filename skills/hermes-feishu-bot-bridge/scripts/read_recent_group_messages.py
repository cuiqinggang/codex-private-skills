import json
import os
import time
from pathlib import Path

import requests

from feishu_hermes_bridge import load_credentials, message_text


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "feishu-recent-messages.json"
BASE = "https://open.feishu.cn/open-apis"
CHAT_ID = os.environ.get("FEISHU_CHAT_ID", "oc_3f39754af456234fa1d4de77022ef059")


def main() -> int:
    app_id, app_secret = load_credentials(os.environ.get("FEISHU_SECRET_FILE"))
    token_resp = requests.post(
        BASE + "/auth/v3/tenant_access_token/internal",
        json={"app_id": app_id, "app_secret": app_secret},
        timeout=20,
    ).json()
    token = token_resp.get("tenant_access_token")
    if not token:
        print(json.dumps({"token_code": token_resp.get("code"), "token_msg": token_resp.get("msg")}, ensure_ascii=False))
        return 1
    now = int(time.time())
    params = {
        "container_id_type": "chat",
        "container_id": CHAT_ID,
        "start_time": str(now - 3600),
        "end_time": str(now),
        "page_size": "20",
    }
    resp = requests.get(
        BASE + "/im/v1/messages",
        params=params,
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    body = resp.json()
    items = (body.get("data") or {}).get("items") or []
    summary = {
        "http_status": resp.status_code,
        "code": body.get("code"),
        "msg": body.get("msg"),
        "count": len(items),
        "items": [
            {
                "message_id": item.get("message_id"),
                "chat_id": item.get("chat_id"),
                "message_type": item.get("msg_type") or item.get("message_type"),
                "create_time": item.get("create_time"),
                "sender_type": (item.get("sender") or {}).get("sender_type"),
                "text": message_text((item.get("body") or {}).get("content")),
            }
            for item in items
        ],
    }
    OUT.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
