# Orca 集成操作流程 1.2｜原终端恢复与官方结算已限定验收
2026-10-16 北京时间。方法仍《三人行》第2版C002，执行桥仍V7（C优先/A暂停/B备用）。这是项目流程小修订，不是方法新版本或正式融合技能包发布。
前版OPERATING_FLOW_1_1.md保留历史；本文件为当前操作入口。

## 本次两处完成结果
1. 身份绑定：固定官方源码查清服务端对pane、真实调用方和process incarnation的核验。采用保留同一Orca终端与父执行器、只停止并恢复业务子进程的成熟路径。真实验证中恢复前后dispatch、handle、pane、process incarnation一致，官方worker_done成功结算。新终端/新profile不得复用旧dispatch冒名完成；整终端失效属于另一个恢复场景，未认证。
2. 分层超时与计时：已冻结并实际运行的验证脚本使用min(单次上限,全局剩余预算)，普通CLI25秒，完成回执150秒，全节点1200秒，超时后不重置。单调起点在资源及输入核验之前，终点在本地业务QA、清理、证据写入与回读之后；随后记录含首次网上证据归档回读的接受时点。5项纯函数边界检查通过；首次Linux整模块导入缺psutil的失败保留于冻结说明，未冒充完整本地运行。
官方120秒runtime_unavailable退避由原CLI承担，同请求ID、1秒起指数退避、最大15秒间隔；此次没有人为断网或等待120秒，不能声称网络故障恢复窗口已实测。

## 一次实际验证的合同和结果
LIFECYCLE-F001：LIFECYCLE_F001.md@867c4518ef3fad9853be80f0dc80a70cbd19ff95
脚本：analysis/lifecycle-validation-r1.py@51377283b4a692ad33caf7009036f33c8c559719
SHA256：4b71dd9f6439b51b350aaa0ee9d3427f7cb0d7000f1ee3192c16c42bd39ae6aa

通过C通道在Windows新隔离目录实际完成：
官方run/task→独立worker终端→context-only dispatch→新建三份已验成果的摘要清单→一次受控子进程超时→原终端一次恢复→官方worker_done→原请求重放→task/dispatch completed回读→独立hash及size核对→关闭所属终端/进程。
此次产物是新摘要清单，既有T03源码/测试/DELIVERY没有改动；三份文件均与此前接受摘要一致。没有启动Codex/新模型，不将确定性子进程恢复称为Codex resume实测。官方context-only仍为unsupervised，不是Orca自动监督模式。

- Run：run_040a5b80cfc5；Task：task_2f5b52e2e2c6；Dispatch：ctx_01b08a04a6fe。
- Worker：term_ad78f5a6-8d29-444b-b03f-27c0eb107d4f。
- 受控child PID59968在2秒上限终止，确认退出后仅恢复一次；有真实部分产物保留，不是仅等空脚本。
- 完成request：ef14b4d6-233a-4140-b154-d8eb0d33ada7。首次及同请求重放均返回msg_c1ee16bf0263，没有产生第二份完成消息。
- task与dispatch均completed，task.result.provenance=worker_report，messageId对应同一回执。
- 独立成果检查3/3；两个官方terminal close均ptyKilled=true；所属进程清理后独立检查server60028/daemon58500/child59968均不存在。
- 摘要清单SHA256：6f60c0f177cfd648715bea2223aca8d2949f159c55ff5a1369c4c2e05654d62c。
- 脚本退出0；连接器记录39.56秒；本地有效验收39.091秒。
- 从Windows脚本入口到独立QA、清理、首次网上证据归档回读及最终进程核对：101.271秒（单调时钟）。不包括此前方案分析/脚本投放及后续总结发布，不是全项目T_VALID，也不是Codex任务速度或A/B提速。

证据：evidence/LIFECYCLE_R1_ACCEPTANCE.json@99ab8cb0c0a55ede29eb59e6b7df09ee7fff02b7，已逐字回读；
计时：evidence/LIFECYCLE_R1_FINAL_TIME.json@4480ba8b0728d68de9ba4fd1a9dcdca62b724e5e；
本机：C:/AI/Orca-Codex-Validation-20261014/lifecycle-validation-20261016-r1。
运行日志仍见agent-state-rules HTTP404，本次限定管理任务通过，不表示该告警已修复。

## 后续直接采用的操作规则
- 已验GOOD不重做。本次摘要任务也DONE，不再次执行脚本；目录存在则对账。
- 模型使用已验官方exec stdin；超时只在原会话、原工作树、原权限、原Orca终端中resume。保留父执行器和Orca runtime，只结束已核验归属的模型子进程。
- 沿用模型初次360秒、最多一次恢复600秒、节点1200秒的候选预算；这组模型预算尚未与本次官方任务管理链联合实测。预算耗尽回到分析，不自动加时或循环恢复。
- 保留真实官方注入身份，不复制令牌、不改数据库。终端或runtime也退出时停止自动恢复，先按官方身份/派发规则对账；没有身份重绑定验收就不得带旧dispatch继续。
- 工具running只取原call_id/PID结果；UNKNOWN查原run/task/dispatch及已有产物。禁止把连接超时当成未执行。
- 完成回执使用150秒外层cap且受总预算约束；官方120秒重试不能被旧25秒通用限制提前截断。原request/body持久化，UNKNOWN先查状态，必要时原--retry-request恢复。
- 官方completed与外部业务QA分别判断；二者均通过才接受业务。完成回执重放只恢复管理状态，不再运行模型。
- 结果/失败/恢复/清理/归档回读全部计时；局部秒数不冒充端到端。安全拒绝、身份拒绝不换通道绕过，A仍暂停，不改代理/ACL/全局模型配置。
- 旧R3/恢复脚本是不可变历史证据，未热改为通用生产执行器；本次脚本是一次性验证适配，非新增调度或恢复引擎。

## 当前边界及下一自然节点
这两处的限定方案、实现和一次管理链Reality通过。已验Codex exec/resume与此次已验管理链仍是两个证据层，不能直接拼接成“Orca→Codex整套业务已通过”。
下一节点才是将两条已验路径按同终端方案组合，冻结一个未完成的真实业务任务并验收；不要重新做已验T03，不再次做本管理烟测。若该整合产生新失败，定位最小差分再回虚拟阶段。
完整三任务Reality=0；连续十轮=0/10；AB=0/10；全局极限效率UNKNOWN；正式融合包尚未发布。
