# 状态合同

## RC-MIN 页面发布

- 本地通过、尚未发布：LOCAL_MINIMAL_PATCH_PASS_READY_FOR_DEPLOY
- 原站发布并完成线上验证：DEPLOYED_MINIMAL_PATCH_5_OF_5_PASS_WAITING_L4
- 源、发布或验收阻塞：MINIMAL_PATCH_BLOCKED

## 禁止

- 不使用 FINAL_PASS、FINAL_PASS_WITH_LIMITS 或“基本部署完成”。
- 不把保存 Sites 版本称为已发布；必须 deployment succeeded 且原网址复验通过。
- 不把虚拟测试 5/5 称为 A 关真实有效。

## 永久能力边界

- 真实有效样本：0
- 成熟度：L3
- 最终决定：REVISE
- 下一关口：L4｜GPT三题真实烟雾测试

