# 模型守护与回退工作流 v1.0

## 回退触发
- Core-3 中任一模型不可用
- 多个模型返回低质量
- AUTH_FAILED 或 RATE_LIMITED

## 回退流程
1. 激活替补模型（优先级：Kimi → Gemini → GLM）
2. 最多激活 2 个替补
3. 保持 Core-3 中正常的模型
4. 标注"替补参与"

## GPT 不可用时的特殊处理
- D_Final 必须标注"GPT 质量锚点缺失"
- 提升其他模型的评审严格度
- 增加 D 层 counter-example testing 深度
