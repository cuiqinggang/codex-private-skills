---
name: solo-founder-success-research
description: 研究、验证、对比并持续更新独立开发者、一人公司、独立站与应用产品案例。用于人物研究、产品拆解、多人对比、赛道研究、失败分析、收入/MRR/ARR核验、是否真正一人运营判断，以及把新案例写入证据分级案例库；触发词包括“研究独立开发者”“一人公司案例”“分析为什么成功”“对比创始人”“适合一人公司的赛道”“更新人物近况”。
---

# 独立开发者与一人公司成功方法研究

## 开工流程

1. 先运行 `python scripts/detect_stale_records.py`，读取 `data/indexes/update-status-index.md`。
2. 判断请求属于人物、产品、多人对比、赛道或失败研究。
3. 按需读取对应框架与模板，不要一次性加载全部案例。
4. 优先检索 A/B 级来源；涉及当下状态、价格、团队或收入时必须联网复核。
5. 将每条关键事实写入证据表；收入必须区分收入、利润、MRR、ARR、单月峰值和累计收入。
6. 对创始人自报数字标注“自报，非审计”；冲突数字并列呈现，不擅自平均。
7. 生成中文报告，明确事实、推断、未知项、适合复制、条件性复制和不建议复制。
8. 用户要求入库或更新时，保留历史记录，运行 `python scripts/build_indexes.py` 和验收脚本。

## 能力路由

- 人物研究：读取 `frameworks/founder-research-framework.md` 与 `templates/founder-profile-template.md`。
- 产品研究：读取 `frameworks/product-analysis-framework.md` 与 `templates/product-profile-template.md`。
- 多人对比：读取 `templates/comparative-analysis-template.md`，所有人物使用同一维度。
- 赛道研究：读取 `frameworks/monetization-framework.md`、`frameworks/solo-operability-framework.md`。
- 失败分析：必须读取 `frameworks/failure-analysis-framework.md`，不能只写成功故事。
- 更新案例：读取 `frameworks/update-framework.md` 与 `sources/fact-checking-rules.md`。

## 八阶段研究门禁

1. 定义对象、时间范围和用户最关心的问题。
2. 建立候选来源：官方站、官方博客/访谈、公开面板、Indie Hackers、Hacker News、Product Hunt、权威媒体、社交原帖、二手总结。
3. 提取事实：内容、链接、来源类型、发布日期、事实对应时间、证据等级、自报标记、二次验证需求。
4. 检查收入、用户、团队、产品状态、出售与转型的冲突。
5. 构建“时间—动作—结果—成败—能力—后续影响”时间线。
6. 提炼需求、MVP、收费、获客、交付、复购、组合、淘汰和维护机制。
7. 分成适合复制、条件性复制、不建议复制。
8. 使用最终报告模板输出，并注明信息更新时间。

## 强制输出项

人物报告必须覆盖背景、起步、产品、时间线、失败、成功、商业模式、获客、自动化、真实 solo 状态、收入证据、转折点、教训、可复制与不可复制部分，以及对用户业务的启发。

产品报告必须覆盖问题、用户、MVP、上线、获客、定价、商业模式、技术依赖、成本、自动化、竞争优势、风险、当前状态与可持续性。

赛道报告必须覆盖定义、验证案例、付费意愿、拥挤度、技术门槛、获客成本、单人维护难度、上游依赖、合规风险、进入方式、MVP 与退出条件。

## 评分

对需求真实性、付费意愿、分发能力、自动化、单人可维护性、技术可控性、利润结构、竞争壁垒、生命周期、可复制性各评 0–10 分。80–100 高度值得研究；65–79 有价值但需条件；50–64 局部可借鉴；30–49 风险较高；0–29 不建议模仿。评分是分析判断，不是事实，必须给出依据。

## 证据底线

- A：创始人/产品官方站、官方博客、官方原帖、公开财务面板。
- B：直接访谈、Indie Hackers/Hacker News 原帖、Product Hunt、权威媒体。
- C：二手分析、新闻转载、未能验证的社交转述。
- D：截图、无来源图片、营销号；只能当线索。
- 关键数字至少需要一个 A/B 级来源；仅有 C/D 时写“未验证”。
- 当前状态不得从旧采访推断；必须标注核验日。

## 数据与更新

- 方法放在 `sources/`、`frameworks/`、`templates/`；人物和产品记录放在 `data/` 或 `examples/`。
- 核心人物 90 天、高变化 AI 产品 45 天、稳定工具 180 天复核。
- 超期记录由脚本报告 `STALE_REVIEW_REQUIRED`，不伪造已验证状态。
- 历史收入和状态按日期追加，不覆盖旧值。
- 每次更新写入 `data/updates/`，记录新增来源、修正内容、可信度变化和是否改变结论。

## 完成条件

运行：

```powershell
python scripts/validate_structure.py
python scripts/validate_sources.py
python scripts/detect_stale_records.py
python scripts/build_indexes.py
python scripts/run_acceptance_tests.py
```

只有结构、来源、陈旧检测、三个用例和最终验收全部通过，才报告 `PASS`。
