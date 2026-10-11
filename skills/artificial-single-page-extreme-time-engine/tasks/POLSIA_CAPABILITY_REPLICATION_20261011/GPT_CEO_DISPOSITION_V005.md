# Polsia｜GPT CEO 事实复核、CRLF误判修复与CODEX-006授权
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
DISPOSITION_ID=POLSIA-CEO-D005-CRLF-20261011
ENGINE=28
PREVIOUS_FREEZE=V005;POLSIA-MOTHER-V005-F001
DECISION=ACCEPT_V004_F002_AND_V005_FACTS_WITH_SCOPE_LIMIT;AUTHORIZE_CODEX006_OFFLINE_ONLY
MOTHER_STATUS=IN_PROGRESS
MOTHER_FINAL_VALID=NO
CEO_FULL_FINAL_ACCEPTANCE=NOT_GRANTED

## 真实复核
- V004-F002 的GitHub不可变Freeze回读与本地文件一致：本地23文件内容运营交付，独立内容/归档审查范围内通过；未发布、未商业清权、未证明Polsia等效或优化。
- V005 GitHub CURRENT与VERSION_CURRENT一致，Freeze blob=163f849ec161ae89d18ef14ae03ac85b6ae44236；本地Freeze SHA256=09403505F7311F26A0C16C55D167A90F38466E94667858564F1D91BED3B3E2DB，manifest SHA256=D378E405E49E83985ED000379630D183E942BFEF5A174CCF0357EDD0C34837BE。原Codex日志CODEX_EXIT=0；21文件ZIP、18组FAQ、16条SYNTHETIC答复，非作者审查回执PASS_WITH_SCOPE_LIMIT。未发送、无真实客户业务证明。
- NEEDS_GPT误报：CODEX_EXIT_WITHOUT_NEW_VERIFIED_FREEZE；版本V004→V005真实已更新；Windows CRLF文本上 ^MANIFEST_SHA256=([A-Fa-f0-9]{64})$ 返回False，修正为 ^MANIFEST_SHA256=([A-Fa-f0-9]{64})\r?$ 返回True。相同CRLF兼容修复覆盖MOTHER_FINAL_VALID=YES。完整条件重算freezeValid/manifestValid/指针一致和版本递增均True；错误SHA仍不接受。
- 修复只作用于既有Windows接续脚本/同源GitHub副本，原计划任务保持不变，既有V004/V005 Freeze不修改；首次修复静态与回放通过不冒充下一节点完成后的现实连续接续PASS。

## 下一节点CEO决策
正式允许既有Windows原生计划任务启动唯一CODEX-006_MATURE_PRESALES_QUALIFICATION_DELIVERY自然节点。继承已验V004/V005 GOOD，不重做旧节点、不新建调度器/桥/数据库/站点/CRM/重复Codex。
输出真实中英售前能力说明、资格判断与发现问题模板、适配与不适配规则、明确SYNTHETIC案例的实际未发送答复、范围排除与人工交接、独立只读审查、必要的不可变事实Freeze+SHA及GitHub回读。本节点仅离线草案，无真实获客、报价、合同、外联、广告、上传、付款、账户/密钥调用或代理变更。
V004/V005 CEO事实复核不代表优化通过。T_BASE_REAL/T_VIRTUAL_BEST/T_PHYSICAL_LIMIT继续UNKNOWN，STOP_GATE=NOT_PASSED；不做FINAL_REALITY或新10轮，不计算ROI。完成后按照母任务真实缺口判断下一自然节点；授权范围外或重大方向才由GPT CEO再决策，已核验正常节点由原runner自动接续。
规则：仅在CODEX005确证DONE、无活动Polsia Codex和校验通过后，将错误NEEDS_GPT及遗留INFLIGHT归档，保留原始证据；触发已有计划任务一次，核对不重复开实例。不得以手动复核代替后续现实接续测试。
