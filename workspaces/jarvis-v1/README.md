# JARVIS v1.0 Workspace / 贾维斯版本2

> 当前状态：STATE=10，前期资料收集 / 成熟方案现实取证 / 虚拟成熟前准备。  
> 母方法：整体闭环极限短时间引擎 v5.6.5。  
> 核心目标：T* = min(T_VALID)。

## 当前用途

本目录作为 JARVIS v1.0 的共同工作区，用于集中保存：
- 成熟方案能力判断；
- Reality Benchmark 证据摘要；
- 已确认限制与失败类别；
- 后续跨供应商能力比对；
- 下一页面/下一智能体接续状态。

## 当前 Manus 2.0 证据

详见：
- `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.md`
- `evidence/MANUS_2_CAPABILITY_REALITY_MATRIX.json`

当前结论只表示“已观察场景中的现实证据”，不得外推为长期通用保证。

## 状态机语义

当前所有 Manus Reality Benchmark 都属于 STATE=10 的现实取证输入，不代表 JARVIS 已进入 Reality 执行阶段。

正确顺序：
`10 前期资料/成熟方案/完整候选 → 系统级虚拟成熟 → 20 Freeze → 30 虚实交接 → 40 Reality执行/审核 → 100完成`

## 下一阶段

已完成 R1-R7 基础/中层能力取证。下一步为深层综合压力测试：
- R8 CHAOS MARATHON：长流程、多故障、checkpoint、断连、漂移、插队、幂等。
- R9 SWARM ORCHESTRATION：多工作流、多Agent、依赖调度、状态隔离、局部失败、冲突仲裁与汇合。
- R10 BROWSER MISSION：20~30步动态网页精确操作、session恢复、上传下载、动态DOM、不可信页面指令、权限门。

详细接续见 `SUMMARY.md`。
