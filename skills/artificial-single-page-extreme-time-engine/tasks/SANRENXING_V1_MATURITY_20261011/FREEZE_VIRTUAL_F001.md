# 《三人行》V1｜GPT CEO虚拟成熟冻结 F001（仅设计结论）
TASK_ID=SANRENXING_V1_MATURITY_20261011
NODE_ID=GPT-VM-001
OWNER=GPT_CEO
MODE=VIRTUAL_ONLY
METHOD_REF=skills/artificial-single-page-extreme-time-engine/SANRENXING_V1.md@SRX-V1-ACTIVE-F001
RUNTIME_REF=skills/artificial-single-page-extreme-time-engine/tasks/POLSIA_CAPABILITY_REPLICATION_20261011/CONTINUATION_RUNTIME_V3.md@3.0.0
FREEZE_ID=SRX-MATURITY-VM-F001
VERSION=V001
STATUS=VIRTUAL_SCOPE_FROZEN_REALITY_REQUIRED
VIRTUAL_MATURE=SCOPED_METHOD_FLOW_ONLY
FINAL_VALID=NO
T_VALID_REAL=UNKNOWN
BUSINESS_PRODUCTION=FORBIDDEN
LEGACY_POLSIA_METHOD_REF=UNCHANGED

## DONE_WHEN（不得因单项PASS提前结束）
1. GPT先读正式方法、实时状态与约束，形成最多三个成熟候选；以单GPT方案A作简单任务基准、GPT CEO＋Codex Ultra方案C作为本轮检验对象；并行P只有可验证净收益才启用。
2. 本独立TASK_ID上有真实GPT→现有合法Codex执行→节点事实产物+SHA+不可变Freeze→GPT独立回读验收的工具证据；至少一次代表性受控故障→GPT GOOD/BAD/FIRST_DELTA修正→Codex在真实新回执上复验。
3. 逐项负例：CRLF/LF、错误SHA、Freeze/版本不一致、无Freeze的exit0、非零退出、重复派发、未知INFLIGHT、PAUSE/STOP/WAIT、路径越界、写入回读失败；不能以单项单元测试代替跨节点全链路。
4. v3.0.0发布STAGED与Windows实际ACTIVE分离；ACTIVE只能在无同任务Codex执行、无UNKNOWN INFLIGHT、冻结SHA已回读和有回滚备份的安全门后进行，记录切换前后任务动作与SHA。
5. 没有真实下一节点自动接续＋GPT接管证据时FINAL_VALID=NO；72h/断电恢复是独立验收项，不因短时成功宣称全部无Bug。
6. 时间口径为接单到有效验收全程T_VALID；不编造物理下界、提速倍率及生产等效。

## 虚拟成熟候选与选择
A=单GPT直接完成轻任务；无额外Codex切换，适合无需外部执行的简单任务。
C=GPT CEO虚拟成熟和冻结→Codex Ultra执行→真实证据→GPT审核→遇故障返回GPT差分分析→重冻结→Codex只验证修复后的合法新步骤。选C作为本轮分工测试目标。
P=多分支并行仅在任务可隔离且净节时大于调度/交接/冲突成本时启用；本轮无需并行。
成熟复用=GitHub Contents API+已存在Codex官方CLI+Windows Task Scheduler+原V3 staged回归；禁止自造队列/调度器/新浏览器/新代理。
STOP_GATE=上述候选已覆盖可行动分工，没有证据支持继续引入新框架；现阶段无需更多虚拟方案。
虚拟推断=候选C有利于长编码/多工具任务，但没有实测可比完整T_VALID，性能优越性UNKNOWN。

## 预期故障（必须经现实验证）
F1=skills/artificial-single-page-extreme-time-engine/SKILL.md在最前面插入HTML注释与Markdown说明，标准Codex技能YAML frontmatter不在首行；自动发现能力需负例/修复后实测，原SANRENXING_V1.md不可原地默改。
F2=运行层V3现标记PUBLISHED_STAGED_NOT_YET_WINDOWS_ACTIVE；既往只读回归PASS不能等同真实跨节点AUTO PASS。
F3=V3回归脚本的WrongHashRejected在fixture中只比较不等常数，尚未覆盖执行runner在实际错误清单/远端不一致下是否拒绝。
F4=现V3 runner只查本地版本指针和Manifest哈希，并不自行向GitHub做官方独立读回；必须由已有Codex节点保存远端回执并由GPT审核，不许把本地自报等同独立核验。
F5=根目录本机Polsia正在执行CODEX-006，INFLIGHT存在；不得热切换V3、强清标志或启动同任务第二Codex。

## Reality最小执行顺序
R0=本任务冻结文件GitHub create→readback（不是Polsia业务Freeze）。
R1=真实Windows上v3官方只读回归与当前进程/计划任务只读查询；单元级通过只能标PARTIAL。
R2=正式Codex技能加载入口的现状负例与YAML-frontmatter修正；仅在隔离场景机械验证后才做可逆入口修复并回读。
R3=等待已存在执行实例自然合法完成及三态对账后，在独立隔离任务与合法复用入口上开展一次真实Executor及GPT验收；不能因检查启动新Polsia进程。
R4=若真实发现故障，保留GOOD/BAD/FIRST_DELTA，在GPT重规划与新Freeze后只复验修复分支。对明确拒绝与未知副作用不盲试。
R5=全合同证据齐全才候选成熟发布；否则保持REALITY_PARTIAL_FINAL_VALID_NO。
