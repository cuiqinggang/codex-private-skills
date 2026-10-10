# ENGINE29 G模式 E29-01~08｜GPT直接Windows v0.3.1组件级现实验收
DATE=2026-10-10
MODE=G
OWNER=GPT
BRIDGE=Desktop Commander Remote v0.3.1
DEVICE=DESKTOP-4A1EGTM
DEVICE_ID=f6990966-5870-484b-bf79-409bc6fb963e
WORK_DIR=C:\Users\A\Documents\Codex\ENGINE29_G_REAL_20261010
SCRIPT=run-g29.ps1
RAW_RESULT=result.json
STATUS=COMPONENT_LEVEL_PASS_WITH_REPAIR
FULL_G_BROWSER_EXECUTION=NOT_TESTED
FULL_G_C_H_SAME_CONTRACT=NOT_TESTED
PUBLIC_ENGINE29_ACTIVE=NO

## 真实调用记录
- 使用GPT原生DCR成功创建独立目录并写入PowerShell测试脚本；直接调用start_process运行，PID=45036，退出码0，进程总runtime=19.72秒（含下表所有测试与合成并发批次），未访问受保护GPT聊天。
- E29-01：真实创建/写入/回读本机文件，127.9ms，PASS（组件范围）。
- E29-02：真实将临时Freeze文件原子移动为freeze.json并读回，408ms，PASS（组件范围）；失败保存阻止接管仅逻辑测试，未真正故障注入跨页。
- E29-03：唯一Owner/冲突检测规则，37.4ms，PASS（逻辑范围），无实际GPT标签页。
- E29-04：三级权限断言，19.5ms，PASS（逻辑范围），无真实九Agent协同。
- E29-05：本机PowerShell区间合并实现，3个回归输入有效，116.4ms，PASS；不是GPT/Codex同合同竞速。
- E29-06：原先尝试SHA256.HashData报错（Windows PowerShell兼容性），171.5ms FAIL；主动改为成熟.NET SHA256.Create().ComputeHash重验，DCR PID=12464，617ms，独立比较系统Get-FileHash与ComputeHash结果完全相同，REPAIR_PASS=True。原始哈希=01A522ED657401A2B829B9E1865E25CA4E95403E18984F155A32378DA6CDB90E。不是Codex独立审核GPT浏览器动作。
- E29-07：注入一次逻辑瞬态失败、第二次成功，2.7ms，PASS（模拟范围），未实际注入网络/标签故障。
- E29-08：Windows本机PowerShell Start-Job 8个合成独立250ms延时作业，各并行度1/3/5/8均8/8结果返回，所有32/32实际作业有效。只是一轮非随机次序、不同调度波数的本机工具层负载，不能代表GPT多页面T_VALID。

## E29-08并行度现实观测（仅本机合成作业）
| concurrency | batch wall ms | valid |
|---|---:|---:|
| 1 | 6778.6 | 8/8 |
| 3 | 6861.4 | 8/8 |
| 5 | 2666.2 | 8/8 |
| 8 | 1827.1 | 8/8 |
本轮8路测得最快，但无重复与次序平衡，不提供成熟并行度决策。

## 有效性与缺口
组件层8项均有真实运行或实际逻辑断言；E29-06确有一次失败并被GPT通过现成API修复。不能把8/8组件测试写成8/8业务现实验收：GPT专用浏览器单页/多页真实发送、跨页面Freeze接管、双写冲突、9Agent三级任务、独立Codex审计及G/C/H同合同完整有效时间均未实测。VIRTUAL_MATURE=NO，FINAL_VALID=NO，T_VALID_REAL=UNKNOWN。保留ENGINE28、A29、B33及受保护聊天边界。

## 故障恢复示范
E29-06原命令失败→具体定位HashData不可用→寻找成熟SHA256.Create/ComputeHash等效API→GPT原生DCR现实重验PASS，不因局部失败停任务，亦不绕过权限策略。
