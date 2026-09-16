# H3-P0 Failure Index — local experiment control

## AI_MODEL_CAPACITY_MUST_NOT_INTERRUPT_LOCAL_EXPERIMENT

- 触发：Codex/AI 会话出现 `Selected model is at capacity`、浏览器关闭、对话重连或工具响应中断；本机 H3 GPU 实验可能仍在执行。
- 本轮证据：1.0 GiB 候选期间出现模型容量事件。只读核对后，8194 已停止监听，3 份正式 run/QC、summary 和插桩 SHA 恢复证明完整；候选自然完成，无需重启。
- 禁止动作：仅凭 AI 会话错误终止 H3 PID、再次启动 8194、重跑已完成阶段、重做 V1/2.0 GiB。
- 恢复门禁：读取 `pid.json`、`heartbeat.json`、`iteration.json`、`state.json`、`last-good.json`、lock、8194 端口、server log 与本轮 summary/QC。只有 PID 已失效、8194 不再属于该实例、心跳超过期限、当前结果未完成，才允许恢复同一阶段。
- 控制器：`H3-P0-controller.py --status|--resume|--stop-safe`。本地独立进程保持单 GPU 实例；每轮完成立即 checkpoint。已完成阶段重复调用只读复用结果。
- 验收：对话断开时 GPU 作业继续；恢复后无双实例、无重复 prompt；`samplers.py` 前后 SHA 相同；KEEP/ROLLBACK 和远端事实源收口仍按正式命令包执行。

## PSUTIL_NOSUCHPROCESS_POSTRUN（收尾进程扫描竞态）

- 触发：服务进程在 `psutil.process_iter` 枚举后、读取 `cmdline` 前自然退出，抛出 `psutil.NoSuchProcess`。
- 本轮证据：V6 的 3 个正式样本、QC、分块报告与全部源码 SHA 恢复证明已完成；控制器收尾扫描碰到刚退出的 8194 Python PID，保留了锁。
- 处理：将该 PID 视为已退出，重新核对 8194、控制器与运行器 PID、完成文件、QC 和 SHA；若均完整，归档为 `COMPLETED_LOCK_RECOVERY（已完成锁恢复）`，从检查点恢复至 `IDLE（空闲）`。
- 禁止：因此异常重跑 GPU、重启 ComfyUI 或把已完成轮次误判为实验失败。
- 实现：进程枚举捕获 `NoSuchProcess`；异常退出保留锁；已完成锁和未完成失活锁分别接管并留审计记录。

## SOFTWARE_FRONTIER_DEPENDENCY_STARTUP_FAILURE（软件前沿依赖启动失败）

- 触发：隔离的 ComfyUI v0.36.0 首次启动时缺少 comfy_aimdo.malloc_graph，服务尚未接受 H3 prompt。
- 本轮证据：首次 V9 只有启动失败日志，没有正式 run；startup-failure-V9_SOFTWARE_036.json 保存错误与检查点状态。
- 处理：只在隔离的 software-frontier/python-overlay 安装兼容的 comfy-aimdo 0.5.3，验证导入；先核对旧控制器/运行器已退出、8194 无监听、samplers SHA 已恢复，再从 V9 检查点重试。
- 禁止：因软件前沿启动失败重跑 V1–V8、覆盖已完成结果，或修改原始 .venv 和网络代理。
- 验收：V9 重试的 3 条正式样本通过 QC；较 V3 慢，ROLLBACK（回滚）；隔离工作树干净，原始基准保持 V3。

## DIAGNOSTIC_PROFILE_IS_NOT_KEEP_EVIDENCE（诊断插桩不是保留裁决证据）

- 触发：CUDA 事件/算子剖析增加开销，诊断轮总时间与无插桩 V3 不完全可比。
- 处理：只用诊断数据定位内部块、驻留未命中和候选机制；正式 KEEP（保留）/ROLLBACK（回滚）必须用同合同、同 seed 的无诊断候选测量与 V3 比较。
- 验收：诊断轮标记 DIAGNOSTIC_ONLY（仅诊断）；逐文件保存修改前备份与 SHA256，结束后恢复并验证哈希相同；LAST_GOOD（最近保留版本）不因诊断改变。

## WINDOWS_ATOMIC_REPLACE（Windows 原子替换短暂拒绝）

- 证据等级：LOCAL_RAW_LOG（本机原始日志）。controller-launch.stderr.log 记录旧控制器以固定 pid.json.tmp 替换 pid.json 时出现 PermissionError / WinError 5。
- 修复：状态写入使用 PID+线程唯一临时文件名、os.replace 有界重试（最多 20 次，每次 0.1 秒）；保存完成才视作落盘。
- 验收限度：后续多轮正常通过，未见专门并发压力回归，不能声称绝对根治。拒绝时保留旧文件，不因写入错误启动第二个 runner。

## RUNNER_START_PID_WINDOW（启动到 PID 落盘窗口）

- 证据等级：IMPLEMENTED_PREVENTION（已实现的预防）。V5 旧 controller-command 尚无 launch_id；现控制器源码在 spawn 前保存 STARTING、launch_id、controller PID/起始时间、命令哈希、runner_pid=null，再启动并补 runner PID/起始时间。
- 恢复门禁：看到 STARTING 不可直接重新启动；先按 launch_id、命令行、进程启动时间、8194、证据文件寻找已启动 runner。
- 验收限度：本轮无此窗口实际造成重复 runner 的原始事故日志；这是一项防护改进。

## PREMATURE_LOCK_RELEASE（异常时过早释放锁）

- 证据等级：IMPLEMENTED_PREVENTION + LOCAL_RECOVERY（防护实施与本机接管）。异常退出保留 controller.lock；只有 owner/runner 都不存在、心跳失活、8194 不属旧实例、结果无继续进展时才可判 STALE_LOCK（失活锁）。
- 完成阶段例外：若 summary、三条 QC 和 SHA 恢复均完整，走 COMPLETED_LOCK_RECOVERY（已完成锁接管）；V6 的 lock-recovery-1789575692.json 与归档锁是实例。
- 验收限度：未发现过早释放曾真正启动双 H3 的原始日志；不能把防护动机写成已发生事故。

## NESTED_POWERSHELL_EXPANSION（嵌套 PowerShell 展开）

- 证据等级：USER_REPORTED（用户确认），本轮证据目录未保留原始 .CommandLine 报错日志。
- 触发：多层双引号使 $r、$_、.CommandLine、.seed 等被外层提前展开；这不是 H3/ComfyUI 故障。
- 处理：简单只读查询用 Get-Process 或按 PID 的 Get-CimInstance Win32_Process；复杂批处理写独立 UTF-8 .ps1，再显式用 PowerShell 7 -NoLogo -NoProfile -File 执行。
- 禁止：把 PID 12648 的 cpu-guardian.py 当作 H3、因 quoting 错误终止它或重建环境。

## TEMP_SCRIPT_NULL_BYTES（临时脚本空字节）

- 证据等级：EVIDENCE_GAP（指定证据范围未找到原始文件/traceback）。用户要求列入完整回归，但不能虚构发生时刻或影响轮次。
- 可复用处理：检查生成脚本真实字节与 UTF-8 解码，重新生成明确 UTF-8 文本；运行 Python py_compile 或 PowerShell 解析检查后再执行。若脚本生成错误，不要调试 H3 业务逻辑或重复 GPU。
- 新任务若找到原始日志，应追加证据链接与明确受影响阶段。

## V1_WHITE_FRAME_QC_GAP（最初近白视频误判）

- 证据等级：LOCAL_RUN_JSON（本机原始结果）。runs/V1/run-3-910101.json 的五帧均值约 251.9–254.3，缺 frame_ranges/std；旧 task_completed=true 只证明产物路径完成。
- 修复：V1_QC 用 910100/910102/910103 重新建立权威三样本；每帧检验有限、非黑、range≥8、std≥1.5，ffprobe/ffmpeg 验 32×32×5 和产物哈希。
- 禁止：把原 V1 summary-V1.json 当权威 V1；不得为补档再重跑 V1_QC。

## V8_FULL_LOAD_REQUEST_NOT_RESIDENCY_PROOF（完整装载请求不等于完整驻留）

- 证据等级：LOCAL_AB（本机三条同 seed A/B）。V8 QC 全过但总 P50 48.575 秒，比 V3 慢 10.533 秒；v8-mechanism-observation.json 的 loaded_completely_events=0。
- 裁决：ROLLBACK（回滚）这一请求。不能扩大成 VAE 驻留优化原则无效；新候选须证明真正驻留机制发生后再比较。

## EXTERNAL_BENCHMARK_TASK_MISMATCH（外部基准任务错配）

- 证据等级：EXTERNAL_SOURCE + LOCAL_TASK（外部项目与本机任务对照）。2080 Ti 同卡项目公开 T8/PDD 收益来自多步、124 帧任务；本轮只有 1 step、5 帧，无法跳过后续模型调用。
- 处理：先过滤硬件、模型、分辨率、帧数、步数和产物合同；外部加速比例只排候选优先级，绝不直接认定本机 KEEP。
