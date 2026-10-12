# 三人行V2隔离实测合同 C002

任务：28项路由/安全/计时决策＋12行合成事件离线核算。输入、质量与授权固定，DONE_WHEN为全部28项决策、金额及ID集合通过独立预先固定oracle。
测试仅使用现有原生Codex子代理和本地文件；不是GPT官网CEO或Windows调度自动接续认证。root为测试协调者，每个子代理只写所属随机token结果，不改母任务CURRENT。不选择/变更模型或推理档。
基线=冻结V1入口；候选=C002。V1也必须服从本次用户标签/ROI暂停等现行指令，不为制造速度差强制它多读旧资料。
3个配对块，顺序V1→V2、V2→V1、V1→V2；每次全新无历史子代理。同一时刻仅一个被计时执行者；独立审核可并行但不运行额外benchmark。
计时使用本机Python perf_counter_ns：计时起点在派发前写入任务token的start.json，终点在root独立oracle验收后。包括工具调度、读方法/输入、模型、文件落盘、root核验等待；不同进程QPC同基准。实际UTC留作定位。source线上发现/下载为本批一次性setup，不重复摊入每个已锁源测试任务；远端证据发布另列未计入该合同。
end-to-end_ms是该原生Codex隔离测试合同完整耗时；不冒充用户原始本轮发现→修订→发布全过程。局部解析/算术脚本性能单列。
reported_rate=独立验收成功任务数/含失败和审核的批次墙钟秒；agent latency最小/中位数/P95只由有效样本算；失败仍保留批次分母。
只作描述性实测，不进行事后规则变更；小样本、模型排队、root工具等待及未做A/A校准限制推断。不使用显著提速/全局最优/物理极限完成声明；不恢复ROI。
出现决策/金额错误时保留失败原样，C002修订只能创建C003并重新固定合同，不覆盖旧试次。
标签及计时Bug由独立源审查和行为负例确认；36项设计覆盖静态审查不冒充36个平台实际动作。
默认SKILL/START_HERE、旧V1冻结、Polsia、现役runner、系统/网络/浏览器/监控配置保持当前状态。线上仅保存修订候选及证据，不正式激活。

正式PROFILE=SRX-ISOLATED-BEHAVIOR-REAL-CODEX-002，输入fixture_v2.json，oracle expected_v2.json，validator validate_trial_v2.py。旧t001/t002是PILOT_LEAKED_VOCAB，保留且不纳入正式V1/V2判断。词表去重字母序，与案例顺序无答案映射；R16只表示待核验，不表示业务NOT_DONE。
正式六试次token=t101,t102,t103,t104,t105,t106，预定顺序V1/V2、V2/V1、V1/V2。描述性结果；不将A/A未校准的延迟差称显著提速。报告测试输入、oracle、validator与方法SHA。
