---
name: reasonix-fault-repair
description: 统一诊断和处置 Reasonix 空会话竞态、startup_timeout/readiness 异常及历史间歇 React #185 transcript geometry 候选。出现加载会话历史失败、启动 30 秒超时、Maximum update depth、dispatchSetState 或 ResizeObserver stack 时使用；先确认构建身份、保存证据并有界复现，禁止对健康且未确认根因的构建打补丁。
metadata:
  version: 1.1.0
  chinese_name: Reasonix 故障诊断与成熟修复
  summary: 收录已验证案例、历史候选、诊断路径、最小修复策略、验收门与复发处置。
  tags:
    - reasonix
    - troubleshooting
    - startup-timeout
    - readiness-race
    - empty-session
    - hydration-race
    - electron
    - renderer
    - react-185
    - resize-observer
    - transcript-geometry
    - playwright-native-ai-browser
    - protective-deployment
    - skill-catalog
---

# Reasonix 故障诊断与成熟修复

## 1. 目标

本技能不是“某一个补丁”，而是 Reasonix 故障修复统一入口。遇到 Reasonix 异常时，优先搜索本技能，先匹配成熟案例，再决定是否需要新诊断。

固定原则：

1. 先保存成功态与失败现场，再修。
2. 先排除数据库、更新器、网络、版本指针、重复进程等基础原因，再进入代码层。
3. 不因为报错文案相似就把不同故障混为一类。
4. 只修真正根因，避免清缓存、重装、删库等扩大修改面操作。
5. GPT 负责根因判断和补丁范围；Codex 负责本机检索、修改、测试、备份和部署。
6. 所有写入动作前备份并回读；成功态恢复后，不为“理论完美”扰动当前可用系统。
7. 浏览器协作固定复用 `playwright-native-ai-browser` existing owner；不得启动第二 owner、另建 profile、切 isolated mode 或绕过正式入口。
8. 同版本安装包重装不能替换已经确认缺陷的同版本 bundle；根因已确认且补丁已审核时，使用可回滚、单文件、哈希校验的 hotfix。

## 2. 当前成熟案例与历史观察

### Case A：新建空会话偶发“加载会话历史失败”

入口：`cases/empty-session-race.md`

核心根因：

```text
EnsureBlankSurface / EnsureBlankTab
        ↓
visible tab 已返回，但 controller ready=false
        ↓
前端提前 loadSessionDataForTab
        ↓
TranscriptSnapshotForTab -> workspace-not-ready
        ↓
UI 映射为“历史加载失败”
```

最终修复：前端 hydration 在 controller ready 前禁止读取会话数据；等待 `waitForTabReady` 后再加载。

完整执行链：GPT 负责证据复核、根因与补丁范围决策；Codex 负责检索、实现、测试、备份、部署与回传。浏览器桥复用既有 `playwright-native-ai-browser` owner。主机安全策略阻止 Codex 写 AppData 后，不绕过策略，由用户在普通 PowerShell 7 中执行已审核的单文件保护性替换并回读哈希。

为什么选择 hotfix：目标 Reasonix v1.38.7 安装器与当前缺陷 bundle 同版本，同版本重装只会恢复原始缺陷文件；已确认根因位于前端 hydration 顺序，故采用最小前端 hotfix，而不是清缓存、删库或同版本重装。

已验证热修复 SHA-256：

```text
5C5C6C26DA638680F63533CFC9A234A38F327697C8D1967ED3BEB4681A131447
```

状态：`PASS / RUNTIME_ACCEPTANCE_PASS`

运行验收：`10/10` 快速新建、`30/30` 零消息首次打开、`20/20` 快速导航且错误数为 0、`10/10` 重启后零消息会话、`5/5` 旧会话回归；首条消息转换 PASS。

技能接入：

```text
C:\Users\A\.codex\skills\reasonix-empty-session-race-repair
  -> C:\Users\A\.agents\skills\reasonix-empty-session-race-repair (Junction)
  -> reasonix-cli.exe doctor capabilities
  -> winner=~/.agents/skills/reasonix-empty-session-race-repair/SKILL.md
  -> catalog visible / VERSION=1.0.0
```

### Case B：Reasonix 启动时报 startup_timeout / startup_failed

入口：`cases/startup-readiness-timeout.md`

本次最终分类：

```text
TRANSIENT_COLD_START_ANOMALY
```

失败现场核心时间线：

```text
backend ready
  ↓
desktop/domReady timeout
  ↓
window native-call timeout
  ↓
rendererAttached timeout
  ↓
迟到生命周期响应被记录为 orphan-response
  ↓
shell readiness timeout
  ↓
launcher ~31s 判定 startup_failed
```

关键判定：

- backend 实际已 Ready；
- SQLite quick_check=ok；
- updater 非根因；
- 无端口冲突；
- 无重复实例证据；
- 空会话补丁哈希未漂移；
- 后续两次完整冷启动均 PASS；
- 因此当次不打代码补丁。

两次恢复验证：

```text
RUN1 backend_ready=2524ms dom_ready=3643ms renderer_attached=6241ms app_usable=9836ms
RUN2 backend_ready=2344ms dom_ready=3377ms renderer_attached=5122ms app_usable=6601ms
```

同时发现潜在设计弱点：

```text
TIMEOUT_BUDGET_INVERSION=YES
LATE_RESPONSE_VALID=YES
```

但只有在同类 readiness 失败连续两次可复现时，才重新打开代码补丁设计。

状态：`PASS / HEALTHY / NO_PATCH_REQUIRED`

### Case C：React #185 / transcript geometry feedback 候选

入口：`cases/react185-transcript-geometry-loop.md`

适用于 `Minified React error #185` / `Maximum update depth exceeded`，特别是 stack 含 `dispatchSetState` 与 `ResizeObserver.<anonymous>`。

固定处理：

1. 先确认 active version 与 exact renderer bundle。
2. 重启前保存完整 stack、renderer/shell logs、会话与窗口状态。
3. 不因大量 `IsMainWindowMaximised` breadcrumbs 直接判定 maximize loop；记录案例中的 setter 有同值保护。
4. 将 `TranscriptProjectionView`、`onGeometryWillChange`、`beginAnchorRestore`、`settleGeometry`、`forceRender`、`revision` 作为静态候选链核查。
5. 只执行一轮有界复现；不能复现时保持成功态，不打补丁。
6. 只有 active build 真实复现且 ResizeObserver → revision → render/layout → same target resize 闭环成立，才允许补丁评审。

已记录状态：`HISTORICAL_INTERMITTENT / CURRENT_HEALTHY / REACT185_NOT_REPRODUCED / ROOT_CAUSE_NOT_CONFIRMED / NO_CODE_CHANGE`

## 3. 快速路由

出现以下现象时：

### 新建空会话失败，但发第一条消息后恢复

优先匹配 Case A。

### 启动窗口显示：

```text
startup_failed
startup_timeout
startup was not verified within 30 seconds
Reasonix did not become ready within 30 seconds
```

优先匹配 Case B。

### 出现 React #185 / Maximum update depth，stack 指向 ResizeObserver

优先匹配 Case C。先确认 active bundle 并保存原始 stack；若一轮受控复现未出现故障，保留健康构建，不为静态候选打补丁。

第一步不是重装，而是确认：

```text
backend_started?
backend_ready?
domReady?
rendererAttached?
orphan-response?
SQLite quick_check?
updater state?
duplicate process?
```

## 4. 启动故障复发时的固定处理顺序

```text
保留失败现场
↓
确认版本与补丁哈希
↓
读取 desktop-shell logs
↓
确认 backend 是否 Ready
↓
确认 renderer/domReady/native-host 握手
↓
确认 updater / SQLite / 重复进程 / 端口
↓
完整结束 Reasonix 失败进程树
↓
确认进程数=0
↓
等待约5秒
↓
正常冷启动并计时至少60秒
```

如果恢复：

```text
TRANSIENT_COLD_START_ANOMALY
NO CODE CHANGE
```

如果一次失败一次成功：

```text
INTERMITTENT_READINESS_RACE
```

如果连续两次均复现：

```text
DETERMINISTIC_READINESS_BUG
```

此时才允许进入最小 readiness 补丁设计。

## 5. 禁止默认操作

除非证据明确支持，不得默认：

- 重装 Reasonix；
- 升级/降级；
- 清整个 AppData；
- 删除 SQLite；
- 重建历史会话；
- 修改系统代理或 FlClash；
- 回滚已验收空会话补丁；
- 把所有 timeout 粗暴改成 60/120 秒；
- 删除 lock 文件而未先确认相关进程已退出。

## 6. Readiness 设计原则

若未来 Case B 稳定复现，补丁应遵循：

```text
backend alive + backend ready + renderer handshake 有进展
        ↓
保持 STARTING，不直接 FAILED
```

生命周期迟到响应若仍属于当前 startup generation / renderer / correlation，应作为 `late-but-valid lifecycle response` 接纳，而不是简单丢为 orphan。

外层 launcher deadline 与内层 domReady/native-call/rendererAttached timeout 必须统一预算，避免 timeout budget inversion。

## 7. 证据与验收

每次修复至少保存：

- 版本号；
- 进程树；
- 关键日志；
- SQLite quick_check；
- updater 状态；
- 关键文件 SHA-256；
- 修改前后 diff；
- 冷启动时间线；
- 回归结果。

详见：

- `DECISION-TREE.md`
- `ACCEPTANCE.md`
- `RECURRENCE-RUNBOOK.md`
- `cases/empty-session-race.md`
- `cases/startup-readiness-timeout.md`
- `cases/react185-transcript-geometry-loop.md`
- `CHANGELOG.md`
- `USAGE-LOG.md`
- `ACCEPTANCE.html`

## 8. 版本与兼容

- 统一入口版本：`reasonix-fault-repair v1.1.0`。
- 原独立案例 `reasonix-empty-session-race-repair v1.0.0` 保留，不删除、不覆盖，继续作为历史兼容入口。
- GitHub 私库用 `reasonix-fault-repair-v1.0.0` 标签保留升级前快照；v1.1.0 只发布本技能包及其验收资产。
- 下次出现空会话竞态，先读 `cases/empty-session-race.md`，不得重新从“0-byte JSONL 损坏”开始。
