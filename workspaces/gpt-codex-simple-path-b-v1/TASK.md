# gpt-codex-simple-path-b-v1

OUTPUT=toy-result.txt
CONTENT=GPT_CODEX_CODE_TO_CODE_OK
VERIFY=exact readback + SHA256

GitHub bus: 000001 REQUEST -> GPT 000002 COMMAND -> CODEX 000003 RESULT -> GPT 000004 DECISION. Page ACK is transport only, never a GitHub bus type.
GPT must validate parent.type before publishing. For 000004, write type=DECISION with result_message_id, accepted, status, control_action and verification.
v1.5.1 PATH A is preferred. If GPT GitHub write is blocked but read works, use PAGE GPT_COMMAND/GPT_DECISION. If GitHub is unavailable, use the current-step page context. Do not treat page ACK as a Bus message.
