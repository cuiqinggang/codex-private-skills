---
name: ultrafusion-sites-test-page-deploy
description: Safely integrate, test, version, deploy, and verify UltraFusion validation pages on the existing private ChatGPT Sites project. Use for UltraFusion RC/RC-MIN test-page revisions, real-source discovery, isolated Git Worktree changes, first-screen copy/paste workflows, VT-01–VT-05 virtual tests, same-URL Sites publishing, production rechecks, commit parity, or when preventing a local candidate from being mislabeled as deployed.
---

# UltraFusion Sites 测试页面集成发布

## 核心原则

把“本地候选”“Sites 已发布”“A 关真实有效”分成三个互不替代的事实。

- 只改真实站点源码；找不到真实源码、Git 仓库、提交或 Sites project_id 时立即停止。
- 在独立 Git Worktree/副本中修改；旧 RC、正式提示词和本地主分支只读。
- 只前置复制粘贴交互；复用原解析、计算、保存、导出和阻断函数，不建立第二套业务逻辑。
- 发布必须复用 .openai/hosting.json 中的现有 Sites 项目，不创建相似新站点。
- 虚拟测试通过后仍保持真实样本 0、L3、REVISE，下一关口为 L4 GPT 三题真实烟雾测试。

## 开工顺序

1. 运行 Knowledge Brain / 现有技能复用检查和高收益门禁。
2. 若仓库含 .openai/hosting.json，读取并使用 sites:sites-building、sites:sites-hosting。
3. 使用 safe-parallel-exploration-and-acceptance 的 Worktree 隔离规则；未经用户明确要求不合并本地主分支。
4. 运行：

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\\preflight_ultrafusion_site.ps1 -SiteRoot "<真实站点源工程>" -ExpectedProjectId "<project_id>"

5. 阅读 [DEPLOYMENT-SOP.md](references/DEPLOYMENT-SOP.md) 并按阶段执行。
6. 验收前逐项核对 [ACCEPTANCE-CHECKLIST.md](references/ACCEPTANCE-CHECKLIST.md)。

## 最小页面合同

默认首屏只突出：

原始题目 → 复制 Q0 → 粘贴 Q0 → 复制 V15.1-A → 粘贴完整回复 → 解析确认

详细结果区默认折叠，但必须保留：

- 正式提示词身份与哈希阻断；
- A_RAW、A_PRESSURE_RECORD、A_FINAL；
- 压力、Q0/QR/Q1/Q2/QF、时间最优和硬闸门；
- 十二关、十二项证据、保存和导出。

不得重写评分/压力公式、核心数据对象、数据库、API、账号系统或正式提示词。

## 测试合同

- 原业务回归：10/10。
- VT-01 至 VT-05：5/5；严重回归 0。
- 每套保存 3 张关键截图，共 15 张；另存断言 JSON、控制台日志和导出文件。
- VT-02：剪贴板首次失败、重试、刷新恢复。
- VT-03：缺块/命令回显阻断，同题修复后继续。
- VT-04：Q2 退步，选择或回退 Q1。
- VT-05：时间预算、10/12 证据阻断、禁止 FREEZE、最终 REVISE。
- 1920×1080 主要操作无滚动；1366×768 最多轻微滚动。

运行证据校验：

    python scripts\\validate_release_evidence.py --local "<AUTOMATED_ASSERTIONS.json>" --postdeploy "<POSTDEPLOY_ASSERTIONS.json>" --screenshots "<15张截图目录>"

## Sites 发布合同

1. 构建、测试并提交精确候选源。
2. 获取 Sites 源仓写凭证时，先 get_site，再用返回的原样 id 请求凭证。
3. 通过单次 Git HTTP header 推送；不打印、不保存 token。
4. 用相同提交生成 Sites 支持的部署包，保存新版本，再部署私有版本。
5. 轮询部署到 succeeded。
6. 打开原网址；执行 1 次完整线上 E2E 和 4 次关键路径，控制台错误必须为 0。
7. 核对本地 HEAD、远端分支和 Sites 版本提交完全一致。

任何 Sites 凭证若出现在日志中，立即旋转并清理证据。详细故障处理见 [FAILURE-REVIEW.md](references/FAILURE-REVIEW.md)。

## 状态词

只使用 [STATUS-CONTRACT.md](references/STATUS-CONTRACT.md) 中的精确状态，不使用 FINAL_PASS 等模糊措辞。

## 防落灰

- 触发词：UltraFusion 测试页面、RC4.3-MIN、真实站点集成、原网址发布、Sites 新版本、五次虚拟测试、首屏复制粘贴。
- 失败复盘：[FAILURE-REVIEW.md](references/FAILURE-REVIEW.md)。
- 最近使用：[RECENT-USE-LOG.md](references/RECENT-USE-LOG.md)。
- 全局规则草案：[AGENTS-PATCH-DRAFT.md](references/AGENTS-PATCH-DRAFT.md)。
- 验收页：[ACCEPTANCE.html](assets/ACCEPTANCE.html)。

