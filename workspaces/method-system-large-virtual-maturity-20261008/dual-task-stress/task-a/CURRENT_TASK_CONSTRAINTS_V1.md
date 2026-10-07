# TASK_A《当前任务目标与正反约束 第1版》

TASK_ID=DUAL-STRESS-A-LTMVH-PAGE-CONTROL-20261008
CONTRACT_VERSION=1
TYPE=LARGE_MATURE_MOTHER_TASK_REPLAY

目标：完整重放旧双页面控制恢复 / LTMVH 页面控制闭环，从 TASK_ACCEPTED 到本任务 FINAL_VALID。

必须保持历史 Oracle：CEO/Executor、多阶段、并行、Freeze、Reality、FAIL/Delta、Repair/Reverify、True New Chat、exactly-once、stall recovery、existing persistent browser reuse、R15 duplicate-browser guard、Merge、页面回收。

并发覆盖层：
- ACTIVE_CEO 只对本 TASK_ID 唯一；
- A 只能写 task-a 路径；
- shared persistent browser 可与 TASK_B 共用既有实例，但不得启动第二套；
- 关闭页面必须匹配 TASK_ID + PAGE_ID；
- A 单任务历史“最终 1 个空白根页”在 B 仍运行时解释为：A 页面残留=0，系统共享浏览器保持 B 所需页面；只有全部并行任务结束后才恢复系统 1 个空白根页。

DONE_WHEN：A 历史控制链全覆盖；A FINAL_VALID=YES；无跨 B 污染、重复执行、误关页、双 writer。
