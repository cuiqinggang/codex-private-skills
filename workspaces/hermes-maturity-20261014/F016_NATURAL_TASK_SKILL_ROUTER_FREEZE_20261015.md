# F016｜自然语言任务自动选择 Codex / Knowledge Brain 成熟技能：真实验收前冻结
TASK HERMES-ECO-20261014；METHOD《三人行》V2；C桥V6；Hermes母技能v2.0；前置F013原生母技能加载PASS与F014指定路径跨根读取PASS。
尚缺不是能否读指定文件，而是能否**仅凭任务意图**从Knowledge Brain技能索引找到最合适的Codex成熟规则并定点实际加载，而不是GPT指定一个SKILL.md路径。避免纯展示索引或模型自报会使用。

## Reality真实隔离输入
单次合法Hermes正式CLI任务：用户意图'准备修改一个Windows PowerShell5.1自动化脚本，需要成熟的兼容性检查、变更前备份、Parser/编码可靠性与独立验证方法，但本轮只做安全的执行计划，不修改任何脚本'。
不给具体Codex技能名，只告知必须先使用已部署Hermes母技能及其F014知识库索引路线，按已成熟INDEX/ROUTING_MAP/skills-index定位Top 1~3，再用原生read_file实际读取所选相关 SKILL.md（候选通常包括已部署powershell-reliability-guard等，但不向模型点名），输出使用的真实技能名、源路径、引用证据及三条具体可靠性/验收要点。
一次自然模型任务，禁止批量扫描所有目录、执行修改、调用不允许的工具、重装、改FlClash/代理/私有配置。

## PASS规则
真正通过native skill_view母技能或F014 reference、实际KB category索引检索、真实Codex SKILL.md read_file回执；选中条目与任务高度相关、来源存在且至少三条内容匹配。任一步失败不能直接宣称AUTO_ROUTER_PASS；只能记录最低可证据等级。
若能做到，证明'任务意图→成熟索引→单个实际Codex技能'真实端到端，可作为未来约400项来源候选的按需选择方法；仍非所有技能完成运行认证。全程墙钟含检索，不拿一次样本作为物理极限。旧整站0/5，FINAL_VALID=NO。
