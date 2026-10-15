# F017｜基于F016实证的同质量按需路由减负候选（Reality前冻结）
继承F016完成结果，TASK=HERMES-ECO-20261014，METHOD《三人行》V2，本项目调用Windows V6 C通道与Hermes v2.0母技能。

## 真实成熟基线
F016相同用户意图：Windows PowerShell5.1脚本变更前，需要成熟的host冻结/编码解析/原件备份/独立验收，要求只生成计划、没有任何修改。通过Hermes母skill_view→KB INDEX.md/ROUTING_MAP.md→skills-index.md关键词搜索42结果→真实加载3个Codex技能→给出3组正确执行要点。exit0、process runtime202.49s，真实可用但不是稳定时间基线。

## FIRST_DELTA与成熟候选
F016在用户意图明确且前一个自然节点已冻结Knowledge Brain路由的情况下，仍重复展开完整INDEX/ROUTING_MAP并读取3份技能。其主要技能powershell-reliability-guard本身已包含WindowsPS5.1主机绑定、UTF8 BOM、byte backup、parser、外部独立测试和exit code规则。对同样质量目标，单个最适配源通常足够，只有遗漏强制能力才加载第二/第三份。此为成熟渐进披露与局部资料按需加载，不造新的库/执行器。
候选新流程：Hermes母技能当前索引可用且F014当前冻结验证INDEX/ROUTING→目标类型已归入Codex，则在相同节点不再读完整INDEX/ROUTING；native search_files对 `C:/Users/A/.codex/knowledge-brain/indexes/skills-index.md` 以 PowerShell5.1/兼容/备份/独立验收等词精准查找并读取对应局部；从唯一最佳候选的精确C盘Codex SKILL.md实际read_file，能完整涵盖三类质量门即STOP，多条证据不足时最多增至3候选。不可告诉模型真实技能名。

## Reality与决定
用既有正式CLI，固定与F016完全相同自然任务意图和三个必备输出门：①host 5.1明确锁定+parser/compat preflight，②修改前byte backup+UTF8 BOM/atomic，③原生外部测试/exit code独立验收。无源文件编辑/安装/脚本执行/密钥读取。只改变冻结的资料读取路线，不改变模型和质量合同。
执行进程退出0并确认真实技能 read_file、三组实质内容齐全才VALID；测一次完整进程耗时并与F016 202.49s样本作**观察比较**，记录检索轮次、技能文件数、失败重试；没有多次同分布测试不宣称T*或稳定提速。
若结果质量不足/技能误选/任务未完成，标ABANDONED，保留F016真实基线；如果完整质量有效且节时，KEEP并将简洁路线写入原F014参考，不添加冗余引擎或隐式自动并行。
