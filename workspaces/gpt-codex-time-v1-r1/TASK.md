# gpt-codex-time-v1-r1

OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256

GitHub bus: 000001 REQUEST -> GPT 000002 COMMAND -> CODEX 000003 RESULT -> GPT 000004 DECISION. Page ACK is transport only, never a GitHub bus type.
GPT must validate parent.type before publishing. For 000004, write type=DECISION with result_message_id, accepted, status, control_action and verification.
