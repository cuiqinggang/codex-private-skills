# UltraFusion 测试索引

**最后更新**: 2026-06-17 (Gate Review 修复)

## 测试问题

| ID | 问题 | 验证目标 | 路由 |
|----|------|----------|------|
| Q1 | 孩子口呼吸问题 | 验证高风险谨慎性（医疗） | Full-ABCD 或 Strict D-Lite |
| Q2 | PM2.5 浓度飙升原因 | 验证多因果推理 | Full-ABCD |
| QX | 家庭认知专家测试 | 验证完整 A/B/C/D 链路 | Full-ABCD |

## Qwen 消融测试

建议先用 Q1、Q2、QX 三题小样本验证 Qwen 消融测试。

### 测试流程
1. 对每个问题跑流程 A（Core-3）
2. 对每个问题跑流程 B（Core-3 + Qwen）
3. 对比 D_Final 分数、扣分、独有贡献
4. 输出消融测试报告

## 每题文件

每题目录包含：
- `question.md` — 测试问题
- `expected_route.md` — 期望路由和理由
- `test_goal.md` — 测试目标
- `scoring_focus.md` — 评分重点

## 答案存储

完整 A/B/C/D 输出在执行后存储在各子目录中。
