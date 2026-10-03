# 《十几年》10秒精品视频极限生成 v1.0 — Reality 生产交接 R1

【《十几年》10秒精品视频极限生成 v1.0｜Reality生产交接R1｜001｜实】
STATE=30 | STATUS=REALITY_HANDOFF_READY | FREEZE_ID=TEN-YEARS-v1.0-PREMIUM-BENCHMARK-R1 | REALITY/CODEX_MAX_STATE=40
TASK_ACCEPTED=2026-10-03T20:36:25.2807538+08:00 | CURRENT_NODE=STATE30_HANDOFF | T_VALID_START=NOT_STARTED | T*=N/A

## 1. 权威输入
- Freeze: `workspaces/ten-years-premium-video-v1.0/FREEZE.md`
- Freeze blob SHA: `f59f5ea4dcc06d5816a2c401d6fedf9e07a1e274`
- Freeze ID: `TEN-YEARS-v1.0-PREMIUM-BENCHMARK-R1`
- 视频方法: `skills/video-extreme-time-engine/SKILL.md`, version=0.5
- 视频方法 Freeze: `VETE-v0.5-H3P1-R1`
- 父级方法: `整体闭环极限短时间引擎 v5.6.5`
- 本地执行桥: `skills/extreme-time-automation-bridge/SKILL.md`, version=0.2.0

## 2. 已核验本地参考资产
- Device: `DESKTOP-4A1EGTM`
- Reference video: `C:\Users\A\Desktop\1abf89ceb41c6cfae2d0d13006b8a1e6.mp4`
- ffprobe duration: `14.255601s`
- 与 Freeze R01 的 14.255601s 完全一致。
- 该资产只作视觉/人物/动作/摄影第一锚点，不允许直接复用为最终输出。

## 3. Reality 固定故事
严格执行 FREEZE.md 第4节，禁止重写：
手机年轻女人+暧昧信息 → 妻子视觉反差 → “她是谁？！” → 抢手机 → 扫桌 → 重耳光 → 抓衬衫/推搡/哭喊 → “十几年！我跟了你十几年！” → 手机怼脸 → “就因为她年轻？！她漂亮？！” → 躲眼神 → “那我算什么？！” → 丈夫下跪 → 妻子“滚！”离场 → 丈夫抓空。

## 4. Quality Contract
必须整体满足 Freeze 的 Quality Contract v2。
任何强制失败项触发：
`PREMIUM_VIDEO_VALID=NO`
且该候选不得计入 `T_VALID/T*`。

尤其不可缺失：
- 第一秒出轨证据可读；
- 年轻女人与妻子反差成立；
- 扫桌/耳光/抓衬衫/推搡/下跪关键冲击成立；
- 对白、呼吸、哭喊、耳光、碰撞、跪地音画同步；
- 人物脸/衣服/身份稳定；
- 无严重手指/面部/肢体结构错误；
- 关键5传播帧至少3张具备独立传播力；
- 整体达到 Benchmark-10 质量等价。

## 5. Time Contract
```ini
INTERNAL_OBJECTIVE=T*=min(T_VALID)
VALID_REQUIRES=PREMIUM_VIDEO_VALID=YES
EXTERNAL_COMPARISON_REQUIRED=YES
FIRST_STAGE_TARGET_T_VALID_MS=259000
RAW_EXTERNAL_10S_FRONTIER_MS=91000
CURRENT_15S_2K_REFERENCE_MS=343000
```

`T_VALID_START` 只能在“正式生成任务已被生产执行器接受”时落表。
预检、资产发现、报告整理、ZIP、哈希、归档不进入 T_VALID。
`T_VALID_END` 停在最后一个必要业务 VALID verifier PASS 的真实时间。

## 6. 执行架构
优先复用已 Reality 证明的成熟模式：
```
single closed-loop runner
+ warm service/model reuse
+ safe conditioning/static-node reuse
+ new sampler execution
+ bounded output publication wait
+ single decode
+ parallel independent verifiers
+ VALID_END before report packaging
```

禁止：
- 复用旧最终输出；
- 为追求速度降低冻结质量；
- Reality 侧自行改剧本/Benchmark/Quality/Time Contract；
- 把失败候选时间冒充 T_VALID/T*；
- 把报告打包时间算进 T_VALID。

## 7. 首轮 Reality 输出合同
必须产生：
1. 新生成候选视频文件；
2. `T_VALID_START` / `T_VALID_END`；
3. 机械计算 `T_VALID_MS`；
4. 生成阶段分解；
5. 关键5传播帧；
6. 音频/对白/冲击声/AV sync 核验；
7. 人物一致性/肢体结构核验；
8. Benchmark-10 Quality Equivalent 结论；
9. `PREMIUM_VIDEO_VALID=YES|NO`；
10. 若 VALID，则更新本项目当前 `T*` 候选；若 INVALID，仅记录诊断。

## 8. 当前 Reality 入口状态
```ini
STATE=30
FREEZE_VERIFIED=YES
REFERENCE_ASSET_VERIFIED=YES
REALITY_PACKAGE_READY=YES
VIDEO_GENERATION=NOT_STARTED
T_VALID_START=NOT_STARTED
FINAL_VALID=NO
NEXT_ACTION=SUBMIT_FROZEN_JOB_TO_EXISTING_MATURE_VIDEO_EXECUTOR
```

## 9. 状态边界
Reality/Codex 最高合法状态为 40。
只有 GPT Final Review 可执行 40→100。
