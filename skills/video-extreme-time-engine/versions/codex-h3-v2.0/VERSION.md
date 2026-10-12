# 版本与迁移说明

VERSION=2.0.0-method
TITLE=Codex+H3 视频制作技能包 V2.0｜全帧源图连续制作版
STATUS=METHOD_SPEC_READY_REALITY_PENDING
LOCAL_PACKAGE_STATUS=LOCAL_STATIC_CHECK_PASS
REALITY_CERTIFICATION=PENDING
FINAL_VALID=NO
AUTHORITATIVE_PARENT=skills/video-extreme-time-engine
PLANNED_REMOTE_PATH=skills/video-extreme-time-engine/versions/codex-h3-v2.0
REMOTE_PERSISTENCE=VERIFY_ACTUAL_COMMIT_AND_READBACK_RECEIPT
DATE=2026-10-12

## 已核验来源

- 仓库 `cuiqinggang/codex-private-skills`、分支 main，核对快照 `bb5c0e1f91ea14545e8bc968c341fae14f86db54`。
- 父入口版本字段 `0.5+codex-h3-v2`，主体为视频极限短时间引擎 v0.5。
- V2 合同 `skills/video-extreme-time-engine/CODEX_H3_V2_FULL_FRAME.md`，blob `9f2af2701adf303ffea504f9c67e0d750f7c7a28`，新增提交 `ada04131c5389356eb539108e509f0312e57ed64`（北京时间 2026-10-12 20:43:36）。
- V2 入口关联提交 `d03e233859c820b4d34faf013a60d95adb977d37`（北京时间 20:49:56）。
- 父冻结为 `VETE-v0.5-H3P1-R1`，`STATUS=FROZEN`；H3-P1 与 V2 的 VALID 规格不同。

## NEEDS_VERSIONED_UPGRADE

原冻结 v0.5 不允许原地更改。本次在同一父包血缘的 `versions/codex-h3-v2.0` 新增版本资产，既有 `FREEZE.md`、`CASE-H3-P1.md`、原始 v0.5 与远端 V2 合同保留。不得新建与父包竞争的权威目录 `skills/codex-h3-video-production`。

V2 替代 8 张稀疏源图覆盖 56 帧的正式路线；新增 56 次真实源图生成、双参考继承、逐帧门禁、无插帧编码、声音与现实验收。规范 ready 与商业现实认证分开，未通过实际视频和声音验收时不称生产成熟。

本版本文档记录方法与并发生产的时点状态，不意味着 Codex 全局安装或商业认证。GitHub 持久化以实际 commit、精确路径回读和包外 publication receipt 为准；文档本身不能预先证明写入成功。远端迁移需检查最新 main 与本次授权范围，新增版本文件并核对提交、远端内容和 SHA。只有非冻结索引确认可维护时才新增指向本版本的索引；不得为了入口便捷修改被冻结父入口。实际成功日志按证据更新，后续冻结后任何变更新增版本。

## 状态推进

METHOD_SPEC_READY → LOCAL_STATIC_CHECK_PASS → REMOTE_READBACK_VERIFIED → REALITY_CERTIFIED（56 源图及全部验收实际通过）→ 另行记录生产冻结。
每一状态只代表自己的证据，不能跳过；`REMOTE_READBACK_VERIFIED` 也不能推出 `REALITY_CERTIFIED`。
