# Hermes 自动化执行手册 v1.0

## 执行方式

```
# 加载 UltraFusion 技能，提交问题
"Use ultrafusion-low-cost-multi-model-extreme-fusion to answer: <question>"
```

Hermes 自动完成：
1. 加载 V15 spec 和模板
2. 对 Core-3 模型逐层执行
3. 拼装 prompt（V15 + Template + Materials）
4. C_Fusion 和 D_Final
5. 输出 D_Final_Ultra_Answer_Final

## 验证
- 检查 V15 注入记录
- 检查 D_Final 结构
- 检查评分
