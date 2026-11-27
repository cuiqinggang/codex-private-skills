# 本人账号权益与实机验收台账（脱敏）

> **安全红线**：本文件**严禁**写入密码、API Key、Cookie、OAuth 回调 URL、授权码、令牌或一次性数字。只记档位、脱敏账号标识、到期日、实机结果与报错原文。

---

## 一、当前总体状态（2026-11-27 北京时间）

- **技能包版本**：`V0.2.0`
- **整体状态**：`PRO_CORE_VERIFIED / GDRIVE_AND_BILLING_PENDING`
- **已实机确认档位**：`Google AI Pro (5 TB)`（自 `2026-11-17` 起成为会员，主订阅者，未建家庭组）
- **绑定 Google 账号**：`崔清岗 (cuiqinggang@gmail.com)`

---

## 二、第一轮 4 项验收状态表

| 验收项 | 目标状态 | 当前状态 | 实机证据 / 备注 | 最近核对时间 |
|---|---|---|---|---|
| 1. Google One 账号档位回读 | 确认付费 Pro、5 TB、主订阅者身份 | `PASS` | 通过 9223 专用浏览器实机读回 `one.google.com`：`Google AI Pro (5 TB)`，自 `2026-11-17` 起，已用 `0.87 GB / 5 TB`（0%），主订阅者（未建家庭组） | 2026-11-27 |
| 2. Cloud / Gemini API 月度赠金 | 领出 \$10/月并确认首笔小调用抵扣 | `WAITING_BILLING_SETUP` | 已实机读回：`me.developers.google.com` 尚未点「加入计划」；`aistudio.google.com/billing` 显示「没有结算账号」。涉及结算绑定，待本人决定启用时开通 | 2026-11-27 |
| 3A. Antigravity `gdrive` 插件 | 插件已连接并读写测试交接件 | `PENDING_USER_SIGNIN` | `gdrive` CLI 已注册（`cl/1015343799`）；待本人在聊天插件卡点 Sign in 授权（`gdocs`/`gsheets` 已连同账号） | 2026-11-27 |
| 3B. Antigravity Remote Control | 网页控本机在临时工作区读写一致 | `PASS`（限常规任务） | 直接继承 2026-11-27 `google-windows-three-entry` 权威回执（具名项目 `google-three-entry-uat-20261127-r2` + `agy 1.5.18`：主机/HTTPS `00:04:132`、Codex `00:51:862`、Pi `00:20:149`、5/5 防重哈希均 PASS；断线重连另验） | 2026-11-27 |
| 4. 官方 Colab CLI 闭环与回收 | `new -> exec -> download -> stop -> sessions` + CU 记录 + 2080 Ti 对照 | `PASS` | `google-colab-cli 0.8.0` Windows 原生 OAuth2 已存 keyring；余额 **`400.28 CU`**，可用 GPU：`G4/A100/L4/T4`（H100 不可用），TPU：`V6E1/V5E1`。实跑 T4 同参数 1080p NVENC：下载校验 SHA-256 逐字节一致（`6D931A94...043F`，300 帧 h264 PASS），`stop` 后 `sessions` 为空、`Active assignments: 0`，实耗 `< 0.01 CU` | 2026-11-27 |

---

## 三、2080 Ti vs Colab GPU 同参数实测基准（2026-11-27）

**统一任务**：10 秒 `1920x1080` 30fps `testsrc2` → `ffmpeg -c:v h264_nvenc -preset p4 -b:v 6M -pix_fmt yuv420p`

| 执行端 | 实际 GPU | 纯计算耗时 | 分配/排队 | 传输与校验 | 回收 | 完整 `T_VALID_E2E` | 校验结果 |
|---|---|---:|---:|---:|---:|---:|---|
| 本机工作站 | RTX 2080 Ti 22GB | `00:02:522` | `00:00:000` | `00:00:000` | — | **`00:02:522`** | `PASS`（`8,656,481 B`，300 帧） |
| Google Colab CLI | Tesla T4 15GB（L4 503 后自动降级） | `00:02:733`（含 `exec` 往返 `00:18:758`） | `04:41:376`（含 L4 4 次 503 重试约 `03:46`；T4 单次约 `00:55`） | `00:11:314`（下载 `00:11:133` + 本地校验 `00:00:181`） | `00:13:033` | **`05:57:225`**（仅 T4 路径约 `01:38`） | `PASS`（`8,660,020 B`，远端/本地 SHA-256 完全一致，`sessions=0`） |

**实测结论**：单条或短时视频/计算任务固定走本机 RTX 2080 Ti；仅当显存超出 22GB、本机被占满，或大批量/长时间计算可摊平约 1–2 分钟冷启动与下载开销时，再分流到 Colab CLI。

---

## 四、本机工具链基线核对（2026-11-27）

- `python`：`C:\Users\A\AppData\Local\Programs\Python\Python313\python.exe`（可用）
- `uv`：`C:\Users\A\.hermes\bin\uv.exe`（可用）
- `colab`：`C:\Users\A\.local\bin\colab.exe`（`google-colab-cli 0.8.0`，Windows 原生 OAuth2 已授权并闭环 `PASS`）
- `gdrive`：`cl/1015343799`（已注册 PATH，待点 Sign in）
- `ffmpeg`：`ffmpeg-8.1.1-full_build`（支持 `h264_nvenc / hevc_nvenc / av1_nvenc`）
- `git` / `gh` / `node` / `codex` / `agy`：均已就位；`gh` 已登录 `cuiqinggang`
- WSL2：`Ubuntu-24.04-Restore`（Version 2，备用）

---

## 五、\$20 → \$100 升级观察日志

| 日期 | 任务号 | Antigravity/Gemini 封顶？ | 当月累计 CU | 当月 API 消耗 | 是否触发升级门禁 | 备注 |
|---|---|---|---|---|---|---|
| 2026-11-26 | 初始化建包 | `NOT_MEASURED` | `NOT_MEASURED` | `NOT_MEASURED` | 否 | 建包基线 |
| 2026-11-27 | 首轮 Colab 实机闭环 | 否 | 余额 `400.28 CU`（本轮消耗 `< 0.01 CU`） | `NOT_MEASURED`（未绑结算） | 否 | 当前 5 TB 存储仅用 0.87 GB，CU 余额充裕，远未触及升级门禁 |

---

## 六、故障与复盘记录

- `2026-11-27 18:59`｜Colab OAuth 浏览器打开｜原始错误：`400 invalid_request: Missing required parameter: redirect_uri`｜根因：CDP `/json/new?URL` 截断了 OAuth 链接中的 `&` 参数｜修复：改用 `/json/new?about:blank` + CDP `Page.navigate` 原样传完整 URL，立即通过。
- `2026-11-27 19:14`｜`colab new --gpu L4`｜原始错误：Google 服务端连续 4 次返回 `503 Service Unavailable`（重试退避 10s/20s/40s）｜处置：脚本自动降级至 `--gpu T4` 成功完成闭环并强制 `stop -> sessions` 核销，零 CU 泄漏。
