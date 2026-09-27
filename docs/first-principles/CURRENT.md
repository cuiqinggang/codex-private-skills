# 当前版本入口：整体闭环极限短时间引擎

当前认证状态：**已因新的真实产品差异重新打开；尚无已核验的新正式替代版本。**

最近一次正式发布：**v5.2.1（历史发布，不代表当前完整认证仍然有效）**

当前状态：**REOPENED_REAL_PRODUCT_DELTA / FINAL_VALID=NO / DONE=NO**

最新候选：**v5.3.1（等待可见真实用户旅程验收，未提升为正式版）**

## 固定入口与历史发布定位

稳定入口分支保持不变：

`current/first-principles-physical-limit-convergence`

历史源发布分支保持不变：

`codex/first-principles-physical-limit-convergence-v5.2.1-closeout`

历史源发布 Commit 保持不变：

`cc7c7c1abaa37be82e0d831254ed5a0ce9018f1a`

## 以后任何 GPT / Codex 的查找顺序

1. 先读取本分支的 `docs/first-principles/CURRENT_VERSION.json`，检查 `status/final_valid/done`，不能仅取版本号。
2. `current_version`、`source_release_*`、`canonical_paths` 只保留 v5.2.1 历史发布定位；其中 SKILL、状态文件及证书中的历史 FINAL_VALID 不得覆盖本入口的重新打开状态。
3. 查询新候选时，按 `latest_candidate.commit` 读取对应的 `current_state` 和 `skill`；不要在仍承载 v5.2.1 资产的 current 分支读取 v5.3.1 路径。
4. 只有新的正式验收证据成立后，才允许更新正式发布指针；版本号更高、虚拟成熟、Freeze 完成或低层测试通过均不能代替正式验收。

## 本次纠正的证据

v5.2.2 已明确记录 v5.2.1 因下游真实使用暴露的验收范围缺口而重新打开：

- Commit：`48ca2cd26779066e23c2dbb22009ee5b29860b8e`
- 文件：`docs/first-principles/v5.2.2/CURRENT_STATE.json`

v5.3.1 的候选状态仍为 `VISIBLE_REAL_USER_JOURNEY_READY`，`final_valid=false`、`done=false`：

- 分支：`codex/first-principles-physical-limit-convergence-v5.3.1-visible-user-journey`
- Commit：`a6db0c901f79495b1ab8b19e18c130e5e44fc94e`
- 文件：`docs/first-principles/v5.3.1/CURRENT_STATE.json`

本次只纠正两个 current 入口文件；不修改任何历史 Freeze、版本资产、运行代码或验收证据，也不把本次入口核查充当 v5.3.1 的用户旅程验收。
