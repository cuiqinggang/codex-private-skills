# 宿主已执行更新：2026-11-11（最新优先）

65.6GB三份清单已在宿主拆解为289项并核运行、计划任务、静态引用及具体效用。已执行5批精确清理：126615文件、逻辑11.8045GiB；C可用316.647GiB。完整结果见[HOST-65GB-AUDIT-20261111.md](HOST-65GB-AUDIT-20261111.md)，权威回执K:/Video-Storage-Audit-20261110/pi-v12-65gb-summary-20261111.json。

Node/npm/Codex/Blender版本、共享Torch导入、3个模型链接/51路径通过。VoxCPM2有本机实际语音成果，Polsia/DeepSeek仍被调用，保留；源码、Git、唯一资料保留。旧MSIX阻塞源仍在且不计成果，不自动重试。Etcher只观察到GUI启动，完整GUI和Wan8秒未通过。以下旧“下一步在宿主运行整批Apply/uv清理”的待执行表述已经被本轮实际执行与回执覆盖，不再交给用户整批运行，也不重复清理同路径。

剩余仅按新证据差量处理；75%和全工具GUI不报通过。Wan没有新资源Freeze，不恢复旧intent/GPU。原V1.2规则/历史证据保留如下。

---

# 进度（C 盘清理 V1.2）

最后更新：2026-11-10 23:45（北京时间）。

## 一句话状态

宿主复核把我的"整批删"否了（误删 7 条 + 脚本 2 个缺陷）。V1.2 已按复核重做：**运行态门控 + dry-run 严格只读 +
大块需人工批准**，被拦的 7 条进 denylist。清单仍在，但**不再提供"整批一键删"**。

## 现状

| 项 | 值 |
|---|---|
| C: 可用 / 已用 | 302.2 GB / 629.2 GB |
| 宿主本轮已清 | pip 3.79 GB（3,314 文件 + 160 目录）、npm exit 0、pnpm 3,940 文件/13 包；**净 +10.53 GiB**；uv 超时未认证 |
| 本包可自动回收（门控通过后） | 01 0.33 + 02 26.16 + 03 39.06 ≈ **65.6 GB** |
| 需人工批准 | 05 清单 **58.41 GB** |
| 另需单独处理 | uv 缓存 ~24 GB；Docker vhdx 只读盘查、需单独审批；回收站本包不再处理 |

## 下一步

```powershell
cd "C:\Users\A\Documents\DSH-Workspace\pi-capability-enhancement-20261028\workspace\C盘清理技能包"
# 1) 只读预演（沙箱里 02/03 全部 blocked-unverified 属正确行为）
powershell -NoProfile -ExecutionPolicy Bypass -File .\bin\SAFE-CLEAN-V1.2.ps1 -Manifest .\manifests\01-scratch.csv
# 2) 在正常 PowerShell 里执行（有 Win32_Process 权限，L2 才可用）
powershell -NoProfile -ExecutionPolicy Bypass -File .\bin\SAFE-CLEAN-V1.2.ps1 -Manifest .\manifests\01-scratch.csv -Apply -PurgeCaches
powershell -NoProfile -ExecutionPolicy Bypass -File .\bin\SAFE-CLEAN-V1.2.ps1 -Manifest .\manifests\02-ai-old-projects.csv -Apply
powershell -NoProfile -ExecutionPolicy Bypass -File .\bin\SAFE-CLEAN-V1.2.ps1 -Manifest .\manifests\03-codex-dailies.csv -Apply
# 3) 大块：明确批准后
powershell -NoProfile -ExecutionPolicy Bypass -File .\bin\SAFE-CLEAN-V1.2.ps1 -Manifest .\manifests\05-optional-heavy.csv -Apply -ApprovedBy "A"
```

跑完：把 `bin\runs\receipt-*.json` 的 `freedGB` 写回本节；复验 `uv/npm/pip` 可用 + `uv sync` 一次；
视频环境按宿主口径复验 Torch/Requests/WebSocket 可导入，SpeakMore/Polsia/LTMVH 进程仍在。

## 本轮已完成（有回执）

| # | 事项 | 状态 | 产物 |
|---|---|---|---|
| 1 | 复核输入与 7 条误删项逐条对照 | DONE | `REVIEW-20261110-GPT.md` |
| 2 | 修 dry-run 副作用（purge/recycle 仅 `-Apply`） | DONE（实测 `PURGE skipped (dry-run)`） | `bin\SAFE-CLEAN-V1.2.ps1` |
| 3 | 运行态门控（deny → L1 → L2 → manual） | DONE（L1=True / L2=False 实测） | 同上 |
| 4 | 清单加 Category，剔除被拦 7 条与"最近仍在写"3 条 | DONE（01:11 / 02:167 / 03:113 / 05:6） | `manifests\` |
| 5 | 门控前不计量（167 项 239s → 6s） | DONE | 同上 |
| 6 | V1.1 归档并标注缺陷 | DONE | `bin\deprecated\` |
| 7 | 02/03/05 在沙箱内全部 BLOCKED（证明不会误删） | DONE | `bin\runs\receipt-2026*.json` |
| 8 | 真实删除 | **BLOCKED（沙箱 L2 不可用 + 无删除权）** | 需正常 PowerShell |
| 9 | 完整界面验收 | PENDING | 依赖第 8 步 |

## 红线（本轮换来，别再犯）

1. 日期旧 / 服务没开 / 名字像一次性 → 只是候选信号，**不是**无用证据。
2. `查不到引用` ≠ `无引用`；L2 不可用时结论只能是 `unverified`。
3. 本地 AI 环境有**跨环境依赖**（Aaki 的 UMT5、Star7 便携包的 INT4 编码器/VAE 被 H3/Wan 引用）。
4. dry-run 必须零副作用；自检只证明引擎，不证明业务可删。
5. 沙箱里 `Get-CimInstance Win32_Process`、`Get-NetTCPConnection`、`tasklist` 均 `拒绝访问` → 运行态核验要在宿主做。