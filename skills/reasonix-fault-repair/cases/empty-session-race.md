# Case A — Reasonix 空会话 hydration / ready 竞态

## 1. 症状

新建零消息会话后偶发：

- “暂时无法加载会话”
- “无法打开会话”
- “加载会话历史失败”

但同一会话发送第一条消息后又能正常工作。

## 2. 已验证根因

版本：`Reasonix v1.38.7`

Build commit：

```text
036c7c50c5c154f747419aee6b75667f9044c8fa
```

后端已经证明 zero-message session 合法：

- 0-byte JSONL 可解析为空消息；
- missing / empty event log 合法；
- 缺失 transcript projection checkpoint 为可选状态；
- snapshot 数组语义为 `[]`；
- SQLite quick_check 正常。

真正竞态：

```text
handleNewTab
  -> blank navigation
  -> ensureBlankSurface / ensureBlankTab
        ↓
后端允许 visible tab 先返回、controller build 异步继续
        ↓
ready=false
        ↓
前端立即 loadSessionDataForTab(...)
        ↓
若 tab.Ctrl == nil
        ↓
TranscriptSnapshotForTab -> workspace-not-ready
        ↓
UI 映射为通用“历史加载失败”
```

根因：前端 navigation hydration 在 controller ready 前提前读取会话数据。

## 3. 最小正确补丁

只修改：

```text
desktop/frontend/src/lib/useController.ts
```

在 `ensureBlankTab` / `ensureBlankSurface` 中：

```text
await waitForTabReady(meta.id)

if (!navigationCompletionCurrent(...)) return

await loadSessionDataForTab(...)
```

并保持：

- 创建命令立即返回；
- `monitorNavigationHydration` 继续监控 promise；
- callback 依赖加入 `waitForTabReady`。

## 4. 回归要求

至少覆盖：

1. EnsureBlankSurface 返回 ready=false；
2. ListTabs 在 controller build 前持续 ready=false；
3. ready 前 History/Transcript 调用次数=0；
4. ready=true 后才读取合法空历史；
5. hydrateError 未定义。

## 5. 已验收结果

```text
QUICK_NEW_SESSION_TEST=10/10 PASS
ZERO_SESSION_FIRST_OPEN=30/30 PASS
RAPID_NAVIGATION_ERROR_COUNT=0
FIRST_MESSAGE_TRANSITION=PASS
ZERO_SESSION_RESTART=10/10 PASS
OLD_SESSION_REGRESSION=5/5 PASS
OTHER_ERROR=NONE
```

哈希：

```text
HOTFIX_SHA256=5C5C6C26DA638680F63533CFC9A234A38F327697C8D1967ED3BEB4681A131447
SOURCE_PATCH_SHA256=AA892F1D19059941BB17BFFE373537B049C58FB67C08BE535DD747A774B8A7D4
```

最终：

```text
ROOT_CAUSE=CONFIRMED
PATCH_DEPLOYMENT=PASS
RUNTIME_ACCEPTANCE=PASS
EMPTY_SESSION_FIX=PASS
FINAL=PASS
```

## 6. 兼容入口

原独立技能仍保留：

```text
skills/reasonix-empty-session-race-repair
```

该目录作为历史兼容入口，不删除；新的统一入口为：

```text
skills/reasonix-fault-repair
```
