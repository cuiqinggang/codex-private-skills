# ENGINE29｜GPT/Codex双执行者与最多三级拓扑｜8会话并行虚拟审查证据

日期：2026-10-10
关联候选：`skills/artificial-single-page-extreme-time-engine/ENGINE_V29_DRAFT.md`
源方法：公共ENGINE28／A路线A29／B路线B33（均未被本次改动）
执行环境：Windows DESKTOP-4A1EGTM；Codex CLI 0.160.0；模型 gpt-6.1-sol；ChatGPT登录；隔离只读提示词
TASK_ID=UNIFIED_ENGINE29_VIRTUAL_CASES_20261010
METHOD_STATUS=DRAFT_RECORDED
DISPATCH=8_SEPARATE_CODEX_CLI_SESSIONS
VIRTUAL_DESIGN_AUDIT=8_OF_8_RETURNED
VIRTUAL_MATURE=NO
GPT_BROWSER_REALITY=NOT_TESTED
CODEX_IMPLEMENTATION_REALITY=NOT_TESTED
FINAL_VALID=NO
T_VALID=UNKNOWN
ROOT_ENGINE29_ACTIVE=NO

## 1. 本轮实际执行范围与缺陷

在获准的Windows执行桥上实际创建8个彼此独立的Codex CLI非交互会话，各有E29-01至E29-08编号、独立会话ID、对应自包含案例。采用只读模式；案例明确要求不打开已有浏览器、不读取先前遭策略拒绝的本地snapshot、不修改文件/仓库、不发送ChatGPT消息、不触碰原代理。所有真实结果仅是模型对给定任务合同的**虚拟设计审查**，不是8个浏览器执行页通过、不是GPT并行执行的现实证明。

首轮CLI直接以参数传入提示词，远程会话因等待标准输入EOF未启动推理，已清理。之后以标准输入管道交付自包含任务；日志显示8个提示均成功进入模型会话。E29-08第一次模型明确返回 LOCATOR_GATE=BLOCKED，原因缺少其要求的中文定位格式；已用中文页面/任务/序号定位重新派发，二次完成虚拟审查。上述都是实际出现的准备/返工成本。

过程中全部或多数CLI会话报WebSocket多次Reconnecting，最终回退HTTPS（request timed out）；开局存在两个本机skills YAML-frontmatter无效日志和skills context budget被超限警告。本轮未修改用户CLI技能、代理或模型配置。

## 2. 编号结果

| CASE_ID | 虚拟审查结果与反例 | Codex本轮成功会话实际进程运行时长 |
|---|---|---:|
| E29-01 | 有效审查；普通小任务强制页面派发可能净增交接成本；真实同合同对照缺失 | 135.56s |
| E29-02 | 有效审查；旧CEO在Freeze后仍有在途写入，可能和新CEO双写 | 149.75s |
| E29-03 | 有效审查；多标签同Profile不证明上下文隔离，焦点漂移及错误清理须拒绝 | 153.02s |
| E29-04 | 有效审查；总CEO+3模块CEO+每模块2执行者最多三级可描述，但模块结果可能存在共享接口版本冲突 | 142.75s |
| E29-05 | 有效审查；相同代码缺陷的首轮补丁速度不等于最终T_VALID，必须独立测试加返工计时 | 144.60s |
| E29-06 | 有效审查；Hybrid不是必胜，交接开销、唯一写者歧义与错误根迁移可能使其更慢 | 148.55s |
| E29-07 | 有效审查；唯一全局写者不足以抵御检查后焦点漂移、错误目标会话及桥中断 | 146.59s |
| E29-08 | 第二轮有效审查；G/C/H×并行1/2/4/8共12个真实实验条件，提出匹配任务与盲验；首次受中文定位缺失门禁拦截 | 154.47s |

上述进程时长来自实际Codex CLI结束时输出的runtime，包含模型连接重试等开销；**它们不是同一实质任务在GPT、Codex、Hybrid三个模式的对应T_VALID**。本轮8个CLI启动时间错开，不具备严格同步释放点；因此无法据此宣称8路对比4路或1路的加速比。E29-08首次门禁拒绝耗时125.76s，属于额外返工时间，不能从总成本中消失。8项中0项做过获准GPT专用浏览器真实自动发信/恢复，0项取得统一质量的现实测时基线。

## 3. 下一步最小验收合同

- 用相同可合法执行的任务输入和最终质量标准测试 G=GPT-only、C=Codex-only、H=Hybrid，记录客观接收、最终VALID及失败返工全过程。
- 为同条件比较设计并行度1/2/4/8，预注册运行顺序、样本数量、资源与模型预算；避免重用已看答案或因模型上下文/浏览器会话污染。
- 仅在权限允许的独立测试会话中验证合法Freeze、唯一目标标签绑定、新CEO接管、旧写者失效、错误标签不受影响；受平台安全拒绝的ChatGPT自动发送门禁继续保留，不得以换工具规避。
- Codex监控/派发只在授权有意义时启用。GPT具备独立实际执行资格，但真实GPT多页浏览器并行测试尚未发生，不得将计划写成真实通过。
- 实测完整版 `T_BASE_REAL` 与可复核整体虚拟最佳时长、长期净收益形成后才能称 VIRTUAL_MATURE=YES；Freeze后只按既有许可做一次最终Reality，验收后再发布公共ENGINE29。

## 4. 状态冻结

本文件仅冻结**实际已经收到8条Codex虚拟审查**和其中识别的差分/故障现象；公共`ENGINE.md`保持第28版，`routes/A/ROUTE.md`的A29与`routes/B/ROUTE.md`的B33仍各自生效。B33受保护发送硬停不变；未获准的浏览器动作与GitHub平台预派发安全拒绝均不可通过替换工具绕过。

RESULT=VIRTUAL_DESIGN_AUDIT_RETURNED_8_8
RELEASE=NOT_AUTHORIZED_YET
NEXT=Matched REAL G/C/H benchmark and isolation tests when legal execution entrance is available.
