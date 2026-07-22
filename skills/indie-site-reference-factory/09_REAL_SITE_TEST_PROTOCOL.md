# 09_REAL_SITE_TEST_PROTOCOL

真实测试目标选择原则：
1. 公开可访问
2. 无登录
3. 简单落地页
4. 不需要反爬
5. 不涉及敏感数据
6. 适合参考结构，不复制品牌

默认测试 URL 候选：linear.app、stripe.com、vercel.com、framer.com、notion.so/product。强品牌网站只能参考结构，不得保留品牌资产。

真实测试必须输出 outputs/tests/REAL_SITE_TEST_REPORT.md，包含目标 URL、合规判断、环境预检、目标站截图证据、侦察结果、生成项目路径、构建结果、生成站截图证据、QA 评分、修复记录和最终结论。

## PASS 标准
`npm build` 通过只证明工程能跑，不证明克隆能力通过。

克隆能力 PASS 必须同时满足：

- 真实目标 URL 截图存在
- 生成站桌面/移动截图存在
- outputs/progress 强制进度包完整
- 每轮截图对比已公开
- 桌面相似度 >= 95%
- 移动端相似度 >= 95%
- 综合相似度 >= 95%
- npm install / lint / typecheck / build 通过
- 合规替换完成

如果相似度不足，只能标记 `PARTIAL_SIMILARITY` 或 `FAIL_SIMILARITY`。
如果缺进度包，必须标记 `INVALID_TEST`。

## 输出要求
- 所有结论必须中文可读。
- 关键证据必须落盘。
- 没有真实 URL、截图、build 和 QA，不得标记 PASS。
