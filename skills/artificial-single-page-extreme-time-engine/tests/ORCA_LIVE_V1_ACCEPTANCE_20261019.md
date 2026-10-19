# V1 官方 Orca 在线生命周期现实验收 | 2026-10-19

STATUS: OFFICIAL_ORCA_LIFECYCLE_PASS
BRIDGE: V10 C
WORKSPACE: C:/AI/Orca-Codex-Validation-20261014/lifecycle-v1-live-20261019-1945
RUN: run_98190e9796fb
TASK: task_0ab7edb72388
DISPATCH: ctx_77a78833f1f2
MESSAGE: msg_5de2f23d86e0

本次实际启动官方 Orca 本地隔离运行实例，注册工作树，创建 run/task、官方 coordinator/worker 终端并派发任务。业务读取原已验收的三份 T03 文件，计算哈希和大小，生成 artifact-manifest.json；独立 QA=3/3。

worker 官方 CLI dispatch-show 被主动设置极短 0.001 秒阈值，实际发生 subprocess.TimeoutExpired，control-fault.json 记录 REAL_CLI_READ_TIMEOUT。随后官方 CLI 只读查询恢复原 task、dispatch、terminal handle、pane；control-recovered.json same_dispatch=true，未重新派发或重发未知控制变更。业务子进程另有一次受控超时恢复；worker_done 官方回执和相同 retry-request 再次查询返回同一 messageId；task-list 和 dispatch-show 状态 completed；终端关闭，remaining_owned=[]。

完整本地有效时间 79031.2107 ms（79.031 秒），final result.json passed=true，local-acceptance.json accepted=true。执行期间无需用户逐节点人工指挥。

限制：这是官方 CLI 真实请求超时，但超时由人为设置极短阈值触发，不是实际网络断开或 Orca 服务重启。业务是文件哈希交付，不是 Codex 模型执行；不能推断模型中断恢复或断网重连已经通过。未验证真正 worker_done 发送时 UNKNOWN 状态的远端持久化去重。后续 GitHub 归档时间不在79.031秒内。

原始证据均位于上述 WORKSPACE，包括 control-fault.json、control-recovered.json、worker-done.json、coordinator-done.json、artifact-manifest.json、result.json、local-acceptance.json。代码保留于 tests/prepare_orca_live_v1.py 和 tests/orca_live_lifecycle_v1.py。原有历史 GOOD 未覆盖。
