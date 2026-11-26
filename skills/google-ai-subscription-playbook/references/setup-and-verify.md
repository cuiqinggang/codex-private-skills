# 第一轮实机配置与验收清单（4 项闭环）

> **执行原则**：先在当前 \$20 Pro 档把 4 项入口全部打通并落盘回执。每通过一项就在 `account-receipts.md` 标记为 `PASS`；未登录/未测试项保持 `PENDING`，不得跳步或虚报。  
> **安全红线**：截图与日志必须避开一次性验证码、密码、API Key、OAuth 回调参数与令牌。

---

## 第 1 项：确认个人 Google 账号档位与主订阅者身份
- **入口**：用同一个个人 Google 账号打开 `https://one.google.com/`（复用专用浏览器 Profile：`C:\AI\Playwright-Native-AI-Browser\profile\shared-mcp`）。
- **核对内容**：
  1. 当前套餐名称（确认是否为付费 Pro，而非试用版）；
  2. 续费价格与周期；
  3. 本人是**主订阅者 / 家庭管理员**还是家庭成员；
  4. 存储配额（预期 5 TB）及地区审核后的各产品开放状态。
- **通过条件**：读到明确档位、续费价、主订阅者身份，并脱敏记入 `account-receipts.md`。

---

## 第 2 项：领取 Google Cloud / Gemini API 开发者赠金并核对首笔小调用
- **入口**：`https://aistudio.google.com/billing` 或 `https://me.developers.google.com/`。
- **操作步骤**：
  1. 找到开发者月度云赠金领取入口（Pro 为 \$10/月）；
  2. 将赠金应用到指定 Billing Account，并勾选/确认后续月度到账自动应用到同一账户；
  3. 用该关联项目发出一笔最小测试 API 调用（例如短文本 echo）。
- **通过条件**：
  1. 看到实际赠金金额、到期日（每笔有效期 12 个月）、关联 Billing Account 与项目 ID（脱敏）；
  2. 第一笔小调用在用量记录和计费/赠金抵扣记录中能对上。

---

## 第 3 项：打通 Drive 交接与 Antigravity 网页远控（Remote Control）
- **3A. Drive 插件接入（推荐，免软链接）**：
  - 在 Antigravity 插件管理器中登录 `gdrive` 插件（同账号 `cuiqinggang@gmail.com`，与已连接的 `gdocs`/`gsheets` 一致）。
  - 验收：列出指定交接目录或读写一个临时测试文档，确认源码仍留在本地 Git。
- **3B. Antigravity 网页远控 Windows 本机会话**：
  - 在 Windows 的 Antigravity 桌面端开启 **Remote Control**；
  - 用同账号打开 `https://antigravity.google.com/`，选中 Windows 上正在运行的本机会话（注意区分：Remote Control 控本机，Remote Agents 跑在 Google 托管环境）；
  - 在临时工作区写入一个唯一标记文件并读回验证。
- **通过条件**：临时工作区写入与读回一致；若 Windows 10 上 CLI 沙箱或 Auto 模式存在界面限制，按实机界面如实记录。

---

## 第 4 项：Colab GPU 远程计算小样闭环与强制回收检查
- **前置入口**：登录 `https://colab.research.google.com/` 或在完成 OAuth 登录后直接运行 `colab usage` 核对当前 CU 余额与消耗速率（Pro 预期 200 CU/月）。
- **CLI 安装状态（本机已于 2026-11-26 实测通过）**：
  - 已通过 `uv tool install google-colab-cli` 安装官方 **`google-colab-cli 0.8.0`** 至 Windows 原生 PATH：`C:\Users\A\.local\bin\colab.exe`（`colab --help` 与 `colab version` 均退出码 0，无需强制切 WSL2；若个别交互子命令遇终端兼容问题再回退至 WSL2 `Ubuntu-24.04-Restore`）。
- **五步固定验收流程**（也可按需搭配 `colab usage` / `colab drivemount` / `colab run`）：
  ```bash
  colab usage
  colab new
  colab exec <session> "<最小 GPU 探针与输出文件脚本>"
  colab download <session> <远程输出文件> <本地临时路径>
  colab stop <session>
  colab sessions
  ```
- **通过条件**：
  1. 下载的小样文件可校验（大小/哈希/内容正确）；
  2. 记录实际分配的 GPU 型号、CU 消耗，以及完整 `T_VALID_E2E`（上传 + 排队 + 启动 + 运行 + 下载 + 校验），与本机 RTX 2080 Ti 同样本做一次对照；
  3. **`stop` 后执行 `colab sessions`，确认该任务会话已彻底消失**；异常中断路径也必须补做一次同样的回收检查。
