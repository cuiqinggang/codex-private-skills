# Qwen3.8 / Bonsai 2 27B 256K — 当前执行入口

当前正式命令包：

DOWNLOAD-AND-BASELINE-COMMAND-PACK-v4.md

## 为什么进入 v4

- v1：Phase A PASS。
- v2：固定官方 release 直下被 direct GitHub TLS/443 阻断。
- v3：漂移检查 PASS；含 HKCU 的 composite discovery 在进程创建前被 managed policy 拒绝，其余来源未执行。
- v4：永久排除 HKCU；Git、WinHTTP、FlClashCore listener 分别原子只读发现；只有 1 MiB probe PASS 才同链复用内存中的既有 endpoint。

v4 不改变模型、上下文或 runtime：只 PQ2_0、262144、KV4、thinking off、no PTQ1_0、no 128K fallback、no proxy/network/system change。