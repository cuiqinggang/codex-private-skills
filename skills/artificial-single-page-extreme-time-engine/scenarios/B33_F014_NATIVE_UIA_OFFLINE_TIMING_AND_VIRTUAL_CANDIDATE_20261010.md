# B33 F014｜原生UIA离线同构与极限时间分层复核
DATE=2026-10-10
TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
PREVIOUS_FREEZE=B33-VM-F013
METHOD=B33/B29/B23
ROOT_METHOD=ENGINE28/BRAIN25_TIME_BASELINE_FIRST_CLARIFIED
METHOD_REF=2a18746124fdb26ba50e9813a50d687b5758e7ff
MODE=ISOLATED_OFFLINE_REAL_WINDOWS_CONTROL
REAL_CHATGPT_SENDS=0
ORIGINAL_B33_COMMIT_DISABLED=YES
VIRTUAL_MATURE=NO
STOP_GATE=NOT_PASSED
FINAL_VALID=NO

## 1 成熟源与方法
直接复用既有Windows AutoHotkey v2 + Descolada/UIA-v2成熟库；生产B33_Handoff.ahk仍受--commit硬停保护、没有改动。新增仅本地测试专用离线夹具B33_F013_NativeIsomorphism.ahk，使用原B33 SelectedChatDocument(root)选中标签/文档匹配逻辑、UIA按钮Click、输入框SetFocus、ClipboardAll/粘贴文本核对、Send Enter一次。本地独立测试网页file:///C:/AI/B32_ChatGPT_Handoff/B33_OFFLINE_UIA_TEST.html不含外部网络/API请求，只有本地DOM回执，不是官网ChatGPT。未部署调度器或常驻服务、未更换代理/浏览器配置。
本地测试脚本：C:\AI\B32_ChatGPT_Handoff\B33_F013_NativeIsomorphism.ahk
本地安全运行入口：C:\AI\B32_ChatGPT_Handoff\B33_RunF013_NativeIsomorphism.ps1
本地三轮结果：C:\AI\B32_ChatGPT_Handoff\B33_F013_NativeThreeTiming.json
安全约束：必须唯一匹配标题B33_OFFLINE_UIA_TEST_ONLY的Chrome窗口，UIA地址精确等于C:/AI/B32_ChatGPT_Handoff/B33_OFFLINE_UIA_TEST.html，唯一选中Document、测试标题归属标记、唯一New chat按钮；只针对受控本地文件执行页面动作。生产聊天不触碰。

## 2 已真实运行的离线UIA证据
- 原生测试第一次单轮通过：脚本内部672ms，外层911ms，唯一窗口→New chat点击→编辑框SetFocus→F013码粘贴读回核验→Enter一次→本地固定ACK。
- 为贴近原正式脚本，后续测试原样复用SelectedChatDocument逻辑，补齐唯一选中Chrome标签、唯一Document、本地路径/标题归属等检查。一次严格同构测试成功：原生动作与本地ACK总609ms，唯一Enter约406ms。
- 测试夹具启动阶段发现同名本地窗口有2个时，真实只读检查UNIQUE_OFFLINE_WINDOW=2并立即退出，未点击/粘贴/发送。根因是首次测试启动器用Chrome进程MainWindowTitle代表所有窗口；已在测试启动器移除该重复窗口自动创建逻辑，专用窗口由独立初始化入口管理。只是测试夹具缺陷，并非生产B33路径修复。
- 本地地址栏UIA读取只提供C:/AI/B32_ChatGPT_Handoff/B33_OFFLINE_UIA_TEST.html（省略file:///），最初过严的file scheme断言会安全拒绝；按真实观测修为精确本地规范化路径匹配，未放宽生产官网的chatgpt.com安全边界。
- 严格版本在唯一受控离线窗口连续3次有效执行PASS，脚本内部完成（到模拟ACK）593/578/578ms，中位578ms；外层进程时间1357/1385/1374ms，中位1374ms。Enter唯一提交时刻375/375/391ms；测试页面本地ACK不是官网模型ACK。每次运行前只重置当前测试文件页面，150ms重置开销不在脚本内部计时内，但进入外层进程时间。总计仅为本机隔离模拟控制动作的测量，不能计为B33现实全程T_VALID。
- 测试期间重复窗口被目标专属清理器关闭，不涉及生产ChatGPT标签或Chrome进程。全部ChatGPT官网自动发送数0，旧UNKNOWN短码不重发。

## 3 ≤3成熟方案和虚拟收益选择
A_BASELINE：成熟B33原生AHK/UIA + GitHub已连接入口的六文件顺序读取；已知单次同六文件实测2297ms，B33现实官网新建/发送未认证。
B_CANDIDATE：保持原生AHK/UIA及安全归属验证，通过现有GitHub连接器两轮Promise.all并行预取独立只读文件；已有同六文件单次实测1141ms，SHA匹配，局部读取阶段节约1156ms（约50.3%），无新状态机、无常驻服务。只读预取不得绕过短码、CURRENT版本、TASK_STATE_REF/CONTRACT/FREEZE校验，也不得并行副作用写。由于已证明正向局部收益且适配成本极低，选择B作为继续优化的成熟候选。
C_UNVERIFIED：ChatGPT官方Chrome扩展和桌面应用在Windows发现已安装/正在运行，但本会话无可证实的官方API能在原现有Chrome会话执行安全自动新聊天并产生被允许的模型接管回执。不得凭安装状态认定有效，也不使用替代通道规避此前被拦截的真实ChatGPT自动发送。
净收益：B相对于A有单次六文件只读局部增益1156ms；因启动/模型/真实网页/任务续做和恢复时间未知，完整系统NET_GAIN与T_VIRTUAL_BEST仍不能填值。若后续合法全链路证据显示完整收益非正则回退A。

## 4 现实基线、物理极限、完整虚拟最佳
时间合同：同一任务从接单与GPT自然节点实际完成、合法Freeze入库，到原有Chrome创建新ChatGPT聊天、一次F013短码提交、新GPT联网重新读取GitHub CURRENT/CONTRACT/FREEZE、ACK及继续同质量原目标FINAL_VALID，含恢复、部署与用户操作全部成本。
T_BASE_REAL=UNKNOWN：历史F011用户手动换聊回读成功但未提供该合同完整起止计时；历史其他五任务115.670s属于不同边界，不可嫁接。
T_UIA_LOCAL_MOCK_ACK_MEDIAN=578ms；T_UIA_LOCAL_MOCK_ENTER_MEDIAN=375ms；T_UIA_PROCESS_WALL_MEDIAN=1374ms。这些是独立离线受控Chrome UIA数据，页面不是真实ChatGPT，不能当原官网操作或模型物理下界。
T_GITHUB_READ_SEQUENTIAL_REAL_6_FILES=2297ms（历史单次）
T_GITHUB_READ_PARALLEL_REAL_6_FILES=1141ms（历史单次）
T_PHYSICAL_LIMIT=UNKNOWN：真实网站/服务端不可并行因果链和模型启动/回答的有量纲物理下界尚无测量，已测局部不能拼接为同合同真实理论极限。
T_VIRTUAL_BEST=UNKNOWN：至少缺真实合法新ChatGPT官网交接和同质量GPT续做恢复时间校准；禁止将578ms+1141ms或其他离线片段当完整最佳值。
DELTA_T=UNKNOWN
GAIN_PERCENT=UNKNOWN
SPEEDUP=UNKNOWN
NET_GAIN_FULL=UNKNOWN
FINAL_REALITY_VALID=NO

## 5 成熟停止门与后续路线
新贡献：证明原生AHK/UIA动作可按原SelectedChatDocument+目标归属约束在本地离线页执行；3/3连续PASS并有真实分段计时。局部故障回退正确。此结果提升原生执行器离线信心，但严格说FULL_B33_PRODUCTION_ISOMORPHISM=NOT_VERIFIED，因离线本地页面不具有官网新ChatGPT路由、服务端发送/模型ACK语义。
STOP_GATE=NOT_PASSED、VIRTUAL_MATURE=NO，因为同边界全程T_BASE_REAL、T_PHYSICAL_LIMIT和T_VIRTUAL_BEST均未知；现有平台前置安全拒绝及真实--commit硬停仍在，不触发官网Reality、不改写用户生产会话、不改FlClash。
NEXT：优先从合法同边界原始现实基线取得全程时间（已有完整原始日志可直接复用，不反复跑）；有官方允许的真实接管入口后仅在独立TEST任务获取一次新的现实基线，不重发历史UNKNOWN；随后用这组实测校准各环节虚拟模型，继续最大净收益虚拟攻击，算出完整T_VIRTUAL_BEST/物理极限差距与净收益门，再整体Freeze→一次最终Reality。若原路线经事实证明不合规/不可用则进入至多三个成熟候选重新选型，不自研通用控制器。
