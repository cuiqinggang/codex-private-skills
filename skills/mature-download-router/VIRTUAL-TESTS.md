# v0.1.4 Pre-release maturity

## Real pre-execution

```text
HF_RESOURCE_FETCH=PASS
HF_RESOURCE_BYTES=665
HF_RESOURCE_SHA256=0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4
GENERIC_HTTPS_FETCH=PASS
GITHUB_REPOSITORY_FILE_FETCH=PASS
SHARED_REPO_SAVE_AND_REREAD=PASS
```

## Environment attack learned from REAL 07

```text
WINDOWS_SCHANNEL_CURL=FAIL_EXIT_35
SCHANNEL_ROUTE_REUSED=NO
```

Public independent reproductions show restricted-token Windows sandboxes can break Schannel while OpenSSL-based Python/HTTP stacks remain usable.

## Mature candidate

```text
LOCAL_TOOL=hf 1.19.0
PROXY=HTTP_PROXY/HTTPS_PROXY process-local only
COMMAND=hf download openai-community/gpt2 config.json --revision 607a30d783dfa663caf39e06633721c8d4cfcd7e --local-dir <dir>
```

Official Hugging Face v1.19 docs:
- proxy is configured globally through HTTP_PROXY / HTTPS_PROXY;
- hf download supports repo, filename, revision and local-dir.

## Freeze

```text
GPT_REAL_PREEXECUTION_EVIDENCE=PASS
RESOURCE_IDENTITY=PASS
COMMAND_CONTRACT=PASS
PROXY_CONTRACT=PASS
KNOWN_SCHANNEL_FAILURE_AVOIDED=PASS
USER_LOCAL_HF_TLS_EXECUTION=UNEXECUTABLE_BY_GPT
PRE_RELEASE_REAL_MATURE=PASS
LOCAL_REAL_CERTIFIED=NO
CODEX_RELEASE_ALLOWED=YES
```
