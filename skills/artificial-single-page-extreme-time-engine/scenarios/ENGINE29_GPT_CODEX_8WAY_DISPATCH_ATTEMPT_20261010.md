# ENGINE29 GPT×Codex 8任务并行派发尝试｜2026-10-10

STATUS=BLOCKED_NO_VALID_SUBAGENT_RECEIPTS
ROUTE=METHOD_DRAFT_ONLY
PUBLIC_ENGINE_CURRENT=28
A_ROUTE_CURRENT=A29
B_ROUTE_CURRENT=B33
CANDIDATE_PATH=skills/artificial-single-page-extreme-time-engine/method-drafts/ENGINE29_GPT_CODEX_COMPETITIVE_PARALLEL_CANDIDATE_20261010.md
TASK_ID=ENGINE29_GPT_CODEX_COMPARATIVE_VALIDATION_20261010
RUN_ID=ENG29_8WAY_COMPARE_VIRTUAL_001
MODE=VIRTUAL_REVIEW_ONLY
FINAL_VALID=NO
VIRTUAL_MATURE=NO
T_VALID_REAL=UNKNOWN

## 1. 已经完成的事实

1. GPT通过已连接的GitHub官方工具真实回读公共ENGINE28、START_HERE、A29、B33等文件，确认公共ENGINE29未激活。
2. ENGINE29 GPT×Codex角色竞争/最多三级/1、3、8路对照方案已独立落库并回读：提交`4fccad68766c74cd5aeab28f4a3cbefb05be9d37`。
3. Windows执行桥设备DESKTOP-4A1EGTM在线，Codex CLI之前确认为0.160.0、Logged in using ChatGPT。采用独立目录`C:\Users\A\Documents\Codex\ENGINE29_GPT_CODEX_VIRTUAL_AUDIT_20261010`进行仅文本、无文件读取的8题虚拟审核。
4. 本轮以`codex exec --ephemeral --ignore-user-config --enable multi_agent -c agents.max_threads=8 -c agents.max_depth=1 -c approval_policy=never --sandbox read-only`启动，PID=21560。带四字段定位的UTF-8用户提示词完整进入Codex会话。主代理回复称将启动8个原生子代理。
5. 日志出现`ERROR: Reconnecting... 3/5`以及本机两份Codex技能的`SKILL.md: missing YAML frontmatter delimited by ---`；随后反复出现子会话技能加载错误。没有收到逐个子代理的成功派发确认、有效产物或回收统计。
6. 为避免无证据的无限等待，GPT通过合法Windows执行桥终止PID=21560，并核对其不再是活动远程会话。只停止本任务自身进程，没有操作用户浏览器、真实ChatGPT聊天、代理、GitHub正式引擎文件或任务CURRENT。

## 2. 8个编号任务的真实验收状态

T01 单CEO简任务=NOT_TESTED
T02 Freeze/CURRENT跨页接力=NOT_TESTED
T03 A29标签归属=NOT_TESTED
T04 最多三级及全局单写者=NOT_TESTED
T05 共享浏览器/资源冲突=NOT_TESTED
T06 UNKNOWN/断线/重复写=NOT_TESTED
T07 A29/B33/公共29版本兼容=NOT_TESTED
T08 同批8任务P=1、3、8真实全链路计时=NOT_TESTED

重要：主代理的“将启动”文字不等于实际spawn/wait成功；技能加载ERROR既不能证明0个也不能证明8个子代理成功。可确认已完成任务数为0；实际启动数UNKNOWN。此前被安全策略拒绝的本地snapshot.md读取动作未被绕过，当前题目为全新自包含虚拟案例，无保护资源访问。

## 3. 正确后续动作

- 使用产品/管理员认可的正常路径排查Codex多智能体会话连接和技能YAML头是否有效；不得因安全策略拒绝而切换凭据、文件访问路径或工具绕过。
- 先取得实际子代理启动/回收可核验证据，必要时只验收最小合法调度入口；不要把大量新启动当作成绩。
- 若恢复，沿用当前8项任务合同，分别比较GPT协调/执行、Codex协调/执行及混合组合；同批工作量使用P=1、3、8（可加5）进行公平实测，记录从TASK_ACCEPTED到全部FINAL_VALID的墙钟时间、失败与恢复开销。
- 不自动发送受保护的GPT页面，不改FlClash，不启动第二浏览器，不重造通用状态机/调度器。拿不到实际GPT并行多聊天合法接口则标记NOT_TESTED，不伪造对照。
- 未通过同合同计时与真实合法Freeze→FINAL_REALITY_ONCE，不发布公共ENGINE29，不更新START_HERE和A/B正式入口。
