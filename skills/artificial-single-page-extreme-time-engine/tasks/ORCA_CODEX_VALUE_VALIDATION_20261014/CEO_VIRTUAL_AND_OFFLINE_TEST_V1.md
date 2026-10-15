# 虚拟推演与离线源码执行 V1
日期：2026-10-15 接单，北京时间；方法三人行V2 C002，桥V6。
结论：部分准备验证完成，整套虚拟成熟未通过，Windows正式Reality未执行，连续业务0/10、AB0/10。

本次实际执行的是Linux工作容器中的Node v24.19.0离线源码测试，不是Windows、Orca后台或Codex业务。固定Orca提交2bb20586ebc39d605e16d95f57420e20a16e7485的两份原始TypeScript源码先验证Git blob SHA，再去类型并装入隔离VM；外部依赖替换为会记录调用的虚构对象，分支平台模拟win32。没有真实凭据、文件系统副作用、网络、端口、模型调用。不得将模拟win32称为Windows解释器实测。

## 实际结果
11/11分支断言通过，含正例与反例：
- 缺迁移记录、已有非空基线、managed归属、空runtime auth：没有调用系统凭据写入。
- system-default旧记录、基线为空、镜像非空：调用条件写入、记录provenance、快照。反例通过表明存在风险条件，不是候选可上线。
- 系统条件写入被拒时：仍记录provenance，因此不能称没有任何状态变化。
- 默认账户且无custom-home选择真实home；custom-home使其离开该分支。
- 无旧pane不触发旧配置同步。
- prepareForCodexLaunch真实home分支仍调用两个兼容辅助函数，然后返回null。
- 官方read-only home resolver不调用启动准备辅助函数。

这里证明的是固定源码在虚构依赖状态下的分支行为；未执行构造器整条迁移链、真实hooks、系统配置加载、Windows子进程或文件写入。新空profile可能避开部分条件，但尚不能推出全启动过程零复制/零全局改写。

## 测试工具自身失败保留
第一次执行退出1：TypeScript去类型保留abstract所在空白，生成“export          class”，测试器只替换“export class”而未移除export，VM报SyntaxError。发生在用例运行前，不是Orca业务失败。仅把测试器的export匹配改为空白兼容正则；第二次运行退出0，11项通过。官方源码未改。Node提示stripTypeScriptTypes为实验功能，记录保留。
第一次墙钟工具回执约0.056s，第二次约0.031s；均仅测试程序运行，不是项目T_VALID、Windows业务耗时或提速证明。

## 冻结判决
F001保持原候选不可变，N002不批准。
阻塞1：实际启动构造器及hooks全链仍未证明符合不复制凭据/不改全局配置合同；配置更新入口也未完成核验。
阻塞2：原GitHub运行时预检被OpenAI安全检查拒绝，原文“此工具调用被 OpenAI 的安全检查屏蔽。请仔细检查你发送的内容。”仅此一句，原因未知。本次没有重发、换通道或让用户手动代执行。用户已授权测试，无需重复泛化授权；平台执行边界仍须遵守。
阻塞3：旧会话退出、实际用户环境与有效权限仍无本轮新回执。
不得用11项离线通过替代首次业务闭环、十轮稳定性、效率或容量认证。

## 可复核产物与接续
- analysis/home-routing-v1/routing-snapshot.json：固定源码、blob身份、上游MIT许可。
- analysis/home-routing-v1/routing-branch-test.mjs：可复现离线测试器。
- analysis/home-routing-v1/routing-result.json：本次真实离线执行结果。
复现命令为在同目录执行node routing-branch-test.mjs；仅适用于此离线夹具，不连接Windows。
下一步沿实际构造器syncForCurrentSelection和hooks调用链证明空profile的条件，再核对官方设置更新落点；这些独立准备可继续。满足合同和平台条件后才能冻结整套WindowsReality，不能只因用户说实际测试就把未知条件算通过。
