# HANDOFF_MECHANICAL_GATE v1

适用：CONTRACT_VERSION=4 三任务所有 CEO handoff。

必须解析并验证：
1. LOCATION_ANCHOR：四字段定位锚存在。
2. STATE_ANCHOR：状态机锚存在。
3. TIME_ANCHOR：时间锚存在。
4. TASK_ID 与目标 execution package 一致。
5. CONTRACT_VERSION=4。
6. FREEZE_VERSION 与 FREEZE_PATH 文件名/正文一致。
7. ENGINE_VERSION=22。
8. BRAIN_VERSION=19。
9. NEW_PAGE_TEMPLATE_VERSION=17。
10. METHOD_REF 可解析且含上述方法版本。
11. STATE_REF 可解析。
12. TASK_CONSTRAINTS_PATH 在 STATE_REF 可解析状态中真实存在。
13. FREEZE_PATH 在 STATE_REF 可解析状态中真实存在。
14. FREEZE_TAG 与路径版本一致。
15. NEXT_NODE 存在且 TASK_ID 相同。
16. prompt 不含其他 TASK 的 STATE_REF/FREEZE_PATH/PAGE_ID。
17. prompt 不引用 stale freeze，不携带大量旧聊天正文；fresh CEO 仅凭 prompt + 明确引用权威文件可恢复。

附加盲测门：
- ORACLE_POINTER_ABSENT=YES
- FINAL_ANSWER_PATH_ABSENT=YES
- FUTURE_SLICE_ABSENT=YES
- PUBLIC_ANSWER_SEARCH_DISABLED=YES

失败语义：
任何一项失败 => HANDOFF=FAIL；不得靠当前模型记忆补洞。
Freeze failure → 责任判断 → Repair → 重生 prompt → True New Chat → 再验。
