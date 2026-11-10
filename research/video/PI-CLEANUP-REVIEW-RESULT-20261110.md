# Pi C盘清理分析复核与执行结果

日期：2026-11-10。依据：用户上传Pi分析、本机实际清单与SAFE-CLEAN-V1.1.ps1、进程/共享引用、本轮官方缓存命令回执。

## 结论
Pi清点可作线索，但删除清单和脚本不能直接整批执行。已实际执行确认可再生成的缓存清理，未删除171项目或114工作区。

## 本轮实际结果
| 操作 | 实际结果 |
|---|---|
| Python pip cache purge | 成功，3314文件、160目录，工具报告3793.1MB |
| npm cache clean --force | 成功，退出0 |
| pnpm store prune | 成功，3940文件、13包及缓存元数据 |
| uv cache prune | 180秒超时，未认证完成，不按Pi预估23.99GB计入成果 |

C盘本轮开始可用314114134016字节，结束325416296448字节，净增加11302162432字节（10.526GiB），结束可用约303.07GiB。其他任务同时写入，不能严格将净值分摊到每条命令；命令报告的逻辑删除字节也不等于分配空间。没有把之前视频清理/迁移的收益重复算入本轮。

## 拦截的误删项
| Pi判断 | 实际证据与处置 |
|---|---|
| SpeakMore-Windows-Test为历史无引用 | Electron及Python多个实例仍运行；保留 |
| LTMVH-Recovery为历史 | PowerShell当前cwd/命令引用；保留 |
| Polsia-V5-Parallel-20261012为历史 | Python监控服务仍运行；保留 |
| StartupQuiet-20261024为历史 | 多个cmd进程引用；保留 |
| ltmvh-v03-test为历史 | Node进程仍运行；保留 |
| Star7-Manual无引用可整删 | 当前H3配套配置引用其INT4编码器/VAE；保留所需资产 |
| Aaki整包无用 | 当前Wan model-paths.yaml明确共享其UMT5；不能整删 |

当前运行并非保留的唯一标准；日期旧、服务没开、文件可重新下载，也均不足以证明无用。Pi声称历史源码已合并Github/DSH，没有提供每目录的备份提交和内容校验，不能据此删除唯一源码、工作流或经验。

## 脚本问题
- PurgeCaches分支不受Apply限制：dry-run也可能真正清缓存。
- uv的“cache clean”和npm的“cache clean --force”被拼成一个参数传递，CLI可能不接受；程序非零退出也可能仍打印ok。
- 只检查目标目录本身重解析点，再递归删除，缺少对子目录junction/符号链接及逐文件身份变化的防护。
- 8196字节自测只能证明测试夹具删除成功，不能证明业务清单安全。
- Temp并非每项都可直接删除；浏览器Profile、启动/恢复工具、模型缓存必须检查活动引用。
- Docker prune -a --volumes可能破坏保留业务数据；本轮未执行prune、关闭Docker/WSL或动VHDX。
- Pi所谓26.79/61.36GB两套数字含junction重复计量，不能相加；MiniMax-H3逻辑/实占差不能未经核验一概归为稀疏文件。

## 保留与待复核
保留当前视频/共享环境、代理、系统文件、浏览器档案、Docker业务数据、知识库、原素材及错误证据。LM Studio/HF模型不因端口未开就删除。171项目与114工作区仅保留为待复核候选，没有整批清掉。已废弃且有实证的S2V/W4A8/NVFP4/VEDA及旧分片、重复VAE已在此前视频清理中删除，详见VIDEO-STORAGE-CURRENT，不能重复计算。

## 可用性与证据
视频环境Torch2.9.1+cu130、Requests、WebSocket导入成功；已核查SpeakMore、Polsia及LTMVH进程仍在。此为基础检查，不是完整GUI验收。
本机回执：K:/Video-Storage-Audit-20261110/pi-review-cache-result.json；逐进程冲突pi-manifest-active-conflicts.json；复核决定pi-review-decisions.json。Pi包内新增GPT-REVIEW-DECISIONS.json，原删除脚本未被运行。前期空间98→292GiB主要来自本线程实际清理与历史迁移，非Pi会话删除、非来源未知。

完整清理与75%目标尚未认证；本轮只报告实际完成的动作。
