# 2026-09-23 成熟方案增量索引

本文件只记录这次“虚”新增、且直接影响 256K 极限时间的外部成熟事实。

1. Bonsai 2 27B 官方模型卡：
   - Qwen3.8-27B hybrid attention；
   - ~75% linear / ~25% full attention；
   - context 262K；
   - PTQ1_0 / PQ2_0 两种 GGUF packing。
2. PrismML Bonsai-demo PROMPT-CACHE.md：
   - cache_prompt:true = common-prefix reuse；
   - --ctx-checkpoints = hybrid/recurrent state snapshots；
   - --cache-ram 与 KV 分离；
   - --cache-reuse 是另一套 chunk shifting，hybrid memory 可不支持；
   - 同一 idle slot 应比较 prompt_n / prompt_ms 与 checkpoint restore log。
3. Frozen Prism b10709 commit 9a9394a 已直接确认支持：
   - --ctx-checkpoints；
   - --checkpoint-min-step；
   - --cache-ram；
   - --cache-idle-slots；
   - --cache-reuse。
4. llama.cpp 2026 hybrid/recurrent slot restore issues：
   - save/restore 不持久化 server context checkpoints；
   - restore 可报告成功，但下一请求仍完整 prefill；
   - 因此跨重启 slot persistence 不进入冻结方案。
5. Bonsai 2 没有官方 DSpark drafter：
   - speculative decoding 不进入当前方案。
6. q4 KV 是 memory fallback，不作为 speed optimization。

这些新事实只用于调整当前冻结执行链；旧 workspace / 旧 Reality evidence 全部保留。
