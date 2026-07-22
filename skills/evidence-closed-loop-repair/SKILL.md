---
name: evidence-closed-loop-repair
description: Use this skill for file, prompt, skill-pack, command-pack, template, generated-artifact, ZIP/7z, or multi-file repairs where a change must propagate through source files, derived files, generators, validators, mirrors, reports, screenshots, and final downloadable packages. Trigger especially after two failed revisions, when users say “you said it was fixed but it is still wrong,” or whenever final-deliverable evidence, recursive archive inspection, negative-zero checks, hashes, screenshots, and cold-start verification are required.
---

# 全量证据闭环修复（Evidence-Closed-Loop Repair）

## 核心原则

**没有被独立、可复核证据证明已经完成的事项，一律视为未完成。**

不要验证“工作过程看起来是否完成”，只验证：

1. 用户确认的正确内容是否出现在全部必要位置；
2. 错误内容及其别名是否严格为 0；
3. 真源头、生成器、派生文件、镜像母版和最终压缩包是否一致；
4. 用户最终下载的 ZIP/7z 是否在全新目录冷启动解压后仍然通过；
5. 每个 PASS 是否绑定路径、计数、哈希、字节比较、截图或语义证据；
6. 无法证明的内容是否明确标记为 `PENDING`，而不是猜测为 PASS。

## 何时必须使用

满足任一条件，强制启用完整模式：

- 同一问题已经返工两次；
- 用户反馈“你说改了，但我下载后仍然没改”；
- 修改跨越 5 个以上文件；
- 存在源文件、派生文件、装配文件或稳定母版；
- 存在生成脚本、同步脚本或验证脚本；
- 最终交付 ZIP、7z、安装包或嵌套压缩包；
- 修改模型名、品牌名、版本号、全局配置或核心规则；
- 用户要求逐文件检查、截图、哈希、三轮测试或证据矩阵；
- 验证器可能与生成器共享同一真值或替换字典。

## 不适用或可降级的场景

单一、无派生、无压缩包、无生成脚本的低风险文本改动，可使用轻量模式。但只要出现一次“最终文件与声明不一致”，立即升级完整模式。

## 执行前置字段

每次执行前必须先写明：

```text
执行平台/工具：
模型版本：
工作强度：
运行位置：Local / Git Worktree / 临时副本
是否允许并行：只读检查可并行；同一文件写入禁止并行
是否允许自动merge：否，除非用户明确授权
是否允许自动push：否，除非用户明确授权
是否允许修改原版：否
失败回退：删除候选副本或恢复至冻结哈希
```

## 简洁收益成本闸门

```text
中文名称：全量证据闭环修复
要解决的问题：声称完成但最终交付仍错误
预计收益：Forbidden残留降为0；派生同步率和最终包验证率达到100%
预计成本：小型任务约增加5—20分钟；大型多派生任务约增加20—60分钟
量化指标：Required=100%；Forbidden=0；镜像字节一致=100%；锁定哈希不变；最终包冷启动验证=100%
收益成本判断：出现两次返工、多层派生或压缩包交付时，收益显著高于成本
是否执行：满足触发条件时强制执行
完成后实际数据：必须在最终报告填写，禁止空泛写“已完成”
```

# 十二道 Gate

## Gate 0｜建立独立变更合同

先创建 `CHANGE_CONTRACT.json`。正确真值必须来自用户确认，不得从生成器的替换表推导。

合同至少定义：

- `required`：必须存在的内容、作用域和最低次数；
- `forbidden`：禁止内容、别名、大小写变体和最高次数（通常为0）；
- `locked_files`：禁止变化的核心文件与 SHA-256；
- `derived_relations`：目标文件如何由源文件生成；
- `mirrors`：0号/1号、模板/运行母版等必须逐字节一致的文件；
- `deliverables`：最终 ZIP/7z 等用户下载文件；
- `semantic_checks`：不能用字符串扫描替代的功能判断；
- `pending_checks`：只能通过真实运行验证的事项。

**禁止**让生成器和验证器共享同一替换字典作为真值。

## Gate 1｜建立全量影响图

盘点并分类所有可能受影响对象：

1. 真源文件；
2. 派生/装配文件；
3. 稳定母版、镜像副本；
4. 构建、同步、迁移脚本；
5. 验证脚本和测试夹具；
6. README、报告、网页、索引；
7. 截图和视觉证据；
8. 文件名、目录名、元数据；
9. 独立压缩包；
10. 最终完整压缩包和内部嵌套包。

使用 `templates/IMPACT_GRAPH.template.md`，不得只列“我准备修改的文件”。还要列“可能重新引入旧值的文件”。

## Gate 2｜冻结原版

原版只读。记录：

- 根目录；
- 文件总数；
- 聚合哈希；
- 核心锁定文件 SHA-256；
- Git commit（如有）；
- 编码、BOM、换行等必要属性。

所有修复在独立副本或 Git Worktree 中进行。

## Gate 3｜修复真源头和生成逻辑

优先修改：

- 源提示词、模板、配置；
- 生成器、装配器、同步器；
- 验证合同，不是验证器内部硬编码的旧真值。

禁止只修改最终产物来掩盖错误源头。若生成器仍会重新引入旧值，任务不得进入下一 Gate。

## Gate 4｜全量重建派生物

从已修正的真源头重新生成全部派生物。不要对派生文件逐个手工打补丁，除非合同明确它们是独立源文件。

重建后同步：

- 装配命令；
- 稳定母版；
- 报告和网页；
- 验证脚本和夹具；
- 截图；
- 独立包与最终包。

## Gate 5｜正向必需项验证

证明正确内容存在，而不是只说“看起来对了”。

每个 required 项必须报告：

- 路径；
- 出现次数；
- 期望阈值；
- 实际文本或行号；
- PASS/FAIL。

## Gate 6｜负向禁止项清零

证明旧错误为 0。检查：

- 正文；
- 文件名和目录名；
- 脚本字符串；
- 报告、网页和截图文字；
- ZIP/7z内部文件；
- 嵌套压缩包。

“新词出现”绝不能替代“旧词为0”。

## Gate 7｜派生关系与镜像一致性

验证：

- `target = source A + source B` 等装配关系；
- 0号/1号、模板/母版逐字节一致；
- 派生文件没有旧槽位、重复区、截断或拼接粘连；
- 核心锁定片段在装配后仍保持原哈希或精确字节。

## Gate 8｜独立验证器

验证器必须读取 `CHANGE_CONTRACT.json`。不得从构建脚本导入正确模型、品牌或替换映射。

至少运行两类夹具：

- Good fixture：应通过；
- Bad fixture：即使多数文件正确，只要一个派生物或最终包残留旧值，就必须失败。

如果坏样本也能 PASS，验证器本身失败。

## Gate 9｜最终包冷启动复核

最终交付物生成后：

1. 建立全新临时目录；
2. 分别解压 ZIP 和 7z；
3. 不使用旧工作目录或旧扫描缓存；
4. 再次执行 Required、Forbidden、哈希、镜像和语义检查；
5. 递归打开嵌套压缩包；
6. 比较 ZIP 与 7z 解压树的路径集合和逐文件 SHA-256。

若环境无法检查 7z，状态必须是 `PENDING_UNVERIFIED_7Z`，不能写 PASS。

## Gate 10｜视觉和语义证据

截图用于证明用户实际看到的关键结构、顺序和报告页面。截图不能替代机器扫描。

语义 Gate 用于检查：

- 文件虽然包含正确关键词，但功能是否成立；
- 审核层是否只评论、不落实修复；
- 最终答案是否可独立使用；
- 是否把不应承担的职责混入某层；
- 是否出现与核心评分或规则冲突的第二套逻辑。

无法由静态文本证明的真实质量，标记 `RUNTIME_VALIDATION_PENDING`。

## Gate 11｜证据矩阵与状态分层

每个结论必须绑定证据。使用 `templates/EVIDENCE_MATRIX.template.csv`。

证据等级：

- E0：只有口头声明，禁止发布；
- E1：局部文件或截图，只证明局部；
- E2：工作目录全量机器检查，状态为 `WORKTREE_PASS_PACKAGE_PENDING`；
- E3：最终包冷启动、递归扫描、哈希、截图全部通过，可标记 `FINAL_ARTIFACT_EVIDENCE_PASS`；
- E4：真实环境端到端运行，才能证明真实质量、时间和商业收益。

## Gate 12｜发布纪律

发布时必须提供：

- 新文件名或明确版本号；
- SHA-256；
- 最终报告；
- Required/Forbidden量化结果；
- 冷启动解压结果；
- 仍为 PENDING 的项目。

返工两次后禁止继续使用无法区分的新旧同名文件；默认使用新版本号或时间戳。

# 标准执行顺序

```text
用户要求
→ CHANGE_CONTRACT
→ 影响图
→ 冻结原版
→ 修真源头和生成器
→ 全量重建
→ Required验证
→ Forbidden清零
→ 派生/镜像/哈希验证
→ 独立验证器Good/Bad夹具
→ 最终ZIP/7z冷启动重解压
→ 嵌套包递归检查
→ 视觉和语义Gate
→ 证据矩阵
→ 分层发布
```

# 工具入口

```bash
# 1. 生成/核对哈希清单
python scripts/hash_manifest.py <root> --output MANIFEST_SHA256.txt

# 2. 按合同验证工作目录
python scripts/verify_contract.py --root <root> --contract CHANGE_CONTRACT.json --out-dir evidence

# 3. 比较两个目录树
python scripts/compare_trees.py <tree_a> <tree_b> --out compare.json

# 4. 冷启动验证最终包
python scripts/cold_extract_verify.py --archive <file.zip|file.7z> --contract CHANGE_CONTRACT.json --out-dir cold_verify

# 5. 一键编排
python scripts/run_evidence_closed_loop.py --root <candidate_root> --contract CHANGE_CONTRACT.json --archives <a.zip> <b.7z> --out-dir evidence

# 6. 技能自测试
python scripts/self_test.py
```

# 强制停止条件

出现任一情况立即停止发布：

- Forbidden > 0；
- Required 未达到阈值；
- 锁定哈希变化；
- 镜像字节不一致；
- 派生关系不成立；
- Good fixture失败；
- Bad fixture意外通过；
- 最终包未冷启动解压；
- 嵌套包未验证；
- 7z无法检查却被宣称PASS；
- 语义问题无法确认却被宣称已解决。

# 输出格式

最终输出必须包含：

1. 实际修改了什么；
2. 真源头和派生链；
3. Required计数；
4. Forbidden计数；
5. 锁定哈希；
6. 镜像/派生关系结果；
7. 最终ZIP/7z冷启动结果；
8. Good/Bad验证器测试；
9. 截图和报告路径；
10. `PASS / FAIL / PENDING`；
11. 唯一下一步建议。

详细逻辑和真实试错过程见：

- `FULL_LOGIC_EXPLANATION.md`
- `examples/ultrafusion-qwen-case/CASE_STUDY.md`
- `tasks/`
