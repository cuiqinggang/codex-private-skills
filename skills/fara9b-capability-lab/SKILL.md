---
name: fara9b-capability-lab
description: 在 Windows 本机独立部署 Fara1.5-9B，执行浏览器能力、性能、稳定性、桌面边界及与现有工具的对照验收；按实测建立能力清单和适用范围。
metadata:
  version: "0.1.0"
  status: deployment-and-test-protocol
---

# Fara 9B 独立能力实验室

目标：先测自身能力与边界，再判断独特用途；不预设备用、替代或小模型救援大模型。
首次部署完整执行 [部署与验收命令](references/DEPLOY-AND-TEST.md)，测试用例见 [矩阵](references/TEST-MATRIX.md)，记录见 [结果口径](references/RESULTS.md)。复测仅重跑受影响用例，保留历史结果。
此技能发布不代表模型已经部署、兼容或测试通过。模型固定 microsoft/Fara1.5-9B，不换4B/7B/27B，不把基础Qwen或其他模型当Fara。
用“当前成熟能力 / 实际缺口 / 缺口原因 / 复用成熟方案”四列法处理每个阻塞；只做与已证实原因有关的最小修复。
浏览器优先复用官方 fara CLI；Windows桌面不是已证实能力。已有桌面工具可单独测试；不得把它代替Fara的结果归到Fara名下。
后续使用只根据本机 capabilities.json 中已通过的任务范围路由；证据失效或配置变化时标记待复测。不得仅凭包存在就宣传成熟。
