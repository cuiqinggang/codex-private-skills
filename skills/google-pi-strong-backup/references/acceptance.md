# V2.0 当前入口与验收

2026-10-31（北京时间）。任务GSB-PI-GOOGLE-20261031-001。状态：DEPLOYED_SCOPED_PASS；14项发布门通过。主执行为Official Oh My Pi＋现有DeepSeek provider，Google按需网页协作，DSH仅显式回退。组织总版本保持AI自动化组织V5。

## 当前入口

- 桌面：`C:\Users\A\Desktop\谷深强备.cmd`。
- 宿主：`C:\Users\A\Documents\DSH-Workspace\gsb-pi-google-v2-20261031`；先读CURRENT.json、DEPLOYMENT.json，核实际SHA。
- 原强备导航：`C:\AI\DeepSeek-Gemini-Failsafe\CURRENT.json`已指向V2。
- 正式订单入口：`C:\Users\A\Documents\DSH-Workspace\aiorg-independent-handoff-20261029-r2\deliver.cmd`，调用同原workspace内`service-pi-v2`，保持原jobs/continuity。
- 宿主根的`order-service`为隔离测试副本，禁止用它的新jobs冒充旧订单账本。
- Google方案：原桌面“强备份-执行Google方案”已转接Pi，保留旧计划claim核账与去重；新可写任务位于宿主plan-jobs。旧UNKNOWN不盲重发，仅匹配来源哈希的CONFIRMED_NOT_EXECUTED核账允许接续。
- 显式回退：桌面“谷深强备-DSH回退.cmd”；旧V1.6原生技能及历史原件未改。兼容副本仅将时间方法的精确版本钉住值1.0.1改为现场2.0.0。

## 同合同完整业务窗口

| 合同 | Pi | DSH | 质量 |
|---|---:|---:|---|
| 48行订单、CSV/JSON/Word/Excel | 00:45:361 | 01:19:503 | 原校验器20/20，输入不变 |
| 正式预约网页完整增改查、刷新、CSV下载、删除测试行 | 02:13:221 | 06:36:962 | 双方PASS，原14行与原页保留，零付款/外发 |
| 真实自有进程树中断＋原生session续接 | 00:50:861 | 02:32:492 | 双方PASS，已确认输入/成品SHA及mtime不变 |

均为限定合同单次结果，不是所有任务稳定分布或网络全局最优。两种DSH基线公开：文件与原生接续为V1.6协议兼容副本；浏览器为原已验收DSH browser入口。没有隐瞒切换后台。

177行核账两端均内容通过；新一组三次Pi原窗口33.059/34.341/59.828秒，DSH原窗口104.964/88.901/96.908秒。DSH报告中的“未调用Codex”被旧文本检测误报，原回执保留并另记更正时间；这些原窗口不作为包含审核修复的T_VALID排名。早期Windows路径/允许修改源码断言误报也原位保留。

## 独立验收

- Pi与Google实发一次匿名审核，Google真实助手回答1600分并拒绝错误1900分；按助手DOM作用域、实际提交次数、任务页关闭与原Target保留独立核验。DSH正确browser配置同题也通过；其首auto配置失败及延迟审核保留，不能用局部窗口作完整速度排名。
- 6种正常/故障订单交接及重复请求通过，每单20项内容检查、只生成一次；其中部分无需模型，不能冒充Pi模型执行。
- 强制主端退出后Pi模型真实接单：原生技能读取门通过、原配方生成、20/20独立QA与一次提交，104.040秒（该专门合同不与普通订单合同直接排名）。
- 旧版生成后中断→新版原账本接续通过，原产物SHA/mtime不变；旧已提交请求经新版默认deliver.cmd读回，不重做。
- 提交回执加固11项通过：身份、scope、状态、固定四件、路径归属、输入哈希、生成计数和独立QA；伪/缺回执不能直接接受。
- 实际只读业务写入被原ACL组件拒绝；OMP用官方--cwd访问业务目录，写能力仅给予独立元数据根，未放宽业务目录权限。纯只读任务及原只读session续接通过；写入session原生续接也通过。只读/写入各保留原元数据位置，不复制私有会话。
- DSH session、错cwd、未知UUID拒绝；4种非法输入在模型启动前拒绝。
- 原成熟隔离MCP离线钩子下，Pi本地文件交付通过，原正式MCP未停止。
- Google方案适配器经现有PowerShell guard实跑与独立核算通过；重复计划拒绝且原成品未再生成。原C盘受保护项目根ACL启动失败在模型启动前核账，保留原UNKNOWN与单独RECONCILIATION。
- 最终公开入口写入/只读两类原session实跑通过，原业务产物未变。

## 保存与边界

源代码快照见`assets/host-runtime`；它绑定当前已安装运行时与原配方，不是新电脑完整离线安装包。原始失败、耗时、成品及审核位于宿主根tests、browser-reality、jobs与各独立回执；模型思考、身份和凭据没有复制进本包。

浏览器跨整机重启无人值守、多日SLA、断电、跨设备、任意账号/平台插件/专业任务完整等效仍未认证。原本地文件真实重启20/20证据继承，不冒充本轮新浏览器认证。完整替换工程T_VALID_PROJECT及实际账单NOT_MEASURED；不将局部执行窗口当全部工程用时，不宣称全面最快或成本全面更低。
