---
name: visual-art-engine-performance-ladder
description: 管理视觉作品的成熟制作、逐帧返修与性能证据。用于故事与资产、布局动作排演、MiniMax H3原生视听、手机屏幕追踪合成、对白听审、清晰度修复、混音与人工审核交接；保留P0–P8性能基准和图像来源审计，镜头级成功不等于通用控制认证。
metadata:
  version: "3.1.1"
  short-description: 通用高性能视觉作品生成引擎
---

# 通用高性能视觉作品生成引擎

## V3.1.1 已验证的FASHN原案例（2026-11-08）

静态人物换装优先读取[官方换装原案例直接复现](references/VERIFIED-FASHN-CASE1-20261108.md)：已在本机按未修改的作者原程序、同一素材和参数完成两次，576×823输出字节与像素一致。仅覆盖这个静态案例；需要视频或新内容时继续找对应已合格原案例，不扩大本次认证范围。

## V3.1.0 本机合格短样准入与取消人为总时限（2026-11-08）

- 视频能力以当前条件下按成熟配方直接做出合格作品判定。论文、教程、星数、下载材料、进程退出或文件可解码都不能单独登记为已掌握。先验一个原作本身合格、材料完整的短样，复跑仍合格后才保存具名配方和适用范围。
- 候选必须有作者、原始成品、输入、代码/模型版本、工作流和参数、依赖、执行步骤、真实运行记录与质量结论；缺整包继续检索成熟节点及其原接口。来源覆盖视频分享、作者文章、官方文档、GitHub/模型库、用户复现与实际业务，不以数量替代完整度。
- 取消由助手自行添加的视频生成、渲染、封装、整任务及等待的固定墙钟截断，包括六分钟、24小时等默认上限；不得只因到时就杀进程。保留当前已配置的硬件、内存、温度、性能资源保护和用户明确的时长/资源合同，不自行把CPU/GPU利用率100%判作故障或修改现有保护阈值。
- 工具单次返回/轮询和网络请求超时属于连接行为，不是任务总时限。返回运行会话后持续续读同一会话；断线先核账，不自动杀任务、重投或把UNKNOWN写失败。
- 若直接验证未通过，该路线保持候选/未掌握；查作者已有诊断与缺失材料，不得围绕同一失败样片发明修补链或反复重抽来取得能力认证。成熟节点的原接口配置、字段映射与最小胶水允许复用。
- 普通生产吸收按[直接复现准入与本机验证](references/DIRECT-REPLAY-ADMISSION-20261108.md)执行，不加载历史性能基准的统计门和旧逐帧返修循环；特定原项目接续仍继承其质量合同。历史证据原样保留。
- 已验节点见[官方播客模板本机复现](references/VERIFIED-AUDIOGRAM-20261108.md)：仅认证原固定工程的完整带声渲染与重复性，不认证换人、换装、自动转录或新内容迁移。

## V3.0.0 成熟制作返修与 R9 实证（2026-10-31）

先读 [制作与批量返修路径](references/MATURE-FILM-REWORK-V3.md)；涉及《十几年》接续时，再读 [R9完成情况与原因记录](references/HOTMEAL-R9-DELIVERY-20261031.md)、[可重用参数与恢复方法](references/HOTMEAL-R9-REPLAY-V3.md) 及 [发布状态](references/RELEASE-V3.json)。

- 保留已认可故事、人物及限定几何结果；按“提交—审核—退回对应工序—复审—批准”推进。技术和艺术分别判定，空间/接触错误退布局或动画，不能靠精修/声音遮掩。
- R9已完成15秒、360帧、24fps带声人工审核候选；原生384×320，2倍修复768×640。文件完整性、解码及内部视听复审通过；`human_approval=false`、`final_approval=false`、`T_VALID=null`。不代签最终艺术批准。
- 只把本片的可见约束通过登记为镜头级结果；不得扩大为所有动作可靠控制、全身物理碰撞认证、P0–P8晋级或已证明提速。
- 本片按A动作/布局、B生成控制、C表演对白、D完整带声预演、E动画口型与修复合成、F声音、G最终审核成批接续；复用已批准资产和原生片段，不重复已完成GPU任务。
- 原始已执行脚本与配置见 `assets/hotmeal-r9/`。运行前按恢复说明核对原项目、输入SHA、模型、端口、原生prompt_id、history、claim及输出节点；归档脚本含本片绝对路径，不可直接拿去重投或覆盖新任务。
- 本片资源合同为RAM准入低于90%、运行时95%独立保护；仅适用于本片，不改其他项目。断连先对账同一prompt_id/history，UNKNOWN不重复提交。
- 固定屏幕文字优先使用成熟平面追踪合成，保护照片静止、刚体、手指遮挡；修复后再合成文字。ASR与审片模型会误听、误判左右、虚构帧号/片长；以真实帧和原音复核，保留失败报告。
- 原报告、原生镜头、视频及177项文件清单保存在持久审核包；链接及SHA见发布状态。仅升级技能与固化经验时，运行 `scripts/quality/verify_hotmeal_r9_package.py --package <审核包.zip>`，不为文档升级重做GPU生成。
- 旧V2段落中的 `SLAP_ACTION_VALID=NO` 是参考图阶段记录；当前R9限定动作内部审核见新状态，仍待人工终审。旧P0声明和99门属于性能认证合同，不覆盖或否认已实际执行的生产镜头。
- 本次整版本升级不更改原V2来源真实性门、不修改莲花/烟花或旧基准合同；历史大图仍保留在原保存位置，按证据指针读取。

## V2.0.0 人物魅力与关键动作参考门（2026-10-30）
本次整数升级扩展视觉参考、选角及动作/情绪检查规则，不代表P0–P8晋级、H3生产认证或性能提升。原V1.3.0及其来源审计、历史合同、失败证据继续保留。

涉及《十几年》、青春感/模板脸、同人物连续镜头、耳光方向、愤怒或痛苦流泪时，先读取 [本轮人物与关键帧参考库](references/TEN-YEARS-V14-VISUAL-REFERENCES-20261030.md)。该库含15张持久原图链接及逐图使用资格；用户已认可的年轻女性独立人像作为定脸参考，其他候选待审；两版耳光接触图为失败/反例，不作正式动作模板。
- 先用独立人像确定人物魅力，再锁身份制作场景/关键帧；不可只改“年轻漂亮”文字重抽面孔。
- 关键动作须有出手前、挥动/接触、随动反应；痛苦流泪须单独有表情状态，不能用相似静态怒脸或眼泪覆盖。
- 逐图核对解剖手位、掌心掌背、受击侧与头部随动；禁止为适配错误接触而改坏邻帧。连续纯文字返修失败后先复用成熟动作参考/约束，不无限盲抽。
- 图片的参考许可、技术正确、艺术认可和动态验收分开记录；该V2参考图阶段记录为SLAP_ACTION_VALID=NO、FINAL_VALID=NO；R9状态见V3发布记录，不回写历史批准。
- 本轮图片明确为ChatGPT内置image_gen参考/编辑候选，非ComfyUI/Krea/H3输出。普通视觉参考任务可按用户授权使用；当合同指定本机后端或独立生成时，必须继承下方V1.3来源门，严禁替代或冒称。
- 项目当前为10秒首选、10–12秒可调、15秒硬上限、三句对白与单次耳光；项目版本仍v1.4，技能包版本V2.0.0。历史17/20秒方案仅留档，不恢复执行。

## v1.3.0 来源防作弊执行门禁（2026-10-11；优先级高于旧图像规则）

**新增强制入口**：[《图像生成来源真实性与防作弊执行门禁 V3.0》](references/IMAGE-SOURCE-ANTI-CHEAT-V3.md)。凡用户要求本机 ComfyUI、Krea、Windows 实际生成/修复或完整防作弊证据，必须在任何生图或修图调用前读取该文件，锁定 `BACKEND=COMFYUI_LOCAL` 和 `MODE=T2I_INDEPENDENT / REF_CONDITIONED / IMG2IMG / EDIT/INPAINT`。缺合同或工具不匹配即 `NO_SUBMIT`；不可默默以 ChatGPT `image_gen` 替代，亦不可用 image_gen 绘制左右对比海报。

**严格区分**：`IMG2IMG` 使用源图 VAEEncode 重绘；`REF_CONDITIONED` 使用参考条件；`T2I_INDEPENDENT` 必须空白潜空间且生成路径不使用参考图；`EDIT/INPAINT` 必须声明编辑底图和范围。四者不是一个合同，来源相似/哈希不同都不能单独判造假或独立生成。

正式作品发布必须经过：`G-1 后端和模式锁定 → G0 本机健康 → G1 冻结工作流及图像来源拓扑 → G2 ComfyUI原生 prompt_id/history 和真实 PNG SHA → G3 非生成式像素拼接、视觉质量与合同检查 → G4 第二次只读复核`。任何失败：`FINAL_VALID=NO`，不可冒充完整成果；连接断开或任务结果未知：`UNKNOWN`、禁止重复提交。只准展示真实失败事实，不能伪造缺失证据补救。

本轮连续违规反例（2026-10-11）：**用户明确要求技能包升级和 ComfyUI 修复图片，却又调用 `image_gen` 生成修复图及“原图/修正后”对比海报**。两次 `gen_id` 不等于 ComfyUI `prompt_id`，无相应 ComfyUI workflow/history/文件来源审计；该轮结果一律 `NOT_COMFYUI / INVALID`，不得作为品质/时间基线。见 [本轮再次绕路事故记录](references/INCIDENT-KREA-REPEAT-IMAGEGEN-20261011.md)。

**可执行来源核验器（正式路径）**：`scripts/quality/verify_comfy_provenance.py`，回归测试 `tests/test_comfy_source_guard.py`。它可在生成前核验工作流类型；生成后必须提供本机 ComfyUI `/history` 和真实输出根目录，才能核对原生 `prompt_id`、工作流、SaveImage PNG 及文件 SHA。只有预检结果不得声称执行成功。示例：

```powershell
python scripts/quality/verify_comfy_provenance.py --dir "C:\\AI\\ComfyUI_Aaki_v3\\data\\output\\本轮证据" --mode T2I_INDEPENDENT --api http://127.0.0.1:8188 --output-root "C:\\AI\\ComfyUI_Aaki_v3\\data\\output"
```

仅在既有工作流适用时使用，不得重写 ComfyUI 调度。校验器的 `FILE_PROVENANCE_VERIFIED` 只证明已核验的文件与历史一致，**不自动代表 G3 画质通过或 FINAL_VALID=YES**。对带参考图的模式，输入文件 SHA 仍需人工交叉核对；局部 EDIT_INPAINT 自动审查尚不充分，默认拒绝自动认证。功能自测 7/7 是模拟样例，不代表跨新 ChatGPT 会话真实工具选择门已通过。

版本规则：以本 `SKILL.md` 头部 `metadata.version` 与同目录 `VERSION` 一致为准；不一致必须阻止正式升级 PASS，先修正单一版本事实。与第28版自动化引擎的 Freeze、一次最终 Reality、REUSE_GATE 和性能基准合同并行适用。

**能力边界**：技能文档只能约束本技能的合规判定，不能保证在宿主层物理禁止 `image_gen` 调用。以后必须以真实工具调用和执行证据验证防作弊；不能把“规则已写入”说成“平台级拦截已经上线”。

## v1.2.1 真正的生成前置校验（2026-10-11）

本地 ComfyUI/Krea 独立生图合同下，执行 **工具选择前置门**：任何拟作为正式结果的图片只能通过授权 Windows 执行桥的 ComfyUI API 工作流产生，要求先检查 G0/G1，运行后保存 ComfyUI 原生 prompt_id、history 与实物文件哈希再输出结果。ChatGPT image_gen、编辑图、改写参考图以及仅有图片生成工具的 gen_id 都不得视为 ComfyUI 证据或替代结果。若缺任一证据，只报告故障/不合规和既有证据，不展示为合格出图；严禁用生成工具制作左右“审计”图片。完整 V2.0 证据合同保持不变。

本次工具绕路事故详情见 [2026-10-11 Krea image_gen 替代事故](references/INCIDENT-KREA-IMAGEGEN-SUBSTITUTION-20261011.md)。不得用本次 image_gen PNG 作为 Krea 或 H3 品质/时间基线，FINAL_VALID=NO。


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
- 下述v1.0.1原始P0合同固定声明：`P0_BENCHMARK_EXECUTED=NO`、`PERFORMANCE_OPTIMIZATION_RUN=NO`、`H3_RUN=NO`；这是历史性能合同范围，不是V3生产镜头执行状态。
- 初始状态固定为：`P0_CURRENT=PENDING`、`P0_EXTERNAL=PENDING`、`P0_T_PHY=PENDING`、`P0_ITERATIVE_CONVERGENCE=LOCKED`、`P0_99=NO`。
- 历史 Wan/FAST/COLD 数据只进入 `HISTORICAL_EVIDENCE`，不得作为 P0 CURRENT。
- 普通生产任务走 `RUNTIME_FAST_PATH`。只有规定触发条件才走 `CERTIFICATION_PATH`，详见 [运行与认证分离](docs/RUNTIME-VS-CERTIFICATION.md)。
- 不修改代理、网络、WSL、系统 CUDA/Torch、健康 ComfyUI、显存/offload/allocator/attention 设置；不安装 custom node 或新依赖。
- 不修改 `visual-art-engine`、`mature-replication-four-column`、莲花或烟花成熟技能。
- 禁止用历史固定 baseline 或分时单批 median 裁决毫秒级候选；禁止把 `p>0.05` 当作等价；禁止在 null Type-I error 校准前生成 FINAL_MDE。

## 失败复盘与证据

失败记录必须含阶段、固定 TASK、期望/实际时间、原始事件、输出有效性、是否 `PATH_ARCHITECTURE_ERROR`、回滚结果和冻结基线完整性。使用 [阶段证据模板](templates/STAGE-EVIDENCE-TEMPLATE.md)，写入台账所列 `evidence_path`。任何缺少真实证据的数字保持 `null` 或 `UNKNOWN`。
