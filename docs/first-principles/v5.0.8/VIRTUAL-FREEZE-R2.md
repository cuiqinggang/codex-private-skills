# 整体闭环极限短时间引擎 v5.0.8｜R2 完整虚拟成熟冻结

FREEZE_ID=ESTE-v5.0.8-DUAL-END-NUMERIC-TIME-ASCII-CAPSULE-VIRTUAL-FREEZE-R2

## 顶层保持不变
- 只有：虚 -> 实。
- 原状态机动作不改变。
- 正常权威源仍为共同私库直读。
- 时间总控只有 ALLOW/BLOCK 权。
- 唯一目标：T*=min(T_VALID)。
- 顶层 T_VALID=T_CLOSED_LOOP_VALID。

## v5.0.8 最终时间模型
内部始终计时；不要求每个小动作刷屏。

以下控制边界必须显式携带同一 Timeline 的数值时间：
- 关键方案定案；
- 虚拟成熟时间收口；
- Freeze；
- GPT -> Codex；
- Codex -> GPT；
- PASS / FAIL / BLOCKED；
- FAIL 回虚；
- FINAL_VALID。

GPT 与 Codex 共用一套最小时间信封：
- LOCATOR
- TIMELINE_ID
- T_CLOSED_LOOP_ELAPSED_MS
- T_EXCHANGE_ELAPSED_MS
- T_STAR_MS
- 必要结果

PASS 回报必须再带：
- T_REAL_VALID_MS
- T_CERTIFICATE_ELAPSED_MS

FAIL/BLOCKED 也必须带数值时间。
若证书没有启动：
- T_CERTIFICATE_ELAPSED_MS=0.000
- CERTIFICATE_STATE=NOT_STARTED
但 T_EXCHANGE_ELAPSED_MS 必须是真实数值，失败成本不能消失。

N/A / NULL / MISSING / Infinity / NaN / 空值均非法。

## v5.0.7 Reality Delta 已吸收
旧 Reality 在 run_reality_certificate() 前发生 UnicodeEncodeError。

R2 修正：
- 人类文档可中文；
- 真正执行的 Reality Capsule 必须 ASCII-only；
- Reality 前置物化固定：
  exact remote blob -> blob verify -> source.isascii() -> compile -> fresh namespace exec -> callable check；
- 只有物化 PASS 后才进入 T_VALID_REAL；
- 编码/物化失败必须数值时间信封返回，禁止现场修复和同 Freeze 重试。

新 Capsule：
docs/first-principles/v5.0.8/REAL-CAPSULE-SOURCE-R2.py

## 完整虚拟测试
- GPT -> Codex：32/32 PASS，仅完整 1/32 允许；
- Codex -> GPT FAIL/BLOCKED：512/512 PASS，仅完整 1/512 允许；
- Codex -> GPT PASS：1024/1024 PASS，仅完整 1/1024 允许；
- 完整往返随机链：20000/20000 PASS；
- Timeline 重建：0；
- 时间倒退：0；
- T* 交接漂移：0；
- 返回时间遗漏：0；
- ASCII-only Capsule：PASS；
- ASCII/UTF-8/CP1252/Latin-1 无损：PASS；
- fresh namespace 物化：5000/5000 PASS；
- Reality Certificate：18/18 PASS。

完整虚拟套件 10 轮：
MIN=215.557737ms
P50=222.007210ms
P95=240.230782ms
MAX=245.786124ms

Reality Certificate 10000 次：
MIN=0.002384ms
P50=0.002514ms
P95=0.002624ms
MAX=0.387835ms

使用既有 v5.0.2 Windows/GPT 已认证比率：
4.768616382444736

冻结本次 Reality Certificate 目标：
T*=0.01136838145574825ms

结论：
VIRTUAL_MATURE=YES
ENCODING_DELTA_ABSORBED=YES
DUAL_END_TIME_HANDOFF=PASS
READY_FOR_COMPLETE_FREEZE=YES
