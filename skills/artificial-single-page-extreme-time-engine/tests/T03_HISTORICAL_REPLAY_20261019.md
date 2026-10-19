# T03 历史已完成业务真实重放｜2026-10-19

设备 DESKTOP-4A1EGTM，V10 C 通道。原历史工单 `requests/T03.md`，曾在 n_tasks=0 时产生 ZeroDivisionError。源已验代码未改，复跑副本在 `C:\Users\A\Desktop\SRX_V3_ReadPack\T03_REPLAY_20261019`。

## 证据
- 原已修复工作树：离线回归 5/5 OK。
- 把历史恢复前 `before/scripts/run.py` 覆盖隔离副本：5 项中 2 ERROR，堆栈是 `scripts/run.py:229` 的 `ZeroDivisionError`，真实复现。
- 手动复核复制历史已验修复代码：5/5 OK，SHA256 `320f2bf3825bf000bd501309e44ce39f36ce507005e0e694A07FE950777D2314`（不区分大小写）。
- 使用 `tests/t03_historical_replay.py` 一次自动执行：历史故障复现，before_rc=1，before_ms=1122.0；应用最小历史修复 1 次；after_rc=0，after_ms=2085.36；5/5 PASS。第二次同一程序出现 ALREADY_DONE_NO_REPLAY，没有重复修复。
- 将本机 checkpoint 人为恢复到 FAULT_CONFIRMED 再启动，首先出现真实编码异常：PowerShell Set-Content 写入 UTF-8 BOM，Python utf8 JSON 解码失败。识别为序列化格式不兼容，使用标准 UTF-8 无 BOM 转码后继续恢复：after_rc=0，5/5 PASS，after_ms=1577.26。

## 结论与边界
PASS：历史真实故障再现、预先已有修复复用、状态中途恢复、结果回归、再次执行不重复修复。实测产生一处非预设编码错误，并已修复 checkpoint 文件编码。中间节点恢复是人工设置 checkpoint 模拟跨会话，不是 GPT 真正断线后全自动唤醒。历史修复选择是事先确定的，未证明未知故障自治分析。未调用 Orca/Codex 实时模型任务，未测调度 heartbeat 根因，也未完整实施三广域成熟方案的时间最优闭环。测试仅为历史 T03 的局部真实回归，不能当完整《三人行》第4版终验。
