# Reasonix 空会话竞态修复与保护性部署技能包

版本：1.0.0

这是对 2026-09-12 Reasonix v1.38.7 空会话偶发加载失败问题的完整复盘与可复用修复技能。

## 一句话根因

`EnsureBlankSurface/EnsureBlankTab` 在异步 controller build 完成前合法返回 `ready=false`，前端却立即调用 `loadSessionDataForTab`，导致 `TranscriptSnapshotForTab` 在 `tab.Ctrl==nil` 时返回 `workspace-not-ready`，随后被 UI 误映射为“加载会话历史失败”。

## 一句话补丁

在 blank tab/surface hydration 前：

```text
await waitForTabReady(meta.id)
-> 检查 navigation 仍 current
-> 再 loadSessionDataForTab
```

## 一句话流程

```text
用户复现
-> Codex 收集源码/运行证据
-> 专用 AI 浏览器把证据送 GPT
-> GPT 定根因/审补丁/授权
-> Codex 生成和验证补丁
-> 安全策略若拦安装目录，不绕过
-> 用户普通 PowerShell 单文件替换
-> 30+20+10+5 运行验收
-> FINAL=PASS
```

详见 `SKILL.md`。
