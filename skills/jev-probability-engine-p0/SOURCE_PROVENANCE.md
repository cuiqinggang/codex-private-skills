# SOURCE PROVENANCE

版本：0.2.0
日期：2026-09-21

## 原始内部来源

2026-09-20 接续材料：粘贴的 markdown (1)。md(20260920-172718)
SHA256：c61718f9d235e90519afa944a2f7b5f7fe619b064e791e9513447918cfa695be

旧来源不得被新结论覆盖。

## 0.2.0 外部成熟证据

检查日期：2026-09-21。

- https://docs.typesafe.ai/concepts/how-to-build-with-system-one
- https://docs.typesafe.ai/patterns/fan-out
- https://docs.typesafe.ai/primitives
- https://docs.typesafe.ai/model-jaggedness/jev-1.13
- https://docs.typesafe.ai/models
- https://github.com/typesafe-ai/typesafe-sdk-js
  - package.json blob 40e9181f1874fb8c40f12e925dc5b28b88146239
  - client.ts blob 5846677aaaf2d2578d3c79f09a90f06d8e28a085
  - retry.ts blob e201f0ff3549ffc9c72fcaf11b9c2a9467313183
- https://ajv.js.org/standalone.html
- https://stately.ai/docs
- https://undici.nodejs.org/
- https://openrouter.ai/typesafe/jev-1.13/

公开 latency/uptime 只用于成熟性参考，不替代本机 T_REAL*。


## 0.2.1 command-pack evidence

Checked 2026-09-21:
- OpenRouter model: `typesafe/jev-1.13`.
- OpenRouter Decisions endpoint: `POST https://openrouter.ai/api/alpha/decisions`.
- OpenRouter Jev Lab demonstrates multi-question Decisions requests.
- Full command pack SHA256: `208d816c5372ccb6fec4f4b7055d03774bc2794a875c206518dd274520291ad4`.
- Persistent snapshot: `ChatGPT Library /AI-Skills/jev-probability-engine-p0-v0.2.1-command-pack.zip`.

Runtime winner topology is intentionally not inferred from public latency; it must come from the frozen real benchmark.


## v0.3.0 reality evidence

2026-09-21 用户在本机 Windows PowerShell 执行 v0.2.2 command pack，并在当前 ChatGPT 会话贴出完整控制台结果。关键结果：Decision schema PASS；s1/s2/s4/s8 全部 correctness PASS；s2 30/30 confirmation PASS；COMMERCIAL_GATE_SERIES=PASS；T_REAL*=T_P0=840.6046999999962 ms；REAL_CERTIFIED=YES。

本次没有通过连接器读取用户本机 RESULT.json，因此只把用户贴出的 console transcript 作为当前 reality certification 的直接证据，不声称已独立读取本地结果文件。
