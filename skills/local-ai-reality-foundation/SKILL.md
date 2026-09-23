---
name: local-ai-reality-foundation
description: 本地 AI 现实底座永久资产 v1.1.4。版本化、任务后吸收的 Reality Foundation；本版吸收 Codex Windows 子进程创建 1344 现实差异，以及下载工具存在性事实。
metadata:
  version: "1.1.4"
  status: ACTIVE_VERSIONED_FOUNDATION
---

# 本地 AI 现实底座永久资产 v1.1.4

## 1. 唯一目的

```text
MINIMUM_SUFFICIENT_REALITY_FOR_MIN_T_VALID
```

只吸收未来能够缩短 T_VALID、避免重复 Reality Anchor、避免重复踩坑或提高 Twin 必要一致性的现实事实。

## 2. 任务后吸收门

```text
NEW_FACT
-> 对未来 min(T_VALID) 有实际价值？
   NO  -> ABSORB=NO -> VERSION_UNCHANGED
   YES -> 最小化信息 -> 新 Foundation 版本
```

## 3. 版本规则

```text
PATCH = 数据/时间/状态现实增量
MINOR = 新现实域、新资产类别、新吸收能力
MAJOR = Foundation 合同发生不兼容变化
```

v1.1.4 = PATCH。

## 4. 当前完整资产

### Reality Anchor
- `reality-execution-environment-anchor@1.3.0`
- Host R2 Fingerprint V3: `9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`
- Browser R3 Fingerprint: `9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd`
- Environment-99: PASS

### Exact Reality Twin
- `exact-reality-digital-twin@1.3.0`
- Full Browser Twin: YES
- Legacy selftest: 24/24 PASS
- Browser Twin tests: 6/6 PASS

### 浏览器
- Playwright: `C:\AI\Playwright-Native-AI-Browser`
- OpenHands Canvas: `C:\AI\OpenHands-Canvas`
- 状态：VERIFY_ON_USE

### 本地 GPU / LLM
- GPU: RTX 2080 Ti
- VRAM baseline: 22528 MiB
- Bonsai2: `C:\AI\Bonsai2-27B-256K`
- 242K cold baseline: prompt_ms=1367320.567; e2e_ms=1378701.719; semantic validity=PASS

### ComfyUI / 视觉
- MiniMax H3: `C:\AI\MiniMax-H3`
- Visual-Art-Engine: `C:\AI\Visual-Art-Engine`

### 下载工具现实事实（2026-09-23）

上一轮真实执行已成功运行 Get-Command 检查并确认：

```text
aria2c=AVAILABLE_OBSERVED
hf=AVAILABLE_OBSERVED
curl.exe=AVAILABLE_OBSERVED
gh=UNKNOWN_NOT_REQUIRED_FOR_CORE_DOWNLOAD_ROUTE
```

同一轮还确认：
- C: 可用空间约 360 GB；
- 现有 Git proxy endpoint = `http://127.0.0.1:7890`；
- 对目标 Hugging Face 官方源与 hf-mirror 的小流量访问成功；
- 不因此授权改变任何代理设置。

工具**精确版本仍需在可创建子进程的现实执行通道中 VERIFY_ON_USE**。

## 5. Codex 执行现实约束

```text
OBSERVED_CONSTRAINT_001
= AppData\Local\Temp 可执行 .ps1 staging 可能被拒绝。
ACTION
= 不把可执行 runner staging 到该目录。

OBSERVED_CONSTRAINT_002
= PowerShell 双引号 Here-String 有变量提前展开风险。
ACTION
= 使用 literal-safe 传输。

OBSERVED_CONSTRAINT_003
= 非管理员 w32tm /query /source 可 Access Denied。
ACTION
= 时长使用 System.Diagnostics.Stopwatch。

OBSERVED_CONSTRAINT_004
= Skill load/model refresh/budget warning 可能出现。
ACTION
= 只有影响任务有效性才升级为 Reality Delta。

OBSERVED_CONSTRAINT_005
= workspace-write 下 git fetch 可因 .git/FETCH_HEAD Permission denied 失败。
ACTION
= REAL 启动关键路径不依赖 git fetch。

OBSERVED_CONSTRAINT_006
= 冻结只读探针可能出现“完整有效 stdout + nonzero exit”。
ACTION
= 只读无副作用探针优先判断完整语义证据，exit 保留为诊断。

OBSERVED_CONSTRAINT_007
= Codex v0.155.1 在 Windows 上现实出现默认命令宿主创建子进程失败：
  SetTokenInformation(TokenDefaultDacl) failed: 1344。
  同一现实会话中，普通沙箱 PowerShell 启动失败后，另一个已授权执行通道成功启动 PowerShell 7.6.6，
  并继续执行 aria2c/hf/curl 的只读检查。
CLASSIFICATION
= CODEX_WINDOWS_PROCESS_SPAWN_CHANNEL_FAILURE
!= DOWNLOAD_TOOL_MISSING
!= DOWNLOAD_ROUTE_FAILURE

ACTION
= 任何 REAL 任务在把“命令无法启动”归因给目标工具前，先区分 executor-entry failure。
= workspace-write 现实任务默认不得从用户 Home（C:\Users\<user> / ~）作为工作目录启动；优先使用任务专属窄目录（例如 C:\AI\<Task>）。
= 公开 Codex Windows 1344 复现已显示：Home 工作目录可导致过多 write roots / 默认 DACL 膨胀，窄项目目录可消除 1344。
= 若窄目录仍返回同类 1344，再允许按冻结合同仅重试一次已经存在、已授权、已证明可工作的替代执行通道。
= 若仍不能创建进程，则 STOP，返回最小 Reality Delta。
= 不允许把 1344 错误解释成 aria2/hf/gh 不存在。
```

## 6. 网络硬约束
- FlClash 常驻。
- 禁止为了任务改变代理。
- 不把虚拟网卡作为默认必需条件。

## 7. 本版 delta

相对 v1.1.3：

```text
ADD OBSERVED_CONSTRAINT_007
ADD download tool presence facts
NO METHOD CHANGE
NO HARDWARE FINGERPRINT CHANGE
```

## 8. 使用边界

Foundation 只回答“现实现在是什么”，不决定“应该怎么做”。

方案仍由极限短时间引擎的 VIRTUAL 阶段决定。
