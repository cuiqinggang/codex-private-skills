# H3-P0 Codex 容量路由器安装结果 v1

状态：`INSTALLED / T1-T7_MOCK_PASS / REAL_SERVICE_UNVERIFIED`

## 安装

- 正式目录：`C:\AI\Codex-Capacity-Router`
- Codex Home Skill：`C:\Users\A\.codex\skills\codex-capacity-aware-model-router\SKILL.md`
- Skill SHA256：`9CFE589FF340055FA1C1036B07608380F3CC2227FCF9839130361259346111B5`，与仓库源文件一致。
- `CODEX_CAPACITY_ROUTER=ENABLED`
- `STATIC_MODEL_LIST=NO`
- 当前 Codex Home `models_cache.json` 可读，动态发现 5 个可见模型；模型名没有写入长期 policy 或生产源码。

## 验收

| 项目 | 结果 |
|---|---|
| T1 主模型 PASS | PASS |
| T2 主模型 CAPACITY 后第二模型 PASS | PASS |
| T3 前两模型 CAPACITY 后第三模型 PASS | PASS |
| T4 全模型 CAPACITY、checkpoint、无忙循环 | PASS |
| T5 capacity 后接续且不重放已完成步骤 | PASS |
| T6 路由事件字段 | PASS |
| T7 刷新模型目录后发现新增候选 | PASS |

`CAPACITY_FAILOVER=PASS_MOCK`；`CHECKPOINT_RESUME=PASS_MOCK`；`LOCAL_WORK_REPLAY=NO`。T1–T7 是安装命令包允许的受控故障注入，全部在正式目录运行通过。

真实 app-server `model/list` 启动时会初始化 Codex 受保护的会话/状态数据库。为只读模型目录请求提权被自动权限审核拒绝；本轮遵守拒绝，没有以间接方式重试，也没有运行真实 `codex exec` probe。因此真实远端模型可用性和真实 capacity 切换尚未验证，不能把 mock PASS 写成真实服务 PASS。缓存 fallback 已独立只读验证。

H3 业务保持暂停。已保存 `TASK_STATE=CHECKPOINTED`，`REQUESTED_MODEL=UNKNOWN`，`ACTUAL_MODEL=UNKNOWN`，`NEXT_ACTION=STOP_RETURN_TO_GPT`。本轮 H3 GPU/QC 运行均为 0；没有重做先前 Git 提交或远端核验。

正式证据：

- `C:\AI\Codex-Capacity-Router\reports\INSTALL-REPORT.md`
- `C:\AI\Codex-Capacity-Router\reports\ACCEPTANCE.json`
- `C:\AI\Codex-Capacity-Router\state\checkpoint.json`
