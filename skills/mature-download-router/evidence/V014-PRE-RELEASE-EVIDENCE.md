# v0.1.4 Pre-release Evidence

DATE=2026-09-23

## Public sample actually fetched before Codex release

```text
SOURCE=https://huggingface.co/openai-community/gpt2/resolve/main/config.json
RESOLVED_REVISION=607a30d783dfa663caf39e06633721c8d4cfcd7e
FETCH_RESULT=PASS
OUTPUT_BYTES=665
SHA256=0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4
SHARED_REPO_SAVE=PASS
SHARED_REPO_REREAD=PASS
```

## Mature tool contract checked

```text
LOCAL_TOOL=hf 1.19.0
COMMAND=hf download REPO FILE --revision REV --local-dir DIR
PROXY_CONTRACT=HTTP_PROXY/HTTPS_PROXY process-local
```

## Known bad path removed

```text
Windows curl/Schannel REAL 07
exit=35
classification=LOCAL_WINDOWS_SCHANNEL_TLS_CONTEXT_FAILURE
REUSE_IN_NEXT_REAL=NO
```

## Release decision

```text
GPT_REAL_PREEXECUTION_EVIDENCE=PASS
PUBLIC_RESOURCE_IDENTITY=PASS
COMMAND_CONTRACT=PASS
PROXY_CONTRACT=PASS
ONLY_REMAINDER=USER_LOCAL_CODEX_RESTRICTED_PROCESS_HF_TLS
CODEX_RELEASE_ALLOWED=YES
```