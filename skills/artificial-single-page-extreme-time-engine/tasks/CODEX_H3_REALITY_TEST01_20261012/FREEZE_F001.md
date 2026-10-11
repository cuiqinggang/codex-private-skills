# Codex+H3 微型精品视频 Reality Test 01｜现实执行冻结 F001

TASK_ID=CODEX_H3_REALITY_TEST01_20261012
FREEZE_ID=CODEX-H3-RT01-F001
TIMEZONE=Asia/Shanghai
CURRENT_STATE=BLOCKED
FINAL_VALID=NO
IMAGE_PASS=0/8
VIDEO_PASS=NO
DO_NOT_CLAIM_PASS=YES

## 目标
原合同：由 Windows Codex/本机 ComfyUI 实际生成暖阳厨房果篮 8 张连续源图，经逐张合格验收后使用 MiniMax H3 真正生成 2–3 秒精品广告式微片。严禁使用 FFmpeg 拼接冒充 H3、复制单图冒充8张生成图片。

## 已发生的真实执行与证据
1. Desktop Commander Remote 主路设备 `DESKTOP-4A1EGTM` 在线，Ping PASS，v0.3.2 直连方式真实成功；设备ID `f6990966-5870-484b-bf79-409bc6fb963e`。
2. Windows CLI `C:\Users\A\AppData\Roaming\npm\codex.ps1`，Codex CLI 0.160.0。主路启动多次，最终 UTF-8 中文任务书正确投递，Codex session `01a12c66-0d2c-7013-9ee0-8a7f96d82e5c`。随后出现多次 `Reconnecting... 3/5..5/5` 和 `Falling back from WebSockets to HTTPS transport. request timed out`，没有获得图片生成的完成证据。
3. 本机 ComfyUI 8188 `/system_stats` HTTP 200；MiniMax-H3 安装根 `C:\AI\MiniMax-H3`；存在 Ref2VA/FL2VA 各约19.53 GB，以及视频VAE约4.85GB；H3 8193 服务无响应。未修改代理、FlClash、CUDA、旧图工作流。
4. Desktop Commander 当月额度达到100%，连接器明确暂停远程调用；不能继续在此页面经该通道执行。
5. 复用既存 GitHub Actions 自托管 Windows 桥。
   - R1 任务 `CODEX-H3-REALITY-TEST01-20261012`，运行 https://github.com/cuiqinggang/codex-private-skills/actions/runs/38167819694 ，Windows Runner 真实执行，失败 `CODEX_COMMAND_NOT_FOUND`。
   - R2 `CODEX-H3-REALITY-TEST01-R2-20261012`，运行 https://github.com/cuiqinggang/codex-private-skills/actions/runs/38167961451 ，发现 GitHub Runner 身份为 `DESKTOP-4A1EGTM$`，访问用户 A 安装的 `C:\Users\A\AppData\Roaming\npm\codex.cmd` 报 `Access is denied`，没有尝试修改账户权限。
   - 独立只读巡检 `CODEX-H3-AUDIT-20261012`，运行 https://github.com/cuiqinggang/codex-private-skills/actions/runs/38168129171 ，Windows Runner 返回 AUDIT_COMPLETED_READ_ONLY 与 PASS（仅限巡检本身，不代表视频测试PASS）。
6. 巡检实际机器结果（2026-10-12 03:28 北京时间）：
   `PROJECT_EXISTS=True`
   `FILE_COUNT=4`
   `IMAGES_PRESENT=0`
   `H3_VIDEO_PRESENT=False`
   `PORT_8188_HTTP=200`
   `PORT_8193_OFFLINE`
   项目中实际仅 TASK_PROMPT.md 和 3 个 Codex 执行日志，无8张图片及视频。巡检也没有返回属于本任务的 Codex 进程。

## 真实 Windows 项目根
`C:\AI\MiniMax-H3\projects\CODEX_H3_REALITY_TEST_01_20261012`
已存在 `TASK_PROMPT.md`；不可声称图片或视频已生成。
GitHub Actions 的各次机器证据见相应 run/artifact ZIP。

## 故障隔离
- 主路：Codex CLI 已起、任务已接，但访问模型后端超时；Desktop Commander 额度用尽，使当前页面无法继续调试。
- 备路：GitHub Actions 自托管 Runner 本身在线且可以执行，但运行在机器服务账户，不能访问用户 A 的 Codex 可执行路径/身份上下文。
- H3：模型文件存在，不代表启动、推理或质量验收通过，8193服务当前离线。
- 未触及旧流程删除、系统代理更改、用户目录权限更改。失败路径不得伪装成功。

## 下一步（在具备授权的执行通道恢复后）
1. 通过原用户A的受授权通道恢复 Codex 后端请求连通性，复用本任务的 TASK_PROMPT.md；不得凭模型下载、路径存在宣告PASS。
2. 先做 1 张真实图片和单图真实验收，合格后连续编辑成8图；每张记录真实 ComfyUI prompt_id、输出、种子、哈希、质量。
3. 按本地 H3 原有成熟 Ref2VA 工作流恢复8193并核实真正支持的输入，运行2–3秒；实际视频解码头中尾帧，不用 FFmpeg 过渡冒充。
4. 交付原合同7类产物；只有真实通过后才把 FINAL_VALID 改为 YES。
