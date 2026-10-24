# 双通道故障接管规则 V1
线上 GitHub 优先写入并回读；如线上失败，记录故障，使用 Windows C:\AI\AIORG-Shared\tasks\<TASK_ID>\ 的原生文件写入并回读，主任务继续执行。恢复后对账补同步。不可声称未验证的成功。遵守安全限制，不以切换位置规避明确的安全禁止；普通工具接口失败优先改用官方 GitHub Contents API create_file/update_file，获取 commit SHA 后回读。C 盘使用 Desktop Commander 原生文件操作。任务未全部 QA 通过时保持 OPEN；跨会话需有持久执行器确认接管。
