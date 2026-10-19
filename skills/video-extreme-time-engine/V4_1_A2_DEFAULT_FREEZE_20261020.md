# 高品质视频极限短时间引擎 V4.1.0｜A2 默认路线决策冻结
VERSION=4.1.0
DATE=2026-10-20
STATUS=DECISION_FROZEN
DEFAULT_HD_ROUTE=A2_FBC_SAFE_20STEP
METHOD=三人行V4 + 轻量状态持久化V1
WINDOWS_BRIDGE=V11.0
EXECUTION=C_REMOTE_DESKTOP_COMMANDER_FIRST
NEW_GPU_REALITY=0
FINAL_124F_QUALITY_VALID=NOT_CERTIFIED

## 结论与证据
本机 Windows 10 Pro 22H2、RTX 2080 Ti SM75、22528MiB VRAM、32GB RAM；不改代理/FlClash。
**A2**：现有 MiniMax H3 1024x576、5帧、20步、INT8 ConvRot + FirstBlockCache Safe（与当前工作流匹配的已认证后端/卸载、单次VAE）；热态完整五帧77.640秒，5/5 PNG，单样本初步画质PASS。采样53.360秒，VAE22.281秒。仍须记录缓存与warm条件。
A1：native 20步、同规格热态80.000秒，单样本初步PASS；作为必要回退。
C3 Turbo 8：五帧197.593秒，非统一热态，同质质量未证。
官方Turbo 8：五帧429.638秒，从提交到落盘校验，输出PASS；质量未正式通过，系统端包含不同Qwen3-VL32B/加载路径，不能视为纯算法因果对照。画面前景布料随帧偏移。B不晋级，不与A2叠加。
B1 SM75 SLA+FBC 489.047秒画质FAIL；B2 SLA 115.250秒画质FAIL。不要重测已明确失败组合。
历史首次Safe203.797秒/R2 463.266秒为另一次运行条件，不与本次77.640秒热态混排。
旧Turbo4厨房640x352 124帧49.707秒热态不得作为高清同质成功。
权威证据位于桌面 H3_V4_5F_BATCH_20261017/V4_REALITY_FINAL_REPORT.md、V4_A2_TURBO8_STAGE_AUDIT.md、OFFICIAL_TURBO/OFFICIAL_TURBO_REALITY_20261019.md、B_TURBO8_VS_A2_RECHECK_20261019.md、A2/A2-workflow.json、A2/A2-result.json。

## 生产选择和回退
1. 同样参考图/seed/提示词下默认A2；不可擅自改变步数、缓存阈值、条件编码、注意力后端或精度。
2. 质量硬门槛：人物面容/背影、服装刺绣、瀑布背景、动作连续、字幕及声音（若合同要求）；字幕逐字精确采用可控叠加；5帧静态PASS不代表124帧运动/音画认证。
3. 发生主体变形、纹理漂移、显存保护触发或不满足质量则回退A1原生20步。禁止以质量下降换速度。
4. 最短有效时间 T*=min(T_VALID) 仅在相同规格和质量PASS的真实全程计时里比较。77.640秒只是热态5帧记录，不是124帧物理极限；全124帧正式T_VALID保持UNKNOWN，除非同合同证据补证。
5. 路由C第一，C健康不能跳到A/B；启动服务前必须核对进程所有权、空队列、显存/系统资源。任何真实124帧只在重新冻结质量合同后Exactly-once。
6. 不覆盖V1~V4历史工作流，不删除/重算已验收图像，无理由不得生成新GPU任务。

## STOP_GATE
A2已是本次A/B明确选定生产路径；B终止，不继续“融合式”尝试。版本升级是决策与资料持久化，不是新增视频Reality认证。
