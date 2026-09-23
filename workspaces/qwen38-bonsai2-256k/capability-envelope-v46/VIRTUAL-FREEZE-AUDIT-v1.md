# 千问3.8 27B1 — v4.6 虚拟冻结审计 v1

## 结论

```text
VIRTUAL_ENGINEERING_CLOSEOUT=PASS
TOKEN_ENVELOPE_GATE=PASS
SUITE_EXECUTABILITY_GATE=PASS
RUNNER_BINDING_GATE=PASS
ZERO_GPU_SELFTEST=1018/1018 PASS
RUNNER_CONTROL_PATH_SMOKE=PASS
VIRTUAL_COMPLETE=YES
REAL_ENTRY=READY
```

## 零 GPU 证据

```text
GPU_RUNS=0
MODEL_CALLS=0
UNITS=1018/1018
TOKEN_OVERFLOWS=0
ORIGINAL_16_HARD_CONFLICTS_REPAIRED=PASS
EXPLICIT_RESERVE_CLAMPED_CASES=32
VALIDATOR_BINDING_ALL_CATEGORIES=PASS

ATOMIC_PAIRWISE=800/800
ATOMIC_REALITY_ANCHORS=64
JEV_PAIRWISE=57/57
JEV_REALITY_ANCHORS=24
LONG_STEPS=1800
INJECTED_FAILURES=86
```

有效 suite canonical digest：

```text
9b94215208f55d2ac07065249d72eff113043f9cc18f7e8b8c103271e6487ba4
```

## Runner 控制链 smoke

使用零 GPU 假 llama-server 实际走通：

```text
/health
/apply-template
/tokenize
/completion
strict verifier
result writeback
```

首个 8K group：

```text
TARGET_PROMPT_TOKENS=8192
ACTUAL_PROMPT_TOKENS=8163
CASES=2/2 PASS
REALITY_DELTA=NONE
```

注意：这是 runner 绑定烟测，不冒充 Bonsai 模型现实能力认证。

## 本地文件 SHA256

| 文件 | SHA256 |
|---|---|
| CAPABILITY-ENVELOPE-PATCH-v4.json | `99f779a16a76805bead0a267f9fd79c02de02e3fe37efafddbe712c9761b5d84` |
| BONSAI2-CAPABILITY-ENVELOPE-RUNNER-v2.py | `2fe5c87bb1336c1c82e8c604b4e6bfbd3ee008dc68c512a5c9d4256c54727f6b` |
| MATERIALIZE-CAPABILITY-ENVELOPE-v1.ps1 | `dcb5a89ca620a1ffa0e3a2297a4c495fbe73cb6c8c91e26cb935990a1d1dffa5` |
| ZERO-GPU-SELFTEST-v2.json | `63f3c26aeb0087853849c3152f5da73ad5401a38838d686601549b2248c8ec78` |
| ZERO-GPU-RUNNER-BINDING-SMOKE-v1.json | `bea1af6295fcafdbb3e9d6e7905b2c55cd9dd735d05e19f48e1a1cdbb3a0bf9e` |
| REALITY-BOUNDARY-PLAN-v1.json | `a4d5aca5e89c9df6a7ce88023d3974d8f3118ff38bc9c8df36e1968f972dd0a5` |
| Qwen3.8-Bonsai2-v4.6-CAPABILITY-ENVELOPE-VIRTUAL-FREEZE-v1.md | `6eb1046959481a18ed458dead85ee23954d19c021abc6e0fbd50ee34611defbe` |
| Qwen3.8-Bonsai2-v4.6-CAPABILITY-ENVELOPE-REAL-CONTRACT-v1.md | `2834d8b0cce312096dac04c472496017786a184d09d9286a36752fafd3194890` |

## 共同仓库

```text
REPO=cuiqinggang/codex-private-skills
BRANCH=codex/qwen38-bonsai2-27b1-v4.6-capability-envelope-virtual-freeze-v1
BASE=codex/qwen38-bonsai2-256k-v4.6-incremental-freeze-v2
```

远端已回读确认以下路径存在：

```text
workspaces/qwen38-bonsai2-256k/capability-envelope-v46/
```

并已把：

```text
workspaces/qwen38-bonsai2-256k/CURRENT.md
```

切换到本能力边界 Authority。

## 现实最短化结构

```text
592 Atomic
-> 64 anchors
-> 800/800 pairwise preserved
-> 32 model request groups

240 structured probability cases
-> 24 anchors
-> 57/57 pairwise preserved
```

长上下文使用嵌套共享 prefix，FAIL 只按冻结邻域规则扩展。

模型任务 FAIL = 能力边界数据；
基础设施/合同/runner FAIL = Reality Delta -> STOP -> 返虚。

## 时间连续性

```text
TASK_TIME_ID=QWEN38-27B1-20260923T182700+0800
TIME_RESET=FORBIDDEN
NEXT_SEQUENCE=01
```

本审计不把未仪表化的历史主动时间清零；详见 `TIME-LEDGER-v4.6.json`。
