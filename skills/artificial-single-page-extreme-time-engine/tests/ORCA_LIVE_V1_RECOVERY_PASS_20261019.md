# Orca 真实终端宿主恢复与官方生命周期验收 PASS
DATE=2026-10-19
ROUTE=Windows V10 C
TASK=task_25b473e39f67
RUN=run_cdd2083bbe22
DISPATCH=ctx_10abf2e72c0e
COORDINATOR=term_6b9133e2-6fb3-4a6e-b3d0-ad51cb8ce899
WORKER=term_a0055da1-b5a6-4104-afc4-4e3ea080b003

## 根因及修复
隔离测试脚本将 server.stdout 追加保存，重试循环读到历史 orca_server_ready，误判新服务 READY；orca-runtime.json 指向已退服务 PID，后续 terminal create 报 runtime_unavailable。改为每次启动清空 stdout/stderr 并等待本次实际进程的 ready，恢复官方终端宿主。未修改 FlClash、系统代理、其他用户进程。

## 实际验收
真实 orcad、独立 repo/worktree、coordinator 与 worker 终端创建成功，官方 run-create/task-create/dispatch 成功。在 task-list CLI 正在运行时真实终止客户端进程（control_client_interrupted=true），之后只读 task-list/dispatch-show 核对原 run/task/dispatch/terminal 身份一致，不重新派发。worker 生成 OUTPUT.sha256，独立比对 README SHA256 一致；worker_done 经官方发送，后续再次查询官方任务及派发状态均为 completed。单独检查点 stage=DONE，mutations=1；未要求用户逐节点继续。
原始检查点和事件日志：C:/AI/Orca-Codex-Validation-20261014/live-state-v1-20261019/checkpoint.json 及 events.jsonl。

## 验收界限
本轮为官方 Orca 运行时 + 真实控制 CLI 客户端进程中断 + 文件处理真实业务，不是 Orca 后台 daemon 被杀/机器断网，也不是 Codex 长耗时模型业务。结论为 THIS_SCENARIO_E2E_PASS，不得扩大为任意网络/业务故障都能够自动恢复。测试结束仅退出本次自建 orcad 服务，不影响其他用户程序。
