---
name: visual-art-engine-performance-ladder
description: 管理 Visual Art Engine 从 ComfyUI 控制路径到生产 H3 的 P0-P8 性能进化；用于固定 Benchmark Contract、调用第一性原理四列法 V4.0、记录真实端到端时间、阶段 99、FREEZE/REOPEN、ΔT_STAGE 和 PATH_ARCHITECTURE_ERROR。它不替代 visual-art-engine，也不在缺少证据时宣称性能通过。
metadata:
  version: "1.2.0"
  short-description: 通用高性能视觉作品生成引擎
---

# 通用高性能视觉作品生成引擎

## V1.2.0 高品质图像至 H3 视频主候选（2026-10-11）

选型须先阅读 [Krea 优先的成熟方案与 H3 衔接记录](references/KREA-H3-SELECTION-V1.md)。当前质量优先主候选只有 FLUX.1 Krea Dev FP8 Scaled；Juggernaut XL v9、FLUX.2 Klein 4B 仅作为备选资料保留，默认不得三套并行部署。选型不等于本机生图已经成功。发布用途核查模型的非商业/非生产使用限制；用户当前非营利实验可继续验证，不可直接断言公开运营获得授权。必须完成厨房静物和人物生活照独立采样的真实 G0-G3 证据及 H3 成片关卡，才能评定质量合格后的完整有效成片最短时间。原 V2.0 来源审计不可跳过。

## V1.1.0 强制图片来源审计（2026-10-10）

涉及 ComfyUI 参考图片独立重新生成的任务，执行前必须加载 [《图片独立生成证据与防伪验收规范 V2.0》](references/IMAGE-INDEPENDENT-GENERATION-AUDIT-V2.md)，优先于任何旧的图片展示或无证据 PASS 规则。G0 环境、G1 工作流来源、G2 真实执行证据、G3 真实文件直接像素拼接与质量验收四门必须依次通过，否则禁止输出图片为正式生成成果、禁止虚构运行记录、禁止 FREEZE/PASS。若运行失败仅反馈真实故障和证据缺口，不得以 ChatGPT 图片生成结果替代。此约束只涉及生成任务证据门，不改变原有 P0 性能基准合同与四列法版本。


这是 `visual-art-engine` 的性能进化管理层，不是替代实现。运行、测量、比较和冻结任何阶段前，必须直接加载正式技能 `mature-replication-four-column`，版本必须为 V4.0（metadata `4.0.0`）；不得另造四列法。依赖核验见 [METHODOLOGY-DEPENDENCY.md](references/METHODOLOGY-DEPENDENCY.md)。

## 固定方法

固定 TASK 后，唯一评分指标是 `TIME`，正式值为 `T_END_TO_END`。质量、成功、安全与稳定性只作为 `RESULT_VALIDITY_GATE`；任务合同变化所得时间一律 `INVALID_RESULT`。

四列固定为：

1. `CURRENT`
2. `EXTERNAL FRONTIER`
3. `FIRST-PRINCIPLES PHYSICAL TIME`（第一性原理物理时间，`T_PHY` 或 `T_PHY_RANGE`）
4. `ITERATIVE CONVERGENCE`

`T_PHY` 是唯一终极参照；外部成熟方案只是现实证据与路径库。99 仅表示当前硬件、软件、环境、固定 TASK 和已知可验证方法下的现实收敛，必须保留 `PHYSICAL_GAP = T_99 - T_PHY`。

## 工作流

1. 读取 [当前状态](state/CURRENT-STATE.md) 和 [阶段台账](state/STAGE-LEDGER.json)。
2. 只允许处理第一个未锁定阶段；上一阶段必须 `score_99=true` 且 `frozen=true`，下一阶段才可解锁。
3. 冻结或重开 TASK Contract；先完成前三列，第四列才可解锁。
4. 每次只测试一个局部假设，保留原始事件、输出校验、环境与计时证据。
5. 新阶段记录 `ΔT_STAGE = T_NEW_STAGE - T_PREVIOUS_STAGE`。出现明显数量级退化时先判 `PATH_ARCHITECTURE_ERROR`，检查路径、组件、模型、参数、offload、加载、依赖、软件栈、技能调用和调度结构；不得把崩塌接受为新 baseline。
6. 达到 99 后按 [FREEZE/REOPEN 规则](docs/FREEZE-REOPEN-RULES.md)冻结，并保留 previous stable、fallback 和 archive。

## P0 入口

P0 固定为 ComfyUI API 控制路径：`REQUEST -> QUEUE -> EXECUTE -> SAVE -> RESULT`。读取 [P0 Benchmark Contract](contracts/P0-BENCHMARK-CONTRACT.md) 后再使用：

```powershell
& 'C:\Program Files\PowerShell\7\pwsh.exe' -NoLogo -NoProfile -File .\scripts\p0\prepare-p0.ps1
python .\scripts\p0\run-p0-control.py --dry-run
```

正式运行必须显式提供 `--execute --acknowledge-contract P0-CONTROL-V1`。默认协议为 3 次 warmup、20 次 measured。没有明确执行意图时只做 readiness，不提交 workload。

## Measurement Protocol V2（验证中）

`MEASUREMENT_PROTOCOL_V2_STATUS=UNDER_VALIDATION`。在 `STATISTICAL_SELFTEST=PASS`、`NULL_CALIBRATION=PASS`、`AA_CALIBRATION=PASS` 三门同时成立前，候选裁决保持锁定，不得把 V2 写成成熟 PASS，也不得启动 E4/E5/E7 或 Track B 权威裁决。

开展任何性能比较前读取 [measurement-protocol.md](references/measurement-protocol.md)；遇到校准、漂移、MDE、顺序效应、bracket 或旧批复用问题时同时读取 [failure-lessons.md](references/failure-lessons.md) 与 [evidence-map.md](references/evidence-map.md)。原始 runs/history/PNG/统计分布只留在 Stage，技能包只保存可复用规则与证据指针。

V2 一旦三门通过即冻结为 P0-P3 默认 benchmark harness。只有新的真实证据证明 harness 有缺陷时才能升级；升级必须保留旧版本、记录原因、产生新 runner SHA 并重新 A/A。

A/A 的 arm label 必须是纯 metadata。任何 A/B 标签进入 workflow JSON、
`filename_prefix`、HTTP path/query、计时内 raw/evidence 路径或 client/session
identifier，均为 benchmark contamination。正式 A/A 前必须证明归一化 run token
后的 A/B workflow byte-equivalent，并同时满足
`TIMED_PATH_LABEL_LEAK=0`、`WORKFLOW_LABEL_LEAK=0`、
`HTTP_LABEL_LEAK=0`。

权威 benchmark 身份必须同时记录单文件 `RUNNER_SHA` 与整套
`HARNESS_MANIFEST_SHA`。后者至少覆盖 runner、两层启动器、decision rules、
bracket summary、workflow 与 fixture；任一文件变化都产生新 fingerprint。

2026-09-15 权威 label-blind A/A 已完成 160/160：formal effect
`2.8688 ms`、95% CI `[-0.847625,6.585225]`、noise floor `3.7609 ms`。
旧 label-contaminated A/A 的 CI 全正假效应已消失，故
`LABEL_BLIND_FIX_CAUSALLY_CONFIRMED=YES`；但 order-effect CI
`[-3.081325,22.327025] ms` 未进入冻结等价区间，当前仍为
`AA_CALIBRATION=INCONCLUSIVE / CANDIDATE_LOCK=ON`。

Windows 正式运行前必须实际创建 deepest expected evidence path。失败时改用
短、中性、label-blind evidence root；不得用 arm-specific 路径，也不得因路径失败
修改统计或 workload。

2026-09-15 最终搜索收口：新的独立冻结-harness A/A `a4` 为 160/160
有效，但 environment drift gate 触发，故
`AA_CALIBRATION=FAIL / CANDIDATE_LOCK=ON`。SEARCH_ONLY 找到
`R6_SUCCESS_LOCAL_HISTORY_V2`：两个独立 confirmation 的 paired effect
分别为 `11.451175 ms`（CI `[9.370775,13.531575]`）和
`8.465825 ms`（CI `[6.691,10.24065]`），但 pooled candidate P50/P95
为 `41.5258/58.000845 ms`，未优于历史参考。因此
`P0_99=NO / P0_FREEZE=NO`，不得把真实相对收益误报成绝对 99。

## 强制边界

- v1.0.1 仅表示方法、阶梯、版本、冻结系统、P0 Contract 和 P0 工具就绪；不表示 P0 已测或已优化。
- 本版本固定声明：`P0_BENCHMARK_EXECUTED=NO`、`PERFORMANCE_OPTIMIZATION_RUN=NO`、`H3_RUN=NO`。
- 初始状态固定为：`P0_CURRENT=PENDING`、`P0_EXTERNAL=PENDING`、`P0_T_PHY=PENDING`、`P0_ITERATIVE_CONVERGENCE=LOCKED`、`P0_99=NO`。
- 历史 Wan/FAST/COLD 数据只进入 `HISTORICAL_EVIDENCE`，不得作为 P0 CURRENT。
- 普通生产任务走 `RUNTIME_FAST_PATH`。只有规定触发条件才走 `CERTIFICATION_PATH`，详见 [运行与认证分离](docs/RUNTIME-VS-CERTIFICATION.md)。
- 不修改代理、网络、WSL、系统 CUDA/Torch、健康 ComfyUI、显存/offload/allocator/attention 设置；不安装 custom node 或新依赖。
- 不修改 `visual-art-engine`、`mature-replication-four-column`、莲花或烟花成熟技能。
- 禁止用历史固定 baseline 或分时单批 median 裁决毫秒级候选；禁止把 `p>0.05` 当作等价；禁止在 null Type-I error 校准前生成 FINAL_MDE。

## 失败复盘与证据

失败记录必须含阶段、固定 TASK、期望/实际时间、原始事件、输出有效性、是否 `PATH_ARCHITECTURE_ERROR`、回滚结果和冻结基线完整性。使用 [阶段证据模板](templates/STAGE-EVIDENCE-TEMPLATE.md)，写入台账所列 `evidence_path`。任何缺少真实证据的数字保持 `null` 或 `UNKNOWN`。
