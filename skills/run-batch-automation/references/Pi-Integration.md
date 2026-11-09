# Pi现有入口接入与调用上下文

本包已部署于 C:/Users/A/Documents/DSH-Workspace/pi-rules-r64-20261108/runtime/skills/run-batch-automation。
原pi_rule_runtime.py在已有skills.includeSkills追加run-batch-automation，沿原customDirectories读取；原pi-default-memory-policy.md增加按绑定复用与上下文说明。仅配置适配，非新执行器。

- 宿主、GPT或已有结构化参数：使用ready-bindings.json的native_pi_entry及--fast-office-file原参数。
- Pi当前已在原OMP工具沙箱中：使用同卡的omp_tool_entry，即现有artifact_recipe.py ingest接口，保持原OMP沙箱，不重复套外层启动器。原C1嵌套启动失败，C2直接原业务接口通过。
- 原完整流程自带的固定检查直接继承，额外合同沿其独立方法验收。原检查器、程序、权限、模型和沙箱均不修改。
- 新会话才加载现行规则；不关闭或迁移用户已运行的其他会话。
- 只读绑定就绪与来源状态，精确匹配直接调用。公共来源与模板依赖原平台、账户和字段配置；当前范围以R87-Catalog-Coverage.json为准，目录扩展不等于整体运行通过。

完整实际结果见[R85验收](R85-Reality-Comparison.md)与[R85原始数据](R85-Real-Results.json)。只增加索引的对照未提速；约6秒只认证已选定现成配方的宿主结构化入口。Pi自然选路目前仅认证可用，未认证效率成熟。

R87收尾接入：沿用原includeSkills和现有入口，只在常驻规则追加“每批任务验收后调用本包收尾”的一条路由；不改模型、工具、沙箱、权限或既有验收。capture_flow.py记录候选与使用证据，query.py合并本地收尾索引；新类别不会自动进入原三类调用器。宿主元数据验收与实际配置读回见R87-Completion-Acceptance.json，不推定未来每个模型会话必定遵守。

R88（V1.3.1，2026-11-10）：极限效率流程库为GPT与Pi每项任务的默认优先技能，无需用户逐次点名；有当前批有效MATCH直接继承，否则先核本库已验合同与本地收尾索引。query.py先用 --kind local 查1—3条，再按需转公共来源及原专业包；删除普通任务自动绕过本库的表述。仍按调用上下文、依赖和完整合同判断适用，结束走原收尾。只改默认路由及文档，未改原业务程序、工具、沙箱或模型。
