---
name: local-ai-reality-foundation
description: 本地 AI 现实底座永久资产 v1.1.0。版本化、任务后吸收的 Reality Foundation。每个完成任务都必须判断新现实事实是否能减少未来 min(T_VALID) 或避免重复现实采集/踩坑；只有有价值时才形成新版本。每版自包含完整当前资产、Reality Fingerprints、关键时间基线、约束、本版 delta、证据指针和上一版本。它不是方法步骤，只是“虚”的长期现实输入。
metadata:
  version: "1.1.0"
  status: ACTIVE_VERSIONED_FOUNDATION
---

# 本地 AI 现实底座永久资产 v1.1.0

## 1. 唯一目的

```text
MINIMUM_SUFFICIENT_REALITY_FOR_MIN_T_VALID
```

不是“信息越多越好”。

只有未来能：
- 缩短 T_VALID；
- 避免重复 Reality Anchor；
- 避免重复踩坑；
- 提高 Twin 对现实的必要一致性；

的信息才允许进入。

## 2. 任务后吸收门

每个实际完成任务都必须执行：

```text
FOUNDATION_ABSORB_CHECK
```

判断：

```text
NEW_FACT
-> 对未来 min(T_VALID) 有实际价值？
   NO  -> ABSORB=NO -> VERSION_UNCHANGED
   YES -> 最小化信息 -> 新 Foundation 版本
```

不能因为“新信息存在”就吸收。

## 3. 版本必须自包含

每个 Foundation 版本必须同时记录：

1. version；
2. previous_version；
3. 当前完整有效资产清单；
4. 当前 Reality Fingerprints；
5. 当前关键 T_VALID / 物理时间基线；
6. 当前硬约束；
7. 本版新增/修正 delta；
8. evidence pointers；
9. superseded 状态；
10. 更新时间。

因此：
- 看当前版本即可知道当前现实底座；
- 看 delta 可知道本版改变了什么；
- 看历史版本可回到任何旧台阶。

## 4. 版本规则

```text
PATCH = 数据/时间/状态现实增量
MINOR = 新现实域、新资产类别、新吸收能力
MAJOR = Foundation 合同发生不兼容变化
```

当前 v1.1.0 是 MINOR，因为增加了“任务后吸收 + 自包含版本”能力。

## 5. 当前完整资产

### Reality Anchor
- `reality-execution-environment-anchor@1.3.0`
- Host R2 Fingerprint V3：
  `9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`
- Browser R3 Fingerprint：
  `9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd`
- Environment-99：PASS

### Exact Reality Twin
- `exact-reality-digital-twin@1.3.0`
- Full Browser Twin：YES
- Legacy selftest：24/24 PASS
- Browser Twin tests：6/6 PASS

### 浏览器
- Playwright 专用浏览器：`C:\AI\Playwright-Native-AI-Browser`
- OpenHands Canvas：`C:\AI\OpenHands-Canvas`
- 实时状态：按任务 VERIFY_ON_USE

### 本地 GPU / LLM
- GPU：RTX 2080 Ti，现实总显存基线 22528 MiB
- Bonsai2：`C:\AI\Bonsai2-27B-256K`
- 242K 有效冷现实基线：
  - prompt_ms=1367320.567
  - e2e_ms=1378701.719
  - semantic validity=PASS
  - original validator false-negative 已被复核

### ComfyUI / 视觉
- MiniMax H3：`C:\AI\MiniMax-H3`
- Visual-Art-Engine：`C:\AI\Visual-Art-Engine`
- 只按具体任务补充现实状态

### 网络硬约束
- FlClash 常驻
- 禁止为了任务改变代理
- 不把虚拟网卡作为默认必需条件

## 6. 本版 delta

相对 v1.0.0：
- 新增任务后吸收门；
- 新增语义化版本规则；
- 新增“每版自包含当前全貌”要求；
- 明确 NO VALUE -> NO VERSION BUMP；
- 继续保留 v1.0.0 历史，不覆盖。

## 7. 使用边界

Foundation 只回答：

> 现实现在是什么？

它不决定：

> 应该怎么做？

方案仍由 first-principles v4.1 的“虚”决定。

## 8. 一句话

> **每完成一个任务，都问一次“这个现实新知识以后能不能让我更快？”能才吸收，不能就丢；吸收就形成一个完整、可追溯的新 Reality Foundation 版本。**
