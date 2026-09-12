# Case Study — Reasonix v1.38.7 Empty Session Race

## 1. 用户最初如何判定问题

用户并不是从源码出发，而是从真实 UI 行为发现：

- 连续新建会话时，有时正常，有时立即出现“暂时无法加载会话”。
- 某些空会话失败，但发送第一条消息后又能正常回答。
- 同一机器、同一模型、同一网络下结果不稳定。

这首先说明问题具有明显的“时序性”，而不是稳定的数据损坏。

## 2. 初始证据阶段

对失败空会话检查发现：

- sessionPath 已存在。
- meta 已存在且合法。
- display-index 已存在且合法。
- lease 已存在。
- 主 JSONL 为 0 字节。

成功会话在发送首条消息后会出现完整 JSONL/events/turns/projection。

最初一度怀疑：

- empty transcript 是否被误判。
- missing sidecar 是否被误判。
- nil slice / empty page 是否触发失败。

这是合理的第一候选，但必须继续复核源码，而不能直接修改。

## 3. GPT 第一轮技术决策

GPT initially 将候选压缩到 empty-session reader contract。

随后要求对正式源代码做精确复核，而不是继续猜测。

## 4. 源代码复核翻转结论

Codex 复核确认：

- 0-byte JSONL 合法。
- missing/empty event log 合法。
- missing projection checkpoint 可选。
- empty snapshot 返回 `[]`。
- 已有 `TestHistorySliceColdEmptySession`。

于是原“后端 empty reader”假设被排除。

这是本案例最重要的方法论：

> **高质量调试不是坚持第一假设，而是用源码测试把错误假设及时推翻。**

## 5. 真正根因

前端：

```text
handleNewTab
-> blank navigation
-> ensureBlankSurface
```

后端会在：

```text
startTabControllerBuild
```

尚未结束时先返回 visible tab：

```text
ready=false
```

原前端马上 hydrate：

```text
loadSessionDataForTab
```

此时：

```text
tab.Ctrl == nil
```

于是 snapshot API 返回：

```text
workspace-not-ready
```

UI 最后展示为历史加载失败。

controller build 快则不复现，慢则复现，因此“偶发”。

## 6. GPT 审核与授权

Codex 把精确源码复核和最小补丁通过专用 AI 浏览器提交 GPT。

GPT 给出：

```text
PATCH_REVIEW_DECISION=APPROVE
ROOT_CAUSE_AGREEMENT=YES
PATCH_SCOPE=FRONTEND_ONLY
DEPLOYMENT_AUTHORIZED=YES
REQUIRED_CHANGES=NONE
```

之后 Codex 才进入部署。

## 7. 为什么 AI 浏览器已经打开仍继续使用

本工作流不要求每次重新打开浏览器。

相反，成熟做法是：

```text
已有 owner
-> 复用 owner
-> 保持登录态和会话上下文
-> query/send/wait_extract
```

本案例明确：

```text
REUSED_EXISTING_OWNER=True
SECOND_OWNER_STARTED=False
```

这保证：

- 不丢 GPT 登录态。
- 不丢当前根因分析会话。
- 不开第二套浏览器争抢资源。
- Codex 始终只负责执行。

## 8. 用户一度考虑重装

当修复已经推进到后期时，用户提出：

> 与其这么费劲修，不如重新完整安装。

这是一个合理的成本判断问题。

如果当时根因仍未知，保护性重装可能更划算。

但实际已经到：

```text
根因已确认
补丁已审核
测试已通过
bundle 已生成
hash 已冻结
```

只差安装目录单文件写入。

此时同版本重装反而更差，因为：

- 重装不会改变同一版本里的竞态源码。
- 会引入更多安装变量。
- 单文件补丁可精确回滚。

因此 GPT 最终改判：

```text
HOTFIX > SAME-VERSION REINSTALL
```

## 9. 主机安全策略阻断

Codex 无法覆盖：

```text
AppData\Local\Programs\Reasonix\...\index-QvpapSZM.js
```

但补丁文件、备份和源码 patch 都已生成。

正确决策不是绕过主机保护，而是：

```text
Codex 停止
-> 保留所有交付物
-> 用户普通 PowerShell 执行单文件替换
```

## 10. 最终结果

部署哈希正确。

用户手工验收：

```text
10/10 快速新建
30/30 空会话首次打开
快速导航错误数 0
第一条消息 PASS
10/10 重启空会话
5/5 旧会话
OTHER_ERROR=NONE
```

因此最终：

```text
FINAL=PASS
```
