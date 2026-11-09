---
name: run-batch-automation
description: 使用《极限效率流程库》V1.3（原《批量自动化流程索引》），检索分类成熟流程并按目标、输入、业务口径、输出、环境及验收深度匹配后调用原程序；每批任务验收结束都检查可复用步骤，更新原条目或保存快捷流程候选。用户要求自动化、直接调用、固定配方、流程沉淀、任务收尾、类似任务复用、极限短时间或成熟流程全面整理时使用。保存原程序、参数、依赖、成功与失败证据和真实耗时；已验三类可直达，未接入候选不冒充可运行。
---
# 极限效率流程库

版本：V1.3，2026-11-10（北京时间）。目标：同等质量和约束下，缩短完整有效交付时间；每批收尾积累可复用的快捷入口，消除不必要的模型往返。沿用已有原专业包，不为归档另造业务核心、调度器或强制包装层。

## 每批任务固定收尾

1. 单个任务也视为一批。先完成原任务和用户实际使用路径的验收、产物读回；失败与待完成项如实保留。
2. 每批必检查：本次原程序、固定参数、成熟节点组合或失败修正能否复用。已有同合同条目就更新原条目，不重复造一个流程；没有可复用项就简记原因。
3. 按[收尾合同](references/completion-capture.md)提取本批已实际使用的入口、可变参数、输入语义、输出、环境、原检查及成功/失败证据；GPT/Pi负责填记录，用户不手写JSON。不复制凭据、业务数据或无关文件。
4. 调用下面的收尾记录器。它保存查重后的记录、原件指纹及明确指定的原件副本，并更新下次查询的本地索引；不生成新业务算法、不执行记录里的命令、不自动安装。

```text
python <本包>/scripts/capture_flow.py --record <本批收尾.json>
```

5. `REUSED`追加原流程的使用证据；`NEW_CANDIDATE`生成可检索候选；`NO_REUSABLE_FLOW`只记录检查结果。保存不等于就绪。新增类别按[本地接入顺序](references/local-adoption.md)核原件、依赖、精确合同和实际用户路径，验收通过才登记对应上下文为READY。
6. 下次先查就绪合同和相关本地收尾条目，再查分类公共来源。已知匹配入口不重复搜索、重建或部署。收尾失败不撤销已交付成果，保留本批记录并说明缺口；不无限重复入库。

本机收尾索引固定为 `C:/Users/A/Documents/DSH-Workspace/automation-flow-library/recipes.json`，记录在同目录records，指定原件副本在sources。query.py在Windows自动合并此索引；其他环境用`--learned <索引路径>`。Pi遇当前工具沙箱不可写时保留工作区内收尾记录，按原GPT接续机制归档，不越权写目录。规则加载和将来每次遵守不能仅由文件存在推定；本轮已验证范围见[R87接续验收](references/R87-Completion-Acceptance.json)。

## 一次匹配，直接调用

1. GPT先把用户目标与实际文件明确为本批合同。采用[合同示例](references/request-examples.json)，用户不必手写JSON；必要业务口径缺失时不猜金额单位、去重、大小写或舍入规则。
2. 已有当前批有效MATCH回执时，直接采用其中argv、cwd和两项UTF8环境参数；不重复查全库、匹配或读同一原件。输入或环境改变则重新核对，不能沿用别批回执。
3. 未匹配的新批次调用一个薄接口：

```text
python <本包>/scripts/invoke_flow.py --request <本批合同.json>
```

它只复用只读匹配器，将MATCH参数转交原程序；不含业务实现、原验收替代品、模型、调度或自动安装。原程序退出码及输出直接保留。需预览而不执行时使用：

```text
python <本包>/scripts/match_flow.py --request <本批合同.json>
```

4. MATCH只证明输入与调用合同适用。实际执行后仍以原固定检查、真实产物读回和本批额外要求决定交付；进程结束或模型说完成不能替代验收。
5. NEEDS_CONFIG返回具体缺项，不启动流程；NOT_MATCHED返回冲突，不缩减合同、不猜映射、不擅自分批或变更权限来制造匹配。未命中再查原专业包或下面的公共流程索引，按成熟资料配置和验收后补入。

## 当前已复制并验收的宿主流程

| 类别 | 目标ID | 主要交付与原检查 |
|---|---|---|
| Word/Excel/PPT/TXT正文提取 | office.extract_body | JSON、来源、输入一一对应、源指纹与回执读回；本轮20文件/60内容标记通过 |
| 文件字节归档 | files.archive_exact | ZIP、指纹清单、回执；成员相对路径、原字节、CRC及源不变；本轮48文件通过 |
| 整数分订单报表 | orders.report_integer_cents | CSV/JSON/Word/Excel与原独立20项检查；本轮180行、退款、重复及大小写等边界通过 |

[机器合同](references/executable-flows.json)固定参数和边界。宿主路径READY；复制版本的inside_omp_tool路径当前为CONFIGURED，匹配器不会从宿主通过推定其他上下文通过。原R85已经验收的旧Office沙箱内入口继续保留在[旧绑定](references/ready-bindings.json)，不得重复套外层启动器。现有三类匹配器不因目录新增就自动支持新类别；新类别先配置原专业入口并真实验收，再做最小必要的调用适配。

## 深度匹配条件

- 目标、文件格式和数量、单文件和总大小、授权工作目录、相对输入、唯一输入及新输出必须适用。
- 输出和所有required capabilities必须被原流程覆盖。OCR、版式保真、外部Office重算、ACL/时间戳完整备份等未覆盖要求直接拒绝，不能只看文件后缀。
- 订单要求精确五列表头、显式整数分、保留重复、精确大小写和文本标识符；金额/数量须规范整数文本。原business_pack.load_rows负责原业务准入，不重写该核心。
- 固定Python、依赖、原件指纹及调用上下文须匹配。上下文分别就绪；无已验数据不自动安装或重连账户。原源码、唯一一处目录配置适配及依赖见[原件清单](references/copied-originals.json)。
- 所有原程序和验收器保留原字节；旧订单薄入口只将H目录绑定为同包orders，未修改业务算法。复制后的完整原件在assets/ready-flows/，不只保存网址。

## 实测与极限效率目标

[R86真实验收](references/R86-Library-Acceptance.json)保留三类各两批、14个实际合同匹配边界，以及单入口真实执行；全部业务沿原检查与独立读回通过。匹配用时00:00:144—00:00:622；宿主文档首批00:32:417、第二批00:12:342，归档00:03:717/00:03:129，订单00:12:299/00:05:824；另一次单入口归档00:04:880。不同输入、批次与负载样本分别保留；未核缓存状态不称冷/暖启动，不据此计算稳定倍数。

[旧R85](references/R85-Reality-Comparison.md)的约6秒只对应当时已选配方的样本。Pi模型选路曾更慢，不能把当前程序计时当成任意自然语言整链。已明确参数时优先直接用本库，保留检索、首次配置、失败、恢复和验收投入。首次GPT理解、整个库准备与本页交互总耗时未统一计时，记NOT_MEASURED。

## 扩充来源与兼容索引

原32个公共模板及历史证据保留；本轮扩大平台来源、原生操作与分类覆盖。准确数量、已知限制及未接入清单见[整理总览](references/R87-Catalog-Coverage.json)、[机器索引](references/recipes.json)及[上游目录](references/catalog-sources.json)。这是可扩充的主要成熟来源索引，不声称已收齐所有互联网流程，也不整体安装所有平台。按需查最相关1—3条：

```text
python <本包>/scripts/query.py "具体用途" --limit 3
python <本包>/scripts/query.py "具体用途" --kind local
python <本包>/scripts/query.py --kind source --platform <平台>
python <本包>/scripts/query.py --categories --kind all
```

公共模板收录不等于已配置或验收。新增高频流程时先取原件，按原接口配置、真实验收并登记各上下文；条件齐全才进入可直接调用合同。旧原生程序卡、来源、失败和R85证据不删除，详见[选择规则](references/selection-and-use.md)、[旧专业合同](references/existing-recipes.md)、[原生工具候选](references/official-recipes.md)、[Pi接入](references/Pi-Integration.md)与[历史核对](references/verification.json)。
