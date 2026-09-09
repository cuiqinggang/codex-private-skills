# 结果与判定口径

cases.jsonl 每个计划用例/变体/轮次/路线一行，至少：
run_id, case_id, variant, repeat, route, model_revision, quantization, backend_version,
status, reason, start_utc, elapsed_s, first_action_s, inference_s, browser_wait_s,
actions, retries, manual_interventions, oracle_pass, evidence_paths。
时间不能采样的分项写null并解释，不能伪造拆分。
status枚举：PASS, FAIL, TIMEOUT, BLOCKED_COMPATIBILITY, BLOCKED_ACCESS, OUT_OF_SCOPE, NOT_RUN_TIMEBOX。
成功必须oracle_pass=true且有可读证据；没有证据不能PASS。
被测模型临时输出正确但最终文件/页面错误为FAIL。外部网站变动、网络、模型、执行器错误分别归因。

环境锁记录：OS/shell/GPU及compute capability/显存/RAM/驱动、Python、官方源码SHA、模型revision与权重SHA256、依赖、提示模板、截图大小、上下文长度、精度、端口、启动参数、夹具哈希、被比较系统版本；任何秘密字段排除。
采样在实际执行进程及其子进程统计；每2秒记录本项目RAM、GPU总使用与本项目可测使用。无法归因的GPU读数标明全卡读数，不算项目独占。
计时用单调时钟，不用模型自述；冷/热分开。重试耗时计入最终成本。

summary.json至少包含：
deployment_status, evaluation_status, planned, executed, passed, failed, timed_out,
blocked, out_of_scope, not_run, per_route, comparison_status, recommendation, limitations。
deployment_status=PASS仅代表模型-执行器完整回路及重启验证通过。
evaluation_status=COMPLETE要求无NOT_RUN及无妨碍必测范围的BLOCKED；OUT_OF_SCOPE可作为经过核实的边界结论，但报告必须写明不支持范围。否则PARTIAL或BLOCKED。
性能优劣与覆盖状态分开，COMPLETE不代表高性能。

统计：
- 首次成功率=首次PASS数/(首次PASS+FAIL+TIMEOUT数)，同时展示全部计划数、阻塞及范围外数量，不能只报好看百分比。
- 重试后成功率另列；不混用。
- 成功任务时延P50/P95用nearest-rank，标样本数；全尝试耗时与超时单列，n<20时不作稳定尾延迟结论。
- 总墙钟耗时/成功成果数为每成功成果时间成本，含失败/重试；成功数0时不可计算。
- 只在同任务同起点可比较子集上算速度比和成功率差；缺对照写NOT_COMPARABLE。
- 费用包括下载体积、峰值资源、人工干预、部署维护时间；电费无测量写UNKNOWN。主控用量不可见也写UNKNOWN，“本地模型外部调用费0”不代表总成本0。

REPORT.md用中文表格给出四列法、部署路线、功能成绩、秒级性能、资源成本、桌面边界、对照优劣、失败原因、未测项及可执行继续步骤。
capabilities.json逐项保存 status/route/config_hash/evidence/last_verified，不生成无证据的“成熟”标签。
价值判断不强行合成100分：至少明确一项可重复收益才能推荐用途。成本更低但成功率下降必须同时展示；没有收益或证据不足也属合法结论。
