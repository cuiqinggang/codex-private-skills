# EXP-DELIVERY-001｜成熟交付的执行位置与计时边界

版本V1；核查日期2026-10-29；类型CASE/ERROR/CANDIDATE_RULE。触发：成熟软件/安装包交付、验收太慢、DSH/本地执行选择、重复校验或并发启停。

## 已观察事实
租赁原业务首个记录至限定验收8248.812秒；本页早期回执的连续锚点跨度19242.218秒包含建设、失败、返工与等待，精确用户发起时间缺失。既有Docker主机新目录安装369.112357秒，核心业务与三组20路竞争13.482秒，一轮备份/隔离恢复核账75.902秒，三项局部合计458.496357秒，不能当完整交付时间。
另一既有流程后续修订冻结包，最终ZIP校验16:48:58.499571Z，与本页00:33回执边界不同。停止实例恢复108.936秒，后续写回和交接不隐去；包定位以当前租赁分支及原回执为准，不沿用早期ZIP哈希。
原构建依赖安装872秒，含网络重置/低速下载；Windows复制依赖缺模块、CRLF、端口/等待、脚本编码/导入均有返工。两条流程操作同一验证实例出现启停干扰，不是有效并发。
DSH历史混合任务322.610秒仅覆盖冻结合同到校验/重算/审核，无同合同租赁对照；不能据此认定DSH胜出。订单融合有同内容/公式门的历史对照，不外推软件全流程。

## 采用修正
采用dsh-extreme-effective-time方法V2：固定制品和现成验收入口，机械步骤本地连续执行；独立数据并行，同实例单控制者；以相同合同、输入、资源、产物及独立验收的完整结果选执行器。缺匹配数据保留未知，不以感觉或局部/全程混比。
Windows继续A优先及真实失败复验条件；脚本报错修脚本，UNKNOWN先核账。继承未变合同/版本下的已确认成果，只补变化及影响；不改代理、凭据或正常业务数据。

## 证据边界
规则保存和前向使用检查不等于业务提速认证。不得计算19242.218/458.496357作为已证倍数，不把30–60分钟目标当SLA。V2新编排完整同合同对照仍为NOT_MEASURED。

## 来源
Windows：C:\AI\Rental-N001-20261028\evidence\OFFLINE-FINAL-ACCEPTANCE.json、offline-install-timing.json、offline-isolated-restore.json、docker-offline-build.log及后续离线归档回执。
冻结分支：AI网站与应用高保真复刻能力包 references/rental-offline-kit.md、rental-offline-assets.json。
DSH：C:\AI\AIORG-Shared\tasks\DSH-MATURITY-20261025-002\FINAL.json、holdout-v111\ACCEPTANCE.json。
方法技能references/execution-efficiency-evidence.json保存脱敏摘录。本卡是历史，不替代当前Freeze、实例身份和最新回执。线上EXP-RENTAL-001的20:30 NOT_VALID是当时状态，更晚结果按原回执覆盖，旧失败保留。

