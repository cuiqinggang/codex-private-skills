# Bonsai 2 27B PQ2_0 — 256K 下载与现实基线命令包 v3

状态：READY_FOR_CODEX / TRANSPORT-RECOVERY-ONLY / NOT_EXECUTED

## 0. 继承现实结果

已冻结结果：

- v1 commit: `664a2289ede02d295611384e41fd6777331b369d`
  - Phase A = PASS
  - setup.ps1 路径被证明不满足“runtime-only”合同
- v2 commit: `a4ba30d6768ecadcb700c2fa9b5bfa68d085168e`
  - 最小漂移检查 = PASS
  - 固定 GitHub release runtime 下载被网络传输阻断
  - aria2 x1：30 秒 0 字节
  - aria2 x4：TLS 2746 remote forced close
  - curl HEAD：github.com:443 timeout / exit 28
  - proxy/network/system settings changed = NO
  - model download started = NO

本 v3 **只修复网络传输方式**。模型、上下文、runtime 版本、SHA256、下载算法和测试合同全部不变。

唯一原则：

~~~text
不改变现有代理
不改变代理节点
不改变 FlClash 模式
不改变系统代理
不改变网络设置

只允许“读取当前已经存在的代理路径”
并让 aria2/curl 显式使用同一个既有代理端点。
~~~

如果无法证明正在复用“既有代理”，必须停止，不得猜端口或创建新代理配置。

---

# 1. 冻结合同

~~~text
TARGET_CONTEXT=262144
ONLY_MODEL=Ternary-Bonsai-2-27B-PQ2_0.gguf
PTQ1_0=FORBIDDEN
MMProj=FORBIDDEN
DRAFT_MODEL=FORBIDDEN
THINKING=OFF
SPECULATIVE=OFF
KV4=ON
CONCURRENCY=1
TEXT_ONLY=YES
T_PHY=OFF

DO_NOT_CHANGE_PROXY_CONFIGURATION=YES
DO_NOT_CHANGE_PROXY_ENDPOINT=YES
DO_NOT_CHANGE_PROXY_RULES=YES
DO_NOT_CHANGE_FLCLASH_MODE=YES
DO_NOT_CHANGE_SYSTEM_NETWORK=YES
NO_AUTO_128K_FALLBACK=YES
~~~

---

# 2. 只做最小漂移检查

继承 Phase A，不重跑完整预检。

确认：
- pwsh 可用；
- aria2c 可用；
- RTX 2080 Ti 可见；
- C: free > 20 GiB；
- FlClash 进程如原先常驻则仍存在；
- 本项目 llama-server 未运行。

失败则 STOP。

---

# 3. 只读发现“当前已存在”的代理路径

所有动作只读。

必须保存：

~~~text
evidence/proxy-readonly-discovery.json
evidence/proxy-readonly-discovery.txt
~~~

读取以下来源：

## 3.1 Git 已有代理

~~~powershell
git config --show-origin --get-all http.proxy
git config --show-origin --get-all https.proxy
git config --show-origin --get-regexp 'http\..*proxy|https\..*proxy'
~~~

## 3.2 Windows 当前用户系统代理

只读：

~~~text
HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings
  ProxyEnable
  ProxyServer
  AutoConfigURL
~~~

## 3.3 WinHTTP

~~~powershell
netsh winhttp show proxy
~~~

## 3.4 FlClash 只读状态

只读取：
- FlClash 进程 PID / executable path；
- 与该 PID 相关的本机 LISTEN 端口；
- 若系统代理已经明确指向 localhost/127.0.0.1 的某端口，记录对应关系。

禁止：
- 猜测 7890/7891/其他端口；
- 扫描全部本机端口；
- 修改 FlClash 配置文件；
- 切换节点/模式/TUN；
- 写注册表；
- 写 git proxy config。

---

# 4. 代理候选裁决

只能从“已经明确存在”的配置里得到候选。

优先级：

~~~text
1. Git 已明确配置且可解析的 HTTPS/HTTP proxy
2. Windows ProxyEnable=1 + ProxyServer 明确值
3. WinHTTP 明确 proxy
~~~

若三个来源均没有显式端点：

~~~text
EXISTING_EXPLICIT_PROXY_ENDPOINT=NONE
-> 不猜
-> RETURN_TO_GPT
-> STOP
~~~

如果存在多个不同端点，不修改它们。按来源顺序逐一做**小流量连接测试**，只选第一个能够访问固定 GitHub release 的既有端点。

规范化示例：
- `127.0.0.1:PORT` -> `http://127.0.0.1:PORT`
- `http=HOST:PORT;https=HOST2:PORT2` -> GitHub HTTPS 使用 https 对应项
- 已含 scheme 则原样使用

禁止记录任何认证密码；若 URI 含 credential，日志必须脱敏。

---

# 5. 小流量连接验证

先不做完整下载。

固定 asset：

~~~text
llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip
expected bytes=253442371
expected sha256=f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9
~~~

对每个“既有代理候选”：

1. curl 使用 **命令行临时参数** `--proxy <existing-endpoint>`，不写环境、不写系统设置；
2. 做 HEAD 或 Range 0-1048575（1 MiB）；
3. 超时 20 秒；
4. 成功条件：
   - TLS 建立；
   - HTTP 2xx/3xx；
   - Range 请求实际取得 >0 字节；
5. 保存：
   - endpoint_source
   - endpoint_redacted
   - http_status
   - bytes_received
   - elapsed_ms
   - exit_code

若全部失败：
~~~text
EXISTING_PROXY_TRANSPORT=FAIL
-> 不切节点
-> 不改代理
-> 不尝试镜像
-> RETURN_TO_GPT
-> STOP
~~~

---

# 6. aria2 明确复用现有代理

只有第 5 节 PASS 才允许。

aria2 使用：

~~~text
--all-proxy=<the already-existing verified endpoint>
~~~

这不是修改代理配置；只是让 aria2 显式复用当前已存在的代理出口。

不得：
- 写入 aria2 全局配置；
- 写入 HTTP_PROXY/HTTPS_PROXY 持久环境变量；
- 写注册表；
- 修改 git config；
- 修改 FlClash。

下载算法保持不变：

~~~text
PROBE -> SELECT -> CONTINUE -> MONITOR -> VERIFY
~~~

同一个 partial：
- x1/s1 30 秒；
- x4/s4 继续 30 秒；
- x4 稳定且有明显余量才 x8/s8；
- 选最快稳定配置；
- 保留 partial / .aria2 控制文件；
- 30 秒记录一次实际速率；
- 连续60秒无增长或约120秒低于最佳稳定速率50% -> 保留数据、停止当前下载、重新测速。

注意：v2 留下的是 0-byte partial，因此不存在有效模型/runtime 数据可丢失；仍保留原文件作为历史证据。v3 可继续同名目标文件，但不得删除历史 evidence。

---

# 7. Runtime 仍固定，不换版本

仍只允许官方：

~~~text
LLAMA_RELEASE=prism-b10709-9a9394a
CUDA_VARIANT=12.4

llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip
bytes=253442371
sha256=f565c8428c1f108311f65ed97f02425188b3aa3c745c2bc597521bbd24bcbbc9

cudart-llama-bin-win-cuda-12.4-x64.zip
bytes=391443627
sha256=8c79a9b226de4b3cacfd1f83d24f962d0773be79f1e7b75c6af4ded7e32ae1d6
~~~

两个 ZIP 必须：
~~~text
exact size PASS
SHA256 PASS
-> 才能解压
~~~

目标：
~~~text
C:\AI\Bonsai2-27B-256K\Bonsai-demo\bin\cuda
~~~

必须看到：
~~~text
llama-server.exe
llama-cli.exe
~~~

并验证 `llama-server.exe --version`。

---

# 8. 模型下载同样复用“已验证既有代理”

Runtime PASS 后，才进入模型。

唯一模型：

~~~text
prism-ml/Ternary-Bonsai-2-27B-gguf
Ternary-Bonsai-2-27B-PQ2_0.gguf
~~~

仍禁止 PTQ1_0 / F16 / mmproj / drafter。

优先 aria2 + 已验证既有代理。

如果 Hugging Face/Xet 不接受 aria2 分段，而本机已有 hf/huggingface-cli：
- 可启动 child process；
- 只允许给该 child process 注入同一个“已验证既有代理端点”；
- 不写持久环境变量；
- 不改变代理配置；
- 保留 HF cache；
- 记录 fallback 原因。

下载后：
- exact size；
- local SHA256；
- 有远端 LFS SHA256 则比对；
- GGUF 可读性检查；
- 原子放置到目标模型目录。

---

# 9. 后续 256K 测试合同不变

Runtime + 模型全部验证通过后，继续 v2 的 Phase D/E：

~~~text
BONSAI_CTX=262144
BONSAI_KV4=1
BONSAI_SPECULATIVE=0
BONSAI_NGL=99
THINKING=OFF
~~~

实际 prompt：
~~~text
240000..245000 tokens
~~~

必须保存：
- T_END_TO_END
- prompt tokens/s
- generation tokens/s
- peak VRAM/headroom
- peak RAM/headroom
- marker exact check
- post health

失败：
~~~text
NO_AUTO_128K
SAVE_EVIDENCE
RETURN_TO_GPT
STOP
~~~

---

# 10. 结果写回

创建新结果目录，不覆盖 v1/v2：

~~~text
workspaces/qwen38-bonsai2-256k/results/<new_timestamp>/RESULT.md
workspaces/qwen38-bonsai2-256k/results/<new_timestamp>/RESULT.json
~~~

至少包含：

~~~text
prior_v1_commit=664a2289...
prior_v2_commit=a4ba30d...
proxy_discovery_sources
existing_proxy_endpoint_found
selected_proxy_source
selected_proxy_endpoint_redacted
system_proxy_modified=false
git_proxy_modified=false
flclash_modified=false
network_modified=false
runtime_download_status
runtime_sha256_verified
model_download_status
model_sha256
effective_context
actual_prompt_tokens
T_END_TO_END
prompt_tokens_per_second
generation_tokens_per_second
peak_vram_mib
vram_headroom_mib
peak_system_ram_mib
system_ram_headroom_mib
marker_check
post_health
next_action=RETURN_TO_GPT
~~~

精确 stage 新文件；禁止 git add . / force push / reset --hard。
push 同一分支，远端回读验证，STOP。

即使 PASS，也不自动进入 PTQ1_0 或其他优化。
