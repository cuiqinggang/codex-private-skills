# Orca＋Codex 实测｜阶段报告 V2
TASK_ID=ORCA_CODEX_VALUE_VALIDATION_20261014
AUTHOR=GPT_CEO_DIRECT_READBACK_AND_OFFLINE_ANALYSIS
METHOD_REF=SANRENXING_V2_C002@4c48e249ca9c18ecde014d8b2e43f753a1f13139
PREVIOUS_REPORT=CEO_STAGE_REPORT_V1.md@376530b0a665db2b7af490ef8bcd13510f73a4b8
FINAL_VALID=NO
ORCA_FORMAL_BUSINESS_ROUNDS=0_OF_10
AB_PAIRED_BUSINESS_ROUNDS=0_OF_10
NET_TIME_SAVINGS=UNKNOWN

## 1. 本次实际完成
当前自建MCP读取本任务四份文件返回JSON-RPC 32600 Session terminated；未重发业务或假装在线。切换既有GitHub self-hosted Windows Runner，仅做本任务文件只读取证。

READBACK R1：创建一次性、限本文件push触发的原生工作流，不修改旧FULL生产流程、不使用第三方Remote额度。Run38567913904/job115865248409，实际取回N001报告、回执、输入清单及已完成恢复回执。最后对活跃SERVER_STDOUT.log调用Get-FileHash遇到sharing violation，导致作业失败。此为新取证脚本缺陷，不是Orca业务失败，也不是GitHub Runner离线。

READBACK R2：对同一脚本做最小修复，用.NET FileStream的FileShare.ReadWrite|Delete读取只读快照，逐文件隔离错误、保留错误，不解锁/关闭日志写进程。Run38568250674/job115866376804，真实conclusion=success，错误列表为空。快照包含读取文本的SHA256、时间、大小和范围标记，经GitHub原生Contents接口保存为：
`evidence/READBACK_R2_RUN_38568250674.json`
Git blob=673f98ea01d9667cc2e9304b0a20e603d6bdcdb8；本页已独立从共同工作区回读。

实际Runner=DESKTOP-4A1EGTM-etal，执行身份NT AUTHORITY\NETWORK SERVICE。作业started_at13:00:38Z、completed_at13:01:22Z，UTC作业窗口44秒；本地只读采集Stopwatch=8688.9111ms。两者范围不同，均不是模型任务T_VALID。R2只证明本任务只读取证＋快照回传，不代表原FULL的upload-artifact网络故障已修复。

## 2. 对账发现：不要重复已经做完的修复
N001_REPORT.md和N001_RECEIPT.json已于12:51:40Z生成，分别SHA256：
- 3364bdf1adb73b355fbb58f51d36c4d2b38dcf3e5fcea7d20ef3c86e41c97332
- a4a3517109afb9d24d80b51058c08b9299472a3a3b0d11ea69557a1a063ec4db
它们给出的13/14是原始GOOD_003超时工作树；另一个GOOD_003_CEO_RECOVERY恢复副本已经完成14/14检查、21/21源码回归及SHA回读。本次又实际读到恢复回执，SHA256=79bdb794221592e59968ce858037e3a359d77e8b62203b0209339425b65deffe。不能因旧报告T03未完成而重新修复已完成恢复副本，也不能把恢复成果改称纯Codex无故障通过。

CEO_N001_RECOVERY_COMPLETE.md确实不存在，所以上页502后的提示不能假定送达。N001启动回执仍停在STARTING_NOT_ACCEPTED。网络服务身份下按CommandLine过滤得到空进程表，只能证明没有匹配到可见命令行；不证明A用户所有任务已退出，不能据此盲重启或重发。

N001原候选freeze/FREEZE_CANDIDATE.json SHA=0cea978621027967198244e8150c749f3d1a045fd3aea0fee998da34ae938af4。它仍缺具体B模型派发、权限传递等验证，不批准为正式F002/N002，也不修改旧冻结内容。

## 3. 当前真实计时及局限
| 数据 | 实测 | 不能扩张的范围 |
|---|---:|---|
| 原Codex超时尝试 | 1205983.9134ms，约20分5.984秒 | accepted=false，不是成功交付 |
| 原输入至恢复副本SHA回读 | 2219842.5331ms，约36分59.843秒 | 含超时和中间等待；不含更早准备、最终回执写入 |
| GPT局部修复＋QA＋回读 | 1914.9874ms | 不含编写、诊断与交接；不能据此宣称比20分钟快数百倍 |
| 下载摘要验签 | 62946.0231ms | 局部准备 |
| 核心解包 | 55324.0788ms | 不含后续枚举/哈希；两项相加不等于完整部署 |

2219842.5331ms已经包含原超时，不再额外加一次1205983.9134ms。完整T_VALID、Orca配对耗时、所有一次性成本、真实账单均不齐全，节时率/现金收益/回本次数保留UNKNOWN。
资源样本543份，实际间隔median1578.89985ms、样本P955689.4479ms、max17660.9295ms，不能把目标1秒写成严格1秒采样。工作集峰值2303496192字节，最少系统空闲9349808128字节，仅为观测样本，不是稳定容量认证。N001报告记录input tokens2017961、cached1927168、output16260；来源为会话用量而非账单，不换算未知价格。

## 4. 独立完成的离线数据判定
新增`analysis/evaluate_value.py`及18项`test_evaluate_value.py`，在ChatGPT工作容器Python3.13.5真实运行，全18项通过。上传源码的Git blob与实跑字节一致：
- evaluate_value.py：9f7c87ccd1755e2c3f1c89f6ec93c0d560a4306d
- test_evaluate_value.py：1f98e57051f36a32091d89413c98c4217b4607d1
这只是本任务离线结构/算术检查，不是通用调度器、不接触运行环境，也不替代源回执真实性核验。
已验证：不能把9组凑10组、健康检查冒充业务、局部计时冒充全程、重复回执、混合版本、不同模型/质量、NaN耗时、UNKNOWN成本、失败后未重置计数、重复扣成本等判成验收通过。合成数据只位于unit fixture，明确不是真实运行。
真实阶段数据输入`analysis/observed_stage_input.json`，结论`analysis/RESULT_V1.json`：完整配对0、十轮门未通过、净节时null、不推荐据此替换现役系统。18项逻辑测试不计入用户10轮Orca/Codex业务。
Windows全程计时脚本本身仍待合法执行验证，不能把判定器通过冒称计时系统已修复。

## 5. 当前阻塞及停止边界
准备提交Orca运行时预检工作流（本任务CLI status/help＋恢复副本QA，无模型派发）时，GitHub.create_file被OpenAI平台安全检查明确屏蔽。该预检未创建/未执行，不能计作N002。没有通过改写编码、其它工具、其它账户或另一条通道重发这一被拒操作；仅继续不受影响的资料读取、离线算术检查和归档。
下一步运行时动作需先通过平台允许的执行/审批路径，不以本报告或宽泛继续授权绕过本次明确拒绝。自建MCP当前Session terminated，不能自动假设重新可用。原生Runner服务身份与A用户登录身份不同，未证明模型登录或Orca IPC可在此身份使用，不复制凭据、不修改ACL或提权。

## 6. 接续位置
保留恢复GOOD实物、R1失败、R2完整快照和旧原生失败；先从此报告继续，不重复已完成T03恢复或重新下载Orca。待合法执行条件成立，核对用户会话真实进程归属，补B派发/配置/完整计时及授权边界，整套Freeze后一次N002；通过后再按用户原要求连续10轮＋真实同合同A/B比较，所有失败和部署成本入账。当前1000登记/自动推进/同时活跃能力均未认证。
本次没有启动新模型、没有重启电脑/WSL/Orca/执行桥、没有修改代理/现役业务/全局模型配置或安全权限。没有新启后台自动执行机制。
