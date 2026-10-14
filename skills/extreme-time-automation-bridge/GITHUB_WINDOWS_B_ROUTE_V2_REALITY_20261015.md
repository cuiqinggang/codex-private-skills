# GPT直连Windows双路执行桥 V2｜B 路 Reality 5/5 与极限有效时间（2026-10-15 北京时间）

METHOD=SANRENXING_V2_TASK_SCOPED (用户明确指定；三人行V2仍是待审查候选，不改其全局正式状态)
SKILL=skills/extreme-time-automation-bridge/SKILL.md@2.0.0
NETWORK=保留 FlClash、Windows 系统代理、Runner 服务及 A 通道原状
SUBJECT=B GitHub 共同工作区 → GitHub Actions → Windows self-hosted Runner → 官方 Artifact/结果回读
TASK_SCOPE=同构无副作用算术任务；小型 stdout/stderr/result.json 证据
STATUS=BOUNDED_ARTIFACT_5_OF_5_REALITY_PASS;GENERAL_FULL_5_OF_5=NOT_ACCEPTED;LONG_TERM_ZERO_FAILURE=UNKNOWN

## 一、实际 GOOD/BAD 基线，不以成功绿灯替代业务回执

历史原 FULL：
- [Run 38240277230](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38240277230) 2026-10-12 完整 PASS 约156s。
- [Run 38264768349](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38264768349) 2026-10-12 FAIL 约419s，Windows `Set up job` 的 Action ZIP 失败。
- [Run 38405736959](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38405736959) 2026-10-13 FAIL 约422s，`actions/upload-artifact@v4` 固定 SHA 的 `codeload.github.com` ZIP 传输每次100s、共3次失败，payload 未执行。

本轮正式 FULL 新增两次隔离测试，唯一安全纯计算 payload，task_id 每次独立：
- R1：[Run 38601884050](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38601884050)：2026-10-15 00:53:13→00:54:50，**97s PASS**，上传官方 Artifact 11914016875；固定 SHA 冻结文件、Windows 执行、官方 Artifact、回调判断全部完成。Windows job 16:53:45Z 开始外部 Action ZIP 准备，16:54:34Z 完成冻结文件读取；原本易故障的代码下载约占大部分耗时。GitHub CLI 从 Artifact 真实取回 result.json/stdout/stderr，任务ID/状态/退出码对账 PASS。业务约1583.649ms。
- R2：[Run 38602538548](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38602538548)：2026-10-15 00:57:43→01:00:07，**144s PASS**；Artifact 11913683852，三份证据完整回读 PASS。两次 FULL 都成功，但完成时间相差47s。不能宣布 FULL 历史间歇超时根因已修复。

## 二、官方 FAST 原既有候选 Reality

[Run 38602210133](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38602210133)：2026-10-15 00:55:27→00:55:54，**27s PASS**。相同类型纯计算、冻结SHA、Windows独立执行、GitHub日志回执、RESULT=PASS、EXIT=0、stdout SHA256；`TOTAL_STEP_MS=7097`、payload约2187.946ms。**不提供官方 Artifact，因此不与 FULL 功能全等价**。

## 三、成熟组合的隔离 V2 有界证据路线

候选文件：[.github/workflows/windows-bridge-v2-bounded-artifact.yml](https://github.com/cuiqinggang/codex-private-skills/blob/main/.github/workflows/windows-bridge-v2-bounded-artifact.yml)，提交 [f5552136](https://github.com/cuiqinggang/codex-private-skills/commit/f55521366c8fb6e0fc9845c67def4993b9831df1)。

成熟组件，无新桥：
- 复用现有 `windows-bridge-v1-fast.yml` 冻结 SHA 读取、白名单、现有 `Invoke-BridgeTask.ps1`、本地 result.json/stdout/stderr，Windows 上不执行外部 Action `uses:`。
- Windows 小结果以压缩 ZIP 的 base64 加入 GitHub 原生 Job Outputs；显式限制 b64 字符 <=480000 且 hosted 解码 ZIP <=360000 bytes（不是任意大小通路）。
- GitHub 官方托管 Ubuntu Job 校验完整三文件 + task_id + PASS + exit0，使用官方 `actions/upload-artifact@v4` 将 3 个文件归档30天；原可选 callback 配置存在时才发送，不配置就跳过。
- 不修改 FlClash、系统代理、Windows Runner 环境、已有原 FULL。**本候选仅手动触发**；不得作为任意生产任务的自动替代。输出超限发生在任务执行之后，**不能自动重新派发旧 FULL**（Exactly-once），须保留现场并人工核对；失败时证据上传行为未与原 FULL 等价。敏感 stdout/stderr 不得未经审核经 Job Outputs 传输。

### 五次独立本机执行 + GitHub 官方 Artifact (均真实 PASSED)

| 序号 | Run | Github完整耗时（created_at→updated_at） | 官方 Artifact ID | cloud success | 真正下载result.json/stdout.txt/stderr.txt |
|---|---:|---:|---:|---|---|
| R1 | [38603199346](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603199346) | 36s | 11913903599 | PASS | PASS |
| R2 | [38603459215](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603459215) | 36s | 11913529977 | PASS | PASS |
| R3 | [38603580797](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603580797) | 30s | 11914471832 | PASS | PASS |
| R4 | [38603712945](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603712945) | 36s | 11915146889 | PASS | PASS |
| R5 | [38603850316](https://github.com/cuiqinggang/codex-private-skills/actions/runs/38603850316) | 38s | 11914652213 | PASS | PASS |

- 5/5 为互相独立 GitHub Run ID 的无副作用同构计算任务，五次 Window job 和 hosted job 全部 success，五个 artifact 各自独立下载并解析真实 3 文件核验 PASS。另原 FULL R2 工件回读 PASS：此轮批量回读6/6。
- 平均耗时35.2s，中位数36s，最大38s、最短30s。**仅属于此测试集合的已观察短周期极值；不是物理极限。**
- 原 FULL 本轮 97s/144s，均值120.5s；与有界候选35.2s相比，在*成功且小证据的这一任务类别*内观测节省85.3s，约70.8%。由于新路线有证据大小上限、失败取证和静态审核方式差异，**这不是对任意 FULL 合同的同功能71%提速认证**。
- 基准口径：以上 GitHub created_at→updated_at，是**工作流云端可见总耗时**，没有包含上游 CEO 工具派发前端延迟及手工下载结果的人机时间。要宣称完整用户 `TASK_ACCEPTED→FINAL_VALID` 必须将上游外部费用、派发与回读时间也另计，不得只拿 1.6s/7s 的计算段当全程。
- 对“理论极限”：`T_physical_limit=UNKNOWN`。测得30s是 observed_min，不能凭一次最优样本证明全局最短。纯业务执行约2s，剩余主要为 GitHub 调度、网络、结果转移和托管归档固定成本；服务端排队无法靠本机计算优化为零。

## 四、成熟路径后的三路判定（冻结为 V2 小范围运行指南）

1. **FAST 27s（日志回执）**：独立、幂等、只需冻结输入+Job日志状态/简短结果、无需云端 Artifact/失败长期归档/回调的任务，优先沿原 `windows-bridge-v1-fast.yml`；该路线的业务内容权限必须符合原合同，未知副作用不盲重发。
2. **V2 有界归档 5/5（30-38s）**：明确事先已知小型无敏感输出，输出在Job outputs上限内，且用户可接受失败时无等价Artifact回传的任务；使用隔离 `windows-bridge-v2-bounded-artifact.yml`，需要完整真实 Artifact；**保持手工入口**，不得无条件路由任意业务。
3. **原 FULL**：大结果、必须保存失败证据、强认证/最严格合同、无法确定输出大小的任务仍走 `extreme-time-windows-bridge.yml`；目前97/144s两次成功，但历史419/422s失败的 codeload 长尾**没有根治**。GitHub 官方 Runner 层代理可作为网络修复方案，但历史 127.0.0.1:7890 完整 ZIP SocketException_ConnectionRefused，未证明稳定，禁止盲目改 Runner .env/重启服务。
4. 保留 A 自建 GPT-Windows-MCP、B GitHub、R quota 约束。当前任一业务流程只有经过对应质量/权限/Artifact/Exactly-once 合同的完整 Reality 才可升级为正式路由。

## 五、Freeze

DATE=2026-10-15
SKILL_VERSION=V2.0.0
TASK=GITHUB-WINDOWS-B-REALITY-20261015
STATE=BOUNDED_SUCCESS_ONLY_EVIDENCE_5_5_PASS
ORIGINAL_FULL=2_2_PASS_CURRENT;HISTORICAL_TWO_TIMEOUT_FAIL;NOT_FULLY_REPAIRED
WIN_RUNNER_PROXY=UNCHANGED
FLCLASH=UNCHANGED
MICRO_TEST_COMPUTE=VALID_ONLY_WITHIN_STATED_SCOPE
FAST_LOG_ONLY=1_1_PASS_27S
BOUNDED_ARTIFACT=5_5_PASS_30_38S;AVG35.2S
ARTIFACT_READBACK=6_6_PASS_R2_FULL_PLUS_FIVE_BOUNDED
NEXT=REAL_BUSINESS_SCOPE_ROUTING_ONLY_IF_OUTPUT_BOUNDED_AND_SAFETY_APPROVED;ARBITRARY_FULL_CODLOAD_REPAIR_NEEDS_AUTHORIZED_STABLE_RUNNER_NETWORK_EVIDENCE
FINAL_VALID_BOUNDED_SCOPE=YES
FINAL_VALID_GENERAL_FULL=NO
