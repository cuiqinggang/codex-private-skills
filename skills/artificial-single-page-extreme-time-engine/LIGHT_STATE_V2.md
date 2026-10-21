# 轻量状态持久化 V2

VERSION=2
STATUS=ADOPTED_PARTIAL_PASS
PARENT=SANRENXING_V4.md
BRIDGE=V11_C_A_B
ROLLBACK=LIGHT_STATE_V1.md

## 原则
在交付质量、可靠性相同的前提下，以完整有效时间最短为标准。普通短任务 GPT 直达；多步骤、长等待、定时和审批流程优先复用现有 n8n。

## 执行路径
A: GPT -> Windows C 优先 -> 业务验收；短任务不引入额外框架。
B: GPT -> 已有 n8n 工作流 -> 业务工具 -> 业务验收；利用现有执行记录、等待、重试功能。
C: 若 n8n 实际效果不足，再比较 Inngest 或 LangGraph 等成熟框架，不新造调度器。

## 故障恢复
执行未知时先对账：运行中则继续等待，已提交不重复提交，确认未执行才受控重试，无法确定则 STOP_GATE。
不得将工作流执行记录等同于任意节点中断后的自动续跑；外部操作依赖业务收据和幂等措施。
保留 V1 六字段摘要兼容，优先复用 n8n 原生执行身份和持久化机制。最多三轮修复。

## 性能验收
T_VALID = 协调 + 启动 + 执行 + 恢复 + 对账 + 独立业务QA，部署投入按使用次数摊销。只有质量合格的实际业务成绩才参与最短时间比较。
真实任务对照：GPT 直接执行与 GPT+n8n，采用相同输入、质量门槛和故障条件；冷态与热态分开记录。

## 当前事实和未通过项
本机 n8n 2.38.7 健康运行；隔离 Manual->Code 工作流成功，内部 2.520 秒，隔离初始化全程 29.31 秒，非热态性能排名。
仍待验证真实断线恢复、跨重启、Wait 唤醒、避免重复副作用及同业务完整时间。不得宣称 FULL_PASS。

## CHANGELOG
V2：按需复用 n8n；V11 执行桥；保留 GPT 快速路径；原 V1 作为回退版本。

## 2026-10-20 现实恢复验收补充
在隔离 Docker+持久 SQLite，n8n 原生 Wait(120s) 的执行 ID=2 经容器停止和新宿主启动后自动恢复为 success，Before/Wait/After 各执行一次。瞬时 HTTP 503 自动重试(2次请求)最终成功；相同幂等键2次外部请求仅提交1次（依赖接收端幂等）。详细证据见 LIGHT_STATE_V2_ACCEPTANCE_20261020.md。
TECHNICAL_ISOLATED_RECOVERY=PASS；PRODUCTION_REAL_BUSINESS_E2E=PENDING。
