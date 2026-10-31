# EXP-PI-001｜Pi原文件任务跨真实重启与成熟执行选路
版本V1；核查日期2026-10-30；分类CASE/ERROR/CANDIDATE_RULE；证据等级=原本机任务实际运行及独立验收。

触发：OMP/Pi系统要从真实Windows重启后自动续跑，或考虑单父执行、子代理并行、浏览器服务冷就绪。环境：原OMP 18.13.3、DeepSeek Flash high、原权限/既有Windows任务计划程序、单个正式浏览器与MCP。

LAST_GOOD：原本地文件任务ID、冻结输入、10个检查点及原会话保存完好。FIRST_DELTA：登录时原正式MCP助手仅等15秒就报告就绪超时，实际服务依赖未全部启动。最小修复：沿用原transport，仅将已有助手改为最长90秒的有界readiness等待，原任务按需重测PASS；不新建控制器、浏览器或调度器。此修复不等于首次真实冷登录已过。

真实结果：2026-10-30不同Windows boot epoch之后，原本地文件任务在原用户登录触发、GPT未重新派单的条件下完成20/20独立审核，每业务阶段一次，原输入/产物核验通过。原生执行100.175秒；包含用户登录等待的boot→delivery为527.060秒；原整任务跨夜壁钟52388.458秒，均不是完整商业T_VALID改善。随后在同次重启后的既有合成预约UI，人工预先恢复依赖服务后，再由正式MCP完成两行新增与三次修订、15/15业务检查PASS；首个业务请求至独立验收327.599秒。下次完全无人值守的浏览器冷启动仍PENDING。

执行位置对照：同两份供应商条款提取合同，单父直达12.167105秒，原生串行37.307877秒，原生并行29.178664秒（均从请求至独立验收）。三者在此合同均PASS，因此保留原生并行能力，但此类业务默认选单父；仅一组，不外推所有任务。完整增强T_VALID、真实API账单与经验净提速均NOT_MEASURED。

记忆实际复用：原FILE-REPAIRED-ACCEPTANCE.json及DEFAULT-ENTRY-ACCEPTANCE.json明确读取并应用EXP-DELIVERY-001 V1，直接复用旧Pandas账目配方（177行与123行分别限定PASS），避免另写聚合算法，并用标准库独立复算；原第一次候选未读经验，已保留失败记录。证明影响行动，不证明同合同记忆提速。

适用：对原有任务计划、持久检查点、同一原用户和依赖就绪的分层核账；相同质量下考虑单父/子代理分流。不适用：任意账号恰好一次、已认证完全无人值守开机、第三方登录网站、由局部耗时推算全系统收益、替代现有Windows A→B→C通道。

原证据：C:\Users\A\Documents\DSH-Workspace\pi-unified-upgrade-20261030\REAL-BOOT-INDEPENDENT-ACCEPTANCE.json、FINAL-CHECKPOINT.json、FORMAL-MCP-POST-BOOT-HELPER-ACCEPTANCE.json、browser-boot-20261030\BUSINESS-INDEPENDENT-ACCEPTANCE.json、PARALLEL-COMPARISON-FINAL.json、FILE-REPAIRED-ACCEPTANCE.json。原合同/Freeze及当前状态仍以原项目控制文件为准；2026-10-30-DSE-INCREMENTAL.md是回顾而非独立运行证据。

## 2026-10-31追加｜Pi/DSH正式浏览器限定单轮对照
在相近正式MCP测试合同（保留原tab、只关自有tab、CSV15行下载/修订、报告SHA）下，原full-pi/ACCEPTANCE.json为PASS/119.202秒，full-dsh初版ACCEPTANCE.json为NOT_VALID/243.819秒；随后AUDIT-CORRECTION.json指出该FAIL仅由于将十六进制SHA大小写文本作严格匹配，原报告的大写digest与原CSV字节一致，更正为PASS，保留旧审计记录。此处只有一轮、两臂工序与成本边界可能不同；不能发布全业务稳定排名，不等于记忆净T_VALID提速。原证据位于C:\Users\A\Documents\DSH-Workspace\pi-dsh-browser-full-compare-20261031\full-pi和full-dsh。该项目原实际窗口为10月31日18:44—18:51北京时间。
