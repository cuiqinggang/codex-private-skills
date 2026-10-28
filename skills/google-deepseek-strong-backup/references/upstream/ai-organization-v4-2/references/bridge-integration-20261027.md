# V4.2 接入 Windows 执行桥 V12.0.4
日期：2026-10-27；类型：执行依赖补丁，组织方法仍为V4.2。

## 必须继承
1. 每个Windows任务首次调用前加载 gpt-windows-execution-bridge 当前有效版本（当前V12.0.4），先发现和核验A。
2. A=收费Remote Desktop Commander；B=免费GPT-Windows-MCP-Bridge；C=GitHub Actions Windows Runner。默认A→B→C，按桥规则保留失败复验和副作用对账门槛。
3. A/B均先判断安全本地批量：多文件纯读一次read_multiple_files，本地处理校验闭环一次start_process复用成熟脚本。批量不固定5项，按依赖、资源、权限、输出与恢复边界决定。
4. 逐项校验并汇总返回；RUNNING/PID续读到真实结束，计时包括续读和验收。部分成功或UNKNOWN先核账，只续做确认未执行项；外部审批和不可逆动作按边界拆批。
5. 不另造调度、连接池、锁或状态机，不改FlClash、代理、密钥、生产隧道或其他任务。规则不等于所有旧聊天已被平台强制拦截。

## 证据与边界
已加载的执行桥V12.0.4原技能及其references/batch-validation-20261027.json是本次依赖来源。原始对照为A内置2.663秒、B内置8.140秒、B命令4.197秒、A命令2.537秒，每种1次、每次5项核验，共20/20。它们是局部工具调用时间，不是V4.2完整业务T_VALID。

本补丁仅核验规则、引用和已保存文件一致性。V4.2-FROZEN-RELEASE.md、V42_RELEASE_GATE.json及原能力归属规则作为历史验收保留，不能把其V12.0.1记载改写成V12.0.4已跑过原业务。
