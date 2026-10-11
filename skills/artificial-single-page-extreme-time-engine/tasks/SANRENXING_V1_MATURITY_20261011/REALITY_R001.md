# 三人行V1｜首轮Reality与GPT差分修复报告 R001
TASK_ID=SANRENXING_V1_MATURITY_20261011
NODE_ID=GPT-REALITY-001
METHOD_REF=skills/artificial-single-page-extreme-time-engine/SANRENXING_V1.md@SRX-V1-ACTIVE-F001
RUNTIME_TESTED=3.0.0_READONLY;3.0.1_CANDIDATE_STATIC_AND_FAULT_FIXTURE
PREVIOUS_VIRTUAL_FREEZE_ID=SRX-MATURITY-VM-F001
RESULT=PARTIAL_REALITY_WITH_REPRODUCED_AND_FIXED_SCOPED_BUGS
FINAL_VALID=NO
CODEx_NEW_EXECUTIONS=0
POLSIA_METHOD_REF_CHANGED=NO
BUSINESS_FREEZE_CHANGED=NO
WINDOWS_SCHEDULER_CHANGED=NO
PROXY_OR_BROWSER_CHANGED=NO

## GitHub正式证据
原SANRENXING_V1.md blob=a05fc51d661952790837dfa462bf766b16aba078（未改；FROZEN_ACTIVE）。
原技能入口SKILL.md blob=72a8dc24aaa9183f098d87412235881b1f770554，开头是HTML注释而非YAML元数据。GPT机械检查失败；官方GitHub Contents API按最小差分重排YAML到首部且修正描述；提交3981e894f663ec5b57daf3c13018f2f47851b349与3ee43b2f7c2499c14620e7a36aabdf5f403547f0；重读最终blob=528a0015abb717b10798b504bab1316f40a43a48；frontmatter-first=PASS，其余旧方法保留。正式Codex技能加载器的端到端发现测试未做，不冒称其PASS。
虚拟Freeze文件=FREEZE_VIRTUAL_F001.md，blob=4aca2d2da44b79b6929065f9cea036ab7c32d246；明确先GPT虚拟成熟再Reality，真实与虚拟分开。

## Windows实测：原v3.0.0
真实执行原生PowerShell调用C:\AI\Polsia-Codex-20261011\CONTINUATION_RUNTIME_V3_REGRESSION.ps1，实际结果：
{"Result":"PASS_READONLY","Version":"3.0.0","Parser":"PASS","LF":true,"CRLF":true,"WrongHashRejected":true,"FinalYesCRLF":true,"FinalNoRejected":true,"CurrentLocal":"PASS_READONLY_LOCAL_SHA","CodexStarted":0,"SchedulerMutated":false}
真实Windows原生Task Scheduler Action=C:\Program Files\PowerShell\7\pwsh.exe -NoLogo -NoProfile -NonInteractive -File "C:\AI\Polsia-Codex-20261011\CONTINUE_EXISTING_CODEX.ps1"；所以v3.0.0仍非ACTIVE。
核验时确有1个执行Polsia母任务的Codex实例（本轮未启动），InFlight属于现有任务，禁止第二个Codex及热切换。

## GPT GOOD/BAD/FIRST_DELTA与隔离修复
GOOD=期望只承认独立行 FREEZE_ID=<完全相同的值> 且恰好出现一次。
BAD=原v3.0.0使用文件全文字符串包含匹配[regex]::Escape($motherFreezeId)。Windows真实PowerShell负例输入仅在NOTE中包含目标ID，但FREEZE_ID字段错误；宽松匹配返回True，规范精确字段比较返回False。
FIRST_DELTA=全文子串命中≠独立权威Freeze字段，存在假阳性，其他条件即使成立也可能错认不可信Freeze。
修复=创建独立CONTINUATION_RUNNER_V3_0_1_CANDIDATE.ps1，继承既有官方runner，仅改为唯一完整FREEZE_ID=行匹配，拒绝无字段/重复字段/错误值；版本v3.0.1-CANDIDATE仅用于隔离验证、不自动部署、不覆盖发布的v3.0.0。
首次候选FAILED_PARSER=TRUE，原因是生成代码使用JavaScript String.replace(str,replacementString)，替换文本内的字面 `$'` 被解释为输入后缀，导致新文件拼接截断；该失败已保留事实，没有发布生产。
修复生成方式=使用replace(str,()=>literalFix)保证美元符号和正则原样，重新经官方GitHub update_file提交4fed6899757327027514a83765e06d7a829b143d，独立读取blob=55409acc0fc81157487f38698199dfee81dd455a。
Windows实际隔离位置=C:\AI\Sanrenxing-V1-Maturity-20261011\CONTINUATION_RUNNER_V3_0_1_CANDIDATE.ps1；PowerShell ParseFile真实结果ParserPass=true、ParserErrors=0。
本机实际负例矩阵：GoodLF=true；GoodCRLF=true；NoteOnlyRejected=true；WrongFieldRejected=true；DuplicateRejected=true；EmptyRejected=true；CandidateExactMatcher=true；RemovedLooseMatcher=true；CodexStarted=0；SchedulerMutated=false。

## 未通过而不可夸大的门
1. 修复候选未执行真实runner，也没有真正官方Codex技能加载器进程的技能发现回执；只能记录PARSER+NEGATIVE_FIXTURE PASS。
2. 已运行的Polsia实例与未知/进行中INFLIGHT构成热切换禁令。不能随手清标志、改计划任务或从本页启动第二个Polsia Codex来凑测试。
3. GPT→官方Codex的独立TASK_ID合同→真实节点业务产物/Freeze SHA→GitHub双重回读→GPT独立验收→故障回到GPT→Codex同合同新修复节点复验，仍无本测试的一次真实完整回执。
4. v3.0.0自身只读回归中的WrongHashRejected为fixture级校验；不证明真实runner的全部路径、业务远端回读。V3也不自行取得GitHub服务端权威版本，远端证明须由Codex节点与GPT CEO复核。
5. 真实跨节点自动接续、72小时长期稳定、断电恢复、全合同有效时间和全部质量负例均尚未验收；FINAL_VALID=NO。

NEXT=在既有同任务Codex自然完结、无未知INFLIGHT且当前Freeze/SHA远端回读一致后，使用独立SANRENXING测试TASK_ID执行受控Codex Executor最小有效任务，回到GPT独立验收并做一次故障修复闭环；最后再考虑v3.0.1候选激活，须备份/回滚门。不得从当前只读单元PASS推广为成熟版全链路PASS。
