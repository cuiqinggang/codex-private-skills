# LIFECYCLE-F001｜两处缺口的静态闭合与一次验证冻结
2026-10-16 北京时间；三人行V2 C002、桥V7 C优先/A暂停。用户本轮明确授权完成两处后验证。

## 身份差分结论
固定Orca提交2bb20586ebc39d605e16d95f57420e20a16e7485已核对：
send-methods.ts blob35ca1237227819e0c74231a1898522af1c258d8e从runtime/attested caller取得pane，不信任请求的senderPaneKey；
lifecycle-caller-fence.ts blobcb8b58f2883f82fa9a4e8ce7ef3d16af01ef4bbb拒绝另一coordinator/worker冒名；
send-point-to-point.ts blob9a6852f9ab707c81ac7fa681020e21e89dfe6908核对dispatch process incarnation；
worker-report-admission.ts blob31401d382c03fda9a4e9b68e75dcfacb1e862d9e拒绝身份变化；
lifecycle-reconciliation.ts blob838d2ce03276cf182accfb2c7a2e0b4c1f1b80d9核对task/dispatch/pane并原子结算；
orchestration-legacy-authority.ts blob71e9f83acfaefc86c29f0d30422ef7b92d6261d4对旧合同attested caller及process再次检查。
采用最小已支持路径：保持原Orca runtime、终端pane和父执行器，只结束超时的业务子进程；同一终端中恢复子进程。不能重建profile/terminal后继续报旧dispatch。整机/Orca终端失效不纳入此自动恢复范围，保持UNKNOWN并走官方对账；V4新profile恢复仅证明Codex会话可恢复，不能迁移成旧Orca派发身份。
不读取/伪造launch token，不直接改数据库。

## 计时与等待差分
单调时钟从脚本入口、资源/输入核对之前开始；整节点1200秒上限。普通CLI cap25秒、完成回执cap150秒，均min(cap,全局余额)。原请求超时不自动重发；结算幂等验证使用同一request ID/正文。实际本地验收终点在独立QA、进程清理、结果写入及回读之后。云端归档回读另记录最终接受时点，不能用局部秒数冒称包括此前分析/部署。
静态语法通过；确切remaining函数5项边界检查通过。第一次整模块离线导入因Linux未装psutil失败；改为抽取同一纯函数验证，不安装包、不冒称Windows依赖已测试。

## 本次Reality范围与验收
一次确定性官方管理链验证，不启动Codex，不重做T03。
实际Orca run→task→独立worker终端→context-only dispatch→新业务产物（已验三文件的摘要清单）→子进程受控超时→原终端内一次恢复→worker_done→同请求重放去重→task/dispatch completed回读→独立三文件hash/size核对及源不变→关闭所属终端。
受控故障仅一次性测试child睡眠60秒，被2秒预算终止并wait确认退出；不是网络故障模拟，不关闭代理/隧道/其他任务。普通模型360/600秒策略不在此测试运行；既有Codex exec/resume成果继续复用，不能称新编排模型业务通过。
失败保留节点目录和回执，停止后回虚拟分析，不在本次冻结里偷偷修脚本重跑。最多两官方终端，零模型，4GiB资源门，原权限和全局配置不动。

冻结脚本analysis/lifecycle-validation-r1.py@51377283b4a692ad33caf7009036f33c8c559719
SHA256=4b71dd9f6439b51b350aaa0ee9d3427f7cb0d7000f1ee3192c16c42bd39ae6aa
目标C:/AI/Orca-Codex-Validation-20261014/lifecycle-validation-20261016-r1（存在则不得重跑）。
本冻结只闭合这两处的限定设计，不是完整Orca→Codex业务虚拟成熟、效率最优认证或融合包发布。首次实际结果必须独立回读后判定。
