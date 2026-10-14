# Hermes现有生态站成熟化｜真实接续报告 F002

任务：HERMES-ECO-20261014。方法：《三人行》第2版，限本任务显式使用；不改变仓库全局V1。执行桥：GPT直连Windows双路执行桥V1.0。
目标仍为升级现有生态站：成熟资产复用、轻入口、重资料按需、真实执行与独立审核、Repair、原生多智能体、多模态、长任务及checkpoint/handoff。没有新建工作站。

## 1. 当前结论

**整站未完成验收；尚无可独立核实的连续五轮通过记录。上次本机验收是否启动仍为UNKNOWN，不能写成已执行，也不能写成确定未执行。**
本轮已完成：实际尝试A/B两条已授权路径、定位当前访问阻塞、修正验收候选、在隔离环境与GitHub托管Windows验证候选、保存网上接续资料。
F002仅为验收候选编号，不是Hermes版本升级，也不是《三人行》升级。F001原文件和已有生产资产保留。

## 2. 已发生的Windows配置变更，不否认也不扩大

上轮自建桥真实回执记录：2026-10-14T12:31:23.505908+00:00，仅修改现有config.yaml的platform_toolsets.api_server。
保留原六项file、terminal、vision、video、skills、code_execution；追加web、delegation、todo、session_search、cronjob五项原生工具集。
原SHA256：37c5cf0fb52e21d4173c2a9232977bf9eb07949480abfc180af9fbdda48298b5。
修改后已回读SHA256：02dca0e1d3dfc80f693bf9ecfe3c3e70dd3f85e4f361a670d60ade2a5ed75983。
备份仅在本机任务evidence/backups中；没有上传配置或凭据。未重启Gateway，未改代理或模型。
这证明当时配置写入成功，不证明当前运行已加载、不证明新增工具调用成功。本轮因权限阻塞不能重新核实配置是否后来改变。

## 3. 本轮真实阻塞与原始证据

A自建MCP：本轮read_multiple_files返回code=32600，message=Session terminated。上轮验收启动命令返回TimeoutError，未得到进程ID/验收run_id。因此必须先对账，禁止重复派发。

B原有Windows Runner：只读对账Run [38567587445](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38567587445)，Job 115864123548，已独立读取运行日志。
2026-10-14T12:55:56Z，DESKTOP-4A1EGTM-etal实际接单；Set up job成功。
2026-10-14T12:55:58Z，Test-Path被系统拒绝：

```text
Access to the path 'C:\Users\A\.hermes\skills\hermes-mature-supertool\evidence\HERMES-ECO-20261014' is denied.
Process completed with exit code 1.
```

因此是“此Runner身份不能访问本任务用户目录”，不是“GitHub不能派单”，也不是本次codeload超时。未读取到目录内容，不能把拒绝访问解释为文件缺失。
未修改ACL、服务身份、认证、FlClash或系统代理；未切换身份绕过拒绝，未启用额度耗尽的第三方Remote，未重复启动同一Hermes业务。

## 4. 发现并修复验收器问题（候选，尚未部署至用户Windows）

- F001只检查round-result，没有把已保存的request/ack作为中断对账入口；F002看到任何既有请求/接单回执立即阻止重新派发。
- F001豁免所有terminal工具错误，可能掩盖非预期故障；F002直接核对本run的SSE事件，只允许一次明确对应run-tests.cmd的预置负例失败，其它终端、视觉、联网或恢复错误不豁免。
- F001没有独立绑定实际模型/provider和跨会话身份；F002核对runtime、run_id、session_id及幂等回执，拒绝拿请求别名或同一会话冒充。
- F002将五轮合同通过与整站、重启、浏览器聊天端到端、长时耐久和物理极限分别记录，绝不自动把五轮样本扩大为整站终局。
- F002保留失败/未知记录，计算连续通过而非累计成功；拒绝空检查集、字符串假PASS、篡改输入、配置漂移、重复run及无效时钟。
- F002在非completed状态先退出，避免对等待批准/阻塞状态继续读取不会正常结束的事件流；未知接单单独留痕；回执采用同目录临时写后替换。
- 新脚本没有创建调度器、数据库或恢复引擎；仍调用已存在的Hermes原生runs/幂等/子代理，以及既有连续性脚本。新增检查器只读取本任务证据，不替Hermes执行业务。

## 5. F002实测结果及严格边界

固定源码提交：037e8bfaadb6ddb03122fbabb404b95a8b4e7e7f，目录acceptance-f002/。
GitHub托管Windows静态验证Run [38569144049](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38569144049)，Job 115869421123；完整日志已回读。

```text
POWERSHELL7_PARSE=PASS
POWERSHELL51_PARSE=PASS
Ran 42 tests in 2.328s
OK
CLOUD_STATIC_ONLY=PASS;USER_HERMES_RUNS=NOT_EXECUTED;FIVE_REAL_ROUNDS=NOT_CERTIFIED
```

这42项是合成回执/反例单元测试，不是42次Hermes调用，不是五轮用户电脑端到端，也不是“虚拟次数”代替现实。2.328秒只是云端单元测试时间，不能充当用户任务T_VALID或提速成绩。
隔离容器先完成相同42项单元测试，GitHub托管Windows随后独立复验；远端取回三文件的字节哈希与容器一致。

| 文件 | SHA256 |
|---|---|
| evidence_guard.py | 0049708928b099c74a0d6cb213f2b67aafe5573de975b9755c9cfe64a2ddb712 |
| test_evidence_guard.py | 2333fca3eeeb2777703a510c60956662c9491815f34c13e2fdbcafe19ec6e44c |
| Invoke-Acceptance.ps1 | ea285ede3571db4ef8c6ecf9005b3a1036d4f4fd1a4728dca29c3d9586cd0009 |

## 6. 启动资产继续继承，不重修已完成部分

先读skills/windows-hermes-operations/references/docker-startup-recovery-20261014.md及其归档提交4c48e249ca9c18ecde014d8b2e43f753a1f13139。
该既有修复记录了Windows Hermes0.21.5、C盘启动器、8642→Docker→OpenWebUI3000、认证模型发现、保留数据和健康态跳过固定等待。其热启动和入口验证为历史限定PASS；整机重启、下次登录及浏览器实际聊天仍须独立实测。
本轮不重启Windows、不更改已登录浏览器、不清理其它容器，不把“页面能显示”当作全部Agent能力通过。

## 7. 唯一继续点

先恢复用户已授权的自建MCP用户会话，使用已有桌面GPT-Windows-MCP-一键恢复入口，不新建桥或要求发送密钥。
恢复后第一步：一次批量读取本机HERMES-ECO-20261014的CONFIG-DELTA、REALITY-F001、BATCH-RESULT、各round/ack/run/grade，并核对本任务进程；只读本任务，不读私人会话。
若已有运行：按真实run_id接收/审查；若结果未知：继续对账；不得先运行F002。
确认旧尝试终态后，在同任务下新建隔离F002证据目录，不覆盖F001。F002依赖原prepare.py，固定源为674b241507051fbbb7084714a4b3f61881297ef7，Git blob为2ad59dbb2feb2c7535165d0aef34fcd0527dea46；只复用既有fixture/连续性资产。
部署候选前建立REALITY-F002.json：task_id、contract_ref=F002、真实prior_attempt_reconciled=true、当前config_sha256、fixtures_sha256、三份运行源source_sha256。此文件目前未创建，不能预填成PASS。
随后按冻结合同完成真实修复、检索、视觉、两个独立子代理审核、checkpoint/handoff、新会话resume及外部unittest。固定配置连续5轮，意外失败保留并回虚修复，重新固定后再计数。
启动/浏览器实际聊天、音视频和真正长任务耐久等不在上述小样本内的能力单独列出缺口，不作虚假整站认证。现有资料库重资料仅按需加载，不压进每个运行上下文。

## 官方机制核验来源

- Hermes工具按平台启用：https://hermes-agent.nousresearch.com/docs/user-guide/features/tools/
- 原生runs、幂等、session、runtime与SSE事件：https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server/
- 本机启动既有成功资产：skills/windows-hermes-operations/references/docker-startup-recovery-20261014.md。
