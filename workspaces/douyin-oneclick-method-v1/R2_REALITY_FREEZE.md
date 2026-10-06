CEO_FREEZE_TAG_JSON={"schema":"CEO_FREEZE_TAG_V1","freeze_id":"DOUYIN-ONECLICK-METHOD-V1-R2-REALITY-F001","page_id":"EXTREME-TIME-V8-HIPE-FUSION-20261006","task_id":"DOUYIN-ONECLICK-METHOD-V1","node_id":"DOUYIN-ONECLICK-METHOD-V1-R2-REALITY","sequence":4,"state_code":100,"freeze_status":"FAIL_FROZEN","final_valid":"NO","t_valid_ms":null,"t_star_ms":1351629.297,"source_repo":"cuiqinggang/codex-private-skills","source_ref":"c20210acec620f5b2dfbb6f8089cee68d6597e3f","freeze_path":"workspaces/douyin-oneclick-method-v1/R2_REALITY_FREEZE.md","next_node":"DOUYIN-ONECLICK-METHOD-V1-R3-VIRTUAL"}

# R2 REALITY FREEZE — DOUYIN-ONECLICK-METHOD-V1

【抖音极限直下方法验证｜DOUYIN-ONECLICK-METHOD-V1-R2-REALITY｜04｜实】
状态机：100｜R2=FAIL_FROZEN｜FINAL_VALID=NO｜FORMAL_REALITY_COUNT_R2=1｜EXACTLY_ONCE=PASS
时间锚：READY_STATE=2026-10-07T00:18:12.2689060+08:00｜RUN_START=2026-10-07T00:18:27.5557477+08:00｜FAIL_AT=2026-10-07T00:18:27.7806305+08:00｜RUNNER_FAILURE_ELAPSED=206.974ms｜T_RUN_VALID_R2=null｜BUILD_T*=1,351,629.297ms

## 1. 正式 Reality 结论

```text
FORMAL_REALITY_COUNT_R2=1
FORMAL_ENTRY_START_COUNT=1
EXACTLY_ONCE=PASS
FINAL_VALID=NO
FAILURE_CLASS=DOUYIN_URL_NOT_FOUND
T_RUN_VALID_R2=null
R1_T_RUN_VALID=11,219.662ms
BUILD_T_STAR=1,351,629.297ms
```

本页严格只启动一次冻结的桌面正式入口。R2 persistent claim 已创建：

```text
run_id=R2-20261007-001827-555
claimed_at_local=2026-10-07T00:18:27.5887339+08:00
formal_reality_count=1
```

失败后没有第二次 R2 Reality，没有边跑边修改 runner / verifier / entry，也没有重跑 R1。

## 2. Reality 前门禁

权威 R2_VIRTUAL_FREEZE 已从固定共同工作区 commit 回读。

冻结 bundle SHA256 全部 PASS：

```text
runner-r2.ps1
c80e767ddf56199da89c6f19d84251aa08952af240f9556e7f2b3c1b1371a1a0

verify-final-r2.ps1
f9a74506ef9b22caf6aaa9c23af6c71701c3d9429f1ccb931b5de7eece158777

R2_REALITY_ENTRY.cmd
cf658c5037e96a87c9c2672c47a189e972c4135df51b18c3107ef18b5496b18b
```

R1 保护 PASS：

```text
runner.ps1
4db6bfd6898191d203b70f67391f76ab908c8a27db774ec8c7af594d23c8a500

verify-final.ps1
2b38abafb311ce76397c452755f1bb2dbe3b72ba533de3c45e98ee93239490d0
```

门禁时：

```text
R2_FORMAL_CLAIM_EXISTS=False
DESKTOP_ENTRY_BEFORE_SHA256=6ce5769249c4453a6a9c499a8b6eeefb2664c9111f5f904bbc245a74ee061f60
DESKTOP_ENTRY_AFTER_R2_DEPLOY_SHA256=cf658c5037e96a87c9c2672c47a189e972c4135df51b18c3107ef18b5496b18b
DESKTOP_MP4_COUNT_BEFORE=9
READY_STATE=FROZEN
```

前门禁曾有两次纯 shell/parser 失败，均发生在 formal entry 启动之前，未创建 R2 claim、未启动 runner、未改变冻结 bundle，因此不计入 FORMAL_REALITY_COUNT_R2。

## 3. 正式 Reality 证据

Evidence root：

```text
C:\Users\A\Documents\Codex\2026-10-06\douyin-oneclick-method-v1\evidence\R2-20261007-001827-555
```

事件：

```text
exactly_once_claim=PASS @ elapsed 121.993ms
failure=DOUYIN_URL_NOT_FOUND @ elapsed 208.578ms
runner failure elapsed=206.974ms
verifier result=FINAL_VALID=NO
```

FINAL_RESULT：

```text
schema=DOUYIN_ONECLICK_R2_FINAL_V1
final_valid=NO
runner_exit_code=2
failure_class=DOUYIN_URL_NOT_FOUND
verified_at_local=2026-10-07T00:18:28.2656248+08:00
t_run_valid_ms=null
t_build_valid_ms=null
```

## 4. 本轮未执行的冻结候选阶段

失败发生在 clipboard_extract，早于 Route A。

因此以下全部只能写为 NOT_EXECUTED，禁止冒充已认证：

```text
route_A_resolve_race=NOT_EXECUTED
race_winner=NOT_EXECUTED
resolver_bugpk=NOT_EXECUTED
resolver_aa1=NOT_EXECUTED
resolver_xinyew=NOT_EXECUTED
route_A_download=NOT_EXECUTED
staged_ffprobe=NOT_EXECUTED
atomic_publish=NOT_EXECUTED
independent_final_ffprobe=NOT_EXECUTED
fallback_A_sequential=NOT_EXECUTED
route_B_content_downloader=NOT_EXECUTED
browser_fallback=NOT_EXECUTED
```

独立 verifier 进程本身已运行，但因为 runner_exit_code=2 且没有 run_context.json，按冻结 verifier 合同直接记录 FINAL_VALID=NO；它没有进入 final ffprobe。

## 5. 根因边界

本次失败不能归因于并发 resolver bundle。

Reality harness 在 READY_STATE 前通过远程 PowerShell 写入正式分享文本；正式运行后独立回读剪贴板得到乱码文本，且：

```text
contains_expected_url=False
expected_url=https://v.douyin.com/jRJYc4pme7Q/
```

也就是说，runner 真正读取剪贴板时并没有 TASK_CONTRACT 要求的正式 URL。冻结 runner 正确拒绝了不合格输入并退出。

冻结结论：

```text
FAILURE_DOMAIN=REALITY_HARNESS_INPUT_PREPARATION
R2_RACE_CANDIDATE_CERTIFIED=NO
R2_RACE_CANDIDATE_DISPROVEN=NO
```

按本页硬规则，既然 FINAL_VALID=NO，R2 必须 FAIL_FROZEN；不得把“测试器输入准备错误”当理由在同页再跑一次。

## 6. 输出与目标保护

```text
DESKTOP_MP4_COUNT_BEFORE=9
DESKTOP_MP4_COUNT_AFTER=9
NEW_DESKTOP_MP4=NONE
NEW_MP4_SIZE=NOT_PRODUCED
NEW_MP4_SHA256=NOT_PRODUCED
NEW_MP4_VIDEO=NOT_PRODUCED
NEW_MP4_AUDIO=NOT_PRODUCED
NEW_MP4_DURATION=NOT_PRODUCED
```

没有 staged 文件被 publish，没有覆盖旧桌面 MP4。

## 7. 生产入口回滚

R2 未获认证，因此没有把未认证入口留在生产桌面。

Reality 证据采集后，桌面入口已原子恢复到 R1：

```text
PRODUCTION_ENTRY=R1_RESTORED
DESKTOP_ENTRY_SHA256=6ce5769249c4453a6a9c499a8b6eeefb2664c9111f5f904bbc245a74ee061f60
```

未重跑 R1。

## 8. 时间与 T*

R2 没有产生合法 FINAL_VALID，因此：

```text
T_RUN_VALID_R2=null
R1_PRODUCTION_T_RUN_VALID=11,219.662ms
BUILD_T*=1,351,629.297ms
T*_UPDATED=NO
```

不得用本轮更晚的建设时钟覆盖 R1 已冻结的建设 T*。

## 9. 下一节点

下一页只允许：

```text
DOUYIN-ONECLICK-METHOD-V1-R3-VIRTUAL
```

R3-VIRTUAL 的目标不是再次运行 R2，而是先修复 Reality harness 的输入前门禁：

- 不改变 R2 下载候选逻辑；
- 使用编码安全的正式样本注入；
- 在 persistent claim 之前 deterministic readback，必须确认同一正式 URL 存在；
- 将“输入 readback PASS”加入 READY_STATE 强制门禁；
- 只有新 Freeze 完成后，才允许未来新的 R3 Reality；
- R2 正式 Reality 永久保持 count=1。
