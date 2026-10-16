# SUITE_AB_F003｜只读对账与失败回执最小修正
日期2026-10-16。继续三人行V2 C002@4c48e249ca9c18ecde014d8b2e43f753a1f13139、桥V7、合同V1和用户本轮真实十轮/A-B授权。
继承SUITE_AB_F002.md@a98384478bccf3bf0de1c627d277b0c1868413b2全部输入、模型、权限、业务SPEC、质量、资源、1900秒总预算、900+600模型预算、A/B顺序和完整计时边界。仅以下差分。

## GOOD→BAD→FIRST_DELTA
F002 pilot通过外部14/14、回归16/16、目录/关闭/进程与CEO审查，完整首归档回读759204.6176ms，证据evidence/SUITE_R2_PILOT_B.json@9233ec517290db4d61cc1b2380a553f5bef791e0及FINAL_TIME@2a2ca9d486af84671c1c9eceda69837bf205e9ba。
正式p01-B业务14/14、22/22，worker_done消息msg_41082d5a3442，task_4a677ce0d22f/ctx_28538fa1ab01，精确会话01a144a7-48f7-72b3-8015-637d7e93b15e exit0，无外部resume。
随后task-list25s超时；finally中后台wait10s又抛异常，覆盖汇总写入，result/local-acceptance缺失。此为真实全套失败，不计稳定性，亦无完整配对。业务成果已保留且源码与三测试全文审查通过，不重做此副本。
只读对账完整证据evidence/SUITE_R2_P01_B_RECONCILIATION.json@73ddb8b576d6a109191557638bae0afd1ed4f15d（逐字回读一致）。runtimePID21400、Codex20424、parent58704后续均pid_exists=false，未手工杀其它任务。C一度离线后list_devices在线，继续C，未启A或B。
原因边界：CLI等待和退出等待超时是直接证据；系统负载/网络具体根因未证实，不将增大超时当根治。

## 最小成熟修正
1. 仅官方task-list/dispatch-show只读查询白名单：25s超时最多重读一次，1s间隔且受原总截止约束，每次超时单独落盘。不重试派发/完成/创建/关闭等变更请求。
2. 清理用原psutil进程树有界等待并回读活性；剩余/未知即失败。Windows kill与terminate同义，不能声称kill更强。对已经退出Popen先poll返回，避免PID复用误终止。
3. finally隔离清理/进程读取/采样摘要异常，仍写失败result及local-acceptance；保留错误数组，不能写成功或删旧错误。若磁盘本身写失败仍不能保证持久化，此边界保留。
官方依据：https://docs.python.org/3.13/library/subprocess.html （wait超时抛异常；Windows terminate和kill语义）。不是改Orca源码或新造恢复框架。
六项离线边界实际PASS：只读首次超时后二次成功、两次超时有界失败、变更请求禁止重试、清理等待异常保留剩余、进程已退出回读、真实main/finally清理异常仍落失败回执。分析测试不计业务轮数。

## 冻结与执行
脚本analysis/suite-ab-r3.py@d4c450345b82e5d5512c94526da88963bbc80639
SHA256=4d12f5c55d4ac8ade9437d56f5d799319cc3ec2ecf9ede06080fee7ce8acbd96
边界测试analysis/check_suite_recovery.py@bc5969bda7a2b8d8146e7dea1d704831bb3abba9
Windows脚本C:/AI/Orca-Codex-Validation-20261014/suite-ab-r3.py
新批次C:/AI/Orca-Codex-Validation-20261014/suite-ab-20261016-r3
CEO批准本具体修正先main B pilot真实验收，随后同版十组p01BA,p02AB交错至p10AB。连续计数重置0；旧F001/F002失败、成功、部署与等待全保留。不得将已验旧pilot或被修复后的旧p01算新版本十轮。
实际tier仍未知，完整前期摊销未知；即便20套成功也只能报告有边界的实测耗时，不能绕过分析器未知条件门宣称公平性/净收益已全证。400/1000容量、全故障矩阵、正式融合发布仍未认证。
