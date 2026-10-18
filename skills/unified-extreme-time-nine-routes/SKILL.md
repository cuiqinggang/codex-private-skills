# Unified Extreme-Time 9-Route Skill v1.0
日期：2026-10-18 | 状态：LOCAL_DRAFT（未经九方案端到端验收，不称生产冻结）
继承：《三人行》第3版、Windows 执行桥 V10.0（C→A→B，C故障须有日志）、UltraFusion 6.1B、complex-problem-virtual-maturity、物理下界系列。旧技能保留，不创建新的调度器或登录共享。

## 目标与分档
目标：同输入、同质量下最短有效完成时间 T_VALID=min(质量合格、可复现、端到端执行时间)；成本是硬约束/次级目标，不把廉价但不达标算胜利。
普通任务 GPT 直接完成；高价值、长流程或用户明确要求极限方案才启动九路线模式。
先做一次最小的 Windows 真实任务：冻结输入、合格标准、起止界限，得到 T0；同时分解依赖链、不可并行时长和硬件上限，给出有依据的 T_phys_lower，未知则标未知。独立的微基准不能冒充该任务 T0。

## 9路线（一页规则）
GPT、DeepSeek、Gemini 或 Qwen 三名独立分析者，各自提交 3 个端到端成熟方案；每个方案须：成熟证据/版本、完整实施路径、质量门、预期关键路径时间、资源成本、依赖与最大失败反例。不能只提交三个局部优化。
三个角色分别侧重：最快稳定直达；成熟并行/缓存复用；低资源高鲁棒恢复。若某模型不可调用，单模型多视角代替并标注“视角模拟，非独立模型验证”。
九方案去重，选不多于3条可兼容的强者，做整体依赖图融合；消除重复、冲突和增加协调成本的分支。攻击最慢关键路径节点，虚拟迭代直到无可靠净收益，执行 STOP_GATE。计算 T_virtual=关键路径各步骤预测时长+必要协调/验收开销（给区间与依据）；必须满足 T_virtual>=T_phys_lower，不能假定方案融合必然加速。
Freeze之后只对最优完整方案执行一次端到端Reality；认证只用真实质量合格的T_VALID，不以虚拟时间、估计或未经验证的模型声称替代。

## 执行线路
控制器 GPT；默认 GPT 自执行；Windows优先 C，只有C故障证据才A、然后B；保持网络代理不变、不得独占浏览器。Gemini CLI/Antigravity和官方DeepSeek Harness是候选执行者，不是现有C/A/B桥的自动替代；需单独验证账号、权益、权限与同任务完成率。Dot适合持续云端项目，但是否可由当前GPT程序式派发必须另行验证，不得假设已接通。Codex仅在其他成熟路线无法解决或净收益更高时使用。
严禁把网页登录的免费额度等同免费API；不绕过收费、验证、反自动化或账号使用限制。执行本地文件/命令先限定工作目录与权限；需批准的危险操作不自动执行。

## 固定输出（缺一项即不完整）
任务定义+质量门；现实 T0（含证据）；T_phys_lower（含约束与不确定性）；九方案摘要；融合最优路径；T_virtual（区间/依据）；实际 T_VALID 或 NOT_TESTED；时间收益与额度消耗；Freeze / Reality 状态；未完成阻塞。

## 2026-10-18 官方能力核验（非执行认证）
- DeepSeek 官方 2026-10-17 changelog：V4.1-Flash-1017 已覆盖 Web/App，API 使用 `deepseek-flash`，但 Web 订阅/免费对话不等于 API 或本地终端执行许可。来源：https://api-docs.deepseek.com/updates/
- Gemini Apps 官方 Task：符合资格的 Google AI Pro/Ultra 个人账户可使用任务、Skills、定时及云端远程浏览器或经授权 Chrome 自动浏览；确认、登录、浏览器控制、地域、账户权益和额度限制均需核验。来源：https://support.google.com/gemini/answer/17094507 与 https://support.google.com/gemini/answer/17094710
- ChatGPT Dot 官方：有独立云端电脑、浏览器、计划任务与插件；本地电脑连接为可选且需明确授权，Dot 可按权限创建 Work/Codex 任务；但当前聊天没有官方直接程序式派单给 Dot 的已验工具。来源：https://help.openai.com/en/articles/20001530-getting-started-with-your-dot
- 学术警示：多智能体辩论未必在同等预算下优于 self-consistency/ensemble；九方案必须先去重、限制辩论轮数、提供单模型三视角廉价对照。来源：https://proceedings.mlr.press/v235/smit24a.html

## 合约与验证门（2026-10-18 增量）
1. 采用任务级 `T0_valid`；硬件理论下界 `T_phys_lower` 是下界且可能不可精确算出，必须附不可并行步骤与吞吐公式。九条模型估算不构成实测。
2. 小样本测速只叫 `micro_baseline`，不能代表整项任务物理极限或真实性能。分别统计读入、算法、写出、验收和工具通信开销，避免用不同口径比较。
3. 将对比组固定为：单GPT直达、单模型三视角、三模型九方案；质量门相同，计算总耗时和额度，并记录真实置信区间或 UNKNOWN。
4. 资源路线按实测优先：GPT+C；Gemini Task/远程浏览器（账号内单独授权）；DeepSeek网页只做分析，除非受支持桥接经权限审查并真实验收；Dot持久任务（人工在Dot聊天派单）；Codex条件升级。新云端执行者不自动并入C/A/B故障切换。
5. 状态只有 `CONFIRMED_COMMITTED`、`CONFIRMED_NOT_EXECUTED`、`UNKNOWN`；未经提交/完成确认不得重放有副作用操作，涉及支付/发布/删除/登录均需批准。

## C 通道最小现实试验（2026-10-18 21:xx 北京时间）
- 在 DESKTOP-4A1EGTM 使用 C 通道 PING PASS 后，PowerShell 固定随机种子 20261018 生成 1000 行 CSV；五轮执行读入→按 amount/id 排序→导出→回读验收，全部 PASS。
- 轮次总计（含输出回读验收，单位毫秒）：437.55、128.12、89.50、97.98、103.18；最快 89.50ms；冷态首轮 437.55ms。输入生成在计时外；不含远程 MCP 命令派发与进程启动开销，且没有复核全部 ID 集合。
- 此成绩严格标记为 `micro_baseline`，是特定 PowerShell CSV 试验的可复查快值，并非九方案完整任务 T0、物理极限或理论下界。脚本：`C:\Users\A\Desktop\SRX_V3_ReadPack\nine_route_microbaseline.ps1`。
- 本次没有真正从三个独立模型获得九份输出，也没有 Gemini/Dot 登录操作认证，九方案端到端状态 `NOT_TESTED`。不能将本地 Skill 文件写入称为发布完成。
