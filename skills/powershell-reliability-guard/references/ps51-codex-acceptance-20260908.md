# PowerShell 5.1 × Codex CLI：2026-09-08 用户回传案例

## 来源和边界

本条根据用户粘贴的本机执行报告整理。编写端未取得Windows原始8个脚本或独立读取本机报告，不能称为原技能包逐字上传、独立实测或全部技能兼容认证。原技能名为 codex-cli-windows-sandbox-fix；本次将可复用的命令编写规则并入 powershell-reliability-guard，避免另造重复守卫。

## 回传验收

- Codex 0.153.4；PS7基线7.6.5通过，退出码0。
- PS51_LAUNCHER=PASS；从5.1启动Codex，内部默认Shell仍是7.6.5。
- PS51_EXPLICIT_EXECUTION=PASS；实际powershell.exe返回5.1.19041.6456。
- 工作目录 C:\Users\A\Documents\Codex；ExecutionPolicy据回传为RemoteSigned，未更改。
- 基本输出、中文/空格/方括号路径、UTF-8、JSON、原生参数与退出码、预期失败7、稳定性3/3均最终通过。
- EXISTING_CONFIG_CHANGED=NO；耗时约12分钟。PASS仅覆盖以上测试。

## 关键教训

初轮T2/T3曾误判通过：无BOM UTF-8脚本在该5.1环境按ANSI/GBK读取，创建了乱码目录，同一错误字符串往返仍相等。T4语法错误暴露问题。含中文脚本加UTF-8 BOM后，核对磁盘上的正确中文目录、内容及预期长度，重新通过。

先前还遇到方括号目录创建失败，后改用.NET目录创建；缺少原始脚本，不把该条概括成所有New-Item在5.1均失败。通过Bash传递PowerShell时$_被提前展开，说明应避免跨Shell字符串拼接。

## 最小验收方法

1. 冻结目标Shell与窄项目目录，确认实际执行版本。
2. 静态检查5.1语法、脚本BOM、LiteralPath适用性及跨Shell引用。
3. 在独立测试目录验证Unicode实物、JSON、参数及原生退出码；故意非零退出应识别为预期失败。
4. 一次一个调用；稳定性任务可做3次，普通小改动无需重复整套验收。
5. 分别报告启动入口、实际Shell、退出码、内容核验和未测范围。区分进程完成与模型回复超时。
6. 修正仅限已证实的脚本问题；不要自动改全局配置或沙箱。

## 本机资料索引（路径由用户提供，非本环境可访问文件）

- 验收报告：C:\Users\A\Documents\Codex\outputs\PS51-ACCEPTANCE-20260908-222311\SUMMARY.md
- 原Reasonix技能：C:\Users\A\AppData\Roaming\reasonix\global-workspace\.reasonix\skills\codex-cli-windows-sandbox-fix\SKILL.md
- 知识库副本：C:\AI\knowledge-brain\10_STABLE_MEMORY\reasonix\codex-cli-windows-sandbox-fix\SKILL.md
- 索引：C:\AI\knowledge-brain\10_STABLE_MEMORY\reasonix\SKILL_INDEX.md
- 修复报告：C:\Users\A\AppData\Roaming\reasonix\global-workspace\CODEX-FIX-REPORT-20260908.md
- 长期记忆键：project/ps51-codex-compat-acceptance

## 与此前CLI修复的关系

用户报告同版本npm重装本身未解决故障；另报告elevated沙箱处理大量条目超时及主目录1344故障，随后配置调整与窄目录启动通过。此处仅保留案例背景，不独立确认因果或上游issue，不提供自动降低沙箱保护的流程。托管审批拒绝与本机运行故障须分开处理。
