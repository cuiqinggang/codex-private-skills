---
name: local-ai-reality-foundation
description: 本地 AI 现实底座永久资产 v1.0.0。为 first-principles-physical-limit-convergence v4.0.0 的“虚拟成熟”提供持续更新的现实输入：Reality Fingerprint、Exact Reality Twin、浏览器/网络、本地 GPU/LLM、ComfyUI/视觉与本地自动化资产。它不是方法步骤，不拥有独立优化目标；只在环境漂移、缺证据或现实验证返回新 Reality Delta 时增量更新。
metadata:
  version: "1.0.0"
  status: ACTIVE_PERSISTENT_FOUNDATION
---

# 本地 AI 现实底座永久资产 v1.0.0

机器名：

`local-ai-reality-foundation`

## 1. 角色

这是“现实资产索引 + 更新协议”，不是第三步。

唯一消费者：

```text
first-principles-physical-limit-convergence@4.0.0
-> 虚拟成熟
```

唯一目的：

```text
减少重新认识现实环境的时间
提高 Virtual Reality 与 Physical Reality 的一致性
最终服务于 min(T_VALID)
```

## 2. 已认证 Reality 核心

### Host / Browser Reality Anchor
- 技能：`reality-execution-environment-anchor@1.3.0`
- Host R2 Fingerprint V3：
  `9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`
- Browser R3 Fingerprint：
  `9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd`
- Browser R3 real capture：PASS
- Environment-99：PASS

### Exact Reality Twin
- 组件：`exact-reality-digital-twin@1.3.0`
- 中文：现实执行环境精确数字孪生唯一版
- Legacy selftest：24/24 PASS
- Browser Twin tests：6/6 PASS
- Material Reality/Twin Delta：0
- Full Browser Twin：YES

## 3. 本地现实资产索引

以下项目属于“已知本地资产”。它们的实时运行状态不能由历史记录永久推断；使用前只做与当前任务相关的最小 readback。

### 浏览器自动化
- Playwright 专用浏览器
- 已知本地路径：`C:\AI\Playwright-Native-AI-Browser`
- 技能索引：`playwright-native-ai-browser`
- 角色：唯一成熟网页执行入口候选

### OpenHands Canvas
- 已知本地路径：`C:\AI\OpenHands-Canvas`
- 角色：本地浏览器/编码自动化候选资产
- 实时状态：VERIFY_ON_USE

### 本地长上下文 LLM / GPU
- Bonsai2-27B-256K 工作区：
  `C:\AI\Bonsai2-27B-256K`
- GPU：RTX 2080 Ti，现实总显存基线 22528 MiB
- 242K 冷现实有效基线（2026-09-22）：
  - prompt_ms = 1367320.567
  - e2e_ms = 1378701.719
  - POST_RUN_ADJUDICATION=PASS
- 角色：本地长上下文/低成本现实算力候选

### ComfyUI / H3 / 视觉生成
- MiniMax H3 工作区：
  `C:\AI\MiniMax-H3`
- Visual-Art-Engine：
  `C:\AI\Visual-Art-Engine`
- 角色：视觉生成、GPU 工作流、ComfyUI API 候选资产
- 实时模型/工作流状态：VERIFY_ON_USE

### 网络
- FlClash 常驻
- 硬约束：不得为了任务改变系统代理
- 虚拟网卡默认不作为必需条件
- 网络 Reality 只在当前任务实际依赖网络链路时增量读取

## 4. 更新协议

不允许每个任务重新全量采集。

默认：

```text
FOUNDATION_REUSE=YES
FULL_REANCHOR=NO
```

只在以下情况刷新相关域：

```text
FINGERPRINT_DRIFT
新硬件
驱动/Runtime/模型版本变化
浏览器/Profile/Auth/Network 发生关键变化
本地资产新增/移除
实际验证返回未建模 Reality Delta
用户明确要求重新锚定
```

更新必须：
1. 保存旧快照；
2. 新建版本/时间戳；
3. 只更新变化域；
4. 回读；
5. 不把 Shadow 假设写成 Reality。

## 5. 使用规则

虚拟成熟开始时只问：

```text
当前任务需要哪些现实资产？
这些资产是否有足够新且可信的 Reality 证据？
```

如果 YES：
直接复用。

如果 NO：
只补最少必要 Reality。

最终仍只比较：

```text
min(T_VALID)
```

## 6. 禁止事项

- 不把本技能升级成第三步骤；
- 不因为“数据更完整”而无条件全量扫描；
- 不修改 FlClash/系统代理；
- 不用历史“已运行”状态冒充当前运行状态；
- 不覆盖旧 Reality Snapshot；
- 不让 Foundation 自己决定业务方案。

## 7. 一句话

> **底座负责“现实是什么”，虚拟成熟负责“在这个现实里什么最快”，实际验证负责“现实里是不是真的这么快”。**
