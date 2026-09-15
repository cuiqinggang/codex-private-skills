# Case: React #185 Transcript Geometry Loop Candidate

## 当前状态

- FINAL_STATUS=PASS
- CURRENT_STATE=HEALTHY
- REACT_185_REPRODUCED=NO
- LOOP_CONFIRMED=NO
- ROOT_CAUSE_CONFIRMED=NO
- GEOMETRY_OSCILLATION=UNKNOWN
- PATCH_APPLIED=NO
- 决策：NO CODE CHANGE

Historical intermittent React #185 incident; current build healthy; strong static candidate retained; no code change justified.

## 1. 用户可见症状

- `Minified React error #185`
- `Maximum update depth exceeded`

## 2. 原始 stack 线索

`getRootForUpdatedFiber`、`enqueueConcurrentHookUpdate`、`dispatchSetStateInternal`、`dispatchSetState`、`ResizeObserver.<anonymous>`。这优先指向 ResizeObserver callback 发起的状态更新，但不能单独确定 setter。

## 3. 初步误导项

breadcrumbs 大量重复：

```text
[bridge] window IsMainWindowMaximised
[bridge] window IsMainWindowMaximised done
```

现归类为 resize/focus 事件风暴伴随信号，不是直接根因证据。

## 4. 已排除的直接根因

`setMainWindowMaximised` 存在同值返回原状态的保护，因此不能作为现有证据下的直接无限更新根因。

## 5. 当前生产 build

- Reasonix v1.38.7
- Active bundle: `index-QvpapSZM.js`
- SHA256: `5C5C6C26DA638680F63533CFC9A234A38F327697C8D1967ED3BEB4681A131447`

## 6. H/M 调查

截图疑似显示 `index-QvpapSZH.js`，实际系统限定 Reasonix 安装、实例和修复目录未找到 H 文件，也没有 build swap 证据。除非后续出现反证，当前按截图字符误读处理。

## 7. 静态高概率候选

```text
TranscriptProjectionView
-> ResizeObserver(.transcript__projection)
-> onGeometryWillChange
-> beginAnchorRestore
-> setRevision(n => n + 1)
-> render / layout / placements
-> same projection may resize
-> ResizeObserver
```

次要分支：

```text
onGeometryChange
-> settleGeometry
-> invalid / blank geometry
-> forceRender
-> revision++
-> render / layout
```

两条链均为静态候选。“可能 resize/重入”不得改写为已观察事实。

## 8. 关键限制

- LOOP_CONFIRMED=NO
- REVISION_BURST=UNKNOWN
- BEGIN_ANCHOR_RESTORE_REENTRANT=UNKNOWN
- FORCE_RENDER_REENTRANT=UNKNOWN
- GEOMETRY_OSCILLATION=UNKNOWN
- LaTeX/Unicode warning 没有布局闭环证据，不能作为根因。

不得把候选写成最终根因。

## 9. 实际压力测试

Windows UI Automation + User32 + Visual Recovery 完成：

- TEST A IDLE: PASS
- TEST B ORIGINAL SESSION: PASS
- TEST C SCROLL STRESS: PASS
- TEST D WINDOW RESIZE: PASS
- TEST E MAXIMIZE/RESTORE: PASS
- TEST F SIDEBAR: PASS
- TEST G COMBINED STRESS: PASS
- TEST H CONTROL SESSION: PASS
- TEST I NEW SESSION + SEND: PASS

A-I 9/9 PASS，React #185 未复现，无 renderer crash，空会话补丁无回归。

## 10. 当前决策与复发入口

NO CODE CHANGE。不得修改 Reasonix、production bundle、SQLite、updater、startup timeout、代理或网络。

触发关键词：`React #185`、`Maximum update depth`、`ResizeObserver.<anonymous>`、`TranscriptProjectionView`、`beginAnchorRestore`、`settleGeometry`、`revision burst`。

下次命中时，先读本案例，重启前保存 stack/log/window/session 证据，确认 active bundle，只做一轮有界复现。若同一 M build 再次真实复现，且 stack 和运行时证据证明 ResizeObserver → revision → render/layout → same target resize：

- REOPEN_CASE=YES
- PATCH_REVIEW_REQUIRED=YES

否则保持 ROOT_CAUSE_CONFIRMED=NO。

证据目录：`C:\Users\A\Documents\Codex\Reasonix-React185-Diagnosis-20260915-051142`
