# Qwen3.8 / Ternary Bonsai 2 27B 256K — v4 结果

状态：BLOCKED_TRANSPORT / RETURN_TO_GPT / STOP

## 结论

v4 三个 Markdown 文件本地校验通过，未被重写。原子代理发现找到一个既有 Git proxy endpoint，但固定 runtime asset 的 0-1048575 Range probe 失败（curl exit 35、HTTP 000、0 bytes）。按冻结合同未启动 aria2c、runtime、PQ2_0、llama-server 或 256K baseline。

## v4 文件校验

- CURRENT.md：PASS；SHA-256 `37721ce31d3b0e727e73937f80030678f9af148f3e724e0dc6ae411cce29087d`
- DOWNLOAD-AND-BASELINE-COMMAND-PACK-v4.md：PASS；SHA-256 `dd1c7fb17b2c45e22db233b6a95e8570423ceb724b5a2c81896d82d235bfaefa`
- COMMAND-PACK-AUDIT-v4.md：PASS；SHA-256 `d94cd96b903c05d8a5a03cd918641f8d463244c6e3b86d308d2416e56b3b3a26`
- git diff --check：PASS（仅 LF→CRLF working-copy warning，无 whitespace error）
- unexpected_changes：false

## 原子代理发现

- v3_commit：`8a293bb4a459436893b9d8e6ce1187e0497ca529`
- windows_hkcu_source：`POLICY_BLOCKED_EXCLUDED`
- git_proxy_source_status：`FOUND`
- winhttp_source_status：`NONE`
- flclash_listener_source_status：`POLICY_BLOCKED`
- flclash_listener_error：`PermissionDenied / HRESULT 0x80041003`
- atomic_commands_used：true
- policy_bypass_attempted：false
- existing_endpoint_found：true
- endpoint_source：`git_http_proxy`
- endpoint_fingerprint：`f1410cd719dcee161d171a3729c50bffabb9325546e31867d85db2b0773db22e`
- raw_endpoint_persisted：false

## Range probe

- asset：`llama-prism-b10709-9a9394a-bin-win-cuda-12.4-x64.zip`
- requested_range：`0-1048575`
- range_probe_status：`FAIL`
- curl_exit_code：35
- http_status：000
- bytes_received：0
- existing_proxy_transport：`FAIL_OR_NONE`

## 冻结边界

- TARGET_CONTEXT：262144
- ONLY_MODEL：`Ternary-Bonsai-2-27B-PQ2_0.gguf`
- PTQ1_0：FORBIDDEN
- KV4：ON
- THINKING：OFF
- SPECULATIVE：OFF
- CONCURRENCY：1
- TEXT_ONLY：YES
- T_PHY：OFF
- NO_AUTO_128K_FALLBACK：YES

## 未启动项与无修改声明

- aria2c_started：false
- runtime_started：false
- model_started：false
- server_started：false
- baseline_started：false
- system_proxy_modified：false
- git_proxy_modified：false
- flclash_modified：false
- network_modified：false
- registry_modified：false
- persistent_proxy_env_modified：false

TASK_COMPLETED=FALSE
RETURN_TO_GPT
STOP
