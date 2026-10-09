# 《A/B路线分叉任务冻结状态 第1版》
TASK_ID=AB_ROUTE_SPLIT_20261009
FREEZE_ID=AB-ROUTES-F001
FREEZE_VERSION=1
CONTRACT_VERSION=1
STATUS=IN_PROGRESS
方法版本=A28/A25/A18; B29/B26/B19

## 已有物化证据
- 标准技能单入口：`skills/artificial-single-page-extreme-time-engine/SKILL.md`。
- 唯一方法引导：`skills/artificial-single-page-extreme-time-engine/START_HERE.md`。
- A路线：`routes/A/ROUTE.md`，继承原 ENGINE.md(28)、BRAIN.md(25)、NEW_PAGE_TEMPLATE.md(18)。
- B路线：`routes/B/ROUTE.md`，新增 ENGINE_B_V29、BRAIN_B_V26、NEW_PAGE_TEMPLATE_B_V19，仅存与成熟基线的差异。
- 生产同构测试设计：`scenarios/IMAGE_QUALITY_AB_V1.md`，替换不具区分力的菜谱搜索任务。
- Windows主设备经 Desktop Commander 当前查询 Online：DESKTOP-4A1EGTM / f6990966-5870-484b-bf79-409bc6fb963e。
- GitHub官方桥技能：`skills/extreme-time-automation-bridge/SKILL.md`，已经核实 v0.3.1；完整离线备份路径为 Windows `K:\自动化单页面极限短时间引擎-20261009-备份.zip`，包含引擎、桥、n8n控制平面源文件；完成本冻结后须更新压缩包以纳入此冻结文件。
- 原 n8n 工程 `N8N-MCP-SHARED-20261009` 的 F002 独立保留，本冻结不更改它。

## 尚未完成
- Dot 作为可靠状态中继的能力验收及 Codex 在成熟代码库接口中的实际增益。
- A/B真正同边界生产同构虚拟执行、时间参数与关键故障重放，ComfyUI随机噪声生成的精品质量真实验收。
- 资源冲突协调、UNKNOWN对账及正式生产入口完整恢复。
- T_BASE_REAL=UNKNOWN; T_VIRTUAL_BEST=UNKNOWN; DELTA_T=UNKNOWN; GAIN_PERCENT=UNKNOWN; SPEEDUP=UNKNOWN。
- STOP_GATE=NOT_PASSED; VIRTUAL_MATURE=NO; REALITY=NOT_AUTHORIZED; FINAL_VALID=NO。

NEXT_ACTION=先在相同图片质量任务上记录A/B相同输入的阶段时耗与恢复证据，避免重新测试菜谱任务；达到时间门禁后再进行经授权的整体Reality。
