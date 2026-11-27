# Windows 已验证配方与历史证据

新任务按[正式派发及验收流程](formal-run.md)推进。本页证据路径以 Windows 工作区 `pi-comprehensive-20261113` 为基准，保留原生终态、关联任务与实测范围。

## 部署配方与阶段接续

- 复用已签收的 Compose 配方。先用 `docker compose config` 读回最终挂载和依赖，再按目标实例核对容器、当前端口、数据库、对象存储和实际应用健康。固定配置可评估 `configs.file`。文件 bind 使用长语法 `create_host_path: false`。冻结请求的 `required_files` 将实际使用的相对路径映射到可信 SHA-256，审批、派发和启动前分别检查文件类型与指纹。Louez 核对实际挂载的 `stream.conf`。
- R102 宿主 Docker CLI 可读 `desktop-linux`，实际两路隔离启动器访问 `dockerDesktopLinuxEngine` 命名管道时遭拒，显式指定 context 仍复现。证据 `louez-medium/{temporal,conductor}/R102-context-startup.log`。因此探测必须以实际执行身份完成。
- R109 漏带 `stream.conf` 导致中继挂载失败并使原 Run 原生 `FAILED`。R110 先核原项目、容器、卷和账本，保留误建空目录供审计，从 R75 可信原件补文件，恢复受影响的中继并沿已验安装检查点续跑。三项构建、可见 GUI G00–G12、原账本五笔 CNY 和独立隔离还原通过。完整宿主 QA 和同 Run 自动返修仍待签收。证据 `r109-temporal-louez/R110-FINAL-AUDIT.json`。
- R112 真实 Windows 入口在审批截住缺失、目录和错误散列，在派发前截住审批后篡改。四个负例均无 `DISPATCH.json`，原件成功。证据 `r112-bind-preflight/RESULT.json`。R114 的已解析配置确认只读文件挂载与正确指纹。本机 Compose v5.1.1 / Docker Desktop 在独立无网络负例仍为缺失源建出目录，所以保留实际文件检查。证据 `r114-temporal-louez/COMPOSE-BIND-VERIFIED.json`、`COMPOSE-MISSING-BIND.json`。
- Temporal Workflow 编排阶段，实际部署、构建、GUI、备份和验收放在原生 Activities。长 Activity 记录心跳与进度。按已冻结策略处理瞬时重试及确定性纠正，提交状态不明时先核账。请求里的可选 `stage_receipts` 映射阶段与独立 PASS 回执，沿用最终回执的 `task_id`、`status`、`artifacts[].path` 和 `artifacts[].sha256` 契约。阶段验收后原子落盘。
- R130 在合成安装写入和阶段回执已落盘、Activity 尚未确认时中断 Worker。原 Run `<RUN_OR_SESSION_ID_20>` 成功，尝试数 `[2, 1]`，安装写入一次。证据 `r130-stage-receipt-probe/STATUS.json` 及阶段回执。Louez 真实安装的阶段回执与同 Run 接续另行验收。R128 原失败保留。

## 原任务接续、关联纠正与范围

| 实测 | 固定做法与证据 |
| --- | --- |
| R104 Conductor 统一入口 | 历史隔离入口 `Open-Pi.cmd --durable-longflow approve/run/status/resume`。冻结 `request.json.scheduler` 支持 `temporal`、`conductor`，旧任务默认 Temporal。Conductor 终态前校验任务号与独立产物指纹。缺回执写 `CORRECTION-REQUIRED.json`，保留原 Workflow RUNNING，`resume` 先对账。用例 `r104-conductor-entry`、`r104-conductor-no-receipt`。 |
| R105 / R105b Conductor 纠正 | `correction_entrypoint` 与命令文件随任务冻结。仅在已接入的缺签收条件触发，成功还需独立产物核验。首次模型未解析，后续继承用户提供方配置后实际请求一次遇到 403，`amount` 保持 90，等待纠正。证据 `r105b-conductor-repair`。覆盖自动触发和拦截误签收，真实裁决成功、同会话改正、同号后续自动恢复待验。 |
| R107 Temporal 同 Run 纠正 | 合成业务已落盘、签收缺失时自动调用冻结 `correction_entrypoint`。已登录 GPT 返回绑定标记的真实裁决，Pi 在原会话把 90 改为 91。原业务标记保留，独立核对五项指纹，原生 COMPLETED。Run `<RUN_OR_SESSION_ID_21>`，证据 `r107-temporal-repair`。 |
| R107 / R108 终态关联复验 | R107 由验收发起 `r107-temporal-linked-audit`，对 SHA-256 大小写误拒做只读复验，关联 Run `<RUN_OR_SESSION_ID_22>` COMPLETED。R108 一次性检测器自动派关联 Run `<RUN_OR_SESSION_ID_23>`，重开返回 `ALREADY_DISPATCHED` 与同 Run。原终态和产物指纹、修改时间保留。证据 `r108-temporal-auto-audit/{DETECTION.json,recheck.json,STATUS.json}`。检测器持续运行和通用自动派发待验。 |

明确记录原 task_id、原 Workflow/Run、冻结输入、修订差异和唯一关联任务。原 Run 仍运行时按原接续入口恢复，原生已终态时保留其终态，用关联纠正另取证。恢复所需等待、裁决、返工与复验纳入完整交付时间。只修受影响验收或缺步骤，核对已提交业务并保留唯一写入和旧回执。

## 原会话求援与独立 QA

- R114 派发时验证所有实际 GUI 阶段均已接过求援规则。关键写入无回执、同一动作再失败或反复开标签而无进度时，暂停写入并核原进程、订单、会话和原标签。Activity 取消时核完整 GUI 进程树。遇到阶段开始标记，按原检查点进入核账。向已登录 ChatGPT 的 `shared_browser` MCP 发一次带唯一标记的求援，读回超时继续查询原会话。MCP `### Result` 若包装 JSON 字符串，先解包再解析答复，并核任务及允许范围。
- R114 原 Run `FAILED`。R122 人工发起关联接续时，读回原 GPT 答复，Pi 原会话仅通过可见界面补 G12。数据库查得两单、原单五笔 CNY、相邻单零收款，原账本和已通过业务保留。自动求援接线与完整宿主 QA 另行验收。证据 `r114-temporal-louez/{R114-GPT-RULING.json,G12-RECOVERY.json,G12-INDEPENDENT-READBACK.json}`。
- `PI-V18-HELP-771D5662` 真实 Windows Open-Pi 同会话回归通过，一次原生提交、真实答复、单 Pi 会话、一次裁决写入、账本不变。证据 `pi-v18-help-771d5662/INDEPENDENT-RESULT.json`。Worker 取消与接管另验。
- `V18-HELP-MATRIX-60A0ACE0` 的正常、发送前缺 target 校验、发送后快照读回校验故障三案独立通过。逐案均一次发送、一个原 Pi 会话、一次裁决写入、账本不变。证据 `v18-help-matrix-60a0ace0/<case>/INDEPENDENT-RESULT.json`。故障由工具校验注入，实际断线另验。新请求先分配专用标签，故障后仅查询原标签。
- R144 的展示编号与 21 位内部订单 ID 对照按[直投长测复盘](temporal-native-submit.md#v112-r144-长测复盘与派工前复验)处理。冻结时记录字段来源、类型、示例、含义、关联键和读回方法，用正例、漏字段及错 ID 负例复验。复核真实 GUI、数据库两单、主单五笔及相邻零收款、独立还原和 QA。保留原 FAILED 与关联成果；缺完整证据记 PARTIAL。

## 预约与交付回执

- R95 两路均用增强 Pi 调用指定 GPT、通过实际 GUI 将两个目标预约各写一次并导出 CSV，两路原生均 FAILED。原任务、会话、账本、回执、导出和终态均保留。
- R97 若验收收到 xdev 包装结果，按同一个调用 ID 关联原生提供者、服务器、工具和参数，再交既有验收器。仅可选快照字段 `format`、`filenames` 允许原生省略。Conductor 对原日志只读复审为 16/16，原生 FAILED 保留。Excel 表名固定「预约明细」「交付摘要」。SHA-256 十六进制按大小写无关的值比较，逐格、行数及最终预约照常核验。
- R97 Temporal 原业务和文件校验通过，独立验收为 15/16。关闭任务标签后单独调用 `browser_tabs list`，与关闭前基线核对原标签索引与完整 URL。会话正常退出和 `native_normal_completion` 仅登记交卷。
- R101 使用真实 Windows 浏览器复验该门禁。遗漏关闭后列表为 `AWAITING_CORRECTION`，补一次只读列表后 PASS，原六个标签索引与 URL 一致。另复查 R97 时当前六个、历史五个，保留 `REVIEW_REQUIRED`，原账本和导出指纹一致。证据 `R101-LIVE-GATE.json`、`r97-temporal-booking/R101-READONLY-CORRECTION.json`。覆盖回执门禁及定点补查，正式调度器自动派 GPT、返修与独立复验另行签收。

## V124-1119 桌面直跑正常交付实测

2026-11-20 在 <Windows 测试主机>，经「Oh My Pi 增强 V3」接单的 B 路（增强 Pi＋Superpowers 桌面直跑）已签收**有宿主援助的 Louez 正常交付**。正式 GUI 经 G00–G12，主单租金收 200＋100 元，押金收 500、退 100＋400 元，相邻预约收款为零。两单五笔人民币流水、原押金凭据删除保护和隔离 SQL 备份还原均经独立验收。接单 21:40:07.023 至次日独立验收 00:28:17.077，正常轮 T_VALID 为 **168:10:054**，含共享桌面等待、模型断线和返工。

复用范围限上述业务与援助条件。三次模型连接中断均经宿主接续，原生无人值守接管、写后回执丢失及其他故障轮仍待独立验收。GPT 对 R2 有援助正常轮签发 PASS，Gemini 实际拒答，依规则 GPT 单签。原件在 `<历史工作区>`。核对 `receipt.json`（SHA-256 `<EVIDENCE_HASH_07>`）及 `<历史工作区>/B-NORMAL-INDEPENDENT-ACCEPTED.json`。需要具有故障接管能力的路线时，继续核对相应场景签收范围。
