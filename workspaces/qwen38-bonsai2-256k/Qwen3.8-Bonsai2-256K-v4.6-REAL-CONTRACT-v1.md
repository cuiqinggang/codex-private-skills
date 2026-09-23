# Qwen3.8 / Bonsai 2 27B 256K — v4.6 实际验证冻结合同 v1

## 角色

```text
PHASE=实
GPT=方案/最终判断
CODEX=冻结合同执行器
POWERSHELL=Codex内部确定性工具
NO_REAL_REDESIGN=YES
```

## 现实入口

```text
ROOT=C:\AI\Bonsai2-27B-256K
MODEL=Ternary-Bonsai-2-27B-PQ2_0.gguf
MODEL_BYTES=7206168928
CTX=262144
PORT=18088
PARALLEL=1
NGL=99
```

优先复用既有：
- 已下载模型；
- IvyBridge/sm75 source-built runtime；
- v3 的 `prompt-242k.txt`；
- v3 cold Reality evidence。

任何一项不存在或与冻结事实矛盾：记录最小 Reality Delta，STOP。

## 必须先通过 0-GPU verifier 9/9

正确 verifier：
- 解析整个 trim 后输出；
- exact 4 keys；
- exact integer values 3817/6241/9053/42；
- extra key/text 均 FAIL。

未 9/9 PASS：GPU_RUNS=0，STOP。

## Server

主：
```text
q8_0 K/V
-c 262144
-ngl 99
-np 1
-fa on
--ctx-checkpoints 32
--checkpoint-min-step 8192
--cache-ram 0
--no-cache-idle-slots
--cache-reuse 0
reasoning off
```

任何参数必须先由当前 `llama-server --help` 确认支持。
若 checkpoint flags 缺失：
```text
REALITY_DELTA=CTX_CHECKPOINT_FLAG_UNAVAILABLE
STOP
```
禁止现场换 runtime。

q8 只有 hard OOM/alloc failure 才允许同模型 q4 fallback；不得因“可能更快”主动切 q4。

## 测量顺序

1. seed：
   - prompt tokens = 242054；
   - n_predict=1；
   - cache_prompt=true；
   - 只建立物理 cache，不重新定义 cold quality。
2. HOT100：
   - original tokens；
   - n_predict=128；
   - cache_prompt=true；
   - strict verifier。
3. HOT98。
4. HOT95。
5. isolated decode x3：
   - short deterministic prompt；
   - n_predict=128；
   - cache_prompt=false；
   - ignore_eos=true。
6. stop server。
7. RESULT readback。

## 禁止

- download；
- source rebuild；
- git fetch 作为启动依赖；
- Temp/AppData executable staging；
- stock llama.cpp；
- PTQ1_0；
- speculative decode；
- JEV A/B；
- 1018-unit suite；
- persistent slot restore；
- batch sweep；
- 修改代理/FlClash；
- REAL 中自行修 verifier/参数。

## RESULT 最少字段

```text
VALIDATOR_SELFTEST=9/9 PASS

SERVER_READY_MS
KV_MODE
CTX_CHECKPOINTS
CHECKPOINT_MIN_STEP
CACHE_RAM
CACHE_IDLE_SLOTS
CACHE_REUSE

SEED_PROMPT_MS
SEED_E2E_MS

HOT100_VALID
HOT100_CACHED_TOKENS
HOT100_PROMPT_MS
HOT100_E2E_MS

HOT98_VALID
HOT98_CACHED_TOKENS
HOT98_PROMPT_MS
HOT98_E2E_MS

HOT95_VALID
HOT95_CACHED_TOKENS
HOT95_PROMPT_MS
HOT95_E2E_MS

DECODE_RUNS=3
DECODE_MEDIAN_TPS
DECODE_MAX_TPS

PEAK_GPU_MEM_MIB
PEAK_GPU_UTIL
MIN_FREE_RAM

REALITY_DELTA
VALID_REAL
ACTION=STOP
```

VALID_REAL=PASS 需要：
- verifier self-test PASS；
- server/runtime/context reality gates PASS；
- HOT100/HOT98/HOT95 strict VALID；
- cache metrics 有效；
- decode 3-run 完成；
- 无 crash/OOM（q4 fallback 成功除外）；
- RESULT 可读。

最终判断权属于 GPT。
