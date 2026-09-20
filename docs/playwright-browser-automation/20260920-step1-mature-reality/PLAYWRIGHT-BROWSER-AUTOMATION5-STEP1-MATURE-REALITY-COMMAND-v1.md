【playwright浏览器自动化5｜STEP1现实环境全面检查｜1】

# Playwright 浏览器自动化5 — STEP 1 现实环境全面检查命令 v1

~~~
SKILL_ID=first-principles-physical-limit-convergence
METHOD_VERSION=3.1.4
CURRENT_STEP=1
STEP_NAME=MATURE_REALITY
TASK_ID=PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-MATURE-REALITY-v1
OPTIMIZATION_OBJECTIVE=T_VALID
OBJECTIVE=T_STAR=min(T_VALID)
~~~

## 0. 方法权威

先读取并服从：

- 仓库：cuiqinggang/codex-private-skills
- 分支：codex/first-principles-physical-limit-convergence-v3.1.4
- 文件：skills/first-principles-physical-limit-convergence/SKILL.md
- VERSION：3.1.4

若方法版本、CURRENT_STEP 或命令内容冲突：

~~~
SKILL_GATE=BLOCKED
ACTION=STOP
~~~

不得自行补全、猜测或跨步。

## 1. 本任务唯一目的

本轮只完成 STEP 1 = MATURE_REALITY。

建立：

1. 当前机器真实浏览器自动化环境；
2. 当前已存在成熟资产与可运行路线；
3. 当前现役方案真实状态与真实能力；
4. 当前可测的端到端时间事实；
5. 当前硬边界、故障、缺口与未知项；
6. 已知成熟方案/实现的现实证据入口；
7. 为 STEP 2 Virtual-99 提供无偏的现实输入。

本轮不得：

- 设计最终架构；
- 决定最终赢家；
- 做 Virtual-99 组合收敛；
- 修改生产浏览器架构；
- 为了提速现场打补丁；
- 把现实测试失败后现场改算法、路由、prompt、模型；
- 宣称已经达到物理极限；
- 宣称任何单一路线必须成为最终主干。

## 2. 唯一优化标准

全项目唯一优化指标：

~~~
T_VALID
= 从任务正式开始
到第一个完整、正确、可用、满足 VALID 的现实结果出现
的端到端总时间

T_STAR = min(T_VALID)
~~~

质量、正确性、稳定性、安全性、权限、恢复能力等只定义 VALID 和现实边界，不成为第二优化目标。

任何已知满足相同 VALID 与相同计时边界的成熟路线 i，都必须满足：

~~~
T_STAR <= T_i
~~~

若后续最终结果仍慢于一个已知 VALID 成熟路线，则不能声称达到极限。

## 3. 当前 Playwright Native 资产的身份

当前已知现役成熟资产：

~~~
C:\AI\Playwright-Native-AI-Browser
~~~

正式身份固定为：

~~~
INCUMBENT_MATURE_BASELINE
= 现役成熟基线
= 强候选之一
!= 强制主干
!= 不可替换架构
~~~

允许它最终获胜，也允许后续 STEP 2/STEP 3 证明其他成熟路线或成熟组合更快。

禁止因为历史投入提前指定赢家。

禁止从零重造没有成熟来源的新浏览器方案。

## 4. 安全与系统边界

固定限制：

- 不修改 FlClash；
- 不修改代理；
- 不修改 Windows 网络设置；
- 不破坏现有 Profile；
- 不删除现有成熟资产；
- 不覆盖历史证据；
- 所有必要写入优先新建证据文件；
- 如必须修改已有辅助文件，先备份、后回读；
- 不持久化密钥；
- 不回显密钥；
- 不把外部账号、登录态、Cookie 做破坏性操作。

本轮允许正常只读检查和无副作用现实测试。

## 5. 现实环境全面检查

### 5.1 系统与执行器

记录但不为记录而升级：

- Windows 版本；
- CPU；
- RAM；
- GPU；
- 当前 Codex CLI 版本；
- Node.js；
- npm/pnpm/yarn（存在才记录）；
- Python；
- Git；
- PowerShell；
- 当前工作目录；
- 与浏览器自动化直接相关的运行时。

只记录与本项目有关的信息，禁止全盘低价值盘点。

### 5.2 浏览器与自动化运行时

检查本机实际存在的成熟执行环境，例如：

- Playwright；
- Chromium；
- Chrome；
- Edge；
- 当前 Playwright 下载的原生/可调试浏览器；
- CDP 可用入口；
- persistent profile/session 能力；
- 现有 browser-use / Stagehand / 其他浏览器自动化资产（仅在已安装或已有项目证据时记录）。

不得因为某个工具听起来更快就在 STEP 1 安装整套新架构。

如果存在可以低成本、只读确认版本/入口的成熟工具，可以记录；
需要明显部署成本的新路线留给 STEP 2 决策，不在本轮安装。

### 5.3 现役工程

全面但非破坏性检查：

~~~
C:\AI\Playwright-Native-AI-Browser
~~~

至少确认：

- 路径是否存在；
- Git/工程身份；
- 当前分支/提交；
- 工作区是否干净；
- 正式入口；
- 技能入口；
- Profile；
- 浏览器二进制；
- 启动方式；
- 重连方式；
- 登录态保存方式；
- trace/log/benchmark/acceptance 历史证据；
- 原 FULLY_SEALED 或同等级封袋证据是否仍可追溯；
- 冷启动与重连历史数据；
- 已有上传、下载、多标签页、复杂页面、恢复等能力证据。

现有 Profile：

~~~
ai-resource-orchestrator
~~~

只确认，不重建、不迁移。

## 6. 现实运行测试

目标：确认当前现实能力到底是什么，不是优化。

优先使用：

1. 已有验收脚本；
2. 已有本地 fixture；
3. 已有无副作用测试页面；
4. 已验证的真实站点只读任务。

不要为了测试重新发明一套 benchmark。

至少覆盖下列能力族中当前已有成熟证据的项目：

- 启动；
- 连接/重连；
- 页面导航；
- 页面状态读取；
- locator/元素识别；
- 点击；
- 文本输入；
- 等待/状态同步；
- 标签页；
- 上传；
- 下载；
- 登录态/Profile；
- 长答案/长页面；
- 表格/JSON/代码内容读取；
- 中断恢复；
- 网络恢复；
- PDF/MD 相关已有能力；
- 其他现役技能明确宣称的正常功能。

规则：

- 有现成可靠历史证据且环境未漂移的，不强制重复高成本全量测试；
- 用最小漂移门确认后可标记 HISTORICAL_EVIDENCE_REUSED=YES；
- 对当前状态不确定或关键入口已变化的，做最小现实复测；
- 任何失败只记录 REALITY_DELTA；
- 禁止本轮现场修改正式架构。

## 7. T_VALID 现实基线

不做优化，只测现实事实。

至少建立：

~~~
T_ENTRY
T_BROWSER_READY
T_STATE_READ
T_DECISION
T_ACTION
T_WAIT
T_VERIFY
T_RECOVERY_IF_REQUIRED
T_VALID_TOTAL
~~~

要求：

- 使用单调时钟/高精度计时；
- 记录计时起点与终点；
- 不偷偷排除必要等待；
- 不把预热时间从主指标里删除，除非任务合同明确区分 warm/cold；
- cold / warm / reconnect 若都存在，分别记录；
- 不凭感觉估算；
- 没证据就写 UNKNOWN。

如果已有历史数据可复用，必须同时记录来源。

## 8. 协议与往返现实检查

只读确认当前真实路径中：

- Playwright API 调用数量；
- CDP/浏览器协议调用；
- DOM/accessibility snapshot 次数；
- 同一页面状态是否重复读取；
- 是否存在固定 sleep；
- 是否存在等待已经满足却仍继续等待；
- 是否存在已知参数仍调用模型生成；
- 是否存在已成熟重复动作仍重新推理；
- 是否存在重复 selector/locator 探测；
- 是否存在模型调用与浏览器动作可以避免串行的地方。

本轮只记录：

~~~
OBSERVED_TIME_SINK
OBSERVED_ROUND_TRIP
OBSERVED_REDUNDANCY
~~~

不得现场优化。

## 9. 成熟现实方案池：只建立事实，不做赢家决策

将以下来源视为 MATURE_SOLUTION_SOURCE / EVIDENCE，而不是强制依赖：

- 当前 Playwright-Native-AI-Browser；
- Playwright 官方成熟机制；
- Jev / typesafe/jev-1.13；
- browser-use / jev-ultrafast；
- Stagehand；
- workflow-use；
- Browser Harness / BrowserCode / persistent browser 类成熟实现；
- BrowserGym；
- WebArena-Verified；
- 已经在本仓库历史分支中完成的 Jev Virtual-99 / shadow 成果；
- 其他已有公开现实证据且能影响 T_VALID 的成熟路线。

对每一项只记录：

~~~
SOURCE
WHAT_IS_PROVEN
WHAT_IS_NOT_PROVEN
TIME_EVIDENCE
VALID_SCOPE
REUSABLE_CAPABILITY
KNOWN_LIMITATION
LOCAL_AVAILABILITY
~~~

不得在 STEP 1 做最终 COMPOSE 或 MATCH 决策。

## 10. Jev 公开路线作为现实事实

Jev / jev-ultrafast 只作为成熟现实证据之一。

需要记录：

- 公开任务是什么；
- 公开计时边界是什么；
- 公开时间数字；
- 请求次数；
- protocol-call 变化；
- 功能覆盖限制；
- 是否与我们的 VALID / T_VALID 主口径完全相同。

特别要求：

~~~
JEV_PUBLIC_NUMBER != 第二优化目标
JEV_PUBLIC_NUMBER = KNOWN_MATURE_REALITY_REFERENCE
~~~

如果后续最终 T_STAR 的同口径结果慢于已知 Jev 有效路线，则逻辑上不能宣称达到全局极限。

本轮不要求为了 Jev 重新设计架构。

## 11. 本地已有 Jev 历史成果

只读检查正式 v3.1.4 及仓库历史中已经存在的：

- JEV-VIRTUAL-99-v2；
- Jev shadow；
- Verify-02；
- Reality Delta；
- 已有 OpenRouter/Jev 本机调用证据；
- 已有成功/失败样本；
- 已有延迟数据。

禁止重复完成已经完成的工作。

如果已有本机真实 Jev 1.13 调用 PASS 证据，直接复用并标明出处。

## 12. 当前现实能力矩阵

生成至少下列字段：

~~~
CAPABILITY
CURRENT_ROUTE
STATUS
REAL_EVIDENCE
T_VALID_OR_COMPONENT_TIME
DEPENDENCY
LIMITATION
REALITY_DELTA
~~~

状态只允许：

~~~
PASS
PARTIAL
BLOCKED
UNKNOWN
~~~

不要使用主观快慢词代替证据。

## 13. STEP 1 输出文件

在本任务分支/工作区建立：

~~~
docs/playwright-browser-automation/20260920-step1-mature-reality/
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-MATURE-REALITY-RESULT-v1.md
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-MATURE-REALITY-RESULT-v1.json
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-CAPABILITY-MATRIX-v1.json
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-TVALID-BASELINE-v1.json
  PLAYWRIGHT-BROWSER-AUTOMATION5-STEP1-MATURE-SOLUTION-REALITY-POOL-v1.md
~~~

必须包含：

~~~
METHOD_AUTHORITY
CURRENT_STEP
ENVIRONMENT_STATUS
INCUMBENT_BASELINE_STATUS
CURRENT_CAPABILITIES
CURRENT_T_VALID_BASELINE
CURRENT_TIME_SINKS
CURRENT_PROTOCOL_ROUND_TRIPS
MATURE_REALITY_POOL
JEV_REALITY_REFERENCE
REALITY_DELTAS
UNKNOWN_FACTS
STEP1_BLOCKERS
STEP1_CLOSEOUT
NEXT_ALLOWED_STEP
~~~

所有新生成文件：

- 写后回读；
- 计算 SHA256；
- 记录最终路径。

## 14. STEP 1 PASS 条件

只有以下同时成立，才允许：

~~~
METHOD_AUTHORITY=3.1.4
CURRENT_STEP=1
ENVIRONMENT_REALITY_CAPTURED=YES
INCUMBENT_BASELINE_REALITY_CAPTURED=YES
NORMAL_FUNCTION_STATUS_CAPTURED=YES
T_VALID_BASELINE_CAPTURED_OR_EXPLICITLY_UNKNOWN=YES
MATURE_REALITY_POOL_CAPTURED=YES
JEV_REALITY_REFERENCE_CAPTURED=YES
NO_ARCHITECTURE_PRESELECTION=YES
PRODUCTION_ARCHITECTURE_MUTATION=0
PROXY_MUTATION=0
FLCLASH_MUTATION=0
PROFILE_DESTRUCTION=0
STEP1_CLOSEOUT=PASS
NEXT_ALLOWED_STEP=2_VIRTUAL_99
ACTION=STOP
~~~

如果某个关键现实事实无法获得：

~~~
STEP1_CLOSEOUT=BLOCKED
BLOCKER=<exact blocker>
ACTION=STOP
~~~

不得跨步。

## 15. 最终回传格式

最终只回传：

~~~
METHOD_AUTHORITY=
CURRENT_STEP=
ENVIRONMENT_REALITY_CAPTURED=
INCUMBENT_BASELINE_STATUS=
NORMAL_FUNCTION_STATUS=
CURRENT_T_VALID_BASELINE=
PRIMARY_TIME_SINKS=
MATURE_REALITY_POOL=
JEV_REALITY_REFERENCE=
REALITY_DELTAS=
UNKNOWN_FACTS=
STEP1_BLOCKERS=
STEP1_CLOSEOUT=
NEXT_ALLOWED_STEP=
ACTION=
EVIDENCE_FILES=
SHA256=
~~~

最后一行必须原样返回定位标签：

【playwright浏览器自动化5｜STEP1现实环境全面检查｜1】
