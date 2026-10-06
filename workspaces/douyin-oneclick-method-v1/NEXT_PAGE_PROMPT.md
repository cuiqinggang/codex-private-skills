CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"DOUYIN-ONECLICK-METHOD-V1-R2-F001","page_id":"EXTREME-TIME-V8-HIPE-FUSION-20261006","task_id":"DOUYIN-ONECLICK-METHOD-V1","node_id":"DOUYIN-ONECLICK-METHOD-V1-R2-VIRTUAL","sequence":3,"state_code":20,"freeze_status":"READY_FROZEN","final_valid":"NO","t_valid_ms":null,"t_star_ms":1351629.297,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"7b787c9d048fcf4dc1a202d570672aaffc95633a","freeze_path":"workspaces/douyin-oneclick-method-v1/R2_VIRTUAL_FREEZE.md","next_node":"DOUYIN-ONECLICK-METHOD-V1-R2-REALITY"}

执行《人工单页面极限短时间引擎 第8版》和《极限短时间执行大脑 第3版》。

【抖音极限直下方法验证｜DOUYIN-ONECLICK-METHOD-V1-R2-REALITY｜04｜实】
状态机：30｜R2-VIRTUAL=READY_FROZEN｜R2-REALITY=READY_TO_RUN｜FORMAL_REALITY_COUNT_R2=0
时间锚：R1_T_RUN_VALID=11,219.662ms｜R1_BUILD_T_VALID=1,351,629.297ms｜当前建设 T*=1,351,629.297ms｜NEXT=exactly-once R2 Reality

权威来源：

REPO=cuiqinggang/codex-private-skills
REF=c20210acec620f5b2dfbb6f8089cee68d6597e3f

ENGINE_PATH=skills/artificial-single-page-extreme-time-engine/ENGINE.md
BRAIN_PATH=skills/artificial-single-page-extreme-time-engine/BRAIN.md
TEMPLATE_PATH=skills/artificial-single-page-extreme-time-engine/NEW_PAGE_TEMPLATE.md
HIPE_INTEGRATION_PATH=skills/artificial-single-page-extreme-time-engine/HIPE_V035_INTEGRATION_FREEZE_V2.md
TASK_PATH=workspaces/douyin-oneclick-method-v1/TASK_CONTRACT.md
R1_FREEZE_PATH=workspaces/douyin-oneclick-method-v1/R1_REALITY_FREEZE.md
R2_FREEZE_PATH=workspaces/douyin-oneclick-method-v1/R2_VIRTUAL_FREEZE.md

HIPE 固定冻结：

HIPE_PATH=skills/hybrid-intelligence-probability-engine-v0-3-5/
HIPE_FREEZE_COMMIT=c6fe2878fd237e7a8120b3af8e75f93e3cd6a4d9
HIPE_FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1

任务：执行 DOUYIN-ONECLICK-METHOD-V1-R2-REALITY。

本页只认证上一页已经冻结的 R2 bundle，不允许边跑边修改，不允许先试跑，不允许重复 Reality。

R2 冻结候选：

- 仅把 Route A 的 3 个轻量公共解析请求从串行改为并发抢首个合法直链；
- provider 集合仍为 bugpk / aa1 / xinyew；
- winner 出现后取消仍在等待的解析请求；
- 正常成功路径仍只下载 1 份 MP4；
- 下载完成后 staged ffprobe 必须 video>=1、audio>=1、duration>0；
- staged PASS 后才 atomic publish；
- runner 完全退出后必须由独立 verifier 再次 ffprobe；
- exactly-once、target protection、failure evidence 全保留；
- race winner 的媒体下载/验证失败时，才进入剩余 A 路旧成熟 fallback；
- race 基础设施异常时回旧 A 串行 fallback；
- 3 个 race 请求都正常完成但均无合法直链时，直接进入 B，不重复同一组 A 请求；
- B content-downloader 与其 browser fallback 仍保留，但未认证前不得声称已认证；
- hot path 不调用 JEV，不调用 OpenRouter，不调用浏览器。

本地冻结 bundle：

ROOT=C:\Users\A\Documents\Codex\2026-10-06\douyin-oneclick-method-v1

RUNNER=runner-r2.ps1
RUNNER_SHA256=c80e767ddf56199da89c6f19d84251aa08952af240f9556e7f2b3c1b1371a1a0

VERIFIER=verify-final-r2.ps1
VERIFIER_SHA256=f9a74506ef9b22caf6aaa9c23af6c71701c3d9429f1ccb931b5de7eece158777

ENTRY=R2_REALITY_ENTRY.cmd
ENTRY_SHA256=cf658c5037e96a87c9c2672c47a189e972c4135df51b18c3107ef18b5496b18b

Reality 前门禁：

1. 回读 R2_VIRTUAL_FREEZE.md；
2. 校验以上 3 个 SHA256，任一不匹配立即 STOP；
3. 确认 R2_FORMAL_CLAIM.json 不存在；
4. 确认 R1 冻结文件与原 R1 runner/verifier 不被修改；
5. 把冻结的 R2_REALITY_ENTRY.cmd 原子部署为本轮桌面正式入口；
6. 冻结 READY_STATE 后，不再改变任何候选字节；
7. 使用 TASK_CONTRACT.md 同一正式样本；
8. exactly-once 启动一次正式入口。

必须采集：

- FORMAL_REALITY_COUNT_R2；
- FORMAL_ENTRY_START_COUNT；
- EXACTLY_ONCE；
- route_A_resolve_race winner；
- 每个已完成 resolver 的状态/耗时；
- route_A download；
- staged ffprobe；
- atomic publish；
- runner_elapsed_to_exit；
- runner 完全退出后的 independent_final_ffprobe；
- T_RUN_VALID_R2；
- 新桌面 MP4 size / SHA256 / video / audio / duration；
- fallback 是否执行。

R1 比较基线：

- T_RUN_VALID_R1=11,219.662ms；
- route_A_request_bugpk=3,608.663ms；
- route_A_download_bugpk=5,972.339ms；
- staged_verify=655.067ms；
- atomic_publish=125.658ms；
- independent_final_ffprobe=107.848ms。

判定：

- 若 R2 FINAL_VALID=NO：FAIL_FROZEN；不得同页补丁重跑；
- 若 R2 FINAL_VALID=YES 且 T_RUN 明显降低：冻结 Reality 证据，记录新的生产 T_RUN 候选；
- 若 R2 FINAL_VALID=YES 但收益不明显/仅属抖动：STOP，保留 R1，不为凑轮数继续；
- 无论 A 是否成功，都不得把未执行的 B/browser 写成已认证；
- 建设任务全局 T*=1,351,629.297ms 继续保留；R2 只比较生产 T_RUN_VALID，不用更晚的建设时间覆盖 R1 建设 T*。

禁止：

- 不重跑 R1；
- 不执行 Greenfield-R11；
- 不读取/复制 Greenfield R1-R10 代码作为实现基线；
- 不在 Reality 期间改 runner / verifier / entry；
- 不新增 Python/httpx resolver；该候选已因本地冷启动 AVG=618.104ms 被淘汰；
- 不启动三路完整视频并行下载；
- 不把 OpenRouter API key 写入任何代码、仓库、日志或冻结文件；
- deterministic hot path 不调用 JEV；
- 不为了凑轮数执行第二次 R2 Reality。

Reality 结束后必须按《新页面运行模板 第4版》写新的 CEO_FREEZE_TAG_JSON；最终回复必须原样完整输出唯一 NEXT_PAGE_PROMPT。
