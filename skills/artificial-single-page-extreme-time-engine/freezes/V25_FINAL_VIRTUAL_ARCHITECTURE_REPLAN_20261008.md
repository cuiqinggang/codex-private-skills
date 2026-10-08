# 第25版编排虚拟成熟：完整架构重选和可执行合同
ENGINE=25；BRAIN=22；NPT=17
状态：方案虚拟重放完成；实施前接口验证未通过；最终STOP_GATE未达成；禁止宣称REALITY PASS。
原现实对照：F011五项真实有效，批次115.67s；数学分段参照76.732s，完全理想并行参照23.625s，二者均非物理实测下界。

## 真实接口审计后的FIRST_DELTA
n8n已有Reasonix Webhook→Code→HTTP(host.docker.internal)→Code工作流，但不能证明这个HTTP地址能够调用原ChatGPT业务入口；原业务入口是Playwright的async(page)函数，通过sessionStorage配置，允许query、send、wait_extract。原v24 task_worker.cjs在Windows直接调用，但包含自建全局JSON租约、不可变硬编码验收消息、并将等待全部包进同一执行单元。因此把现有n8n工作流直接映射成ChatGPT工作流不合法也不完整。

## 重新比较三强
A n8n：无需新编排服务，但是跨容器-宿主机业务接口缺失；若须自建通用HTTP服务器/锁则违反REUSE_GATE。仅保留作为事件入口和监控候选，不强制参与终局。
B Temporal：官方Python SDK + Windows本机Activity Worker + 本地Temporal Service（官方CLI开发模式），可以由官方Activity直接启动既有Node浏览器业务入口（仅薄参数适配），无需另建HTTP桥。Event History恢复、Task Queue与Worker并发上限官方提供。正式生产必须另评估服务部署成本。
C Prefect：Windows本地Python flow/task同样可通过薄适配调用Node；配置轻，但跨进程/长生命周期可恢复语义相对Temporal需精查。
条件性重选：对于「必须证明跨进程恢复」的长期任务，优先虚拟成熟 Temporal Windows Worker 作为新候选；若官方服务部署成本导致长期净收益为负，则回到Prefect或可用的n8n业务入口。不能因选Temporal又发生沉没成本锁定。

## 可执行的Temporal单主干蓝图（调用成熟原语；非已安装或验证）
1 CEO发任务：TASK_ID唯一稳定，记录目标和约束；Temporal启动Workflow时使用相同业务ID作为Workflow ID，重复启动冲突由平台机制处理。
2 Workflow执行Activity A=PrepareAndQuery：在Windows Node调用原既有Playwright业务入口query，记下会话URL、TASK_ID、MARKER、PAGE_ID；使用Workflow/Activity结果持久化。必须先确认页面标识不会跨进程丢失。
3 Activity B=SendOnce：仅当A明确未曾投递且没有UNKNOWN，向原业务入口send一次。配置Temporal RetryPolicy maximum_attempts=1（对外部非幂等发送）；不让系统自动重发。
4 Activity C=WaitAndExtract：B成功后依据会话URL和MARKER重附着目标页面并调用原wait_extract；等待可与其他Workflow的发送阶段重叠。若C中断，可在成熟恢复能力及只读query的先行确认下重取结果。活动不能因为业务函数引用page失效而自动恢复。
5 Activity D=VerifyAndFinalize：核对唯一用户消息、ACK、发送计数、回复完成，得到不可变节点证据，按实际ownership清理本任务页面，由CEO接受。
6 Worker资源控制：调用官方Task Queue/Activity Slot限制共享浏览器写操作，读取/等待不占用写Slot。需验证多个Workflow共享一个写队列时实际只一个写Activity，且其他等待可同时推进。避免自编Lease。任务状态属于各自Workflow ID。
7 故障矩阵：未发送前崩溃，允许重试准备；点击之后确认前崩溃，禁止重试发送，置UNKNOWN只读查询；确认发送后崩溃，按marker+URL恢复等待；回复完成但清理失败，证据不丢并只清理所属页；进程重启读取Temporal事件历史恢复流程但不能假定页面对象本身持久化；过期执行者写入应由官方队列/Activity生命周期和业务所有权检查拒绝。
8 计时指标：五任务完整TASK_ACCEPTED到五条FINAL_VALID，另记录提交/页面准备、send、回复等待、重试、恢复、冻结与部署摊销。对照115.67s；优先压缩发送前累计70.370s及释放回复等待占锁时段。不得把76.7/23.625理想值写成物理下限。

## 虚拟重放与停止判断
S1常规五任务：写Activity单并行槽，读/等待并行，要求所有页面与ACK对应；理想时序参考76.732s，不保证真实成立。
S2重复同业务ID：Temporal Workflow ID唯一阻止工作流重复启动；但不代替ChatGPT外部消息一次投递校验。
S3 Send之前终止：准备可重新执行。
S4 点击后断线：无确定投递证据，必须UNKNOWN；不会自动重发。
S5 Wait中断：只读重新附着目标会话再取结果；若找不到页面或URL，UNKNOWN，不创造新消息。
S6 浏览器共享冲突：单写Activity Queue序列化，有效等待并行，页面所有权校验失败则停止。
S7 单Task失败：其他TASK不回滚；每个Workflow状态隔离。
S8 Freeze阶段崩溃：只有持久化且CEO接受的NODE_FREEZE算完成。
S9 长期成本：Temporal部署新增成本、Worker活动调度额外开销必须用真实测量；因此仅逻辑重放PASS_DESIGN，净收益未知。
S10 再优化判定：进一步纯逻辑猜测不再带来可靠正净收益；可实施形态已有明确任务接口、故障分支、仲裁与计时门，等待真实接口适配和前置验证。不得认为全部虚拟成熟完成到现实资格。

## REQUIRED_PRE_REALITY
a. 官方Temporal Windows CLI本地服务及官方Python SDK最小例程的实际可运行性；
b. 原Playwright技能包能用已有Node入口在同一浏览器中按query/send/wait_extract安全分段调用，且PageID/URL在进程恢复后可重附着；
c. 单个全局浏览器共享写的Task Queue/Slot能覆盖全部Windows活动，并确保不会由多Worker或其他旧执行器越权；
d. 任何非幂等Send maximum_attempts=1，并允许不可确认状态UNKNOWN；
e. 记录开销并满足REUSE_GATE TOTAL_COST；
f. 上述皆通过后才能Freeze整个实施方案并只进行一次完整Reality。

结论：这是真实接口审计及对抗虚拟重放后的完整架构方案，不是系统已经部署成熟。当前缺的是B/C的实际接口可用性与全局仲裁证明，不能把未满足前置条件宣称为完整FINAL_VALID。
