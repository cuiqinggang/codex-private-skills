import json

from feishu_hermes_bridge import (
    DEFAULT_TRIGGER,
    RECENT_MESSAGE_IDS,
    TARGET_REPLY,
    extract_bot_question,
    message_text,
    remember_message,
    should_reply,
)


def test_message_text_removes_at_tag_and_preserves_trigger():
    content = json.dumps({"text": '<at user_id="ou_x">爱马仕机器人</at> 请严格只回复：HERMES_FEISHU_OK'}, ensure_ascii=False)
    assert message_text(content) == DEFAULT_TRIGGER


def test_should_reply_only_for_target_trigger():
    assert should_reply(json.dumps({"text": DEFAULT_TRIGGER}, ensure_ascii=False), DEFAULT_TRIGGER)
    assert not should_reply(json.dumps({"text": "你好"}, ensure_ascii=False), DEFAULT_TRIGGER)


def test_remember_message_rejects_duplicate_message_id():
    RECENT_MESSAGE_IDS.clear()
    assert remember_message("om_test", now=1000.0)
    assert not remember_message("om_test", now=1001.0)


def test_extract_bot_question_from_plain_at_prefix():
    content = json.dumps({"text": "@爱马仕机器人 今天武汉的天气怎么样"}, ensure_ascii=False)
    assert extract_bot_question(content) == "今天武汉的天气怎么样"


def test_extract_bot_question_from_at_tag_prefix():
    content = json.dumps({"text": '<at user_id="ou_x">爱马仕机器人</at> 你好'}, ensure_ascii=False)
    assert extract_bot_question(content) == "你好"


def test_extract_bot_question_from_feishu_mention_placeholder():
    content = json.dumps(
        {
            "text": "@_user_1 你好",
            "mentions": [{"key": "@_user_1", "name": "爱马仕机器人", "id": {"user_id": "ou_x"}}],
        },
        ensure_ascii=False,
    )
    assert extract_bot_question(content) == "你好"


def test_extract_bot_question_from_feishu_placeholder_without_mentions():
    content = json.dumps({"text": "@_user_1 你好，请问你是什么大模型？"}, ensure_ascii=False)
    assert extract_bot_question(content) == "你好，请问你是什么大模型？"


def test_extract_bot_question_ignores_non_mention():
    content = json.dumps({"text": "今天武汉的天气怎么样"}, ensure_ascii=False)
    assert extract_bot_question(content) is None


def test_target_reply_constant_is_exact():
    assert TARGET_REPLY == "HERMES_FEISHU_OK"
