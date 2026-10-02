# CHANGELOG

## 0.2.0 - 2026-10-02

- 吸收 Reasonix Recovery Kit 的成熟通用机制，但不复制历史 96/100 评分为本项目成熟度；
- 新增 `MATURE_CAPABILITY_ABSORPTION_R1.md`，按 DIRECT_COPY / LIGHT_ADAPT / REFERENCE_ONLY 分类；
- 新增 `CHATGPT_MODEL_EFFORT_CONTROLLER.md`；
- 新增 `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`；
- 新增 `CLOUD_RUNTIME_OPTIONS.md`；
- ChatGPT 页面模型/Thinking 自动调整改为“主脑决策 + 外部确定性控制器 + 读回确认”；优先复用 Playwright Native AI Browser；
- 页面卡顿/上下文损坏与 GPT 服务级不可用分层处理；
- 长流程优先复用 ECC v3.1.1，不重造第二套 lease/fencing/checkpoint/Gate/Repair；
- Mature AI Coding SuperTool Ecosystem Station 保持按需唤醒，不做永久中间层；
- OpenAI 托管云、Codex Cloud、Work Cloud Browser 与自有 VPS 明确分层；
- 定义 v1.0 七项 Reality 毕业门槛；
- 当前仍不宣布 VIRTUAL_MATURE。

## 0.1.1 - 2026-10-02

- 新增系统级低相关冗余合同：关键能力至少两条成熟路径；
- 明确主路优化完整 T_VALID，备路首先保证 VALID 与可恢复，允许更慢；
- 新增 Failover-Before-Repair：主路异常先切备路恢复业务，再修主路并补回冗余；
- 新增 `RESILIENCE_REDUNDANCY.md`；
- 新增 `EXECUTION_PROFILES.md`；
- ECC v3.1.1 正式作为长流程成熟档位按需调用，不重复造第二套；
- 本机“成熟态 AI Coding SuperTool 生态站”正式作为复杂任务按需执行档位，不做永久常驻中间层；
- Windows 主备控制面明确为 Desktop Commander Remote + GitHub self-hosted runner；
- 人工只保留用户本人不可替代动作，不作为普通故障兜底。

## 0.1.0 - 2026-10-02

- 建立首个技能包版本；
- 固定“轻入口、强能力池、按需激活”；
- 明确产品定位；
- GPT 作为当前首选主脑候选，但不写成不可替代真理；
- 引用极限短时间智能体宪法 v0.3.1、自动化闭环 v2.0、Windows 双路桥 v0.2.0；
- 建立 TASK_CONTRACT、Checkpoint、漂移 Benchmark、模型路由和独立强备份要求。
