【极限短时间 v5.6自动化1｜v5.6证据裁决现实认证R2｜01｜实】
【状态机｜v5.6｜30｜虚实交接中】
【时间锚｜TASK_ACCEPTED=原连续现实起点不可合法恢复｜当前节点时间=Codex实际读取时记录现实时间｜整体已用=未知｜T_VALID=尚未产生｜T*=未知】

目标：现实认证v5.6修正版“证据→裁决→状态→三行显示”的单一机械链，重点复验上一轮9个现实FAIL根因是否消失。

固定对象：
- skills/first-principles-physical-limit-convergence-v5.6/SKILL.md
- skills/first-principles-physical-limit-convergence-v5.6/runtime.py
- skills/first-principles-physical-limit-convergence-v5.6/display.py
- skills/first-principles-physical-limit-convergence-v5.6/ACCEPTANCE.md

30固定动作：
1. 实际读取四文件并计算摘要。
2. 不允许向runtime传PASS；只能提交证据。
3. 核验20状态证据字段：frozen_body/task_link/time_anchor/materials_readable。
4. 核验30状态证据字段：task_match/materials_match/time_anchor_match/same_package。
5. 30全部证据为True时，运行器必须自己裁决PASS并自动进入40；任一False留30；缺证据UNKNOWN留30。
6. 30 PASS后立即执行同一01包40现实测试，不等待GPT二次授权。

40固定动作：
1. 正常证据链实测10→20→30→40→100。
2. 重放上一轮现实FAIL：A2/A3/A4/A5/A7/A9/A10/A11/A12，必须全部被运行器拦截。
3. 缺30时间证据必须UNKNOWN→30；缺40最终证据必须UNKNOWN→40。
4. 验证不存在外部直接PASS入口。
5. 验证每次状态转换都由runtime调用display并原子返回三行：定位、状态、时间锚。
6. 保留原始日志、文件摘要、现实起止时间和同源局部毫秒耗时。

返回：开头必须直接显示三行核心头；逐项给出正常链、9项现实FAIL回归、UNKNOWN路径、直接PASS入口、三行原子显示结果。执行完成保持40等待GPT最终审核，不自行签100。

时间要求：现实可得时间必须显示；无法合法恢复的整体起点/整体已用/T_VALID保持未知。不得跨宿主拼接、估算或用局部耗时代替整体T_VALID。

禁止修改代理、FlClash、系统设置、正式current、旧证据或旧时间线。