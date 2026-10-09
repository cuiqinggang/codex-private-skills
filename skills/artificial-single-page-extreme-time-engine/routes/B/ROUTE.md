# 自动化B·单层页面｜唯一当前方法指针

**当前已发布路线版本：引擎 B31｜执行大脑 B28｜新页面模板 B21**
继承链：
- B31 → B30 → B29 → 共同 `../../ENGINE.md` 第28版；
- B28 → B27 → B26 → 共同 `../../BRAIN.md` 第25版；
- B21 → B20 → B19 → 共同 `../../NEW_PAGE_TEMPLATE.md` 第18版。

## 当前真实方法文件
1. `ENGINE_B_V31.md`：总规则的单层页面增量；明确B的换页只由至同一实质成果的完整时间、正确性与健康风险决定，不规定“冻结必换”。
2. `BRAIN_B_V28.md`：GPT负责规划与执行；决定任务、自然节点、故障修复、持续推进与动态页面切换。
3. `NEW_PAGE_TEMPLATE_B_V21.md`：仅在确实需要换页时处理先冻结、最小恢复、核验接管与旧页安全收口。
4. 现有根目录 `ENGINE.md` 第28版、`BRAIN.md` 第25版、`NEW_PAGE_TEMPLATE.md` 第18版为不复制的共同继承基础。旧B29/B30等是历史版本，不予改写。
5. 每个 TASK_ID 的合同与最新冻结按其自己 `tasks/<TASK_ID>/CURRENT.md` 定位；此指针不保存任何全局任务状态。

## B路线执行入口和安全门
用户只说“按自动化A/B极限短时间引擎完成【任务】”，GPT从仓库 `SKILL.md`→`START_HERE.md`→本路线最新指针读取；此文件在新方法文件均可读取后一次发布，避免版本混读。GPT默认不经过n8n；仅必要时复用Windows桥、Playwright MCP、Dot、Codex等成熟能力，不自研通用调度器或状态机。

**B31为规则构建/虚拟逻辑检查状态，不代表虚拟成熟或Reality通过**。对应逻辑检查计划：`../../scenarios/B31_VIRTUAL_REPLAY_V1.md`。未实测自动新页创建/接管、完整 `T_B_VALID`、`T_VIRTUAL_BEST` 与恢复成本，`VIRTUAL_MATURE=NO`、`FINAL_VALID=NO`。
