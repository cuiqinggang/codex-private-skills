# 模型失败与空过规则 v1.0

## 状态码定义

| Status | Meaning | Enter Pipeline? | Weight |
|--------|---------|-----------------|--------|
| PASS | 正常完成所有要求 | Yes | 1.0 |
| PARTIAL | 部分完成，可参考 | Yes | 0.5 |
| EMPTY | 无有效回答 | No | 0 |
| REFUSED | 拒答 | No | 0 |
| TRUNCATED | 截断 | Retry once; then skip | 0 |
| LOW_QUALITY | 明显敷衍 | No | 0 |
| ERROR | 接口错误 | Substitute | 0 |
| RATE_LIMITED | 限流 | Substitute/delay | 0 |
| AUTH_FAILED | 鉴权失败 | Disable this run | 0 |

## 硬规则

1. 只融合真实存在的模型稿
2. 缺失模型不得伪造
3. 低质量模型不得强行进入 C_Fusion
4. 少于 2 个模型 PASS → D_Final 标注"多模型不足 / 受限融合"
5. GPT 未参与 → D_Final 标注"GPT 质量锚点缺失"
6. 观察位低质量答案不得写入最终结论
