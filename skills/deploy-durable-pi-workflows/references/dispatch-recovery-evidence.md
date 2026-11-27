# 派工与恢复验收证据

## 冻结范围

| 环节 | 证据 | 适用范围 |
|---|---|---|
| Temporal 原生去重 | Windows 隔离实例同 ID 并发与终态重交返回同一 Run；不同 ID 取得独立 Run；同 ID 换独立实例取得新 Run；改输入后 UseExisting 仍返回原 Run | 原生调度探针 |
| 业务操作幂等 | Windows 隔离 SQLite 提交后进程退出，同操作键并行重试两次仅保留一条，独立操作另存一条 | 组件探针 |
| 正常、Worker 中断、调度重启 | R91 Temporal 与 Conductor 共六个历史短测回执，见 Windows 项目的 durable-three-route-reality-r1/R91-PAIR-RESULTS.json | R91 冻结合同 |
| R144 关联修复 | Run <RUN_OR_SESSION_ID_02>，原生 COMPLETED、独立回执 PASS，回执 SHA-256 <EVIDENCE_HASH_01> | 关联修复签收 |
| Louez 详情页绑定 | Windows 项目 r144-qa-detail-binding/RESULT.json。真实留存回执通过，七个反例均拒绝。包括错订单但格式正确、主单相邻单交换、错误详情页实例、错任务、漏步骤、错实例、显示编号代替 ID | 真实回执回放，修复候选 |

Louez 候选脚本 SHA-256 为 <EVIDENCE_HASH_02>。输入原 GUI 回执 SHA-256 为 <EVIDENCE_HASH_03>。测试只在内存中将回执任务号映射到候选目录，业务实例与详情 URL 沿用原记录。原 R144 保留原始终态及关联修复证据。

## R154 任务登记候选实测

Windows 隔离副本 r154-dispatch-identity-recheck/RESULT.json 签收 PASS。用 SQLite 主键原子绑定任务号、请求 SHA-256 和首个接单目录，两个目录并发登记收敛到同一目录，同号异内容被拒绝。首次执行由本机 Temporal 签收 COMPLETED；结束后从另一目录重交，仍返回 Run <RUN_OR_SESSION_ID_03>。两个目录合计只有一份业务产物。候选入口 SHA-256 为 <EVIDENCE_HASH_04>。

首次测试的合成命令假定单段运行入口注入任务号环境变量，写入后未生成回执，原生 Run FAILED。改为从冻结请求读任务号，在全新身份和目录下重新验证，旧 Run 及其唯一产物保留。覆盖范围为候选 CLI 的并发接单、终态重交、内容冲突和真实 Temporal 短任务。Windows 正式增强 Pi 入口、旧任务迁移、运行中重复提交回执、真实 GUI 并行和故障恢复矩阵继续待验。

## 运行中重复提交复验

Windows 隔离副本 r156-active-duplicate/RESULT.json。复用 R154 候选入口，实际 Temporal Run <RUN_OR_SESSION_ID_04>。原任务写入测试产物后、签收前，从另一目录重交：第二个执行请求被现有 supervisor 锁拦截，随后使用现有 status 操作读回原 Run 的 RUNNING。终态再次重交返回同一 Run，业务写入数为 1。候选脚本 SHA-256 与 R154 一致。已签收的范围为运行中防重复写、跨目录查询及终态重交。运行中重复调用 run 需要再调用 status 的交互差异，以及正式增强 Pi 加载仍待验。

## 同批并行故障实测

Windows 同时启动三个隔离候选入口，原始场景日志在 r157-batch-results，各自的 RESULT.json 在下表目录。所有受控故障都在测试业务产物已写入、签收前触发。

| 目录 | 原生 Run | 结论 |
|---|---|---|
| r157-duplicate | <RUN_OR_SESSION_ID_05> | COMPLETED，一个业务写入，运行中跨目录重复执行被拦截 |
| r157-service-restart | <RUN_OR_SESSION_ID_06> | COMPLETED，一个业务写入，替代调度进程从原库续跑同一 Run |
| r157-worker-restart | <RUN_OR_SESSION_ID_07> | FAILED，一个业务写入，替代 Worker 已触发第二次 Activity，缺已验证提交回执或适用的独立核账接续配方，停止重放 |

Worker 定点返修沿用运行时已有的 resume_preflight 与 resume_entrypoint 合同，按实际业务目标提供只读核账和原检查点接续。另复用已提交回执的原运行读回路径验证写后上报丢失。两种窗口须分别验收，保留原失败 Run。上述测试使用合成业务产物，正式增强 Pi 与真实 GUI 验收独立保留。

Worker 定点复验通过。隔离任务 r157-worker-resume-recheck 使用现有 resume_preflight 和 resume_entrypoint，模拟故障同时停止本组原 Worker 和合成执行子进程。独立核账确认已生效的唯一产物与停止的旧进程，第二次 Activity 按原检查点补回执。原生 Run <RUN_OR_SESSION_ID_08> COMPLETED，一个业务写入。回执存于该目录 RESULT.json，旧失败轮单独保留。此证据覆盖已验证检查点的合成业务接续。

## Docker 恢复后的 R159 并行短测

开始前核对 Windows Docker 启动回执 ENGINE_READY 和 Conductor 当前容器绑定的 /health。五组共同启用 R91 冻结配方，只改测试身份和工作区。原始 Windows 汇总在 durable-three-route-reality-r1/R159-PARALLEL-RESULTS.json，五组各通过七项独立检查。时间从短测派工到独立签收，包含并行资源竞争。

| 调度器 | 正常 | Worker 中断 | 调度服务重启 |
|---|---:|---:|---:|
| Temporal | 01:23:932 | 02:11:996 | 01:35:010 |
| Conductor | 01:28:585 | 01:53:493 | 02:45:547 |

Conductor 调度重启在两个共用服务的场景签收后开始，与 Temporal Worker 尾段同时推进。原工作流 <RUN_OR_SESSION_ID_09> COMPLETED，七项检查通过，产物哈希和修改时间保持一致。重启到读回耗时 01:29:452。原始回执见同目录 r159-conductor-service-result.json。

Temporal 调度重启保持原 Run 与产物指纹；Conductor Worker 接续保持原任务 ID、唯一业务执行以及产物指纹。这组是调度短测，正式增强 Pi 的入口签收另见 R158。真实 GUI 并行和真实写后丢回执待签收。

## 现场验收

1. 在增强 Pi 实际入口部署任务号登记。用原生 Workflow ID 或权威持久登记验跨目录同号只生成一个 Run、同号异内容冲突、重启可读回。SQLite 组件证据只能证明原子写入机制。
2. 新建隔离业务实例，把每组 GUI 标签到任务与目标。给详情页绑定补实测，保留独立账本核对，两组独立目标同时推进。
3. 按新版矩阵验证真实写后回执丢失、Worker 中断、调度重启、GPT 同会话恢复及独立审核。原 R91 可作为回归基线。Conductor 新一轮先复核本机服务可用。
