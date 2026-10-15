# Orca 接入源码与计时审查 V1
TASK_ID=ORCA_CODEX_VALUE_VALIDATION_20261014
METHOD=SANRENXING_V2_C002
BRIDGE=V6.0_C_FIRST
REVIEW_DATE=2026-10-15
STATUS=STATIC_REVIEW_WITH_CONCRETE_FINDINGS_NOT_RUNTIME_ACCEPTANCE
FORMAL_REALITY_ACCEPTED=0
FINAL_VALID=NO

## 拒绝提示纠正
用户已在本页提供原文：“此工具调用被 OpenAI 的安全检查屏蔽。请仔细检查你发送的内容。”
原文没有具体原因。无需再次索取截图，也不将其作为独立资料读取、源码审查、离线分析的前置条件。
保留对原被拒运行时预检的停止；没有重发该请求，没有据此宣称整个Orca或C通道被禁止。
本轮只有GitHub固定提交源码读取与C通道既有文件读取、项目文档写入；没有运行Orca CLI/QA/模型。

## 证据来源
官方仓库 stablyai/orca；固定提交 2bb20586ebc39d605e16d95f57420e20a16e7485（本任务v1.4.224）。
使用GitHub.fetch_file读取以下原始正文和blob身份。目录树接口Transport closed不影响这些成功的逐文件读取。未用移动main推断固定版本。
- src/main/codex/codex-hook-service-implementation.ts：866779468d452ee39aef2143561da59ab119c819
- src/main/agent-hooks/managed-agent-hook-controls.ts：70a2b9bb24d5cd5b585ae3569e5cc72a404b52d2
- src/main/codex/codex-hook-local-maintenance.ts：6797f838f513dfad1fb66c13ec9b074bb2bf7c17
- src/main/codex/codex-home-paths.ts：e838d11fe6b2ec55cd7f831aea040b650f6d22f1
- src/main/codex/codex-config-mirror.ts：74f8b2f0b531e068ba6cc80c0c16291f6ed2a36c
- src/main/codex/hook-trust-promotion.ts：9f6b5a867e96323971f9a2599aa08a69b64ec9ea
- src/main/codex-accounts/runtime-home-service.ts：4f08fb0a64c5f645f0362c086264288d335d375f
- src/main/codex-accounts/runtime-home-service-auth-sync.ts：93c3c9b430dac2feba889651bbb0ca9ac4df4e90
- src/main/codex-accounts/runtime-home-service-launch.ts：cdc5a601f6cf4aad4da8a9e1ec5387653bdfa77f
- docs/site/content/docs/cli/orchestration.mdx：88355cb8c825d11999fe3cade3017e49b5242495
本机只读：tools/run_good.py、freeze/AB_PARAMETERS.json、tools/inspect_orca_package.py；旧官方网页抽取快照仅作定位，关键结论以上述固定提交正文为准。

## 1. Hooks关闭并不等于无写入
事实：
- managed-agent-hook-controls.resolveStartupManagedHookAction：关闭时startup为skip；显式applyAgentStatusHooksEnabled(false)却会调用removeManagedAgentHooks。启动预置和运行后切换不是同一副作用。
- CodexHookService.prepareRuntimeHomeForLaunch：关闭时走refreshRuntimeUserHooksForRuntimeHome或refreshRuntimeUserHooksForLaunchPrep。
- codex-hook-local-maintenance.refreshCodexRuntimeUserHooksExclusively：会写runtime hooks.json，调用配置镜像、信任项更新与旧表示清理。
- hook-trust-promotion：在provenance存在、runtime批准发生变化、匹配系统用户hook等条件满足时，会将用户批准回写系统config.toml。不是每次必写，更不是本次已发生。
- codex-config-mirror：镜像前调用promoteCodexRuntimeSettingsToSystem，存在设置回写路径；具体触发条件尚未完整审查。
判决：不能仅关闭hooks就给出“不改全局配置”证明。也不能靠运行后关闭开关修正，因为关闭本身可能执行清理。
尚缺：实际headless入口到launch准备的调用路径、解析出的home归属、各条件是否在本任务成立。共享源码中存在函数不等于orcad本次必定执行它。

## 2. 登录复用已有成熟分支，但副作用尚未闭合
事实：
- runtime-home-service-launch.prepareForCodexLaunch：system-default real-home分支返回null，含义是PTY/env层不注入managed CODEX_HOME；分支先调用copyMirrorLoginIntoEmptySystemHome和reconcileLegacySharedHomeForRetainedPanes。
- 同文件其余分支可同步选择、资源和配置，并启动历史会话桥接。
- runtime-home-service构造器包含恢复、旧状态迁移和safeSyncForCurrentSelection。
- runtime-home-service-auth-sync存在auth.json读取、快照和写回实现；不能把“复用登录”笼统写成“程序绝不复制凭据”。
- codex-home-paths.getSystemCodexHomePath为homedir()/.codex。当前Orca准备环境重定向USERPROFILE/HOME，故其system home不应凭名字认作用户A真实home。
推断：当前“隔离Orca主目录”与“使用A原生登录”之间需要精确的子进程环境和路由证据。不能通过复制auth.json、放宽ACL或热改全局配置补洞。
边界：本次只读公开实现，未读取用户auth.json、令牌或密钥；未触发这些函数。
尚缺：home-routing、迁移辅助函数和实际PTY环境路径的完整静态调用链；不能宣布凭据复制一定发生或一定不发生。

## 3. 业务入口已缩小到官方Run/Task/Dispatch，但参数仍不完整
固定版本官方orchestration.mdx确认：
- run-create只建命名空间，不自动调度。
- task-create后用worker-start，传--agent codex；可选--model及依赖model的--effort；参数请求与生效值显示在launch.requested/effective。
- worker_done需要taskId、dispatchId和outcome；完成消息仍需外部业务验收。
- 官方工作单元是终端agent；与A的codex exec模式不同，比较对象应标记为“相同底层模型的两种入口”，不声称进程路径完全一致。
- reset影响runtime-global状态，本合同不采用。
尚缺：worker-start的实际参数schema、ultra允许值、priority透传、workspace-write和审批策略最终有效值。文档示例不是本机argv验证。
AB_PARAMETERS的A命令明确-s workspace-write，但审批策略只在描述中写on-request，没有显式固定在示例argv；需读取实际有效策略，而非认为文字等于生效。不能为了公平而放宽任一侧权限。
不生成猜测的可执行B命令，不把extra-agent-args从其他入口推定为worker-start必支持。

## 4. 计时源码审查：两项已定位缺陷
tools/run_good.py的finally顺序是：
end_perf_counter_ns/full_wall_ms → done.set与thread.join → size(ROOT)磁盘统计 →资源汇总 →写TIMING_AND_ACCEPTANCE.json及INFLIGHT.json。
所以旧full_wall_ms排除了这些收尾动作，也未对最终两个回执独立回读。这是代码证据，不能将旧数字改名当作完整时间。
监控循环是sample及日志写入完成后done.wait(1)，实际周期等于采集/写入成本加一秒；不是固定一秒周期。旧采样543份的真实间隔必须保留。
额外问题：thread.join(timeout=3)后未验证线程结束，收尾读取metrics时可能仍有写入；属于静态风险，未在本次实测复现。

## 5. 计时修正设计（待实现、待独立验证）
只最小改动任务仪表，不建立通用调度器，不改旧F001和旧回执。
- t0：输入/环境交付开始前同一进程perf_counter_ns；启动及目录准备排除项必须明示。
- 成果校验、diff/manifest落盘回读、采样器实际结束、必要磁盘统计、状态回执写入与回读均在有效交付终点前。
- 用外层已有任务仪表在验收者完成上述回读后记录t_valid；业务回执本身不自包含其最后一次持久化完成时间，以免循环自证。
- 将记录t_valid的测量记录落盘/回读耗时单列measurement_record_finalize_ms；需要“最终记录也回读完”的全程值时由CEO外层继续计时到该回读完成，缺失则UNKNOWN。不得把排除项悄悄填0。
- 资源采样按单调deadline推进，记录采集开始/结束、实际间隔、错过周期；慢采集不重叠补发。低于1秒目标但未达到时如实报告，不冒充严格达标。
- 采样器未在有界时间内结束就保留仪表失败，不能边写边封存。
这只是修正规格，本轮没有改动或运行Windows仪表，不能标为修复PASS。

## 6. A/B一致修复政策补充候选
双方都允许同等GPT审查和最小修复，以符合已验“Codex+GPT恢复”事实。
每侧均分列首次无人修复成功与修复后成功；修复后成功不得计入固定版本“连续无意外故障十轮”。
同一suite的失败、排队、GPT诊断/编写、桥接、执行、回读全部计时，UNKNOWN先对账，不盲重发。
暂沿用已有suite_timeout_seconds=3000为每侧完整业务预算；所有诊断/修复/证据回读也计入，不在超时后用额外免费窗口补成功。仪表封存失败仍保留实际总耗时。
每次修复在原授权范围内完成；越界或预算耗尽记录失败。实质版本变化后重新冻结并重置连续通过计数；旧失败不删除。
双方干净相同输入、新会话、同模型/强度/资源上限、5AB+5BA顺序不变；不将已修复源码作为下一轮输入。
以上为待纳入新具体冻结的政策候选，不覆盖旧合同证据，不自行宣布N002获准。

## 7. 本轮结论及下一具体缺口
完成了固定版本10份官方文件的源码审查和本机计时/参数文件审查，发现hooks关闭后刷新/有条件回写、登录兼容迁移、计时漏项与采样周期偏差。
正式业务仍0；连续十轮0/10；AB配对0/10；净收益UNKNOWN。
下一准备工作可独立继续：沿home-routing/PTY调用链补具体环境与权限证据，审查模型参数schema，再形成未执行的新冻结候选；原运行时拒绝单独保留，不再要求同一截图。

## 8. 追加home-routing分支核对（同轮）
源码src/main/codex-accounts/runtime-home-service-home-routing.ts，固定提交同上，blob ca68b322667969fa2d78b47ffa5c80f8dfed50dd。
- real-home选择条件是host选择为null且没有custom CODEX_HOME override；不是任意传入真实CODEX_HOME就必走此分支。
- reconcileLegacySharedHomeForRetainedPanes仅在real-home且有已记录旧共享pane时进入同步。
- copyMirrorLoginIntoEmptySystemHome只在Windows、provenance committed且owner system-default、历史auth基线为null、runtimeAuth非null时尝试写入原本为空的系统auth。函数也会读取runtimeAuth以判条件。
- 因此“系统默认路径无条件复制凭据”不成立；“一定不复制”也需要证明分支条件不成立。未检查用户凭据内容，不通过此函数运行来试探。
审查范围现为11份关键官方正文。剩余最小静态问题是custom-home判断、实际PTY环境/调用者以及worker参数schema，尚不能发布正式可执行冻结。
