# HIPE v0.3.5 — 简洁生产成熟版

VERSION=0.3.5；COMMON_SCENARIO_ACCEPTANCE=21/21；CORE_FUNCTIONAL=PASS；
PRODUCTION_READY=YES；DONE=YES。认证范围限定于本包已覆盖的常用任务域。

原有 Reality Solvability Gate v0.2 / Forward Compiler v0.2 接入正式入口，
对成熟直接、组合、探索协议优先判定；未知必须有排除前三类的检索证据。
已认证任务按内容匹配冻结快路径，优先 CODE > JEV > GPT residual。
不满足 JEV 条件时回退 GPT 待审；无可靠验收合同不执行或标为 VALID。

R4 核心执行、deterministic verifier、合法并行与 R5 完整计时保持原样。
原 R4 21/21 哈希匹配；9/9 运行依赖按原字节继承；8 项主要函数 AST 相同。
新增生产适配器只暴露入口、单节点调用、失败状态与使用记录。
正式命令见 SKILL.md；主入口 runtime/production.py。
未认证开放任务是明确 GPT 交接，不能解释为任意开放任务已自动完成。

## 验收

- A–G 各 3 例，固定 21/21 路由和安全语义 PASS，远端请求 0。
- 检查错误 Choice/SQL、延迟最终写入、写入失败、回读损坏、
  旧输出拒绝，以及 JEV/GPT/混合 RuntimeError 的 fail-closed。
- 离线 fixture 标记 OFFLINE_TEST，不作为真实模型实测。
- 历史集成 18/18、R5 28/28（原含 5000 性质案例）、R4 73/73 仅引用；
  未重跑大型攻击集，未扩展正式案例数量。
- 本地 CODE 新真实执行 PASS；完整 T_VALID=20.2368 ms。
- 根据用户后续明确指令，本轮没有新增远端调用：
  JEV、GPT residual、混合路径复用成功的历史真实运行。
  重新核验原 R5 receipt、输出哈希及 8 条真实 SQL 的 verifier 结果。
  历史混合运行完整 T_VALID=15315.9103 ms；这是历史值，不是新版本性能成绩。
- 历史 RuntimeError 明确 FAIL，未产生对应 VALID 输出；
  原记录不足以确定根因，不擅自归因为已证实的瞬态错误。

## 发布与边界

ROUTING_CORRECT=YES；VERIFIER_FAIL_CLOSED=YES；SILENT_WRONG_RESULT=0（已验范围）；
FINAL_WRITE_INCLUDED=YES；CORE_PATHS_USABLE=YES。
PERFORMANCE_30_RUN_CERTIFIED=NO；
PERFORMANCE_BASELINE=ACCUMULATE_FROM_REAL_USAGE。

T_VALID 沿用冻结 R5 语义：覆盖入口到任务最终文件写入、回读、哈希；
计时 receipt 和 status 是事后观察元数据。candidate.json 单独存在不构成成功。
status 写入失败抛出异常，不返回 VALID。未知/缺凭据/不支持的依赖组合明确 FAIL，
指定混合入口处理冻结依赖任务，不现场增加调度架构。
SQL verifier 的认证范围是冻结 fixture，不宣称为通用 SQL 语义证明。

现实限制：本次新增入口未做新的远端实测，远端可用性依据已验且未改的核心及历史真实证据，
配合本轮离线路由安全验收；此限制按用户“不新增调用，仅引用历史真实证据”执行。
这不是 30 轮远端性能认证。

运行记录存于各次 status.json。发布后不主动升级、不新增自动任务。
仅重复、有实际影响的问题交回 GPT 判断 v0.3.6；可识别且 fail-closed 的偶发外部异常
不自动触发升级。ACTION=STOP；RETURN_TO_GPT=YES。

## 正式资产与 SHA256

正式根目录：C:\Users\A\Documents\Codex\2026-09-29\5-hipe-v0-3-5-01\outputs\hipe-v0.3.5

以下是完整资产及依赖清单，发布说明本身的 SHA256 单独回传。

| 相对路径 | SHA256 |
|---|---|
| COMMON-SCENARIO-ACCEPTANCE.json | e97bc77687df7825806f69f0b233208f0a7420cde041990f22a9c7dac2c5c81e |
| CURRENT_STATE.json | 16b86c4ccbd69b8acfbd633f382f74b11d3d3434eece471975fa26b793115947 |
| runtime/inherited/components/comfort-zone-forward-compiler/forward_compiler.py | fe5f73dcbc48b21efb8e8977b8be23b3da802a815617a664022f34abe620f070 |
| runtime/inherited/components/reality-solvability-gate/reality_solvability_gate.py | 92dfe0a356627ddd698b21438f79c919df2d739c65461ddb7d57d7be865c9b88 |
| runtime/inherited/frozen/v0.3.4/HIPE-v0.3.4-real-verify.py | 73e8d239bafba4916cab7d69f0d92f61bb4b406cb35b2a1a9f2e0223d188c519 |
| runtime/inherited/frozen/v0.3.4/PRIVATE-ORACLE-v0.3.4.json | f073bf1264c0f2d46ad497388df68d6203460d92c8064c5fbd5bf254eb57a60f |
| runtime/inherited/frozen/v0.3.4/PRIVATE_REFERENCE_AUDIT.json | 844eac8a6d571e125b5df7a37fa4cbf565dabfc0d2dc7d586437757252188905 |
| runtime/inherited/frozen/v0.3.4/PUBLIC-BENCHMARK-R2-BASELINE.json | 4cdf0e8d483dadcc418715b73d95d1f80f69b4357de89f808dec87b2763c3aa5 |
| runtime/inherited/frozen/v0.3.4/PUBLIC-BENCHMARK-v0.3.4.json | ecd4c20f69c34a8171f75199002164572386a310e8054a0009004bc22d4c6a6f |
| runtime/inherited/frozen/v0.3.4/sql_scope_audit.py | da6a0f641e05c36cdb0af5d37a4976526368ebb2387cb1c8f2a713c503ffd4a0 |
| runtime/inherited/frozen/v0.3.4/timing_boundary_candidate.py | c3f51f04c8269cbf1289416a531344c1e71ca84460597630b31b14e742dd6fe8 |
| runtime/production.py | 92ea9d65316c2e071611a9acc0cf88e60e249f3922220b60cb2bed84d16d90fa |
| SKILL.md | 6958e3602794f04943cd4ec03c02fe4830c428b6f8126743f28fdf465ab9f990 |

## 复用与工具记录

CodeGraph usage:
- MCP available: YES
- CLI available: YES
- .codegraph index present: NO
- status checked before work: YES
- callers/callees/impact checked where relevant: 定向读取及 AST 核验
- sync/refresh run after meaningful code changes: NO
- if not used, reason: 源及目标工作区无 .codegraph

Knowledge Brain usage:
- INDEX checked: YES
- ROUTING_MAP checked: YES
- Relevant indexes checked: skills-index.md
- CodeGraph used where relevant: 无索引，定向源码回退
- OpenHuman reference used where relevant: 不涉及记忆架构，不适用
- Sync run before/after: 未改索引，不运行同步；收尾健康检查 PASS
- If not used, reason: 已使用检索；遵从最小资产范围，不新增知识文档体系
