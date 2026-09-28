【极限短时间 v5.6自动化1｜v5.6三行核心头现实认证｜01｜实】
【状态机｜v5.6｜30｜虚实交接中】
【时间锚｜TASK_ACCEPTED=原始连续现实起点当前无法合法恢复｜当前节点时间=由Codex本机实际读取时记录｜整体已用=未知｜T_VALID=尚未产生｜T*=未知】

目标：现实验证v5.6三行核心头与机械状态流转。不得增加规则或架构。

固定对象：
- skills/first-principles-physical-limit-convergence-v5.6/SKILL.md
- skills/first-principles-physical-limit-convergence-v5.6/runtime.py
- skills/first-principles-physical-limit-convergence-v5.6/display.py
- skills/first-principles-physical-limit-convergence-v5.6/ACCEPTANCE.md

30固定动作：
1. 实际读取上述四文件并计算摘要。
2. 核验定位、状态、时间锚三行均存在且字段完整。
3. 核验时间使用现实可读时间；无法合法恢复整体起点/整体耗时时必须显示“未知”，禁止估算或跨宿主拼接。
4. 核验20/PASS唯一转移为30并自动交接；30/PASS唯一转移为40并立即执行，不等待GPT第二次授权。
5. 全部PASS后自动进入40，立即执行同一01包以下现实测试；任一FAIL才留30回报阻断。

40固定动作：
- 实际运行display.py的五状态显示：10/20/30/40/100，每次必须恰好三行。
- 攻击缺页面名、缺任务名、缺TASK_ACCEPTED、缺当前节点时间、虚/实非法，必须拒绝。
- 整体时间不可合法计算时必须保留“未知”，不得伪造。
- 实际验证runtime.py冻结转移和ACCEPTANCE.md全部攻击项。
- 保留原始日志、起止现实时间、同源局部毫秒耗时、文件摘要和逐项结果。

返回时仍保持40等待GPT最终审核；回报开头必须直接显示同样三行核心头，并填写Codex能够真实取得的现实节点时间。不得自行签100。

禁止修改代理、FlClash、系统设置、正式current、旧证据或旧时间线。