# AIORG-20261024-004/N004｜Tymeslot 真实预约故障恢复 A/B R1
日期：2026-10-24；STATUS=PARTIAL_VERIFIED；INC-002=OPEN
## 真实环境与合同
Windows Docker Tymeslot:4352；Radicale:5233；Mailpit:8026。复用 V1.3 references/booking-validation/acceptance-fault.cjs 的 13 项自动业务断言，真实浏览器提交、2 个独立浏览器上下文抢同一时段、数据库单笔预约、缓存/CalDAV 单份事件、移动端390px、日历容器停止再启动、取消自动一致性、确认与取消邮件、Tymeslot 重启及持久数据回读。两路线采用不同匿名测试标签；其中 A 时段11:00、B 时段11:30（可用性实时变化）。
## 现实回执
A 成熟脚本适配：P0_PASS_PENDING_DUPLICATE_AND_IMAGE，13/13 PASS，业务脚本内部 elapsedMs=114308，容器中断后取消一致性35502ms；进程退出0。
B 虚拟成熟融合适配：事件状态确认、减少固定等待，P0_PASS_PENDING_DUPLICATE_AND_IMAGE，13/13 PASS，内部 elapsedMs=100409，一致性35137ms；退出0。
独立 Python 校验两份原始 JSON：检查名集合相等，均13项、无缺失、无失败；A SHA256=0f606aa2d018258461e804b39e38698e078f9074deab33917dcc6784d06ef9f3；B SHA256=b33f1d8209ebe8acbdedc2ac87db0f00741c57a6b6ced5b271e6fca7d39d8008。
成功轮 B 比 A 少13.899秒（12.16%）。单轮样本，外部容器/日历时间波动；不得认定稳定提速或物理极限。
## 失败和 T_VALID 限制
A 初次原脚本 time-slot 超时；适配后一次在应用重启健康检查失败（161.91s），再一轮完整通过（工具进程117.52s）。B 先后多次失败（时段加载、表单提交后固定等待过短），后采用状态等待和有限重试才通过（进程110.87s）。
本报告的114.308与100.409秒只指各自最终合格轮的脚本内时间，不包含先前失败的修复、重试与人工协调，因此不是原任务起点到最终完整QA的 T_VALID。因未计量工具和操作间全部时间，本次不能计算可信的整体 T* 或完整净提速。
## 尚未完成
该限定脚本没有本轮“改期”业务断言，也没有真实 GPT 新页自动接管或无人值守 n8n ACK。旧任务 N001-N003 继承确认；N004 尚未全合同通过，FINAL_PASS=false, STOP_GATE=OPEN_REQUIREMENTS_REMAIN。
证据路径 C:\AI\AIORG-Shared\tasks\AIORG-20261024-004\N004-A-acceptance-fault.json、N004-B-acceptance-fault.json、N004-AB-INDEPENDENT-QA.json、n004_ab_independent_qa.py。
