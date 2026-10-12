# GPT虚拟成熟｜《三人行 V2》隔离试验候选冻结 F001
TASK_ID=SANRENXING_V2_VALIDATION_20261012
NODE_ID=GPT-VIRTUAL-001
FREEZE_ID=SRX-V2-VM-F001
METHOD_V1_BLOB=a05fc51d661952790837dfa462bf766b16aba078
METHOD_V2_BLOB=6a808beeae22f96fb296f2899bdab9118dba7bfc
V2_STATUS=REVIEW_PENDING_NOT_ACTIVE
MODE=VIRTUAL_ONLY
VIRTUAL_MATURE=NO_TIME_CERTIFICATION
VIRTUAL_DESIGN_FROZEN=YES
FINAL_VALID=NO
T_BASE_REAL=UNKNOWN
T_VIRTUAL_BEST=UNKNOWN
T_PHYSICAL_LIMIT=UNKNOWN
T_VALID_REAL=UNKNOWN
GAIN_PERCENT=UNKNOWN

## 一、商业有效标准与不能越界的条件
原始任务验收一致、用户实际可用（包括质量和正确格式）、用户操作/时间成本全计入；质量、授权、Exactly-once、REUSE_GATE、版本锁、CEO唯一状态写者、真实冻结SHA回读、恢复三态、旧A/B保护均强制保留。任何安全/权限/业务功能回退立即否定候选。
计时应使用从任务接受到最终合法验收的单调墙钟时间；包含规则/资料读取、工具等待、执行、人工交接、故障修复、验收。并行取墙钟关键路径，不将各子任务时间机械相加。
文本体积：V1正文10337字符，V2候选4212字符，减少约59.3%；此数字仅说明潜在上下文负担，不能证明实际完整任务快59.3%。

## 二、至多三条成熟路线与虚拟筛选
A=冻结V1直接执行；保留所有规则和既有成熟组件。优点原证据最多；潜在劣势正文带历史候选及重复解释。
B=V2候选（优先），单GPT默认，只有触发长时/跨页/故障时按实际当前GitHub索引读取对应成熟技能细节；安全硬门从不延迟或省略。优点有望减少无意义加载、派发和等待；净收益尚待真实验证。
C=在B上增加全新状态机、动态锁或定时轮询优化。直接淘汰：违反成熟复用、增加维护和风险成本，缺少正净收益证据。不开发。
选择B作为隔离现实候选，而非宣布它优于A。P多智能体仅在真实独立性和净收益可证明时启用；不为三人行字面强开多个模型。

## 三、按预期净节时排序的真实瓶颈假设
H1=日常任务自动读取长历史/连续运行/监控说明可能浪费上下文与工具调用；具体是否真的读了需现场对比。
H2=长任务的GitHub CEO批准→Windows真实NEXT授权/定位双门断链、无意义反复启动会导致巨大返工；V5专用技能已明确两门，V2只按需加载、不能移除。
H3=为了形式而重复Freeze、重复检验GOOD/旧节点、人工换页和无净收益并行；只可在保证可恢复和商业验收的前提下减少。
H4=新加载决策本身也有开销；若频繁回补遗漏说明，V2可能比V1更慢。因此需要正常+故障两路径共同计时。
当前Windows存在两个属于Codex+H3的exec实例（真实进程只读证据），Polsia母任务没有exec实例但存在NEEDS_GPT；本轮不新启Codex，以免污染公平对照或干扰其他用户项目。

## 四、单次虚拟迭代与净收益停止
BASELINE=A保留全部适用旧能力。
Δ1=以V2短入口选择路由A/C/P，只有命中长任务/故障/跨页加载对应手册，保留持久化和完整硬门。
Δ2=同一节点复用已核验的SHA/授权事实，但当版本/权限/外部状态发生变化时立即重新核验；不得复用过期证明。
Δ3=业务/故障只对未完成或受影响分支重新执行；对UNKNOWN先对账，不为测试重播完成节点。
已不再找到无需新增工具、且具有可说明正净收益的更改；因此冻结本轮**设计候选**，不是通过形式STOP_GATE或极限时间认证。

## 五、Reality最小合同
R0: GitHub只读检验旧版SHA以及V2候选/矩阵/验收合同；新测试分支中冻结事实并回读。
R1: Windows隔离部署、真实PowerShell/Python工具运行验证文件与安全负例（不涉及实际对外副作用）。若无Windows权限则报告阻塞。
R2: 使用一个真正可验收的离线商业任务（例如多渠道文案/报价模板，明确合成业务数据，数据完备与格式可机检）实际制作并独立审查；不能把模拟路由门PASS当商业交付。
R3: V1/V2各自独立、相同输入与输出验收、相同资源占用条件下的完整T_VALID计时。若现有Codex exec竞争运行，禁止在该背景下将新测得差异称为模型效率优势；不得强行启动第二个业务Codex。
R4: 故障仅重验失败的合法步骤，记录GOOD/BAD/FIRST_DELTA、修复前后真实证据。
不允许热切换Polsia runner、修改V1/历史文件和默认入口，不允许无真实回执标记FINAL_VALID=YES。

VIRTUAL_FREEZE_SCOPE=DESIGN_AND_TEST_PLAN_ONLY
NEXT=DEPLOY_ISOLATED_REALITY_NO_NEW_CODEX_WHILE_BUSY
