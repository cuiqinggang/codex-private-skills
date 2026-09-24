# 极限短时间引擎 v4.7.2

## 定位

v4.7.2 不增加新方法核心；它把已经验证有效的规范变成唯一机器状态序列和 deterministic validator。

## 合并来源

- v4.6.1：GPT 能现实预跑的关键公开子路径必须在虚中先 PASS。
- v4.6.2：时间账本必须完整；同一 FREEZE_ID 只允许一次 REAL；REAL FAIL 必须回虚并产生新 FREEZE_ID。
- v4.7.1：VIRTUAL_COMPLETE 与现实命令发布必须原子完成。
- v4.7.0：T_MATURE* + T_CLOSED_REAL 双时间单闭环。

## 唯一状态序列

E00 TASK_BIND
E10 TIME_BIND
E20 REALITY_BIND
E30 VIRTUAL_MATURE
E40 GPT_PREEXEC
E50 FREEZE
E60 ATOMIC_DISPATCH
E70 REAL_EXEC
E80 REAL_JUDGE
E90 FINAL_CLOSE

正常只允许顺序前进；唯一失败回路 E80.FAIL->E20。

## 机器门

非法跳转、缺时间核心、NEXT_STATE 错误、重复序号、同 Freeze 二次 REAL、REAL FAIL 直接重试、FINAL 缺 REAL PASS 或时间账均 BLOCK。

状态机自测 20/20 PASS。

## 现实底座修正

v4.6.1/v4.6.2 的方法文本/manifest 曾写 Reality Foundation 1.1.6/1.1.7，但对应分支实际 Foundation 文件仍为 1.1.3。v4.7.2 以实际资产 1.1.3 为唯一真相。

## 尚未宣称

20/20 是合同/状态机层机器自测，不等于本机 Codex 执行器现实认证。下一门必须由本机 Codex 实际运行 validator 正反例，PASS 后才允许 LONG_TERM_CANONICAL=YES。
