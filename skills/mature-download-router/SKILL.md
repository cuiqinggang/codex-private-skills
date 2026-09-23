---
name: mature-download-router
description: 成熟下载工具最短调用路由 v0.1.4。只做最小来源判断并调用成熟工具；公开样本发布给 Codex 前必须先由 GPT 真实取件成功，Windows 受限沙箱避免 Schannel 路径，优先成熟 OpenSSL/httpx 工具。
metadata:
  version: "0.1.4"
  display_name: "成熟下载工具最短调用路由"
  status: "PRE_RELEASE_REAL_MATURE_LOCAL_REAL_PENDING"
---

# 成熟下载工具最短调用路由 v0.1.4

## 核心

```text
识别来源 -> 交给成熟工具
```

不自建下载器、适配器、队列、状态页或下载算法。

## 发布前证据门

对公开测试资源：

```text
GPT_EXTERNAL_FETCH=PASS
ARTIFACT_SAVED=PASS
ARTIFACT_REREAD=PASS
```

才允许发布本地现实验证。

当前已实测：

```text
HF_PUBLIC_FILE=PASS (665 bytes)
GENERIC_HTTPS=PASS (1093 bytes)
GITHUB_REPOSITORY_FILE=PASS (22434 bytes)
```

## Windows 受限执行环境规则

Reality Foundation v1.1.6 已记录：

```text
Windows curl.exe / Schannel
-> REAL 07 exit 35
-> SEC_E_NO_CREDENTIALS class
```

因此在该受限执行上下文中：

```text
DO_NOT_SELECT=Schannel-based curl / Invoke-WebRequest for HTTPS certification
SELECT=existing mature non-Schannel stack when available
```

当前 Hugging Face 本地路线：

```text
TOOL=hf 1.19.0
NETWORK_STACK=huggingface_hub/httpx
PROXY_INPUT=process-local HTTP_PROXY + HTTPS_PROXY
RESOURCE=openai-community/gpt2 config.json
REVISION=607a30d783dfa663caf39e06633721c8d4cfcd7e
EXPECTED_BYTES=665
EXPECTED_SHA256=0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4
```

## 已验证 vs 未验证

```text
资源存在与内容=GPT_REAL_PREEXEC_PASS
hf命令语义=OFFICIAL_DOCS_VERIFIED
hf 1.19 proxy via HTTP_PROXY/HTTPS_PROXY=OFFICIAL_DOCS_VERIFIED
用户本机 Codex 受限子进程中的 hf 实际 TLS=UNEXECUTABLE_BY_GPT
```

只有最后一项留给 REAL。

## 状态

```text
PRE_RELEASE_REAL_MATURE=PASS
LOCAL_REAL_CERTIFIED=NO
METHOD=first-principles-physical-limit-convergence@4.6.1
REALITY_FOUNDATION=local-ai-reality-foundation@1.1.6
```

一句话：GPT 能真实做的先做成功；只把用户本机独有的最后一小段交给 Codex。
