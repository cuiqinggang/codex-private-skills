# Qwen3.8 / Bonsai 2 27B 256K — v4.6 当前唯一入口

```text
PROJECT=qwen38-bonsai2-27b-256k-final-closeout
METHOD=极限短时间引擎 v4.6.0
CURRENT_PHASE=虚
MODEL=Ternary Bonsai 2 27B PQ2_0
TARGET_CONTEXT=262144
DOWNLOAD=COMPLETE
RUNTIME_BUILD=COMPLETE
COLD_242K_REALITY_ANCHOR=PASS
REAL_ENTRY=READY_AFTER_FROZEN_HANDOFF
```

## 已冻结现实事实

- Root: `C:\AI\Bonsai2-27B-256K`
- Model: `Ternary-Bonsai-2-27B-PQ2_0.gguf`
- Bytes: `7206168928`
- SHA256: `3907dc1658db1f78a9826bf8d5bcb8dc65db0d466388937af57f2294fae62ec1`
- Runtime source commit: `9a9394a895b96003ca842a6041cb28ac49a108f7`
- Runtime: IvyBridge-compatible source build, CUDA sm_75
- GPU: RTX 2080 Ti / 22528 MiB
- Context: 262144
- 242054-token cold prompt:
  - prompt_ms = `1367320.567`
  - e2e_ms = `1378701.719`
  - semantic VALID = PASS
- Old `COLD_FULL_VALIDITY_FAIL` = validator false-negative, not model failure.

## 当前真正未完成的收尾

只剩：

1. 修正 strict JSON verifier；
2. 0-GPU verifier self-test；
3. 一次 242K physical cache seed；
4. 同一 server / 同一 slot 生命周期内测 HOT100 / HOT98 / HOT95；
5. 3-run isolated Decode；
6. 资源、缓存命中、输出有效性与现实时间收口；
7. GPT 最终判断。

## 当前删除

旧 1018-unit executor/JEV/thinking/full certification suite 不再属于本 256K 收尾任务。
它只在未来重新打开“Bonsai 替代 Codex 执行器”独立目标时复活。

禁止：
- 重新下载模型；
- 重新编译已验证 runtime；
- 重跑 242K cold 质量认证；
- stock llama.cpp；
- PTQ1_0 换模；
- speculative decoding；
- 把 q4 KV 当速度优化；
- 跨重启 slot restore；
- 把 JEV A/B 混进当前 GPU 物理测功；
- 大范围参数 sweep。

## 当前 Authority

- `Qwen3.8-Bonsai2-256K-v4.6-VIRTUAL-FREEZE-v1.md`
- `Qwen3.8-Bonsai2-256K-v4.6-REAL-CONTRACT-v1.md`

旧文件全部作为历史证据保留。