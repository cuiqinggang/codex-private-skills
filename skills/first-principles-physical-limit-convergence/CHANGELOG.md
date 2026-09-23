# 版本变化

## v4.7.1
- 新增“虚→实原子发布门”：虚拟成熟只有在同一轮分配 NEXT_SEQUENCE、生成四定位标签并发布/自动发送自包含 Codex 现实验收命令后，才允许 VIRTUAL_COMPLETE=YES。
- 新增机器状态机合同与回归测试，禁止 VIRTUAL_COMPLETE_WITHOUT_REAL_COMMAND、REAL_WITHOUT_REAL_COMMAND、HANDOFF_READY_WITHOUT_COMMAND。
- Reality FAIL 回虚后沿用同一 TASK_TIME_ID，时间不清零、序号不清零；重新冻结必须递增序号并再次发布新的现实命令。
- v4.7.0 双时间单闭环保持不变。

## v4.4.1
- 修正 v4.4.0 的根基层遗漏：现实底座恢复为“虚/实”共同的必需根基。
- 现实底座不是第三步，也不是可选具体工具。
- 虚新增“现实底座足够”完成门。
- 实新增“现实底座吸收检查完成”收口门。
- v4.4.0 的仓库结构实测不再视为完整方法现实认证。

## v4.4.0
- 唯一锚定物直接镶嵌在 `SKILL.md`。
- 删除具体工具特例。

更早版本通过旧分支和 Git 历史检索。
