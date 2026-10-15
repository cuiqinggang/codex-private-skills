# F020｜修复成果的原生双子代理独立 Gate｜Reality 前虚冻结
2026-10-16｜TASK HERMES-ECO-20261014｜承接 HERMES-ECO-F019-20261016｜STATUS=VIRTUAL_MATURE_FROZEN
方法《三人行》V2仅限本Hermes项目，Hermes Mature SuperTool v2.0。Windows V7 C第一、B备用、A暂停；本节点C可用，仅用C。
## GOOD/BAD/FIRST_DELTA
F008 原生 delegate_task 两子代理完整生命周期与manifest已经PASS，但仅报告了修复前样本的审核（1FAIL/1PASS）；F019新Repair结果外部23/23 PASS。BAD=尚无“修复后同一冻结成果经两位独立子代理并行评估 + 父汇总Gate + 操作系统manifest证据”的当前验证。FIRST_DELTA为独立Gate覆盖的业务对象仍是旧故障版本，并非Hermes工具总体失效。
## 冻结对象与只读合同
唯一读取对象：C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F019_REPAIR/requirements.md、refunds.py、test_refunds.py、f019-independent-gate.json。
冻结refunds.py SHA E796F499E5F9B222AAABF89F09AB5CD434BA6C7224F568F4582B20B3D860C243；requirements/test SHA参照F019 Freeze/Reality。已独立实际23/23 PASS，F020不允许为重复认证而另改或再修旧题。
实际模型必须调用原生 delegate_task 派发恰好两个可独立审查的只读子任务：child-A审查代码实现相对requirements边界（金额类型、过滤、去重、异常、纯函数）；child-B审查测试/固定Gate覆盖是否有明显未测重大边界、证据哈希一致性及是否存在test-only伪通过。两个审查范围清晰、共享只读文件，无任一子代理改写生产或夹具文件、无任何授权外副作用。
父代理汇总真实 delegation_id、两个独立review verdict及发现问题，不得把自己分析伪装成delegate_task。至少一个子代理REJECT需报告Gate FAIL，不得声称综合通过。模型退出0本身不足以通过。
独立GPT仅通过C对当前模型产物返回的单次delegation_id读取 cache/delegation/live/<id>/manifest.json，确认 task_count=2、两项completed，时间与本节点一致；只读取指定manifest，不读取私人子日志/密钥或旧会话DB。可额外只读验证F019三源hash保持。不得重启隧道/浏览器/修改代理。无manifest时只给MODEL_REPORTED_UNVERIFIED。
本节点唯一Reality一个Hermes正式CLI自然任务；不重派UNKNOWN，进程结束后独立审查。可生成只读报告和F020 evidence，但不得将当前整站五轮0/5冒充1/5。完整T_VALID墙钟若缺全程精确计时记UNKNOWN。不同业务合同耗时不能比较宣称加速。
攻击树：已有原生 delegate_task 复用+只读Gate KEEP候选；新并行调度器、API Runs、UI自动化 ABANDONED/NOT_APPLICABLE。
