# 《三人行》第3版｜正式方法冻结（2026-10-17）
VERSION=SANRENXING_V3
FREEZE_ID=SRX-V3-F001-20261017
STATUS=FROZEN_PUBLISHED
METHOD_LINEAGE=V2_C002_FREEZE_PLUS_V3_VERIFIED_DELTA
GLOBAL_FINAL_VALID=NOT_CLAIMED
TEN_PAIR_AB=0/10
LEGACY_TASKS=KEEP_PINNED_METHOD_REF

## 一、来源及冻结范围
本版不是把V2正文直接改名。其不变原则继承真实已冻结的V2 C002：
`skills/artificial-single-page-extreme-time-engine/method-freezes/SANRENXING_V2_C002_F001_20261012/SANRENXING_V2.md`，内容固定源提交 `78ffb94c4cacd07662b83a59042bc0fe3e7f69e7`。
V3唯一已定位的增量证据：`skills/artificial-single-page-extreme-time-engine/SANRENXING_V3_ORCA_HEARTBEAT_20261016.md`，内容blob `0071d3e0f658568d616ab39b57de11a353b2b992`。
Windows执行桥规范依赖 `skills/gpt-windows-execution-bridge/SKILL.md` 与 `v9-deterministic-routing.md`。
三者原件不可变；本文件以依赖链接与以下差分构成V3可发现的正式方法版本。

## 二、运行硬原则
GPT CEO为任务唯一总控；按任务实际复杂度按需调用Codex执行、Orca编排、多Executor并行，禁止为形式引入第三方；大量任务编排可以调用Orca，但无需为每个任务强制启动。
目标为同合同质量及安全约束下的完整有效时间最小化 `T*=min(T_VALID)`，包括任务接收、规划、派发、执行、恢复、合并、验收。只计业务最终有效，启动或局部成功不得冒充。
成熟方案优先，既有GOOD→BAD→FIRST_DELTA→最小成熟修复→独立QA；虚拟成熟整体Freeze后现实验证，不逐点Reality。不放宽授权、Exactly-once、业务三态、任务状态隔离及安全边界。
Codex子任务业务面和Orca管理心跳必须隔离；管理心跳超时归类UNKNOWN_RECONCILE，不得通过异常清理正常Codex业务进程。结算使用唯一request_id和官方幂等重试，UNKNOWN先对账再决定重发。原有全局预算、资源底线4GiB、独立QA不取消。
Windows执行统一先加载V9桥正式入口。C为唯一默认首选；C实际失败并有界重试失败才允许A；A也失败才B。不得改FlClash或Windows代理。每个降级记录证据；从备份回归的新任务仍先检查C。
当前任务如已固定METHOD_REF，不自动迁移；本版仅适用于明确选择V3或默认方法正式入口完成更新后的新任务。

## 三、实证边界（不能混写）
2026-10-16 r4/pilot-B 已有本地accepted=true、Orca completed及独立离线回归21项；它只是单次新版本pilot，不计正式十组稳定性。
管理心跳注入测试2/2 PASS但不等同官方服务端真实故障注入；历史r3失败永久保留。
正式10组稳定性=0/10；成对AB=未完成；物理极限、全面生产FINAL_VALID=UNKNOWN；不能宣称V3对V2或原生Codex整体更快。
Windows V9已写入GitHub方法入口，但所有现场运行器是否真正加载、C失败自动转A、A失败转B及C恢复复归尚未通过端到端验收。

## 四、版本解析与停机门
加载顺序：本V3文件→V2 C002固定提交的完整继承规则→V3 Orca增量→Windows V9技能入口→任务CURRENT/合同/Freeze。
若任一必需依赖不可读取，标记VERSION_MISMATCH，不静默降级为V2、不伪造V3验收。
冻结、发布与用户指定默认版本是方法入口状态，不代表十组稳定性与完整生产业务已经认证。
