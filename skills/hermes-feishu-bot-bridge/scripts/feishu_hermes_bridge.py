import argparse
import json
import logging
import os
import re
import sys
import time
import uuid
from pathlib import Path

import lark_oapi as lark
import requests
from lark_oapi.api.im.v1 import ReplyMessageRequest, ReplyMessageRequestBody


TARGET_REPLY = "HERMES_FEISHU_OK"
DEFAULT_TRIGGER = "请严格只回复：HERMES_FEISHU_OK"
DEFAULT_HERMES_URL = "http://127.0.0.1:8642/v1/chat/completions"
DEFAULT_HERMES_MODEL = "hermes-agent"
BOT_NAMES = ("爱马仕机器人",)
FEISHU_MENTION_PLACEHOLDER = re.compile(r"^@_[A-Za-z]+_\d+\s*")
RECENT_MESSAGE_IDS: dict[str, float] = {}
DEDUP_TTL_SECONDS = 600


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        rendered = super().format(record)
        rendered = re.sub(r"access_key=[^&\s]+", "access_key=***", rendered)
        rendered = re.sub(r"ticket=[^&\s]+", "ticket=***", rendered)
${REDACTED_SECRET}
        return rendered


def configure_logging(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    formatter = RedactingFormatter("%(asctime)s %(levelname)s %(message)s")
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[file_handler, stream_handler])


def read_secret_file(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    app_id = None
    app_secret = None
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if line.startswith("cli_"):
            app_id = line
        if line.lower().replace(" ", "_") in {"app_secret", "feishu_app_secret"} and i + 1 < len(lines):
${REDACTED_SECRET}
        if line.lower().replace(" ", "_") in {"app_id", "feishu_app_id"} and i + 1 < len(lines):
            app_id = lines[i + 1]
    if app_id is None:
        match = re.search(r"\bcli_[A-Za-z0-9]+\b", text)
        if match:
            app_id = match.group(0)
    if app_secret is None:
        candidates = [line for line in lines if line and not line.startswith("cli_") and "app " not in line.lower()]
        if candidates:
${REDACTED_SECRET}
    if not app_id or not app_secret:
        raise RuntimeError(f"could not parse App ID/App Secret from {path}")
    return app_id, app_secret


def load_credentials(secret_file: str | None) -> tuple[str, str]:
    app_id = os.environ.get("FEISHU_APP_ID")
${REDACTED_SECRET}
    if app_id and app_secret:
        return app_id, app_secret
    if secret_file:
        return read_secret_file(Path(secret_file))
${REDACTED_SECRET}
    if default_file.exists():
        return read_secret_file(default_file)
    raise RuntimeError("missing FEISHU_APP_ID/FEISHU_APP_SECRET and secret file was not found")


def content_payload(content: str | None) -> dict:
    if not content:
        return {}
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return {"text": content}
    return parsed if isinstance(parsed, dict) else {}


def message_text(content: str | None) -> str:
    payload = content_payload(content)
    text = payload.get("text", "")
    if not isinstance(text, str):
        return ""
    text = re.sub(r"<at[^>]*>.*?</at>", "", text)
    return text.strip()


def should_reply(content: str | None, trigger: str) -> bool:
    return trigger in message_text(content)


def remember_message(message_id: str, now: float | None = None) -> bool:
    now = time.time() if now is None else now
    expired = [key for key, seen_at in RECENT_MESSAGE_IDS.items() if now - seen_at > DEDUP_TTL_SECONDS]
    for key in expired:
        RECENT_MESSAGE_IDS.pop(key, None)
    if message_id in RECENT_MESSAGE_IDS:
        return False
    RECENT_MESSAGE_IDS[message_id] = now
    return True


def extract_bot_question(content: str | None) -> str | None:
    payload = content_payload(content)
    text = payload.get("text", "")
    if not isinstance(text, str):
        return None

    for name in BOT_NAMES:
        for prefix in (f"@{name}", name):
            if text.startswith(prefix):
                question = text[len(prefix) :].strip()
                return question or "你好"
            at_tag = re.compile(rf'^<at[^>]*>{re.escape(name)}</at>')
            match = at_tag.match(text)
            if match:
                question = text[match.end() :].strip()
                return question or "你好"

    mentions = payload.get("mentions") or []
    if isinstance(mentions, list):
        for mention in mentions:
            if not isinstance(mention, dict):
                continue
            mention_name = mention.get("name") or mention.get("display_name")
            mention_key = mention.get("key")
            if mention_name in BOT_NAMES and isinstance(mention_key, str) and mention_key in text:
                question = text.replace(mention_key, "", 1).strip()
                return question or "你好"
    placeholder = FEISHU_MENTION_PLACEHOLDER.match(text)
    if placeholder:
        question = text[placeholder.end() :].strip()
        return question or "你好"
    return None


def ask_hermes(question: str, hermes_url: str, hermes_model: str, timeout: int) -> str:
    payload = {
        "model": hermes_model,
        "messages": [
            {
                "role": "system",
                "content": "你是飞书群内的爱马仕 AI 助手。请直接回答用户问题，保持简洁。",
            },
            {"role": "user", "content": question},
        ],
    }
    response = requests.post(
        hermes_url,
        data=json.dumps(payload, ensure_ascii=True).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    answer = data["choices"][0]["message"]["content"].strip()
    return answer or "Hermes 没有返回有效内容。"


def build_reply_request(message_id: str, reply_text: str) -> ReplyMessageRequest:
    return (
        ReplyMessageRequest.builder()
        .message_id(message_id)
        .request_body(
            ReplyMessageRequestBody.builder()
            .msg_type("text")
            .content(json.dumps({"text": reply_text}, ensure_ascii=False))
            .uuid(str(uuid.uuid4()))
            .build()
        )
        .build()
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--secret-file", default=None)
    parser.add_argument("--log", default="feishu-bridge.log")
    parser.add_argument("--trigger", default=DEFAULT_TRIGGER)
    parser.add_argument("--reply", default=TARGET_REPLY)
    parser.add_argument("--hermes-url", default=DEFAULT_HERMES_URL)
    parser.add_argument("--hermes-model", default=DEFAULT_HERMES_MODEL)
    parser.add_argument("--hermes-timeout", type=int, default=180)
    args = parser.parse_args()

    configure_logging(Path(args.log))
${REDACTED_SECRET}
    os.environ["FEISHU_CONNECTION_MODE"] = "websocket"
${REDACTED_SECRET}

    api_client = lark.Client.builder().app_id(app_id).app_secret(app_secret).build()

    def on_message(event) -> None:
        msg = event.event.message
        logging.info(
            "event_received type=%s chat_type=%s chat_id=%s message_id=%s text=%s",
            msg.message_type,
            msg.chat_type,
            msg.chat_id,
            msg.message_id,
            message_text(msg.content),
        )
        if msg.message_type != "text":
            logging.info("event_skip reason=non_text message_id=%s", msg.message_id)
            return
        if not remember_message(msg.message_id):
            logging.info("event_skip reason=duplicate_message message_id=%s", msg.message_id)
            return
        if should_reply(msg.content, args.trigger):
            reply_text = args.reply
        else:
            question = extract_bot_question(msg.content)
            if question is None:
                logging.info("event_skip reason=bot_not_mentioned message_id=%s", msg.message_id)
                return
            logging.info("hermes_request message_id=%s question=%s", msg.message_id, question)
            try:
                reply_text = ask_hermes(question, args.hermes_url, args.hermes_model, args.hermes_timeout)
            except Exception as exc:
                logging.exception("hermes_failed message_id=%s err=%s", msg.message_id, exc)
                reply_text = "Hermes 暂时没有生成成功，请稍后再试。"
        response = api_client.im.v1.message.reply(build_reply_request(msg.message_id, reply_text))
        if not response.success():
            logging.error(
                "reply_failed code=%s msg=%s request_id=%s",
                response.code,
                response.msg,
                response.get_request_id(),
            )
            return
        logging.info("reply_sent message_id=%s reply=%s", msg.message_id, reply_text)

    handler = (
        lark.EventDispatcherHandler.builder("", "")
        .register_p2_im_message_receive_v1(on_message)
        .build()
    )
    ws_client = lark.ws.Client(
        app_id,
        app_secret,
        log_level=lark.LogLevel.INFO,
        event_handler=handler,
        auto_reconnect=True,
    )
    logging.info("websocket_client_starting")
    ws_client.start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
