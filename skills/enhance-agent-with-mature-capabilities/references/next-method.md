# 下一轮：成熟方法直接复用

> 以下为V1原始历史起点。2026-10-29已完成DSH补测与迟后接续；先读[最新续接](dsh-continuation.md)，不要重跑库存题或沿用“DSH尚未执行”的旧状态。

## 已找到的现成资源

| 内容 | 原位置 |
|---|---|
| DSH成熟入口 | C:\AI\DSH-Acceleration-20261024\launch.py / Run-DSH.cmd |
| 高推理交付配置 | 同目录delivery.patch.yml：Flash/high，官方Office skill、原web与CSV插件 |
| auto配置 | 同目录auto.patch.yml：Flash/low；低推理只在有限既有合同有证据 |
| 官方运行时 | C:\AI\DeepSeek-Harness-Trial\dsh-0.2.1-rc.2-isolated\node_modules\@deepseek-ai\dsh\lib\bin.js |
| 成熟技能 | C:\AI\DeepSeek-Harness-Trial\dsh-home-mature-agent\skills |
| 原生恢复器 | 该skills下dsh-mature-capabilities\scripts\run_resumable.py |
| 成熟业务/经验 | 该技能SKILL.md与references\reuse-and-recovery.md |
| Pi按需技能标准 | 已安装Pi docs\skills.md：展示名称/描述/路径，再按任务加载正文 |

原入口、配置和恢复器已读回，DSH**未执行本轮新题**。不安装或复活DeerFlow/Hermes；沿用已有absorb-deerflow-capabilities的行为映射方法即可。

## 具体顺序

1. **恢复原成果。** 加载本技能与V4.2，执行桥A重新发现/探针；核对V1-CHECKPOINT、CURRENT与哈希。封存时没有后台待跑，不直接重启历史批量测试。
2. **复用合同。** 优先用现有库存新题做最低成本接入验证。原任务根有fixtures\holdout、holdout-prompts.json、holdout-oracle.json、holdout.py。运行者只得业务输入/请求，不得oracle、未来增量或其他运行目录。合同及输入相同才继承A=163.190秒，不再运行已确认基线。
3. **选成熟配置。** 未知复合任务先评估现成DSH delivery（Flash/high），而非盲信auto/low。最多三条可行路线；原Pi与已做通用候选均保留历史，不为凑数搜框架。
4. **只查会改变路线的前置。** 确认原二进制、Office插件、配置、原凭据机制、工作区和权限可用。现成入口满足就直接用，不抄Office、浏览器或恢复实现。
5. **冻结最薄接入。** 用户面对同一个默认入口；明确记录实际后台执行器。若换后台，不得把DSH成绩说成Pi自身能力。冻结输入、全部成品、schema、质量/权限/成本及计时端点。
6. **一次相关Reality。** 独立授权目录执行首次任务→读回→追加相同变化和故障→独立验收。原生skill加载、API/模型/工具往返、排队、返修和审核全计。失败按原机制定向恢复，不重跑全部历史业务。
7. **有净收益再扩大。** 先得到接入验证，再按常用任务补代码、资料、网页、办公、媒体、恢复缺口，用成熟专业包与已有验收器。区分发现、可调用、执行、验收、实测较快。无效则保留原默认，不无限修自制方案。
8. **按证据发布。** 必需质量、完整性、可靠性、约定成本与授权过关后，将获胜路线接入原入口，备份原文件并验证默认调用与测试配置一致；保留回退。不能据一题更快就宣布完整成熟。

## 既有调用合同

以下是冻结后才执行的已读回语法，加载技能不自动启动：

```powershell
python "C:\AI\DSH-Acceleration-20261024\launch.py" --mode delivery --cwd "C:\Users\A\Documents\DSH-Workspace\<新任务目录>" --permission workspace-write "<完整自然语言任务与验收合同>"
```

delivery是固定候选配置，不让用户自行判断业务工具。原入口会加载/dsh-mature-capabilities；不修改C:\AI源文件。浏览器任务复用原正式browser/MCP，不新建浏览器。

本地文件恢复优先原run_resumable.py.execute：官方headless/patch、Tenacity有界重试、原session-id和同cwd。DSH首次从JSON type=session的sessionId获取身份，随后同cwd续用；不要照搬Pi指定新UUID创建会话的行为。恢复器仅用于无外部写入的本地任务；权限错误和他人会话句柄争抢不重试、不改安全边界。

## 已知教训

- Pi官方promptSnippet/promptGuidelines决定工具列表及规则；只注册description或附加文档未必改变原PowerShell偏好，先用官方接口，不猜扩展行为。
- 不同扩展注册同名工具会被SDK拒绝，mock成功不代表真实启动。
- 单次显式任务关闭stdin；Python用现成原生runner/结构化argv，避免多层PowerShell引号。
- DSH日志是session/tool_call/tool_result/status/final；Pi是tool_execution_start/end/message_end，验收解析不得盲套。
- 原故障分类器错误排除带Get-Content的混合命令；必须关联真实执行结果的Traceback、错误标志和提交数据，不能只在源码找故障字样。
- 成品正确但智能体未结束，不算在时限内完成；迟来复核不得套旧时间。超时可能缺usage，账单未知。
- 新题快约9%但SDK估算更贵；文档有变慢样本，不能只展示有利行。
- 已有独立验收覆盖当前数据时只补合同差异，不反复生成校验、扫描全盘或探测已固定依赖。

## 新页面启动语

使用《成熟执行体整体能力增强 V1》，按《AI 化组织》V4.2从检查点继续。优先复用现成DSH成熟交付入口，完成同一默认入口的新题、组合、变化与故障恢复对照；继承已验收成果，不从零探索，不扩写自制框架，以完整有效时间和真实质量/成本裁决。
