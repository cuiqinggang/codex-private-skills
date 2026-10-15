# F019｜Hermes Repair Loop 实际故障注入＋同项独立 Gate｜Reality 前冻结
日期：2026-10-16｜母任务 HERMES-ECO-20261014｜承接 HERMES-ECO-F018-20261016
方法：本项目选用《三人行》V2，沿用 Hermes Mature SuperTool v2.0 和已有 hermes-repair-loop-adapter v2.0。Windows桥 V7，C=Remote_Desktop_Commander、B备用、A暂停派单。全站 FINAL_VALID=NO、历史正式综合5轮0/5。

## 目标与GOOD/BAD/FIRST_DELTA
GOOD：F010原生CLI能够修复隔离Python模块、外部8/8单测；F018原生skill_view已验证Repair适配器存在。BAD：尚无同一真实Repair任务中“真实错误测试→技能调用→最小修复→同项外部独立 Gate→证据闭合”的验收，不能从两个分离样本合并推断。FIRST_DELTA：Repair技能发现已恢复，但未形成联动的故障注入、过程状态与独立验收证据；不归因于模型Provider或重装。
拒绝其他路线：不重复F005 invoice样本；不重造调度器/Runner/API验收器；不碰未知F002 /v1/runs；不更换模型；不控制GUI、不动FlClash代理/密钥。

## 预冻结任务不变量（本节点只执行一次合法真实模型Repair）
唯一隔离节点：C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F019_REPAIR/
输入3文件：requirements.md、refunds.py（故意有缺陷）、test_refunds.py（质量标准），另追加只读文件哈希与Baseline失败回执。唯一可改退款算法文件 refunds.py；修复状态/报告可写在该节点，测试与需求一律只读且SHA不得改变，其他F002/F005/F018文件/配置不得修改。
函数 reconcile_refunds(events)：只统计 kind恰为refund 且status恰为settled；非匹配项跳过；匹配项必须transaction_id为非空字符串且amount_cents为非负int（bool不是int），同交易ID同金额去重、冲突金额ValueError；纯函数不得修改输入；任何非字典事件报ValueError；events需list/tuple，否则TypeError；返回total_cents与unique_refunds的字典。无依赖安装，不访问密钥，不发送消息或网络副作用。
- 冻结外部 unittest 覆盖 >=15个确定性场景（正常/跳过/非法金额/重复/不变性/大数/异常类型）。
- 先外部真实baseline FAIL并记退出码、失败用例，再走当前Hermes正式 CLI ltmvh-hermes-formal.ps1，保留原OpenRouter/deepseek-v4.1-flash。要求模型亲自调用原生skill_view（hermes-repair-loop-adapter），查看要求和测试，执行测试确认失败，FIRST_DELTA定位，仅修改 refunds.py，重跑同项测试，输出修复证据；如技能加载失败记录事实，不能自称原生Repair技能闭环。
- CLI进程如未结束，按pid读取终态，不盲重启/重发。结果不充分时状态UNKNOWN。
- 模型运行后，GPT通过C独立执行原冻结unittest、校验三文件SHA/源码变更、验证未涉及外部原件；不以模型自报/exit0单独判Gate。若FAIL，回虚冻结下一轮最小修复，最多3轮，禁止边测边扩展方法。
- 真正完成的合同为：baseline的预期FAIL、Hermes真实模型执行、至少一次原生skill_view技能可见证据、模型实际最小修复、外部全部测试PASS、原测试和requirements SHA一致、真实T_VALID墙钟、可回滚证据。缺任一则只给局部状态，不能认证全部。
- 时间：进程模型墙钟与外部独立验收分别记；本任务缺同输入完整GOOD，不宣称速度提升或物理T*。不把准备任务工时当作模型性能基线，但报告全流程成本与未知量。

攻击树结论：01 选成熟CLI＋已注册Repair技能 KEEP候选；02 使用固定故障夹具独立Gate KEEP候选；03 重造API/并行/自建修复框架 ABANDONED；04 WebUI GUI与F002原Runs API属于其他节点 NOT_APPLICABLE。
预冻结状态=VIRTUAL_MATURE_FROZEN；现实结果另建 F019_REALITY_20261016.md。
