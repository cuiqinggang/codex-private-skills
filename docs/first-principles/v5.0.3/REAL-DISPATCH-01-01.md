【整体闭环极限时间引擎5.0.2版｜v5.0.3唯一锚定物连续状态现实认证｜01-01｜实】 锚定物=T*=min(T_VALID)｜状态=VIRTUAL_FROZEN｜当前T*=0.831423ms｜现实最优=PENDING

ACTION=REAL_DISPATCH
UNIQUE_ANCHOR=T*=min(T_VALID)
TIMELINE_ID=ESTE-v5.0.3-TIME-LEDGER-MATURATION-01
TIME_ORIGIN_UTC=2026-09-26T15:51:00Z
TIME_EVENT_SEQ=2
ANCHOR_STATE=VIRTUAL_FROZEN
ACTIVE_T_STAR_MS=0.831423ms
BEST_CERTIFIED_T_VALID_MS=PENDING
T_VALID_START=immediately before run_reality_certificate() after exact frozen capsule materialization
T_VALID_END=immediately after run_reality_certificate() returns 27/27 PASS and evidence consistency is confirmed
T_STAR_SOURCE=GPT_27_CHECK_CERT_MIN_X_v5.0.2_CERTIFIED_WINDOWS_GPT_RATIO

本任务只认证“唯一锚定物是否已经成为连续、强制、不可省略的流程状态”。不得重新设计。

权威共同私库：
https://github.com/cuiqinggang/codex-private-skills

权威分支：
codex/first-principles-physical-limit-convergence-v5.0.3-virtual-freeze

1. 读取完整 Freeze：
docs/first-principles/v5.0.3/FREEZE-MANIFEST.json
期望 blob：
ad12352fcd4a3b44004b60b60e8088f58db5667f

2. 读取发布后一致性收据：
docs/first-principles/v5.0.3/FREEZE-CONSISTENCY-REPORT.json
期望 blob：
7dd484fc42ca77bb4a59ee8de03802ad8752fda7
必须确认 asset_count=10、post_publish_reread_count=10、mismatches=[]、FREEZE_MANIFEST_CONSISTENT=PASS。

3. 读取完整 Reality Capsule 源码正文：
docs/first-principles/v5.0.3/REAL-CAPSULE-SOURCE-R2.py
期望 Git blob：
b61c4c2efc50ad144c3b92653da1eb787fe5bbc6

必须取得完整 UTF-8 源码正文，并在同一个 fresh Python namespace 中 compile + exec。
执行后必须确认：
callable(namespace.get('run_reality_certificate')) == True

4. 在运行证书之前，先核对当前控制快照必须与本命令顶部完全一致：
UNIQUE_ANCHOR=T*=min(T_VALID)
TIMELINE_ID=ESTE-v5.0.3-TIME-LEDGER-MATURATION-01
TIME_ORIGIN_UTC=2026-09-26T15:51:00Z
TIME_EVENT_SEQ=2
ANCHOR_STATE=VIRTUAL_FROZEN
ACTIVE_T_STAR_MS=0.831423ms

任何一项不一致：
TIME_STATE_MISMATCH
STOP
RETURN_TO_GPT=YES

5. 现实计时只覆盖最小 Reality Certificate：
紧贴 namespace['run_reality_certificate']() 前记录 REAL_START 和 REAL_START_UTC；
成功返回后立即记录 REAL_END 和 REAL_END_UTC。

T_VALID_REAL_MS=(REAL_END-REAL_START)/1_000_000

证书必须返回：
TOTAL=27
PASS=27

6. REAL PASS 硬门：
FREEZE_MANIFEST_CONSISTENT=PASS
UNIQUE_ANCHOR=T*=min(T_VALID)
TIMELINE_ID 不变
TIME_ORIGIN_UTC 不变
REALITY_CERTIFICATE=27/27 PASS
EVIDENCE_CONSISTENT=YES
T_VALID_REAL_MS<=0.831422572

7. 若 PASS，报告时必须把同一时间轴继续追加为：
TIME_EVENT_SEQ=4
事件 3=REAL_START
事件 4=REAL_PASS
ANCHOR_STATE=REAL_CERTIFIED
BEST_CERTIFIED_T_VALID_MS=T_VALID_REAL_MS

若 FAIL：
仍使用同一个 TIMELINE_ID / TIME_ORIGIN_UTC；
追加 REAL_START + REAL_FAIL；
活动 T* 回到 PENDING；
历史事件不得删除；
STOP；
RETURN_TO_GPT=YES。

禁止现场修复、修改冻结资产、重新设计、改变唯一锚定物或引入第二评分指标。
