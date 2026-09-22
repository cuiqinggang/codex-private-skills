# v4.0.0 Codex 本地部署合同

## 目标

把远端：

```text
codex/first-principles-physical-limit-convergence-v4.0.0
```

部署到本机 Codex skills，并做回读验证。

必须部署：

```text
~/.codex/skills/first-principles-physical-limit-convergence
~/.codex/skills/local-ai-reality-foundation
```

## 权限边界

本任务属于：

```text
实际验证
```

Codex 只执行本文件冻结步骤；不得重新设计 v4 方法。

## 冻结步骤

1. 不修改代理、FlClash、注册表或系统网络设置。
2. 定位本地共同仓库；默认候选：
   `C:\Users\A\Documents\Codex\codex-private-skills`
3. `git fetch origin codex/first-principles-physical-limit-convergence-v4.0.0`
4. 使用临时 worktree 读取远端分支，不切换用户当前工作分支。
5. 对两个现有目标技能目录做时间戳备份。
6. 精确复制两个 v4 技能目录。
7. 回读 VERSION：
   - first-principles = 4.0.0
   - foundation = 1.0.0
8. 回读 SKILL.md，确认“一虚一实 / 虚拟成熟 / 实际验证 / T*=min(T_VALID)”均存在。
9. 检查旧 v3.1.9 远端分支仍存在。
10. 不删除历史 skill references/components。
11. 最终输出机器字段并 STOP。

## 全局 AGENTS 迁移

如果 `~/.codex/AGENTS.md` 仍含旧 v3“三核心第四字段门禁”，必须：
- 先备份；
- 仅替换 first-principles 对应门禁；
- 保留其他 Agent/技能规则；
- 新门禁第四字段只允许“虚拟成熟 / 实际验证”；
- 明确 v4 supersedes 旧 first-principles 三核心 gate；
- 回读验证。

不得因看不懂 AGENTS 其他内容而重写整个文件。

## 最终输出

```text
V4_REMOTE_BRANCH=PASS|FAIL
FIRST_PRINCIPLES_LOCAL_VERSION=4.0.0|OTHER
FOUNDATION_LOCAL_VERSION=1.0.0|OTHER
BACKUP=PASS|FAIL
AGENTS_V4_GATE=PASS|FAIL|NOT_PRESENT
LEGACY_V3_BRANCH_PRESERVED=PASS|FAIL
PROXY_CHANGED=NO
FINAL=PASS|FAIL
ACTION=STOP
```
