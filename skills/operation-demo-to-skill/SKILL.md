---
name: operation-demo-to-skill
description: 将浏览器或 Windows 桌面操作演示转为可发现、可验证的 Codex 技能。用户说“看我操作”“操作演示自动技能化”“录制后做成技能”或提供操作记录并要求技能化时使用，复用现有 record-and-replay，不创建新录制器。
metadata:
  version: "1.0.0"
  display_name: "《操作演示自动技能化》第1版"
---

# 《操作演示自动技能化》第1版

本技能编排现有录制、意图理解和 Codex 技能创建及验收。正式录制依赖 `C:\Users\A\.codex\skills\record-and-replay\SKILL.md`（Junction 正式源：`C:\AI\record-and-replay-evaluation`）。GPT 任务理解由当前对话或用户提供的 GPT 分析完成；本版没有自动 GPT API、自动跨页面派发或端到端无人闭环，不能声称已接通。

## REUSE_GATE 与执行顺序

1. **现实基线**：确认用户定位标签、授权目标、输入记录是否为 completed/非 discarded、录制模式、用户动作是否足够、输出路径和验收标准。先读现有 record-and-replay SKILL、相关总结器；复杂复用按 Knowledge Brain 的 INDEX → ROUTING_MAP → skills-index → Top-K C 盘入口。缺失正式 C 源返回 BLOCKED_C_SOURCE_MISSING。
2. **REUSE_GATE**：按“录制 → 理解 → 技能构建 → 验收”列出可用成熟组件、真实缺口和最小补丁。优先现有 CLI/API/语义能力实现结果；不重建通用录制器、状态机、调度器。母方法参考 `C:\Users\A\.codex\skills\first-principles-physical-limit-convergence\SKILL.md`；不修改冻结运行时、不拿另一任务的四 ID 签证。需要母引擎完整认证时必须由主控绑定真实会话并实际调用其正式入口，本技能的本地 PASS 不等于 FINAL_VALID。
3. **虚拟成熟**：读取实际事件及必要 trace/截图，识别意图、参数、前置条件、停止条件和可观察结果。记录不了人类操作或只有模拟事件时写 SYNTHETIC / HUMAN_DEMO_UNVERIFIED；证据薄弱时只报告缺口，不猜流程。
4. **Freeze**：保存技能候选、所用证据、参数和验收条件的 SHA256/版本；完成静态检查后固定方案。
5. **一次最终 Reality**：按正式使用方式在授权隔离目录运行冻结候选，核验输出、退出码和墙钟时间。失败保留原证据，回到虚拟成熟形成新版本再测；不临场更改冻结文件、不覆写失败记录。耗时注明测量边界，不把本地测试耗时代替完整 T_VALID。

## 录制与安全

浏览器任务优先使用现有浏览器录制器及语义选择器；桌面任务用现有 desktop-record.mjs。按原技能进行一次启动确认和 STOP 完结确认。人类演示期间启动后结束本轮回复，不忙轮询。不要自动复用登录 profile；默认浏览器入口会用 `~/.agents/recordings/.browser-profile`，使用前明确用户授权和数据边界，严格无敏感验收只运行 `--self-test` 的独立临时 profile。

浏览器 JSONL 脱敏是启发式，trace 不脱敏；桌面真实记录完全不脱敏。只在本地读取授权证据，技能和报告不复制密码、OTP、cookie、token 或账户信息。严格无敏感测试使用本版桌面自检的合成输入、假窗口和合成 JPEG；它不证明真实桌面驱动、真实截图或人类演示。

Windows 命令（已装依赖时不要重复 setup）：

```powershell
Set-Location 'C:\AI\record-and-replay-evaluation'
node scripts/recorder.mjs --self-test --name safe-browser --out '<全新证据目录>'
node scripts/summarize.mjs '<该目录>'
node scripts/desktop-selftest.mjs --out '<另一全新证据目录>'
.\.venv-desktop\Scripts\python.exe -B -X utf8 scripts/desktop-summarize.py '<该目录>'
```

自检用 `shutil.rmtree` 只清理自身临时目录；`--out` 保留证据且拒绝已有目录。启动器为子进程设置 PYTHONUTF8=1，总结器使用 UTF-8 输出；不改全局环境。sandbox/权限故障照实记录，通过现有审批执行，禁止修改策略或绕过权限。

## 从记录到技能

实际阅读事件和总结后，由当前 GPT/Codex 对话形成目的、参数、步骤、证据映射和验收。加载现有 `skill-creator`，生成真实 `SKILL.md` 文件夹，保存到用户指定技能目录；需要显示中文名时使用 agents/openai.yaml。脚本只用于确需确定性的任务动作，必须直接验证，不复制像素操作。浏览器定位优先 testId/role/label/text；Windows 桌面没有 macOS AX 的保证，证据不足时改用等价 CLI 或注明缺口。

验证：`python -B -X utf8 C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py '<技能目录>'`，随后检查任务的实际输出。安装后回读文件并对比冻结哈希。可参考 [文件样例](examples/safe-file-demo/SKILL.md) 与 [提取说明](references/LESSONS.md)。

仅当目标是**原生、没有源码的 PE**，且现有语义/CLI 路径不足时，读取 [REA 按需路由](skills/rea-on-demand-router/SKILL.md)。脚本、开源仓库、浏览器任务、本版三个例子不调用 REA。

## 复用与失败入口

- 触发词：看我操作、录制后做技能、操作演示自动技能化、演示转技能。
- 最近使用：`C:\AI\operation-demo-to-skill-v1\USAGE.jsonl`；追加实际记录、证据路径和结果，不补造历史。
- 失败复盘：`C:\AI\operation-demo-to-skill-v1\RESULTS.md` 中基线/限制及各例子的 stderr/result.json；stdout PASS 后仍需确认 exit 0。
- 验收证据：同目录 `acceptance.html`、`evidence/`；模拟例子与人类证据分开报告。
- 下次复用：显式调用 `$operation-demo-to-skill`，读取本入口、确认 C 盘依赖和当次授权，再按 REUSE_GATE 开始。默认自动发现可用，当前已打开会话是否热重载未验证。
- 边界：本地可逆工程连续完成；发布、真实账户、付费、系统/网络变更另需相应授权。仅允许主控在验收、去敏和用户授权后向共同私有仓库发布技能正文，原始记录禁止上传。H 不写、K 不访问、不自动备份；ROI 门禁仍暂停。

[executed on device: DESKTOP-4A1EGTM (f6990966-5870-484b-bf79-409bc6fb963e)]