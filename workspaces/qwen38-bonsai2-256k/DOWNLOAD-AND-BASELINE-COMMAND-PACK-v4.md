# Bonsai 2 27B PQ2_0 — 256K 下载与现实基线命令包 v4

状态：EXECUTED / RESULT=results/20260920-014431 / RETURN_TO_GPT

## 0. 继承与唯一变化

继承 v1 Phase A PASS（664a2289）、v2 direct transport BLOCKED（a4ba30d6）、v3 drift PASS 与 pre-execution policy block（8a293bb4a459436893b9d8e6ce1187e0497ca529）。

REMOVE_HKCU_DISCOVERY=YES；ATOMIC_PROXY_DISCOVERY=YES。v3 第 3–5 节由本文件第 1–3 节完全替代；v3 其余冻结合同、版本、资产、散列、下载算法、256K 测试和停止规则保持不变。

## 1. 永久排除 HKCU

禁止读取或间接重建 HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings，包括 reg query、Get-ItemProperty、其他 registry API、UI automation、配置/API/脚本绕过。不得绕过 managed safety policy。

WINDOWS_HKCU_PROXY_SOURCE=POLICY_BLOCKED_EXCLUDED

## 2. 来源必须独立原子执行

禁止把多个来源组合进同一个 PowerShell composite command。每个来源独立执行并独立捕获 started、exit_code、stdout、stderr、policy_status。raw endpoint/credential 不得持久写入 GitHub evidence。

### 2.1 Git proxy（只读）

以下三条分别执行：

- git config --show-origin --get-all http.proxy
- git config --show-origin --get-all https.proxy
- git config --show-origin --get-regexp 'http\..*proxy|https\..*proxy'

policy 拒绝：SOURCE_GIT_PROXY=POLICY_BLOCKED，不绕过；无配置：SOURCE_GIT_PROXY=NONE；明确代理只在当前进程内保存 normalized endpoint，credentials 脱敏且不得入 evidence。

### 2.2 WinHTTP（只读）

单独运行 netsh winhttp show proxy。policy 拒绝：SOURCE_WINHTTP=POLICY_BLOCKED，不绕过；direct：SOURCE_WINHTTP=NONE；明确 proxy 可作为既有 candidate。

### 2.3 FlClashCore listener（只读）

只按 FlClashCore 精确 PID 过滤仅属于该 PID 的 LISTEN socket。禁止扫描全部端口、猜 7890/7891 或任何端口、读 FlClash 配置、读 HKCU、切节点/模式/TUN、改配置。

policy 拒绝：SOURCE_FLCLASH_LISTENER=POLICY_BLOCKED，停止该来源且不绕过。真实 loopback listener 属于进程直接证据。host/port 只在当前进程内；evidence 只记录 source=FlClashCore_process_listener、candidate_count、loopback、endpoint_fingerprint=SHA256(normalized_endpoint)。

### 2.4 Approval storm 防护

任一独立命令被 managed safety review 拒绝后，该来源立即标记 POLICY_BLOCKED；不得重发同一命令、不得用语义等价命令重试、不得请求第二次 approval，直接进入下一独立来源。Git proxy value 来源已冻结为 GIT_PROXY_SOURCE_STATUS=POLICY_BLOCKED_SENSITIVE_VALUE，不得解释为 NONE。

## 3. 小流量验证与同链复用

固定 asset：llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip；bytes=253442371；sha256=f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9。

只对真实候选用 curl --proxy <in-memory-existing-endpoint> 请求 Range 0-1048575，timeout<=20s。PASS 必须 TLS/HTTP 成立、HTTP 2xx/3xx、收到 >0 bytes。不支持 HTTP proxy 只记 candidate FAIL，不修改配置。

所有候选失败或不存在：EXISTING_PROXY_TRANSPORT=FAIL_OR_NONE；SAVE_EVIDENCE；RETURN_TO_GPT；STOP。

仅 probe PASS 后，立即在同一执行链/进程将同一 endpoint 传给 aria2c --all-proxy=<same-existing-endpoint>。不得写系统环境变量、registry、git config、aria2 global config 或 FlClash config。

严格 PROBE -> SELECT -> CONTINUE -> MONITOR -> VERIFY：x1/s1 30秒；x4/s4 对同一 partial 继续30秒；仅 x4 稳定且明显可提速才 x8/s8；不得删除有效 partial。

## 4. 冻结生产合同

TARGET_CONTEXT=262144
ONLY_MODEL=Ternary-Bonsai-2-27B-PQ2_0.gguf
PTQ1_0=FORBIDDEN
F16=FORBIDDEN
MMPROJ=FORBIDDEN
DRAFTER=FORBIDDEN
BONSAI_KV4=1
BONSAI_SPECULATIVE=0
BONSAI_NGL=99
CONCURRENCY=1
TEXT_ONLY=YES
THINKING=OFF
T_PHY=OFF
NO_AUTO_128K_FALLBACK=YES

LLAMA_RELEASE=prism-b10709-9a9394a；CUDA_VARIANT=12.4。
Asset1 bytes=253442371；sha256=f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9。
Asset2 cudart-llama-bin-win-cuda-12.4-x64.zip；bytes=391443627；sha256=8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6。

两个 runtime ZIP 都须 exact size + SHA256 PASS 后才可 extract，并验证 llama-server --version。仅 runtime PASS 后下载唯一 PQ2_0。仅 runtime + PQ2_0 都完整验证后启动 262144 server，获取 tokenizer 真实计数，以 240000..245000 tokens 做 marker deterministic test，并取得 actual_prompt_tokens、T_END_TO_END、prompt_tokens_per_second、generation_tokens_per_second、peak_vram_mib、vram_headroom_mib、peak_system_ram_mib、system_ram_headroom_mib、marker_check、post_health。

## 5. 证据、Git 与停止

新建 results/<new_timestamp>/RESULT.md、RESULT.json 和证据，不覆盖 v1/v2/v3。必须增加：

v3_commit=8a293bb4a459436893b9d8e6ce1187e0497ca529
windows_hkcu_source=POLICY_BLOCKED_EXCLUDED
git_proxy_source_status
winhttp_source_status
flclash_listener_source_status
atomic_commands_used=true
policy_bypass_attempted=false
existing_endpoint_found
endpoint_source
endpoint_fingerprint
range_probe_status
system_proxy_modified=false
git_proxy_modified=false
flclash_modified=false
network_modified=false
registry_modified=false
persistent_proxy_env_modified=false

精确 stage；禁止 git add .、reset --hard、force push。push 同一 branch 并 remote readback verify。无论 PASS/BLOCKED：RETURN_TO_GPT、STOP；不得进入下一优化。