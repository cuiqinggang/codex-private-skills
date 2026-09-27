# R2 第04号：传输依赖补齐与生产绑定核查 v1.0.3

## 范围

1.0.3仅为本依赖交接合同修订号。母引擎5.3.3、验收修补1.0.1、部署包1.0.2与六个运行时均不变。除本文件明确修正的依赖定位方式外，继续执行FULL-BASELINE-DEPLOY-R2-03-v1.0.2.md@182f8a76d810a43b8f985b17dc8bf6a908acf701。

第03号用户提供的Codex回报：安装PASS、加载PASS，暂存与正式路径各50/50，备份60文件一致，安装单调耗时1122.8072ms；业务和闭环NOT_RUN。GPT未独立读取Windows目录。保留成功项，不重装、不改备份、不重跑01轮业务。

REVIEW_TASK_BINDING_REQUIRED_NO_STATE_CHANGE发生于子任务未受理、四ID未建立时，只说明最终验收缺少绑定，不是人工失败或监督器故障证明。创建前缺少ID不能成为禁止创建新会话的循环前提。

本轮虚拟成熟仅覆盖有界依赖核查和条件续测合同；未声称外部C3运行就绪。原C3的R3要求不降低：证据不足就返回依赖待核，不自行换成一般页面通道后冒称原C3认证。

## 已核实的冻结来源

共同私库cuiqinggang/codex-private-skills，Orchestrator提交c00dbc63abda76acc7b787caf9c2f8fd2cd206a1：
- skills/gpt-codex-convergence-orchestrator/SKILL.md，blob e20245925f44a590ffe6a90a41059c7952877023。
- skills/gpt-codex-convergence-orchestrator/manifest.json，blob fed5a47171cd4cb81df2e4c98d3f375f371d200a。
- docs/gpt-codex/20260919-simple-final/GPT-CODEX-SIMPLE-FINAL-REAL-EXECUTION-v1.md，blob 9dbbb38fa8a90816a75c705f55946376bf2df3c9。

第三份历史记录把实现定位到C:\AI\GPT-Codex-Convergence-Orchestrator\simple_flow.py；页面通道使用现有playwright_native_ai_browser MCP与chatgpt-business-entry.js的query、send、wait_extract。参数必须读当前正式接口，不能猜测。B/C是历史受控测试，不是本轮认证。

已读取R3 runner blob 05a400b542193b7e51cc3b959ad2ac03bab15ae5：它启动本地fixture及headless浏览器，预热后执行编译簇，结果字段含compiled_replay=true、jev_calls=0。它不能单独证明ChatGPT生产入口使用R3；也不证明不存在其他R3生产资产。不得把此runner当网页传输器运行，或虚构必须存在的R3开关。

## 冻结操作

工作区C:\Users\A\Documents\Codex\2026-09-27\este-transport-v533-r2-04。只读核对正式引擎入口与第03号六模块哈希，匹配就继续；不运行部署器或重复安装回归。变化则报告真实差异。

通过既有授权Git通道将上述三个精确对象放工作区references并核验Git blob原始字节，显式读取并记录TRANSPORT_POLICY_LOADED。相同文件幂等使用，不同内容不覆盖。允许这种任务级来源加载补齐规则入口，不要求两个全局技能目录必须都安装Orchestrator；也不安装具有旧母方法的整套技能。规则载入不等于程序或传输已运行。

只读核查C:\AI\GPT-Codex-Convergence-Orchestrator\simple_flow.py及同目录已有版本说明；存在则仅跟踪页面传输直接引用，记录路径/哈希/调用接口。不存在如实记录，不全盘搜索。不要执行旧产品状态机、toy业务执行器或未经授权启动服务。C3允许按上述历史来源复用正式浏览器query/send/wait_extract原语，由Codex执行冻结传输步骤；这不是新写传输脚本，也不声称完整Orchestrator软件已安装。

读取浏览器薄入口C:\Users\A\.codex\skills\playwright-native-ai-browser，解析其实际目标；读取权威目录C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser的SKILL.md、scripts\chatgpt-business-entry.js及其明确引用。一次核查正式工具接口、入口哈希、专用profile/context、登录、新对话/读取/发送/提取/回传能力、R3生产绑定和现有执行权限。未调用的能力不得记PASS，登录正常不能证明全链路。

R3补充历史只读位置：C:\Users\A\playwright-browser-automation5-final-reality-competition-work\TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW\PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json，以及其JEV-NATIVE-VIRTUAL-99\REAL-VERIFY-R3\REAL-VERIFY-R3-RESULT.json。只核对存在的资产，不重新跑基准。R3生产绑定须有生产入口对实际实现的引用、可核对R3身份的原始资产、当前使用该实现的可观察调用证据。仅名字、历史证书、报告数字不够；缺证据写UNKNOWN并列确切缺口，不写R3产品FAIL，不改造浏览器强行通过。

依赖核查一次列齐矩阵，不因第一项缺失就省略其他安全可读项；权限拒绝立即停止对应操作，不绕过。规则来源、生产接口和原C3所需绑定均满足后，不等用户再说继续，直接续测原未受理子任务ESTE-v5.3.3-SUPER-SMOKE-R2-ISO02。否则返回完整依赖矩阵，不自行降低认证范围。

## 续测顺序与边界

沿现有专用浏览器真正新建“极限短时间 v5.3.3冒烟 R2｜独立测试02”，不得复用控制会话6ab94118-27c8-83ea-93c3-599270775902或只改旧标题。新ID依正式创建/首条普通任务提交后回读；生成前写NOT_CREATED。RUN_ID真实生成留证，子时间线由新页GPT真实受理时建立。之后才对最终回报使用已绑定四ID的正式验收入口；不在未建页时用最终门阻止建页。

普通任务和业务目录沿第03号合同：este-super-smoke-v533-r2-02\result.txt，精确V5.3.3_SMOKE_OK，UTF-8无BOM无末尾换行15字节。普通任务→GPT虚→FSM完整派发→Codex→同一新页→GPT裁决。使用已安装六模块，测试器不补证据/状态、不代执行。结果先回同一新页再向控制页报告。

人工只认原始同任务动作；USER角色、自动粘贴、标题、双窗口显示不作人工证据，旧争议数字不继承。匹配ACK已到不重发，有真实进展继续观察，等待超时先核实；不得把60000ms工程目标当超时或通过门。

母Timeline=ESTE-v533-R2-20260927T162319Z，起点2026-09-27T16:23:19.729Z保持，准备等待不扣除。04为第04号派发，最多01–06。安装1122.8072ms不是完整T_VALID。缺早期收件时钟写UNKNOWN，不冒充时间原点。

副作用仅限本工作区、合法新测试页及原授权业务目录；既有浏览器标准日志如实记录。禁止修改六模块、浏览器脚本、代理、FlClash、系统/权限策略、Git全局配置，不安装新浏览器或连接器。

回传CODEX_RETURN_ESTE_v533_R2_TRANSPORT04_04；RESULT=PASS|FAIL|BLOCKED；RETURN_TO_GPT=YES；NO_FINAL_VALID_DONE=YES。分列POLICY_LOADED、TRANSPORT_RUNTIME_BOUND、R3_PRODUCTION_BINDING、DEPENDENCY_MATRIX、BUSINESS、CLOSED_LOOP、ACCEPTANCE_REVIEW、原始证据、真实阶段时间、新页/四ID/匹配ACK/人工已核验次数或UNKNOWN。Codex不签FINAL_VALID、DONE或REAL_T*；规则读取不冒充执行，未运行写NOT_RUN。
