# Orca＋Codex｜官方 exec 输入与原会话恢复实测 V4

日期：2026-10-15 UTC／北京时间10月16日。方法仍为《三人行》第2版 C002；执行桥为V7，C实际执行，A暂停。V4仅为本集成测试报告编号，不是三人行第3版，也不是融合技能包发布。

## 验收结论
本次取得有限业务闭环：**Orca官方隔离工作树/终端 → Codex官方exec stdin → 同一会话官方resume → T03产物 → 外部确定性验收**。恢复成果接受；原360秒尝试失败保留。没有使用orchestration worker-start完成本次业务，不能代替完整编排闭环、三任务Reality、10轮稳定性或AB效率证明。

外部独立检查3/3通过，原始BAD仍2/3（除零被检出）；模型自身五项离线测试通过。独立git差分只有scripts/run.py：6行增加、3行删除；新增五项离线测试与DELIVERY。最终只引入report内部rate函数，0任务显示右对齐--，非空原有百分率计算和格式保持。未修改既有GOOD_003_CEO_RECOVERY。

## 整体分析→最小变化→现实结果
固定Orca源码确认headless按bracketed-paste写入正文再发CR；桌面Windows多行输入PR不能直接当作此链已证根因。R2原生worker-start的ready/turn_started无产物问题仍未根治。
选择官方Codex exec标准输入替代本次任务正文传输，避免依赖交互式粘贴。保留Orca官方二进制、真实home、任务隔离数据、工作树、终端身份、模型与权限；Python仅承接一次进程/回执/有界试验，不新增通用调度器。

R3最初360秒到时停止：请求超时后曾自行恢复，Codex真实执行了源码读取和测试编辑，但业务源码尚未修改，QA2/3、DELIVERY不存在。原进程清理为零。
回到整体分析：已有测试分别修复Windows临时目录创建和路径文本比较，剩余工作已具体定位。冻结官方exec resume，锁定会话01a140cc-584e-7c43-87a1-1f7ce24449c3，不创建新的模型任务或重做已有测试。恢复前复制run.py与测试到recovery-r1/before；新Orca profile防止旧终端启动命令被恢复，注册原fixture，以真实路径指向同一工作树。
恢复第一次入口低于4GiB内存门，未创建目录/未启动模型；随后独立回读available=4622139392、required=4294967296，确认目录不存在，才在原门下受控再试。未结束其他业务、未降低资源门。恢复模型预算600秒，实际正常exit0并交付。
恢复期间保留4条request timed out重连记录；最后五项测试通过。测试自身曾把多一个空格和横线分隔符误计作失败，已修正断言，业务非空格式未迁就错误测试。

## 实际环境、模型和权限证据
实际Codex0.160.0；子进程argv及Codex自己的turn_context一致确认cwd为本次worktree、model=gpt-6.1-sol、effort=ultra、approval_policy=on-request、approvals_reviewer=auto_review、sandbox_policy.type=workspace-write，network_access=false。USERPROFILE=C:\Users\A。
priority是CLI请求；turn_context的service_tier为null，实际后端优先级仍UNKNOWN。没有读取或复制认证文件，没有修改全局Codex配置、网络、代理或ACL。
Orca仅127.0.0.1、动态端口、no-pairing。恢复终端term_10cfb960-c5cc-468c-a779-a50f54fa7a81实际关闭，ptyKilled=true。服务与所属子进程清理完成；最终独立按任务路径核对Node/Codex进程为空。

## 仍保留的故障与边界
- R2交互输入根因未知，不能因exec成功就说原入口修好了。
- 两次模型请求均出现重连超时后继续；稳定耗时未证明，不能推断必为WebSocket、代理或某个服务端原因。
- 另有某MCP HTTP403 challenge、两项本机技能frontmatter错误、未知config字段告警。任务最终完成证明它们没有永久阻断本次T03；不代表可以忽略它们或已修复。
- resume报告缺失上轮某tool-call output，最终正常完成；不能声称硬中断恢复所有场景都可靠。
- 原测试留下五个受限临时目录，按任务合同保留，不改ACL强删。新测试目录正常创建清理。
- 本次只证明使用官方exec/resume的恢复型有限闭环；原生Orca task/dispatch/heartbeat/worker_done仍未Reality。

## 计时口径
初次脚本局部elapsed=407161.1994ms，工具进程观察444.01s；恢复脚本局部elapsed=307058.2712ms，工具进程观察313.17s；恢复模型进程约284.058s。脚本局部计时起点在入口资源/进程核对之后，终点在结果文件写入之前，还不包括后续独立QA、报告归档与回读，**均不是完整T_VALID**。不得相加宣称总耗时或提速。全程有效时间、净节时、AB提升继续UNKNOWN。

## 可回读成果
- 初次冻结analysis/business-exec-r3.py@f743b96dc079725337be2a820c7d22d3bc910189，SHA256 e8589eb8ace1bbaa2ccc6bc670cec6538aae23cc48cb6790638c670ddfc172cf。
- 恢复冻结analysis/business-exec-r3-resume.py@22ae2e278548c20c94d34a32006777c6962a99f9，SHA256 e6276b19d4a0060454037a4454a9c322fec649fe00821290fb273d29dd5da41e。
- 初次负例QA evidence/business-exec-r3-qa.json@143d28e6f510ef941e6fcd8127aff7ce3e7b91ef；首次打包误把异步提示末尾字符存入文件，已修正、JSON解析及逐字回读通过，错误提交保留。此为归档器错误，不是业务代码失败。
- 实际策略 evidence/business-exec-r3-effective-context.json@330f42951c4ae065f3a7eaa84ebc68c85a04c6b3。
- 原执行摘要 evidence/business-exec-r3-event-summary.json@955538ff9abaa46a2169dd1ee2864b6eff6bf6c0；prompt_exact_in_session=false只表示精确字符串比较未成功，不冒称输入字节完全一致。模型确实读到T03并执行由真实工具事件证明。
- 恢复独立QA/差分/最终manifest evidence/business-exec-r3-recovery-qa.json@2cbc8237465909570a356c8eb1b977c27e313f69。
- 成果文本导出 evidence/EXEC_R3_RECOVERED/scripts/run.py@fcffc0b20d3531a04351c205e64d2318d9dfba6b；tests/test_run_report_offline.py@0195194307dc1342adb509d592c2a32444f1491c；DELIVERY.md@d88414a76f421eb6b4165d8af7728b58df9528a1。文本导出逐字回读，Windows原文件SHA见manifest；不把工具文本换行导出冒充全工程字节备份。

Windows成果：C:/AI/Orca-Codex-Validation-20261014/business-exec-20261015-r3/worktrees/fixture/component；初次result不覆盖，恢复证据在recovery-r1。全文大型原日志留本机，未声称全部上传。

## 下一最小节点
停止重做此T03已验恢复成果。已核对官方context-only dispatch可返回preamble而不注入PTY，且明示unsupervised/context_only；详见CEO_OFFICIAL_CONTEXT_ONLY_ROUTE_REVIEW.md@cec0e49fc3b3a21db3e49853bbe43a44a5343f4f。下一步补齐真实协调者/任务/派发绑定与worker_done身份协议，然后把已验exec输入路线接入官方管理生命周期。该候选未执行，不能宣称整套虚拟成熟或正式融合已完成。
正式三任务Reality=0，连续全面运行=0/10，AB=0/10，容量和极限效率未认证。旧平台被拒预检未重发，本次没有新平台拒绝。
