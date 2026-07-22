---
name: industry-knowledge-accelerator
description: 将 PPT、PDF、网页、Markdown、研报和法规等多来源行业资料编译为可追溯、可增量维护、可诊断复测的行业 Wiki。用于新行业学习、PPT 建知识库、行业知识库、研报整理、行业 Wiki、持续补充行业资料、冲突审计或让多个智能体共享同一证据库；资料少于 3 份且只需一次性摘要时不要启用。
---

# 行业知识加速器

把分散资料编译成证据可回查的行业知识库，而不是堆文件或逐份摘要。当前版本为 `PILOT_ONLY`：先用 3—10 份资料完成一个行业试验，达标后再扩容。

## 开工门禁

1. 先运行 C 盘 Knowledge Brain/技能复用检查，确认没有成熟同类库可增量更新。
2. 冻结用途、行业边界、地域、时间范围、目标深度和 12 个验收问题。用户未明确时采用“小规模理解型试验”，不要导入全部历史资料。
3. 在 C 盘新建候选目录或独立 Git Worktree。旧库只读；禁止自动合并、自动 push、静默覆盖结论。
4. 对法律、医疗、金融投资、监管等高风险事实检索并核对最新一手来源；保留发布日期和采集日期。

## 快速启动

```powershell
python scripts/scaffold_industry_kb.py <目标目录> --industry "行业名称" --purpose "用途" --region "地域" --period "时间范围"
python scripts/register_source.py <项目目录> <来源文件> --title "标题" --type report --author-org "机构" --reliability B
python scripts/manifest_tool.py <项目目录>/sources/raw --out <项目目录>/evidence/source_manifest.json
python scripts/validate_industry_kb.py <项目目录> --require-sources --out <项目目录>/evidence/validation.json
```

脚本默认不覆盖已有文件、不访问网络、不修改原始来源。详细字段与命令见 [DATA-CONTRACT.md](references/DATA-CONTRACT.md)。

## 六阶段工作流

### A. 冻结范围

完成 `PROJECT_BRIEF.md`。用途必须落到理解、投资研究、创业、产品、写作或培训之一，并定义能判断第一阶段是否完成的问题。

### B. 登记来源

把原件放入 `sources/raw/`，提取文本放入 `sources/extracted/`。登记标题、机构、发布日期、采集日期、版本、定位、可靠性、主题和 SHA-256。

可靠性建议：A=法规/标准/政府/原始论文/公司正式披露；B=权威研究机构/教材/协会；C=券商研报/专家访谈/专业媒体；D=营销材料/自媒体/未核验二手资料。PPT 只可建立骨架，不得独立支撑高风险结论。

### C. 原子化提取

保留页码、章节、URL、图表标题、年份、单位、统计口径和原始出处。区分事实、推断、假设、数据点、观点与未知问题。

### D. 编译主题 Wiki

按主题综合多来源，不按“每份资料一篇摘要”组织。每页使用 `assets/templates/wiki_page.md`，关键结论必须绑定 `source_id + locator`。无法定位的内容只能进入待验证区。

小试收敛门禁：来源登记完成后，先在同一轮只产出 `01_行业总览.md`、必要的冲突记录和一次验证结果；通过后才扩展其他页面。连续两轮没有新增可验证页面或重复同一错误时，停止并标记 `PARTIAL`，报告阻塞点，不得无限研究或空转。

### E. 诊断与修复

至少覆盖定义、产业链、实体、技术、商业模式、市场数据、监管、风险、因果、对比、情景推演和来源追溯 12 类问题。执行“作答 → 回查 → 标记遗漏/误读 → 修复 → 复测”，保存三轮结果。

### F. 增量维护

新资料先计算哈希并分类为 new/updated/unchanged/deleted/duplicate，再列出受影响页面。冲突写入 `conflicts/`，验证后才修订正式页；更新 `changelog/` 并运行回归问题。

完整流程见 [WORKFLOW.md](references/WORKFLOW.md)。

## 交付闸门

正式交付必须同时满足：

- 来源登记率 ≥95%；
- 关键结论来源绑定率 ≥90%；
- 数据点含年份、单位和口径比例 ≥95%；
- 12 道诊断题可回答率 ≥85%；
- 关键问题可追溯率 =100%；
- 静默覆盖冲突 =0；
- 重复来源进入正式库 =0；
- 三轮实际测试全部通过。

未达标只能标记 `PILOT` 或 `NEEDS_REVIEW`。不得把外部 Wiki 说成模型参数训练结果，不得把包内自报测试当独立验收。

`PASS` 名称锁定：只有 `scripts/validate_industry_kb.py <项目> --require-sources` 返回码为 0，且三轮实际诊断均通过时，才能在任何字段中使用 `PASS`。局部产物检查、自定义 JSON 或结构抽查只能写 `PARTIAL`/`NEEDS_REVIEW`，不得另造 `artifact_validation=PASS` 等标签绕过正式门禁。来源文件必须复制或受控导入项目 `sources/raw/`；正式 registry 不得把项目外相邻目录作为 `relative_path`。

## 与现有技能的边界

- `expert-learning-synapse-skill`：面向个人学习路线和作品练习；本技能面向多来源证据库编译与维护。
- `326-karpathy-llm-wiki-first-real-ingest`：面向特定 326/Obsidian 插件首轮入库；本技能不依赖特定插件。
- `codex-video-to-usable-skill-loop`：把单份高价值材料沉淀为长期能力；本技能编译一个行业的多来源知识体。

## 失败与持续复用

- 失败时读取并更新 [FAILURE-REVIEW.md](references/FAILURE-REVIEW.md)。
- 每次真实调用后更新 [RECENT-USE-LOG.md](references/RECENT-USE-LOG.md)，记录耗时、资料数、通过率和冲突数。
- 项目级约束从 `assets/templates/AGENTS_PROJECT_TEMPLATE.md` 复制，禁止直接覆盖全局 `AGENTS.md`。
- 30 天或 3 次真实调用后复核 ROI；没有实测数据时必须写“尚无实测”。
