# Qwen3.8 / Bonsai 2 27B 256K — 当前执行入口

## CURRENT AUTHORITY

当前唯一 Reality Authority（现实认证权威合同）为：

- Qwen3.8-27B-Bstar-Virtual99-Mature-v3.md
- Qwen3.8-27B-Bstar-Final-Reality-Certification-v3.md
- Qwen3.8-27B-Bstar-Executor-Cert-Suite-v3.json
- Qwen3.8-27B-Bstar-Executor-Cert-Coverage-Audit-v3.json

状态：

```text
METHOD=first-principles-physical-limit-convergence v3.1.7
STAGE=VIRTUAL_99_MATURE_FREEZE_V3
B_STAR_ROLE=ONLY_REALITY_CANDIDATE
TARGET_CONTEXT=262144
REAL_EXECUTOR_CERTIFIED=NO
```

旧 v1/v2 Authority 与旧下载/基线命令包均为历史资料，不再作为当前认证依据：

```text
Qwen3.8-27B-Bstar-256K-Final-Reality-Verify-v1.md = SUPERSEDED
Qwen3.8-27B-Bstar-Virtual99-Freeze-v1.md = SUPERSEDED
Qwen3.8-27B-Bstar-Final-Reality-Certification-v2.md = SUPERSEDED
Qwen3.8-27B-Bstar-Virtual99-Mature-v2.md = SUPERSEDED
```

如果上述旧 Authority 文件未存在于本分支，则不为“补历史文件”而重建；本文件中的 SUPERSEDED 索引即为当前状态标记。

## 冻结执行顺序

1. Suite Integrity Gate
2. Reality Anchor（只读）
3. Transport Preflight（只读发现并临时复用现有代理；禁止修改代理/网络）
4. 只下载 B*：Ternary-Bonsai-2-27B-PQ2_0.gguf
5. Q8 KV 两点门；仅在硬内存失败时切 Q4 并重复同两点一次
6. 完整 Final Reality Certification
7. SAVE EVIDENCE → STOP → RETURN_TO_GPT

禁止边测边重新设计；禁止自动下载 A*/C*；禁止自动降 128K。

## 历史 v4 下载/运行预检记录（仅保留证据，不再是当前 Authority）

历史正式命令包：

DOWNLOAD-AND-BASELINE-COMMAND-PACK-v4.md

历史记录：

- v1：Phase A PASS。
- v2：固定官方 release 直下被 direct GitHub TLS/443 阻断。
- v3：漂移检查 PASS；含 HKCU 的 composite discovery 在进程创建前被 managed policy 拒绝，其余来源未执行。
- v4：永久排除 HKCU；Git、WinHTTP、FlClashCore listener 分别原子只读发现；只有 1 MiB probe PASS 才同链复用内存中的既有 endpoint。
- 结果：results/20260920-014431/RESULT.md
- 状态：BLOCKED_RUNTIME_COMPATIBILITY
- transport probe：PASS
- runtime SHA-256：PASS
- llama-server version gate：FAIL_ILLEGAL_INSTRUCTION (0xC000001D)
- NEXT_ACTION=RETURN_TO_GPT

该历史结果只证明当时的 transport/runtime preflight 状态，不等价于 B* Reality Certification 结果。
