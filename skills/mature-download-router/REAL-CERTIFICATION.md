# v0.1.3 Local Reality Certification

发布前真实取件已通过。现在只验证用户本机能否重复同一个 665-byte 公开文件下载。

固定样本：

```text
URL=https://huggingface.co/openai-community/gpt2/resolve/main/config.json
EXPECTED_BYTES=665
PRE_RELEASE_FETCH=PASS
PRE_RELEASE_ARTIFACT_REREAD=PASS
LOCAL_TOOL=curl.exe
LOCAL_NETWORK_CONTEXT=http://127.0.0.1:7890
TIME_LIMIT=30s
```

PASS：

```text
curl exit=0
output exists
output bytes=665
T_VALID <= 30s
```

成功后：
```text
LOCAL_REAL_CERTIFIED=YES
```

失败后只返回最小 Reality Delta，不切换工具、不改方案。
