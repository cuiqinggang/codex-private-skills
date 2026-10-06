CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"DOUYIN-ONECLICK-METHOD-V1-R0-F001","page_id":"EXTREME-TIME-V8-HIPE-FUSION-20261006","task_id":"DOUYIN-ONECLICK-METHOD-V1","node_id":"R0-VIRTUAL-MATURE","sequence":1,"state_code":20,"freeze_status":"READY_FROZEN","final_valid":"NO","t_valid_ms":null,"t_star_ms":null,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"1f536b256e82343d384ebe579d1eca7fa0df6e27","freeze_path":"workspaces/douyin-oneclick-method-v1/R0_VIRTUAL_FREEZE.md","next_node":"DOUYIN-ONECLICK-METHOD-V1-R1"}

# R0 VIRTUAL FREEZE — DOUYIN-ONECLICK-METHOD-V1

状态：READY_TO_REALITY  
Reality：NOT_STARTED

## 1. Solvability

基于公开成熟生态：

```text
SPEC_COMPLETE=YES
EVIDENCE_SEARCH_COMPLETE=YES
PHYSICALLY_ADMISSIBLE=YES
MATURE_DIRECT_SOLUTION=YES
MATURE_COMPONENT_CLOSURE=YES
MATURE_EXPLORATION_PROTOCOL=YES
ACCEPTANCE_VERIFIABLE=YES
```

冻结分类：

```text
SOLVABILITY=MATURE_DIRECT
WORLD_SOLVED=YES
```

因此禁止从零研究抖音协议。

## 2. Mature Cluster

A. public_api_direct
- 已存在成熟 Douyin/TikTok download API；
- 支持 URL 解析/直接 download；
- 零浏览器成功路径；
- 外部服务依赖。

B. content_downloader_local
- 成熟开源；
- 支持 Douyin 短链；
- direct API/signature + Playwright fallback；
- 本地适配成本高于 A，但更可控。

C. jiji_local
- 单作品、重试、browser fallback；
- 通用配置更重。

D. self_hosted_api
- 成熟、自托管；
- 本任务建设成本最高，不适合首个最快 VALID。

## 3. Jev one-call batch evidence

一个 Decisions API 请求同时判断：

### primary_route
```text
public_api_direct=0.71
content_downloader_local=0.27
jiji_local=0.02
self_hosted_api=0.00
winner=public_api_direct
confidence=0.61
```

### architecture
```text
ordered_fallback_chain=1.00
single_primary_only=0.00
confidence=1.00
```

### browser_role
```text
fallback_only=0.99
exclude_entirely=0.01
primary_path=0.00
confidence=0.99
```

解释：
- Primary 置信度 0.61 仅属中等，不允许单押 A；
- fallback architecture 与 browser fallback 的结论非常强；
- 因此冻结有序成熟路线，而不是单一路线。

## 4. Frozen architecture for R1

```text
Clipboard
→ CODE extract URL
→ ROUTE A: mature direct API
   → staged download
   → CODE ffprobe
   → PASS? atomic publish
   → FAIL? route B
→ ROUTE B: mature local content-downloader
   → staged result
   → CODE ffprobe
   → PASS? atomic publish
   → FAIL? browser fallback already supplied by mature component
→ final target ffprobe
→ FINAL_VALID
```

### Hot path

正常成功只走：

```text
clipboard
→ direct API
→ download
→ ffprobe
→ atomic publish
```

JEV 不进入下载 hot path。

## 5. 为什么这比旧方法快

旧方法：
- 第1轮先自研；
- Reality 后逐个发现分类/提交/等待问题；
- 每个问题一版。

R1 新方法：
- 首版已同时冻结：
  - URL extraction；
  - mature route；
  - fallback；
  - staging；
  - atomic publish；
  - ffprobe；
  - exactly-once；
  - performance timings；
  - failure evidence。

这些不再逐版补。

## 6. CODE / JEV / GPT mapping

### CODE
- clipboard read；
- URL regex；
- HTTP request/download；
- process execution；
- ffprobe；
- file/hash；
- staging；
- atomic replace；
- timing；
- exactly-once；
- final verification。

### JEV
R0 已用于：
- mature route finite Choice；
- architecture Choice；
- browser role Choice。

R1 hot path 默认不调用 Jev。

### GPT residual
仅在：
- mature candidate reality 与文档矛盾；
- 外部 route 行为不符合已知协议；
- fallback 组件无法适配 Windows one-click；
- 新 Failure Class 无法枚举时。

## 7. Parallelism

R1 实现准备阶段允许并行：
- desktop wrapper；
- verifier；
- logging/timing；
- fallback adapter preparation。

运行期：
- 真依赖不得伪并行；
- 若下载器已给出分离 AV，视频/音频独立下载可并行；
- 独立 verifier 可并行，但 FINAL_VALID 仍等全部必要验证完成。

## 8. Instrumentation from first Reality

至少记录：
- clipboard_extract；
- route_A_request；
- route_A_download；
- route_B_bootstrap/execute（仅发生时）；
- browser_fallback（仅发生时）；
- media_verify；
- atomic_publish；
- final_verify；
- total T_RUN_VALID；
- T_BUILD_VALID 当前累计。

## 9. R1 Freeze

```text
RUN_NODE=DOUYIN-ONECLICK-METHOD-V1-R1
FORMAL_REALITY_COUNT=0
NEXT=ONE formal Reality
```

正式 Reality 只启动一次。
若 R1 FAIL，保留证据回虚拟层整包修正；不得在同页微补丁重跑。
