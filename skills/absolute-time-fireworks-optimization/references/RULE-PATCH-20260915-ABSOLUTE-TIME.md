# Rule Patch：极限时间性能项目默认路由

当固定任务以降低真实 T_END_TO_END 为唯一目标时，默认先调用
absolute-time-fireworks-optimization。

优化主循环必须是物理时间账、最大可消除块、极简 fast path、单变量真实 2+5、
KEEP/ROLLBACK。watchdog、monitor、同步 evidence、Git、Knowledge Brain 与复杂统计不得进入
T_END_TO_END。

performance-benchmark-convergence 仅在最终明显更快 candidate 形成后用于 certification。
旧 Measurement 证据保留为失败资产，不删除、不改写。
