# v0.1.4 Local Reality Certification

Everything GPT can pre-execute has already passed.

The only remaining reality question:

```text
Can the user's local restricted Codex process run the already-installed hf 1.19.0 through the existing proxy and reproduce the same 665-byte file?
```

Frozen:

```text
TOOL=hf
VERSION=1.19.0
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
REPO=openai-community/gpt2
FILE=config.json
REVISION=607a30d783dfa663caf39e06633721c8d4cfcd7e
EXPECTED_BYTES=665
EXPECTED_SHA256=0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4
TIME_LIMIT=30s
```

No fallback or redesign is allowed inside REAL.

The command must include --force-download so success cannot be satisfied only from cache.

PASS = hf exit 0 + exact bytes/hash + <=30s.
