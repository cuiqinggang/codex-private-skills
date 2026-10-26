# Case A — Reasonix 空会话 hydration / ready 竞态

## 0. 案例状态与角色

```text
CASE_VERSION=1.0.0
MERGED_INTO=reasonix-fault-repair v1.1.0
ROOT_CAUSE=CONFIRMED
PATCH_SCOPE=FRONTEND_ONLY
PATCH_DEPLOYMENT=PASS
RUNTIME_ACCEPTANCE=PASS
CATALOG_VISIBLE=YES
```

固定分工：

- GPT：复核证据、判定根因、限定补丁范围、审核 diff、授权部署和定义验收门。
- Codex：本机检索、实现补丁、测试、生成 bundle、保存哈希、备份、部署与回传证据。
- `playwright-native-ai-browser`：GPT 与 Codex 的正式桥；必须复用 existing owner，不启动第二 owner、不建新 profile、不切 isolated mode、不走 CDP 旁路。

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

## 4. 为什么是 hotfix，而不是同版本重装

目标版本与 build 已固定为 Reasonix v1.38.7 / `036c7c50c5c154f747419aee6b75667f9044c8fa`。安装器携带的仍是原始缺陷 bundle；同版本重装只会恢复同一份缺陷代码，不能改变 hydration 早于 controller ready 的顺序。

因此最终选择：

```text
已确认前端根因
-> 只改 useController.ts
-> 生成并审核新 bundle
-> 保存原始/热修复 SHA-256
-> 单文件保护性替换
-> 运行验收
```

明确拒绝：删 SQLite、清 AppData、删除空会话、修改代理、升级/降级、用“先发一句话”绕过。

## 5. 主机安全策略阻断后的保护性部署

Codex 对 AppData 安装目录的直接写入被 host security policy 阻止后，没有提权绕过、没有关闭安全策略。处理方式是：

1. Codex 完成补丁、测试、bundle 和哈希审核。
2. 保存原 bundle，确认可回滚目标。
3. 用户在普通 PowerShell 7 中对唯一目标文件执行保护性替换。
4. 替换后立即回读 SHA-256，必须等于审核通过的 hotfix 哈希。
5. 哈希不符立即停止并回滚；哈希一致才进入运行验收。

```text
ORIGINAL_BUNDLE_SHA256=7E86A114D23662F691A1BB95F78E7EC4924441705ACE46CC221D9EB843BD8DBD
HOTFIX_BUNDLE_SHA256=5C5C6C26DA638680F63533CFC9A234A38F327697C8D1967ED3BEB4681A131447
SOURCE_PATCH_SHA256=AA892F1D19059941BB17BFFE373537B049C58FB67C08BE535DD747A774B8A7D4
```

## 6. 回归要求

至少覆盖：

1. EnsureBlankSurface 返回 ready=false；
2. ListTabs 在 controller build 前持续 ready=false；
3. ready 前 History/Transcript 调用次数=0；
4. ready=true 后才读取合法空历史；
5. hydrateError 未定义。

## 7. 已验收结果

```text
QUICK_NEW_SESSION_TEST=10/10 PASS
ZERO_SESSION_FIRST_OPEN=30/30 PASS
RAPID_NAVIGATION_TEST=20/20 PASS
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

## 8. 技能接入与 catalog 验收

成功链路：

```text
C:\Users\A\.codex\skills\reasonix-empty-session-race-repair
-> C:\Users\A\.agents\skills\reasonix-empty-session-race-repair (Junction)
-> C:\Users\A\AppData\Local\Programs\Reasonix\versions\v1.38.7\reasonix-cli.exe doctor capabilities
-> root ~/.agents/skills status=ok scope=global
-> reasonix-empty-session-race-repair [winner]
-> VERSION=1.0.0
```

对照成功样本：`playwright-native-ai-browser` 同样由 `~/.agents/skills` Junction 指向 C 盘正式源并成为 Reasonix winner。`command-pack-quality-gate` 不能直接照抄其 winner：它被 `<reasonix-home>/skills` 的旧版高优先级入口压制；本案例在全部高优先级扫描 root 中无同名冲突，因此 `.agents` Junction 成为 winner。

Reasonix runtime catalog 是动态解析器；`doctor capabilities` 会重新扫描并选 winner。global-workspace 的 `rebuild-skill-index.ps1` 只扫描 `<workspace>/.reasonix/skills`，不用于此次全局外部入口。

## 9. 兼容入口

原独立技能仍保留：

```text
skills/reasonix-empty-session-race-repair
```

该目录作为历史兼容入口，不删除；新的统一入口为：

```text
skills/reasonix-fault-repair
```

## 10. 下次复用入口

触发词：`空会话`、`加载会话历史失败`、`ready=false`、`workspace-not-ready`、`EnsureBlankSurface`、`EnsureBlankTab`。

命中后先验证 active build 和 hotfix 哈希，再检查 `controller ready -> hydration` 顺序；不要重新把合法 zero-message session 判为损坏。
