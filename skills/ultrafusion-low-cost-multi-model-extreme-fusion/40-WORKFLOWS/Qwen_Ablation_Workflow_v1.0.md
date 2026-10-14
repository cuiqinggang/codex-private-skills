# Qwen 消融测试工作流 v1.0

## 测试步骤

1. 选择 6 个测试问题（多样性：医学/因果/推理/事实/风险/中文）
2. 对每个问题跑流程 A（Core-3）
3. 对每个问题跑流程 B（Core-3 + Qwen）
4. 对比 D_Final 分数
5. 记录 Qwen 独有贡献
6. 评估 Qwen 噪声成本
7. 输出消融测试报告

## 推荐首批测试题
- Q1: Child Mouth Breathing（高风险医学）
- Q2: PM2.5 Spike Cause Analysis（多因果推理）
- QX: Family Cognition Expert Test（综合）
