---
name: safe-parallel-exploration-and-acceptance
description: Safely plan, version, isolate, test, compare, integrate, roll back, and deliver complex local work with Git, Worktree, project environments, existing Codex Hooks, route-level acceptance, PARTIAL_PASS extraction, and integration-candidate validation. Use for risky skill upgrades, multi-route architecture experiments, long-running automation, knowledge systems, video/PPT systems, websites/apps, model routing, core configuration changes, L0/L1/L2/L3 skill governance, or when the user asks for 安全探索、稳定基线、工作树隔离、候选整合、强制验收、回滚、三轮测试 or 完整安全探索工作台.
---

# 可回退并行探索与强制验收技能包 V1.0

把复杂变更拆成可验证、可恢复、不会自动污染主线的阶段。优先调用现有 Hooks；不要重复注册 Hook。

## 正式名称与直接调用

- **正式中文名**：可回退并行探索与强制验收技能包 V1.0。
- **日常中文简称**：安全探索技能包。
- **精确技能 ID**：`safe-parallel-exploration-and-acceptance`。
- **推荐说法**：`使用安全探索技能包，帮我对 <项目名称或路径> 做 <目标>；限制是 <禁止事项>。`

将“安全探索技能包”视为本技能的直接中文别名；不必手动指定 Git、Worktree 或 MODE，先按风险分类再决定所需强度。

## 开工顺序

1. 读取项目 `AGENTS.md`、`.codex` 策略、登记表和失败复盘。
2. 运行 `scripts/classification/classify-task.ps1`，结合项目稳定性、失败后果和探索不确定性选择模式。
3. MODE-B/C 先运行基线与 Worktree 就绪检查；不是 Git 仓库时只生成预览，不自动初始化。
4. 记录允许目录、禁止事项、成功/失败指标、停止条件、环境命令和回滚点。
5. 每条路线使用独立分支、工作树、`.codex/acceptance-state.json` 和证据目录。
6. 路线完成后运行路线验收；`ROUTE_PASS` 不等于 `FINAL_PASS`。
7. `ROUTE_PARTIAL_PASS` 必须生成精确的 `PARTIAL_EXTRACTION_PLAN.md`，只导入批准的提交或文件。
8. MODE-C 必须建立独立 `integration-candidate` 工作树，整合后重新完成三轮测试。
9. 只生成主线准入建议。未经用户确认，不合并 main、不 push、不覆盖稳定版本。
10. 交付前验证回滚、敏感信息、ZIP 清单与 SHA256，并更新仪表盘和最近使用记录。

## 2026-07-12 真实运行加固

UltraFusion V9 的首次真实运行证明：部署成功不等于运行可靠。本技能现在把以下项目设为硬闸门：

1. 用 Git plumbing 区分 worktree、bare repository、空/损坏 `.git` 和非 Git 目录。
2. Windows checkout/worktree 前审计 Git tree；尾随空格/点、保留名、非法字符或控制字符必须阻断。
3. 历史树不可在 Windows checkout 时，只允许建立本地保护标签和无父提交的 Windows-safe 隔离工作树；不得自动合并主线。
4. 哈希锁定资产使用 `.gitattributes -text`，同时核验工作副本与 staged Git blob 的 SHA-256。
5. 只读资产的注入测试只修改独立沙箱副本，必须证明源文件哈希不变。
6. 非 Git 的正式技能安装副本使用哈希、静态测试和运行时测试验收，不能因没有 `.git` 误判失败。
7. 修复必须经过候选版、集成副本、正式安装副本三层复测；任一层失败都不得输出 `FINAL_PASS`。

详细复盘和脚本见 `90_RUNTIME_HARDENING/`、`references/WINDOWS_GIT_INVALID_PATH_RECOVERY.md` 和 `references/EXACT_BYTE_READONLY_ASSET_POLICY.md`。

## 模式

| 模式 | 用途 | Git/Worktree | 验收 |
|---|---|---|---|
| MODE-A | 问答、只读、低风险小改 | 不强制 Worktree | 基础安全 Hook |
| MODE-B | 单一方案、中等风险正式升级 | 一个 Worktree | 路线验收 + Handoff |
| MODE-C | 多方案、高不确定性或系统级升级 | 多 Worktree + integration-candidate | 独立路线 + 三轮整合 + 最终验收 |

## 技能默认管理等级

| 等级 | 默认策略 |
|---|---|
| L0 | 不单独版本探索，只做基础检查 |
| L1 | 使用已有共享仓库，本地 diff 与一轮验证 |
| L2 | 单 Worktree 安全探索 |
| L3 | 多路线并行探索和候选整合 |

实际模式 = 默认等级 + 本次任务风险。L3 技能的拼写修复可降级；L1 技能的核心重构必须升级。

## 硬门禁

- 不使用 `git add .`、`git reset --hard`、`git clean`、自动 stash、自动 merge 或自动 push。
- 不跟踪 `.env`、token、key、证书、凭据、大型视频/模型/缓存/ZIP。
- 不在 K 盘建立日常工作树或修改日常内容。
- 不把多个路线共用同一验收状态或证据目录。
- dirty、conflict、未合并或未确认成果的工作树不得自动清理。
- 正式 Git 基线、正式项目修改、合并主线、删除含未提交内容的工作树必须等待用户确认。
- UltraFusion 预接入只建立档案、计划和启动预览；不改稳定版本，不一次创建全部路线。
- 不以 `.git` 目录是否存在作为仓库有效性的判断依据。
- 不在 Windows 路径审计失败后继续普通 checkout/worktree。
- 不自动格式化或换行转换哈希锁定资产。
- 不用未经候选、集成、安装后三层实测的修复覆盖稳定技能。

## 验收状态

- 路线：`ROUTE_PASS` / `ROUTE_PARTIAL_PASS` / `ROUTE_FAIL` / `ROUTE_NEEDS_MANUAL_REVIEW`。
- 整合：`FINAL_PASS` / `FINAL_PASS_WITH_LIMITS` / `FINAL_FAIL` / `FINAL_NEEDS_MANUAL_REVIEW`。
- 只有 `FINAL_PASS` 或用户接受的 `FINAL_PASS_WITH_LIMITS` 才能提出主线准入。

## 资源路由

- 架构与策略：读取 `references/ARCHITECTURE.md`、`references/SAFETY_POLICY.md`。
- Git/Worktree：读取 `03_GIT_LOCAL_BASELINE/`、`05_WORKTREE/`。
- 环境：读取 `06_ENVIRONMENT/`。
- 路线与整合：读取 `07_ROUTE_ACCEPTANCE/`、`09_INTEGRATION/`、`10_FINAL_ACCEPTANCE/`。
- 技能分级：运行 `scripts/skills/scan-skill-registry.py`，读取 `templates/skill-exploration-registry.schema.json`。
- 日常入口：运行 `启动_完整安全探索工作台.cmd` 或 `scripts/dashboard/generate-dashboard.ps1`。
- 失败复盘：写入 `FAILURE_REVIEW.md`；成功复用写入 `RECENT_USE_LOG.md`。

## 下次复用

先运行分类、基线和登记表查询，再选择 MODE-A/B/C。不得因为技能默认 L3 就机械启动最重流程。
