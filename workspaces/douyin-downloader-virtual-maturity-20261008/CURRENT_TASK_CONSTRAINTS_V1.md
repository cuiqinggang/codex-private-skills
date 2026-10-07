# 《当前任务目标与正反约束 第1版》

任务ID：DOUYIN-DOWNLOADER-VIRTUAL-MATURITY-20261008
合同版本：1
状态：FROZEN
任务类型：方法虚拟成熟小样本

## 1. 最终现实目标（作为重放母任务）

用户把抖音分享文本/短链放入剪贴板后，只需双击桌面“抖音极速直下”，程序自动在桌面生成新的可播放 MP4。

## 2. 正向约束

- 用户现实路径保持：复制分享文本/链接 → 双击桌面入口 → 自动完成。
- 输出必须是新的 MP4。
- 必须包含 video + audio。
- duration > 0。
- 双击后不要求人工继续操作。
- 成熟方案优先，不为自研而自研。
- Reality 只验证已经冻结的候选。
- 本轮只做生产同构虚拟重放，不重新执行真实抖音下载。

## 3. 反向约束

- 不把虚拟重放写成新的 Reality 认证。
- 不因页面/版本/路径恢复问题而改变用户目标。
- 不提前伪造未来 Freeze。
- 不在 Reality 阶段边跑边改冻结候选。
- 不把未执行的 fallback / browser 路线说成已认证。
- 不把方法固定版本与动态任务状态版本混为同一个 ref。
- 不为了“架构完整”额外增加 Agent、页面或文件。

## 4. 历史 Reality Oracle（重放判定依据）

历史母任务：
`workspaces/douyin-oneclick-method-v1/`

主要依据：
- `TASK_CONTRACT.md`
- `R0_VIRTUAL_FREEZE.md`
- `R1_REALITY_FREEZE.md`

历史已知正确终局（用于虚拟重放，不代表本轮新 Reality）：
- R1 `FINAL_VALID=YES`
- `EXACTLY_ONCE=PASS`
- 新 MP4 存在
- staged ffprobe：video=1、audio=1、duration=14.883333
- runner 退出后独立 ffprobe 再次 PASS
- `T_RUN_VALID=11,219.662ms`

## 5. 本轮虚拟成熟 DONE_WHEN

必须完整完成以下两次生产同构虚拟重放：

1. 从 `TASK_ACCEPTED` 开始，按当前正式方法版本运行到虚拟 `FINAL_VALID`；
2. 中间必须至少发生一次“虚拟节点 Freeze → CEO 换页 handoff → Reality 重放”，以实际验证跨页状态恢复；
3. handoff 必须机械验证：
   - 方法固定版本能读取 BRAIN/ENGINE/NEW_PAGE_TEMPLATE；
   - 任务状态版本能同时读取本任务约束文件与当前 Freeze；
4. 第一遍若出现确认的方法故障：立即停止、最小修复对应方法版本、从 `TASK_ACCEPTED` 重跑；
5. 第一遍完整无故障后，再从 `TASK_ACCEPTED` 做第二遍 clean replay；
6. 两遍均无结构故障才允许：
   - `VIRTUAL_MATURE=YES`
   - `REALITY_CERTIFIED=NO`（指本轮未重新 Reality）

## 6. 当前方法固定版本

- 《人工单页面极限短时间引擎》第22版
- 《极限短时间执行大脑》第18版
- 《新页面运行模板》第17版
- METHOD_REF=`e64f7593a732a99c82c8d4e36b30e25f89d00aa7`

权威仓库：
`cuiqinggang/codex-private-skills`
