# Bonsai 2 27B PQ2_0 — 256K 命令包静态审核 v2

状态：PASS / READY_TO_RESUME_FROM_PRIOR_BLOCKER

## 已验证阻断

第一次真实执行已证明：
~~~text
Phase A=PASS
setup.ps1 does not implement BONSAI_SKIP_GGUF
setup.ps1:373 unconditionally calls Download-GgufModel
setup_ps1_executed=false
model_download_started=false
~~~

v2 不降低门禁，而是删除错误依赖：不再执行 setup.ps1。

## 上游 runtime 证据

固定 release：
~~~text
prism-b10709-9a9394a
~~~

本机 CUDA driver reported=13.1；固定 setup.ps1 的选择逻辑映射到 cuda-12.4。

官方 release asset 已核对：

~~~text
llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip
bytes=253442371
sha256=f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9

cudart-llama-bin-win-cuda-12.4-x64.zip
bytes=391443627
sha256=8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6
~~~

因此 runtime-only direct bootstrap 是对固定上游 setup Phase 8 的等价提取，不引入 stock llama.cpp。

## 下载方法

~~~text
RUNTIME_ASSETS_USE_SPEED_PROBE=PASS
MODEL_USES_SPEED_PROBE=PASS
PARALLEL=PASS
RESUME=PASS
KEEP_PARTIAL=PASS
MONITOR=PASS
SHA256_RUNTIME_REQUIRED=PASS
MODEL_LOCAL_SHA256_REQUIRED=PASS
NO_PROXY_CHANGE=PASS
NO_SYSTEM_INSTALL=PASS
~~~

## 256K 合同

~~~text
TARGET_CONTEXT=262144
PROMPT_TARGET=240K..245K
KV4=ON
THINKING=OFF
SPECULATIVE=OFF
TEXT_ONLY=YES
NO_AUTO_128K=YES
T_PHY=OFF
~~~

## 关键修正：thinking

固定 upstream 27B start_llama_server.ps1 会重新生成 27B ServerArgs，因此仅依赖脚本前面的 reasoning 参数不可靠。v2 要求通过 trailing args 显式传：
~~~text
--reasoning-budget 0
--reasoning-format none
--chat-template-kwargs {"enable_thinking":false}
~~~

并以实际 /props + 响应行为验证。

## PowerShell / Git

仍受：
~~~text
skills/powershell-reliability-guard/SKILL.md
~~~
约束。

~~~text
PWSH7=YES
NO_EXECUTIONPOLICY_BYPASS=YES
NO_GIT_ADD_DOT=YES
NO_FORCE_PUSH=YES
NO_RESET_HARD=YES
REMOTE_VERIFY_REQUIRED=YES
AUTO_NEXT_OPTIMIZATION=NO
~~~

## 结论

~~~text
V1_BLOCKER=RESOLVED_IN_PLAN
V2_STATIC_AUDIT=PASS
ACTUAL_RUNTIME_DOWNLOAD=NOT_STARTED_UNDER_V2
ACTUAL_MODEL_DOWNLOAD=NOT_STARTED_UNDER_V2
NEXT_ACTION=CODEX_READ_V2_AND_RESUME
~~~
