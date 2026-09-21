# B* Runtime-only Reality Certification v1.0

```text
CURRENT_STEP=3
DESIGN_FROZEN=YES
ONLY_CANDIDATE=R1_SAME_RELEASE_CPU_BACKEND_GRAFT
T_VALID_GATE_MS=60000
AUTO_FALLBACK=NO
MODEL_DOWNLOAD=FORBIDDEN
```

Reality 只允许：
1. 只读重新发现当前 FlClashCore exact-PID loopback listener；不得猜端口/扫描端口/改代理。
2. 用候选 endpoint 做小流量固定 release probe。
3. 下载 exact CPU x64 release asset。
4. exact bytes + SHA256。
5. 提取 `ggml-cpu-sandybridge.dll` 和 `libomp140.x86_64.dll`。
6. 备份现有 `ggml-cpu.dll`。
7. 用 sandybridge DLL 作为 `ggml-cpu.dll`。
8. 运行 `llama-server --version`。
9. 运行 `llama-server --list-devices`。
10. 两门 PASS 且 T_VALID<=60000ms 才认证。
11. FAIL 必须 restore、SAVE EVIDENCE、STOP、RETURN_TO_STEP_2。

禁止：安装/编译/换 runtime/换模型/下载模型/降 128K/改 FlClash/改 Windows proxy/改 Git proxy/写 Registry/现场转 R2 或 R3。
