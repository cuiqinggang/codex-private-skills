# PRE-RELEASE-REAL-MATRIX

Date: 2026-09-23

## Actually fetched before Codex release

| Environment/source | Resource | Result | Saved evidence |
|---|---|---|---|
| Hugging Face external fetch | openai-community/gpt2 config.json | PASS, 665 bytes | evidence/pre-release-gpt2-config.json |
| Generic HTTPS external fetch | https://www.cloudflare.com/robots.txt | PASS, 1093 bytes | evidence/pre-release-cloudflare-robots.txt |
| GitHub repository connector | aria2/aria2 release-1.37.0 README.rst | PASS, 22434 bytes | evidence/pre-release-aria2-readme.rst |

Reread from shared repository: PASS for all three.

## Not claimed

GitHub Release asset body = NOT_TESTABLE_ON_CURRENT_GPT_CONNECTOR
Browser-authenticated download = NOT_TESTABLE_WITHOUT_USER_SESSION

No PASS is invented for those routes.

## Release decision

CODEX_RELEASE_ALLOWED=YES
SAMPLE_BYTES=665
SAMPLE_SHA256=0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4
