# F020｜F019修复后原生双子代理Gate——部分成功、Gate UNKNOWN
日期 2026-10-16｜TASK HERMES-ECO-20261014｜承接F019｜前置冻结F020_DELEGATE_REPAIR_GATE_VIRTUAL_FREEZE_20261016.md
执行桥V7，全部Windows操作仅Remote_Desktop_Commander(C)；A暂停未触碰、B未用；原Hermes正式CLI、OpenRouter deepseek/deepseek-v4.1-flash，不改模型/网络/密钥/浏览器。
## Reality回执（保留FAIL不能美化）
正式CLI自然任务PID43124仅一次执行，Hermes exit0，CLI内实测wall=305575ms，C外层工具进程runtime306.59s。模型返回F020_REAL_DELEGATION_REVIEW_DONE，native delegate_task双子代理并行调用，delegation_id=deleg_e96f8702。
C通道独立只读取系统专用manifest：C:/Users/A/AppData/Local/hermes/cache/delegation/live/deleg_e96f8702/manifest.json，delegation_id一致，task_count=2，manifest两项status=completed、exit_reason=completed。未读取两个私人子任务日志正文。
- child-A task-0：模型称tool_trace实际读到requirements.md与refunds.py，但最终摘要错误自报“文件路径未提供”，没有明确PASS/FAIL。结果=NO_VERDICT/UNKNOWN。这里未独立读取工具事件/子日志，细项tool_trace仅是父代理报告。
- child-B task-1：模型报告独立审查测试覆盖与三份文件哈希，审查 verdict=PASS；没有重跑已完成单元测试，属于只读审查。
- 父代理试图再次派Child-A，被原生one-shot预算拒绝：delegation.oneshot_max_children=2/2。其任务在一次模型自然会话只允两个新孩子，不能盲开第三个；不跨越权限或改配置。
- Overall Gate=UNKNOWN/NOT_PASS；不能用子代理实际completed等于两位评审均PASS。
独立C回读F019源码三个SHA全部保留：refunds.py=E796F499E5F9B222AAABF89F09AB5CD434BA6C7224F568F4582B20B3D860C243，requirements.md=CD8E65EBEF9FEB323B365378048480AFD304A25C6E01452AB7671039080979F8，test_refunds.py=B3B5413EF57677B82A776318EA3F6B5C56C21432E0D4B3322A518FE0E9A17E5B。F019原23/23独立Gate PASS仍有效。
使用记录 f020-usage.json：api_calls=5，总tokens=138002（含cache_read=119040），input=11409，output=7553，estimated_cost_usd=0.013717224；估计值而非账单。这个只读review耗时明显大于历史F008的74.95s，但合同不一致，不能以两者直接计算倍率。
## GOOD→BAD→FIRST_DELTA→成熟候选
GOOD：本轮本机native委派出2个真实child，manifest真实完成；旧F008已通过独立双子生命周期；F019独立代码Gate 23/23。BAD：子A没有机器可判定verdict，致父Gate UNKNOWN；one-shot预算2/2阻止同会话再spawn。
FIRST_DELTA：子代理结果输出合同不足（父代理报告空output_schema导致文本结论不可判定），不是缺文件或代码错误；没有必要重装Hermes或升级全部模型。
官方成熟解候选：Hermes delegate_task各子任务使用明确output_schema，硬要求JSON verdict、evidence，并让官方单次schema纠错作用于同一子任务；先做虚拟成熟并冻结，然后用新隔离审核任务只补缺失的Child-A评审，按冻结F019不变哈希复用Child-B已有可用证据。参考 https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation.md 。但当前未实际运行该改进，不得声称修复PASS。
## STOP与后续
F020未通过正式联合Gate，标记REVIEW_NO_VERDICT，仍存在可恢复差分。本次工具耗时305.575秒、实际额外收益有限，不再反复跑同一整套双子审查。F019功能Gate保持PASS，整站FINAL_VALID=NO、综合5次0/5。后续应优先有明确净收益的缺口；需要补此审查时只补A，严格不重复B，保持Exactly-once。
