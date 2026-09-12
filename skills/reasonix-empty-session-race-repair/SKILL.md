---
name: reasonix-empty-session-race-repair
version: 1.0.0
chinese_name: Reasonix 空会话竞态修复与保护性部署
summary: 用于诊断与修复 Reasonix 新建空会话后偶发“暂时无法加载会话/加载会话历史失败”的前端竞态，并固化 GPT 决策、Codex 执行、专用 AI 浏览器协同与保护性部署流程。
tags:
  - reasonix
  - empty-session
  - race-condition
  - frontend
  - hotfix
  - playwright-native-ai-browser
  - codex
  - gpt-review
  - protective-deployment
  - rollback
---

# Reasonix 空会话竞态修复与保护性部署

## 1. 适用场景

当 Reasonix 出现下列特征时优先使用本技能：

- 新建会话后，空会话偶发显示“暂时无法加载会话”“无法打开会话”“加载会话历史失败”。
- 同一会话一旦发送第一条消息后又能正常工作。
- 新 topic/tab/sessionPath、meta、display-index、lease 已正常创建。
- 数据库 quick_check 正常，不能证明是 SQLite 损坏。
- 用户明确要求永久修复，不接受“先发一句话”“删空会话”“清缓存/重装”等绕过。

本技能的首要目标是：**先判断是数据损坏、后端空历史语义错误，还是前端 ready/hydration 竞态；只修真正根因。**

## 2. 固定角色分工

### GPT：核心分析与补丁决策总控

GPT 必须负责：

1. 读取并复核证据。
2. 判定根因。
3. 决定补丁范围。
4. 审核 Codex 拟实施的修改。
5. 发布最终执行命令/命令包。
6. 定义验收门与回滚条件。

GPT **不把根因判断交给 Codex 自由发挥**。

### Codex：执行器

Codex 负责：

- 源码检索。
- 实际修改。
- 生成 bundle / patch。
- 执行测试。
- 备份。
- 部署。
- 回传证据。

Codex 不应自行改变 GPT 已批准的补丁范围，除非发现直接冲突证据并暂停上报。

### 专用 AI 浏览器：GPT ↔ Codex 正式桥

固定使用：`playwright-native-ai-browser`

用途：

- 打开/复用已有 GPT 会话。
- 将 Codex 收集的证据送交 GPT 复核。
- 读取 GPT 的补丁决策与部署授权。
- 把 GPT 的最终命令交回 Codex 执行。

要求：

- **复用 existing owner。**
- 即使浏览器已经打开，也继续复用现有 owner，不启动第二 owner。
- 不新建 profile。
- 不切 isolated mode。
- 不改用其他浏览器。
- 不直接走 CDP 旁路。
- 浏览器已打开不代表不能继续使用；只要 owner 存活，就继续通过正式入口 query/send/wait_extract 使用 GPT。

本案例审计通过状态：

```text
AI_BROWSER_SKILL=playwright-native-ai-browser
AI_BROWSER_STATUS=REUSED_EXISTING_OWNER
AI_BROWSER_BLOCKED=False
EXISTING_OWNER_REUSED=True
SECOND_OWNER_STARTED=False
NEW_PROFILE_CREATED=False
ISOLATED_MODE_USED=False
CDP_USED=False
ALTERNATIVE_BROWSER_USED=False
```

## 3. 本案例最终根因

目标版本：Reasonix v1.38.7

Build commit：

```text
036c7c50c5c154f747419aee6b75667f9044c8fa
```

### 已排除的错误方向

后端已经证明：

- 0-byte JSONL 能正确解析为空消息。
- missing / empty event log 原生合法。
- 缺失 transcript projection checkpoint 是可选状态。
- snapshot 的数组语义为 `[]`。
- `TestHistorySliceColdEmptySession` 已覆盖空历史成功。

因此不能再把以下内容当成根因：

- 0-byte transcript 损坏。
- missing event log。
- missing projection。
- `revision=1`。
- `entries=[]`。
- SQLite 损坏。
- DeepSeek effort/support 配置。

### 精确竞态

前端新会话链：

```text
handleNewTab
  -> blank navigation
  -> ensureBlankSurface / ensureBlankTab
```

后端 `EnsureBlankSurface/EnsureBlankTab` 的设计允许：

```text
异步 startTabControllerBuild 尚未完成
但先返回 visible tab
ready=false
```

原前端立即执行：

```text
loadSessionDataForTab(...)
```

当时若：

```text
tab.Ctrl == nil
```

则：

```text
TranscriptSnapshotForTab
  -> workspace-not-ready
  -> 被 UI 映射为通用“历史加载失败”
```

controller 构建速度不同，所以故障表现为“偶发”。

**最终根因：前端导航 hydration 在 controller ready 前提前读取会话数据。**

## 4. 最小正确补丁

仅修改：

```text
desktop/frontend/src/lib/useController.ts
```

在：

- `ensureBlankTab`
- `ensureBlankSurface`

中，将 `loadSessionDataForTab` 包装为异步序列：

```text
await waitForTabReady(meta.id)

if (!navigationCompletionCurrent(
    navigationSeq,
    "<对应>.ready",
    meta.id
)) return

await loadSessionDataForTab(...)
```

同时：

- `monitorNavigationHydration` 继续监控该 promise。
- 创建命令本身仍立即返回。
- 两个 `useCallback` 依赖加入 `waitForTabReady`。

### 为什么只修前端

因为后端对 zero-message session 的合法语义已经有直接测试覆盖。继续改后端会扩大修改面，并可能放宽真实损坏检测。

最终审核结果：

```text
PATCH_REVIEW_DECISION=APPROVE
ROOT_CAUSE_AGREEMENT=YES
PATCH_SCOPE=FRONTEND_ONLY
DEPLOYMENT_AUTHORIZED=YES
REQUIRED_CHANGES=NONE
```

## 5. 回归测试要求

新增测试：

```text
desktop/frontend/src/__tests__/new-session-load-race.test.tsx
```

至少模拟：

1. `EnsureBlankSurface` 返回 `ready=false`。
2. `ListTabs` 在 controller build 完成前持续返回 `ready=false`。
3. ready 前 `History* / Transcript*` 调用次数为 0。
4. 切换 `ready=true` 后才读取合法空历史。
5. `hydrateError === undefined`。

已通过：

```text
git diff --check = PASS

go test . -run "TestHistorySliceColdEmptySession|TestTranscriptSwitchReportsActualLoadWithoutLegacyPage" -count=1
= PASS

TypeScript transpileModule syntax diagnostics = 0
```

## 6. 最终部署与验收结果

安装 bundle 原始 SHA-256：

```text
7E86A114D23662F691A1BB95F78E7EC4924441705ACE46CC221D9EB843BD8DBD
```

hotfix SHA-256：

```text
5C5C6C26DA638680F63533CFC9A234A38F327697C8D1967ED3BEB4681A131447
```

源码 patch SHA-256：

```text
AA892F1D19059941BB17BFFE373537B049C58FB67C08BE535DD747A774B8A7D4
```

主机安全策略阻止 Codex 直接写 AppData 安装目录后，没有绕过策略；用户使用普通 PowerShell 7 对已审核 bundle 做单文件保护性替换并验证哈希。

运行验收：

```text
QUICK_NEW_SESSION_TEST=10/10 PASS
ZERO_SESSION_FIRST_OPEN=30/30 PASS
RAPID_NAVIGATION_ERROR_COUNT=0
FIRST_MESSAGE_TRANSITION=PASS
ZERO_SESSION_RESTART=10/10 PASS
OLD_SESSION_REGRESSION=5/5 PASS
OTHER_ERROR=NONE
```

最终：

```text
ROOT_CAUSE=CONFIRMED
PATCH_DEPLOYMENT=PASS
RUNTIME_ACCEPTANCE=PASS
EMPTY_SESSION_FIX=PASS
FINAL=PASS
```
