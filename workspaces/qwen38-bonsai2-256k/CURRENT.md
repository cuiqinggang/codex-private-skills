# Qwen3.8 / Bonsai 2 27B 256K — 当前执行入口

当前正式命令包：

`DOWNLOAD-AND-BASELINE-COMMAND-PACK-v3.md`

## 为什么进入 v3

- v1：Phase A PASS；setup.ps1 的 runtime-only 假设被现实证据否定。
- v2：改为固定官方 release 直下；但本机 direct aria2/curl 到 GitHub release 被 TLS/443 超时阻断。
- v3：不修改代理，只**只读发现并显式复用机器当前已经存在的代理端点**，先做 1 MiB 小流量验证，PASS 后才继续固定 aria2 并行/续传下载。

v3 不改变模型、上下文或运行时版本。

仍然：
- 只 PQ2_0；
- 262144；
- KV4；
- thinking off；
- no PTQ1_0；
- no 128K auto fallback；
- no proxy/network/system change。
