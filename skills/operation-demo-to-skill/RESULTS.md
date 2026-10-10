# 《操作演示自动技能化》第1版｜Windows 实际验收记录
日期：2026-10-10
模式：SYNTHETIC / PILOT；并非真实用户桌面演示的生产认证

## 能力
- 开源录制器固定提交：5e6b52ecb097df67eb1c94e83abfd5f39c663ef5；Windows 录制核心、浏览器录制、摘要器已实测。
- Codex 编写了 Windows GBK/UTF-8、POSIX rm 清理兼容修复和隔离自检入口。
- 由 Codex 从合成文件操作记录提炼出可执行 safe-file-demo/SKILL.md + replay.py。
- 已安装：C:\Users\A\.codex\skills\operation-demo-to-skill\SKILL.md；quick_validate.py 返回 Skill is valid!

## 独立现实结果（授权 Windows 主机，无敏感数据）
| 情形 | 现实耗时 | 结果 | 本机证据 |
| --- | ---: | --- | --- |
| 旧桌面自检基线 | 2536.417 ms | FAIL exit1 | evaluation-v1/evidence/baseline-rm-dcr/result.json |
| 浏览器模拟记录+总结 | 16091.278 ms | PASS | evaluation-v1/evidence/browser-dcr/result.json |
| 桌面合成记录+总结 | 2697.495 ms | PASS | evaluation-v1/evidence/desktop-dcr/result.json |
| 文件示范合成记录+总结 | 2321.818 ms | PASS | evaluation-v1/evidence/file-source-dcr/result.json |
| 文件技能实际执行 | 未纳入相同完整时间边界 | PASS | evaluation-v1/evidence/file-demo-r1/replay-dcr/manifest.json |
| 对已有目录再次执行 | 未纳入相同完整时间边界 | PASS（正确拒绝覆盖） | 控制台错误 Output already exists |

文件技能实际创建 notes/演示.txt 和 archive/演示副本.txt，均38字节、SHA-256=46b4f0b5ddbf1e9ce29a1cb392d8abafaeeb7f58213a1901dae7b601dd97f5cb。

## 剩余门禁
- 没有让真人操作一次并回放到最终相同业务目标，HUMAN_DEMO_VERIFIED=NO。
- GPT API 自动派发没有接通，GPT 在当前对话负责理解，Codex 在 Windows 负责执行。此版是有用 PILOT，不是无人值守生产认证。
- 完整任务同边界 T_BASE_REAL/T_VIRTUAL_BEST/T_VALID_REAL 尚无可靠数据，VIRTUAL_MATURE=NO，FINAL_VALID=NO，不声称极限最优。
- 用户登录浏览器、密码/令牌、网络代理、FlClash 未作为测试对象；录制原始事件和截图保留本机，不得上传 GitHub。

## 下一动作
在用户明确准备好的无敏感真实演示中，录制一次 → GPT/Codex 理解与生成正式任务技能 → 正反例验收 → 同边界实际时间校准 → 按网络正式引擎完成成熟/冻结/Reality。