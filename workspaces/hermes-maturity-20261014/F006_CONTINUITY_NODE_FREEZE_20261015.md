# Hermes F006｜任务级 checkpoint→handoff→resume 最小现实节点冻结
日期：2026-10-15；任务：HERMES-ECO-20261014；NODE=H-ECO-03-CONTINUITY-F006
状态：VIRTUAL_MATURE_FROZEN（未运行时）；方法：《三人行》V2+Windows执行桥V6 C优先+Hermes专用v2.0+hermes-long-task-continuity现有技能。与F005 Repair被阻断的命令测试无依赖。
固定使用原有程序 C:/Users/A/.hermes/skills/hermes-long-task-continuity/scripts/{new-task.py,save-checkpoint.py,write-handoff.py,resume-task.py,close-task.py} 及原有正式根 C:/Users/A/.hermes/runtime/long-task-continuity；不造恢复引擎、不碰Session DB、不使用 --root 切换到非正式数据根。
新任务唯一ID HERMES-ECO-CONTINUITY-F006-20261015，一共两步，均对应本项目已完成且可独立追踪的现实成果：
  1. 既有F004 PowerShell序列化修复候选离线10/10，以及GitHub冻结；
  2. 本页 Hermès 正式CLI 实时读取隐藏校验值成功。
先 task create→checkpoint 1 DONE→handoff→由新Python进程resume核实 next_step=2及prev_hash→checkpoint 2 DONE→close PASS→只读核实 closeout、哈希链和项目数据目录。拒绝重复DONE或跳步，保留错误和副作用。
验收边界：本节点只证明任务连续性脚本与状态持久化原生能力的当前真实复用，不等于Hermes模型对话跨会话恢复、Gateway重启或整个生态站合格。任一命令不返回真实证据则冻结FAIL并停止，不跑回退通道绕开权限；不更改代理、密钥或其他任务。
