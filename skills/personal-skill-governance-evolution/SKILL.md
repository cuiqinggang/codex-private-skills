---
name: personal-skill-governance-evolution
description: 治理、净化、增强或持续进化个人技能库；处理现有技能目录、重复与触发冲突、批量机械整理、内部结构瘦身、入口治理、验证、正式采用和逐技能回滚。用户要求升级技能、联网寻找成熟同类方案、吸收 GitHub/文章/视频优点、技能反复失败或长期未更新时，也使用联网对标增强净化。不得修改系统技能、访问凭据或把外部候选直接批量安装。
---

# 个人技能包治理与进化

${REDACTED_SECRET}

## 触发与模式

- 已有可信目录、活动视图和问题清单，用户要求批量治理：读取 [fast-library-purification.md](references/fast-library-purification.md)，进入高速模式，禁止重复盘点。
- 单一技能或证据不足：用小步模式，先冻结关键行为，再做一项明确改进。
- 用户要求升级/增强、技能反复失败或返工、出现成熟同类方案、用户提供 GitHub/抖音/视频/文章、技能长期未更新、能力明显落后或多个技能重复同一任务：进入联网对标增强净化。
- 创建或编辑技能时复用系统 `skill-creator`，不复制它；不修改 `.system`、安全隔离、凭据、retired、备份和人工争议项。

## 高速治理

1. 排除系统、官方管理、历史/备份、安全隔离、不可写和争议项。
2. 按机械=1、结构=2、超长/重叠=3 加权分成互斥工作面；一个技能只有一个 owner。
3. A 类批量修 frontmatter、精确旧路径、失效引用和确认的发现噪声。
4. B 类把长案例/边界拆到一层 `references/`，确定性重复逻辑写入 `scripts/`。
5. C 类统一重叠 description 和 canonical/alias/specialist/internal 边界，并做正向、反向、边界路由测试。
6. D 类只保留真正需要人工语义判断的合并、退役、安全和系统例外，不得阻塞 A/B/C。
7. 使用 `scripts/fast_governance_batch.py` 执行显式 manifest：批次回滚根、逐技能 before、独立验证、单技能失败回滚并继续。

## 联网对标增强净化

读取 [online-benchmark-evolution.md](references/online-benchmark-evolution.md) 与 [candidate-admission-license-safety.md](references/candidate-admission-license-safety.md)。

1. 只搜索相关能力簇，不重扫全库；用中英文任务关键词，优先官方规范、官方插件、原作者仓库和成熟开源项目。
2. 第一批只发现与核验，不安装、不运行未经审查的外部代码。记录来源、维护、用途、示例、依赖、Windows/Codex 适配、API/付费/凭据、高风险命令、许可证和重复度。
3. 用完全相同的正常、边界、失败恢复任务比较本地、候选与增强方案，记录成功、质量、步骤、人工干预、时间、可得 Token、安全和可维护性。
4. 决策只允许 `ABSORB`、`COMPLEMENT`、`REPLACE_COMPONENT`、`KEEP_LOCAL`、`REJECT`、`DEFER`。至少一个重要指标明确提升且无关键行为或安全下降，才进入第二批。
5. 优先吸收方法和组件；许可证未知或不允许复制时只做独立实现。不得因 Star、点赞或宣传直接采用。
6. 能力差异矩阵必须通过 `scripts/validate_online_benchmark.py`。总控建立统一回滚根和逐技能 before，再正式应用；单技能失败只恢复该技能。

## 多智能体边界

总控按实际能力形成互斥簇、登记唯一 owner、汇总候选、控制正式应用并维护本技能。执行面只做其能力簇的搜索、核验和对标，不得并发写公共治理技能。默认三面为：长任务/编排/治理；浏览器/GitHub/知识/自动化；视频/设计/演示/图像/内容。按工作量调整，不机械按名称排序。

## 验证与回滚

结构/合并前读取 [behavior-coverage-checklist.md](references/behavior-coverage-checklist.md)；精简/入口修改前读取 [writing-quality-rules.md](references/writing-quality-rules.md)。

- 所有修改：UTF-8、frontmatter、引用、路径、结构、官方 `quick_validate.py`。
- 机械修改：全量静态验证 + 至少 10% 语义抽查。
- 结构修改：关键行为合同 100% + 代表性行为抽样。
- 路由修改：每个冲突簇做正向、反向、边界测试。
- 联网增强：正常、边界、失败恢复回归；检查误触发、额外依赖、许可证与安全门禁。
- 合并、退役、安全：逐项完整验证。静态检查不得冒充真实收益；没有观察数据必须写“尚无实测”。

## 完成合同

最终只交付机器可读增强清单、一个统一回滚目录和简明总结。报告搜索簇、有效/拒绝/对标候选、正式增强技能及具体吸收点、新增脚本/规则/references、KEEP_LOCAL、许可证/安全/适配拒绝、真实收益与缺证项、回滚数和总耗时。每批结束后把确定性操作留在 `scripts/`、通用规则留在本入口、长边界留在 `references/`；搜索结果和过程日志留在任务输出，不塞入技能包。
