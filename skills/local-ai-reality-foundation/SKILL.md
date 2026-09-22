---
name: local-ai-reality-foundation
description: 本地 AI 现实底座永久资产 v1.1.2。版本化、任务后吸收的 Reality Foundation。每个完成任务都必须判断新现实事实是否能减少未来 min(T_VALID) 或避免重复现实采集/踩坑；只有有价值时才形成新版本。每版自包含完整当前资产、Reality Fingerprints、关键时间基线、约束、本版 delta、证据指针和上一版本。它不是方法步骤，只是“虚”的长期现实输入。
metadata:
  version: "1.1.2"
  status: ACTIVE_VERSIONED_FOUNDATION
---

# 本地 AI 现实底座永久资产 v1.1.2

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

当前 v1.1.2 是 MINOR，因为增加了“任务后吸收 + 自包含版本”能力。

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



### Codex 执行现实约束

以下均为真实执行中已经观察到、会导致返工的现实约束；虚拟成熟必须在冻结前读取并规避：

```text
CODEX_EXECUTOR=REQUIRED_FOR_DEFAULT_GPT_CODEX_CLOSED_LOOP

OBSERVED_CONSTRAINT_001
= 在 workspace-write / 当前安全策略下，
  向 C:\Users\A\AppData\Local\Temp 写入或覆盖待执行 .ps1
  可能被 Codex 安全策略拒绝。
ACTION
= 默认禁止把可执行脚本 staging 到 AppData\Local\Temp；
  优先使用工作区内已冻结产物，或从不可变 Git 对象直接流式送入解释器。

OBSERVED_CONSTRAINT_002
= PowerShell 双引号 Here-String（@"..."@）会在任务文本送给 Codex 之前
  展开 $变量、$null、$LASTEXITCODE 等 PowerShell 表达式，
  可破坏内嵌冻结命令。
ACTION
= 含 PowerShell 代码的 Codex prompt 默认使用单引号 Here-String（@'...'@）
  或其他经过字节/字符串等价验证的 literal-safe 传输；
  冻结前必须做 SHELL_INTERPOLATION_SAFE 验收。

OBSERVED_CONSTRAINT_003
= 当前非管理员 PowerShell 7 环境中，
  w32tm /query /source 已真实返回 0x80070005 Access Denied。
ACTION
= 不得把 w32tm source query 设为主计时硬依赖。
  有效工作时长使用 System.Diagnostics.Stopwatch 单调计时；
  wall-clock timestamp 仅作审计坐标，时间源查询失败不得阻塞任务。

OBSERVED_CONSTRAINT_004
= Codex 启动时可能出现部分 Skill YAML/frontmatter 加载错误、
  model refresh timeout、Skill description budget warning。
ACTION
= 对自包含冻结合同，明确禁止额外 Skill 读取；
  这些启动诊断只在确实影响任务有效性时升级为 Reality Delta。
```

原则：

```text
已知现实约束
-> 虚阶段预检
-> 不兼容候选直接淘汰
-> 不允许把已知必失败路径再次冻结到“实”
```



### Codex Git / 沙箱现实约束增量

```text
OBSERVED_CONSTRAINT_005
= 在当前 Codex v0.155.1 + workspace-write 现实执行中，
  git fetch origin <branch>
  已真实失败：
  cannot open '.git/FETCH_HEAD': Permission denied

CLASSIFICATION
= LOCAL_GIT_METADATA_WRITE_PERMISSION
!= NETWORK_TRANSPORT_FAILURE

ACTION
= “实”的启动关键路径默认禁止依赖 git fetch / 写 FETCH_HEAD。
  GitHub 继续作为 SHARED_FACT_SOURCE（共同事实源），
  但不作为 Codex 现实执行的必经启动传输层。

DEFAULT_REAL_HANDOFF
= GPT 直接把自包含冻结合同交给 Codex
  -> Codex 本机执行
  -> Codex 返回现实证据
  -> GPT 写正式结果到 GitHub
  -> GPT 重新读取/确认

只有当虚阶段已经现实证明该 Codex 沙箱允许所需 Git 元数据写入时，
才允许把相应 git 写操作重新放进“实”的关键路径。
```

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
