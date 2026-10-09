# B33 隔离无业务真实交接测试合同 V1
TASK_ID=B33_ISOLATED_HANDOFF_20261010_T01
MODE=TEST
REAL_BUSINESS=NO
FINAL_GOAL=短状态码进入另一个独立新聊天后，新GPT真实从GitHub读取本CURRENT与F001，核对TASK_ID/FREEZE_ID，输出唯一ACK。
ACK=ACK-B33-ISOLATED-T01
SOURCE=cuiqinggang/codex-private-skills/main
REQUIRED_INPUT=续接B|cuiqinggang/codex-private-skills|B33_ISOLATED_HANDOFF_20261010_T01|B33T-F001
SAFE_LIMIT=不得读写其它任务CURRENT；不得执行现实业务；不得二次发送同一码。
DONE_WHEN=接收聊天出现精确ACK且可只读核对实际GitHub接管证据。
IF_NOT_READ=禁止虚构ACK；报告阻塞。
