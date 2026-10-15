# F012｜《三人行》V2：Hermes 复用 Codex / Knowledge Brain 的技能发现成熟化冻结
任务 HERMES-ECO-20261014，继承 F011 CLI优先规则、Hermes原专用 v2.0、GPT→Windows V6 C>A>B。阶段=VIRTUAL_MATURE_FROZEN。

## 真实只读盘点（2026-10-15）
经C通道查询：C:/Users/A/.codex/skills 一级目录209，递归SKILL.md文件218；C:/Users/A/.hermes/skills 一级目录85，递归SKILL.md文件161；C:/Users/A/.codex/knowledge-brain 递归文件632。数量跨根有重复/分类/内置技能/非技能资料，不可算379个独立Hermes可执行技能或632额外技能。Hermes config get skills.external_dirs 当前返回 []。先前 hermes skills list --source local 返回0；这个指令统计的local-source类别未必等于运行时 skills_list 真正可发现索引。
官方成熟机制：https://hermes-agent.nousresearch.com/docs/user-guide/features/skills ；使用 ~/.hermes/skills 主目录、skills.external_dirs 额外扫描、skills_list(名称摘要)/skill_view(按需完整SKILL.md及reference)实现渐进加载。新会话通常读取新索引；外部目录只要可写，Agent自身可能修改，external_dirs 不是只读保护边界。不要整库复制、批量激活危险技能，也不生成新执行引擎。

## 最小攻击树，先用合法只读Reality验证，不假定故障
1. D1 GOOD：现有Hermes正式CLI对代码Repair/子代理/文件/视觉已有真实结果，沿用。
2. D2 DISCOVERY：正式Hermes CLI开启独立隔离一次任务，真实调用 skills_list（不是模型根据提示词虚构），检查 hermes-mature-supertool、hermes-repair-loop-adapter 与基础内置/本地skill；若已存在，标记旧 --source local 统计口径误用，勿改配置。若不存在，定位技能发现路径/Profile/嵌套frontmatter。只能一次隔离Reality。
3. D3 POLICY：当确定既有Hermes技能发现正常且Codex目录不包含需阻止的会写敏感配置/网页自动化技能时，先审查正式清单及质量/重复/冲突；允许逐步按官方skills.external_dirs 指向经过选择的Codex技能目录，确保不会因外部目录可写而修改原Codex资产。没有确切安全边界就仅做安全索引+原技能工具内只读读取，不配置全部外部目录。
4. D4 KB：Knowledge Brain不是全部标准SKILL.md，按其已有INDEX.md/ROUTING_MAP.md/索引检索匹配具体问题，只读按需加载；不批量导入模型上下文。
5. D5 ACCEPTANCE：从Codex实际选1个标准技能、Hermes原专项1个、知识库一个定点条目，各通过真实列表/按需文件读取/只读应用的观察回执；母技能v2.0和原有修复代码哈希不变、无代理/密钥/浏览器/Docker修改。

## 本轮已知额外缺口
F011 C盘 SKILL.md/新 CLI-first reference/RECENT-USE-LOG 已增量写入、备份原哈希回读。全包静态检查一条yaml secret pattern 告警致overall FAIL，禁止输出/触碰可疑原文；此项另设安全门解决，不为漂亮统计删历史配置。
所有Reality限只读或明确隔离小任务；旧F002原Runs请求UNKNOWN，禁止重发。五轮整站仍0/5，FINAL_VALID=NO。
