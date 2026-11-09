# 每批任务收尾合同

每批交付、部分完成或故障接续结束，都检查是否有可复用入口。沿用task_id，批次或恢复轮次用不同batch_id；不把后来补齐结果改写成原轮成功。不再增加定时任务、后台进程或新的记忆系统。

## 提取与去重

- REUSED：已存在同目标、语义、输出和验收合同，填写原recipe_id，追加本批记录。
- NEW_CANDIDATE：没有相同条目，记录实际用过的原成熟程序/节点组合，形成候选；相同合同加原来源标识得到同一候选ID，保留多批原记录。
- NO_REUSABLE_FLOW：本次没有可提取的固定流程，写明原因，完成收尾检查即可。
- 相同task_id/batch_id和相同内容重跑返回NO_CHANGE；内容冲突拒绝覆盖，使用新的恢复批次。并发写入采用独占短锁；存在未结束写入先核账，不盲删锁。

## 最少记录

采用[示例](capture-examples.json)。task_id、batch_id、decision、workspace、contains_secrets=false、qa.passed与timing.scope必填；真实源程序和原QA证据用workspace内相对路径，记录器检查指纹。NEW_CANDIDATE另需title、category、search_terms、完整contract（goal/inputs/semantics/outputs/acceptance）、original.identity和原entry。

original.files及qa.evidence_files可提供path、sha256；只有copy=true才保存该明确指定文件的原字节副本，最大每件16MiB，更大原件保留原仓库指纹引用。不扫描任务目录，不收集输入业务数据或凭据。复制受原许可及具体授权约束，云模板不据此变成本地可运行代码。

timing.total_s记录声明范围内实际时间；timing.user_e2e_s记录从接受任务至完整读回的总时间，含理解、检索、配置、模型、等待、失败、恢复、QA与收尾维护。没测填null，表示NOT_MEASURED，不填0。首次和后续批次分别保留，不因第二次快就宣称稳定提速。

## 发现到可用

保存只新增候选与使用记录，capture_flow.py永不把新流程自动标成READY，也不执行entry。查到候选后，核对原专业包、参数、依赖、输入输出、实际调用上下文和独立验收；CONFIGURED表示已配置，实际验收通过才就绪。变化后重新核对；不能从host通过推定Pi沙箱内、GUI或云平台通过。

原专业入口已足够便捷时只登记它和适用合同，不另外包装。需要新调用适配时只用原接口和最小配置；未成熟部分继续检索成熟节点，不从零猜改业务核心。
