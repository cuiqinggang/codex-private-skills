---
name: google-ai-subscription-playbook
description: 串联并最大化利用 Google AI 订阅五项权益（Antigravity、Gemini+Drive/NotebookLM、AI Studio、Colab GPU CLI、Google Cloud 开发者赠金），按当前档位（$20 Pro 或 $100 Ultra 5x）分流任务、统一单任务号交接、控制升级门槛并做实机回读验收。遇到 Google AI 订阅权益配置、Pro 升级 Ultra 判断、Drive 交接、Colab 远程计算分流、AI Studio 赠金领取或网页 Remote Control 验收时使用。
---

# Google AI 订阅权益串联与分档复用包（V0.2.0）

**当前状态**：`PRO_CORE_VERIFIED / GDRIVE_AND_BILLING_PENDING`（2026-11-27 北京时间）  
**当前激活档位**：`PRO_20`（Google AI Pro 5 TB，2026-11-27 已实机回读确认主订阅者身份；Colab CLI Windows 原生五步闭环与强制回收已 `PASS`，账户余额 `400.28 CU`）——未来若升级至 \$100/月 `ULTRA_5X`，只需更新 `references/tier-profiles.md` 与 `references/account-receipts.md` 并补做一轮回读，整套串联流程无需重写。

> **职责边界**：若遇到 Windows 上 Antigravity 桌面登录失败、地区不支持、OAuth 超时、`loadCodeAssist: EOF`、窗口消失或中文界面失效，直接跳转已验收恢复技能 `operate-google-antigravity-windows`（`C:\Users\A\.gemini\config\skills\operate-google-antigravity-windows\SKILL.md`），不在本包重复维护故障修复流程。

---

## 一、五张牌的分工红线（最小化完整 `T_VALID_E2E`）

| 能力入口 | 负责什么 | 禁止什么 |
|---|---|---|
| **Antigravity 桌面端 / Remote Control** | 本地隔离工作区多文件开发、跑测试、读日志、补丁复核；付费 Pro/Ultra 模型菜单内按需调用 Claude（Sonnet 5.5 / Opus 5.5 Thinking 等，以实机菜单为准） | 不拿网页预览替代本地代码测试；桌面登录/网络故障直接转 `operate-google-antigravity-windows` |
| **Gemini + Google Drive / NotebookLM** | Deep Research 调研竞品与卖点；Drive（插件或串流）存放规格书、素材、审核回执、最终交付件；需要逐句溯源的材料加入 Gemini Notebook（NotebookLM） | **源码仓库严禁放进 Drive 同步目录**（源码只走 Git）；客户私料上传前必须核对项目授权与数据条款 |
| **AI Studio 网页** | 审读长日志、长规格书、视频样片，强制要求输出**带时间戳或原文引文的问题清单**，交回 Pi 或 Antigravity 本地修改 | 不把网页订阅额度、API 计费与额外 AI 点数混为一谈；不替代本地真实执行与验收 |
| **Colab GPU（官方 Colab CLI）** | 仅当本机 RTX 2080 Ti 显存不足、被其他重任务占用，或同样本实测总耗时更短时，承接脚本化批量转码、字幕烧录、渲染或推理 | 不凭感觉上云；必须把上传、排队、运行、下载、校验全部计入 `T_VALID_E2E`；禁止跳过 `stop -> sessions` 回收核销 |
| **Google Cloud 开发者赠金** | 优先用于无人值守的 Gemini API 定时/批量调用（先小样核对账单抵扣）；确有真实部署需要再分配给 Cloud Run | 严禁把 API Key、Cookie、OAuth 参数写入台账或仓库；家庭成员不享有主订阅者专属的 Colab/Cloud 赠金 |

---

## 二、标准单任务号串联流程

整单共用同一个 `TASK_ID`，交接时固定携带**规格版本、Git commit、Drive 产物链接**。普通任务只走主线，遇到长材料、视频或重算力时才按需开支路：

```text
1. Gemini 调研（输出带来源链接的结论/卖点/待确认项）
   └─> 2. Drive 项目文件夹保存冻结规格与证据（需逐句核对再入 NotebookLM）
       └─> 3. Pi 接单建账，派发执行
           ├─ 主线：Antigravity 本地隔离工作区开发 / 测试 / Claude 复核（Git 管源码）
           ├─ 支路 A（长材料/审片）：AI Studio 输出带时间戳/引文的问题清单 → 回本地修改
           ├─ 支路 B（重算力/批量）：官方 Colab CLI 执行 `new -> exec -> download -> stop -> sessions`
           └─ 支路 C（无人值守）：Gemini API 定时/批量处理（走 Cloud 赠金，先小样对账）
               └─> 4. Pi 统一回读（Git commit + 产物链接 + 测试日志 + 实际用量 + T_VALID_E2E）→ 交付
```

---

## 三、按需读取参考文档

- **查 \$20 Pro vs \$100 Ultra 5x 参数对比、家庭组边界、升级硬门禁**：读 [references/tier-profiles.md](references/tier-profiles.md)
- **执行第一轮 4 项实机配置与逐项验收**：读 [references/setup-and-verify.md](references/setup-and-verify.md)
- **开新单需要标准交接单与计时记录模板**：读 [references/task-handoff-template.md](references/task-handoff-template.md)
- **查本人账号最新实测台账与历史回执**：读 [references/account-receipts.md](references/account-receipts.md)

---

## 四、防落灰与升级更新规则

1. **触发关键词**：`Google AI 权益`、`Pro 升级 Ultra`、`20 美元升级 100 美元`、`Google AI 串联`、`Drive 交接`、`Colab CLI 分流`、`AI Studio 赠金`、`Antigravity Remote Control`。
2. **虚/实红线**：官方文档核对记为 `DESIGN_VERIFIED`；只有本机/本人账号实际跑通并落盘回执的项目，才可记为 `PRO_VERIFIED` 或 `ULTRA_5X_VERIFIED`；未测项一律保持 `PENDING` 或 `NOT_MEASURED`。
3. **版本递增**：文档/参数纠错升修订号（`V0.1.x`）；第一轮 Pro 4 项实机验收全部通过升 `V1.0.0`；后续切换至 Ultra 5x 并完成回读升 `V1.1.0`。
4. **失败复盘入口**：任何实机步骤失败（含 Colab CLI 环境限制、赠金未抵扣、Remote Control 断连），将原始错误、时间、已试路径与结果追加写入 [references/account-receipts.md](references/account-receipts.md) 的「故障与未决项」小节。
