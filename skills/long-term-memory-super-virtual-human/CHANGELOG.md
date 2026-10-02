# CHANGELOG

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

中文名：**长期记忆超级虚拟人**  
英文名：**Long-Term Memory Super Virtual Human**

- 建立首个技能包版本；
- 固定“轻入口、强能力池、按需激活”；
- 明确产品定位：作为用户授权范围内的长期数字化认知与执行代理；
- GPT 作为当前首选主脑候选，但不写成不可替代真理；
- 引用极限短时间智能体宪法 v0.3.1；
- 引用极限短时间自动化闭环 v2.0；
- 引用 GPT直连Windows双路执行桥 v0.2.0；
- 长流程采用“稳定规则 + 单任务 Source of Truth”，Checkpoint 只负责恢复；
- 新增 `DRIFT_BENCHMARK.md`：与单一权威文件、完整 Spec-Driven 三类方案做同批 Reality 比较；
- 新增 `MODEL_ROUTER.md`：区分 ChatGPT 自身档位与可编程外部模型/推理路由；
- GUI 自动化降为按需执行面，优先原生 API / Connector / CLI；
- 新增独立强备份要求；
- 当前状态仍为 EARLY_REALITY_BASELINE，不宣布成熟。
