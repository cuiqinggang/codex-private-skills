# Windows 测试目录修正：成熟来源与证据边界

Python 3.13 官方 os.mkdir 文档：https://docs.python.org/3.13/library/os.html#os.mkdir

官方说明：Windows 对mode=0o700专门设置仅当前用户与管理员可访问的控制；其他mode值忽略。本机首次TemporaryDirectory创建后沙箱访问/清理失败，与该行为相符。精确沙箱SID/DACL因果没有读取ACL做认证，因此不把推断写为已穷尽所有根因。

已有本任务外部验证器与成功业务回归采用工作树内正常Path.mkdir创建隔离fixture，保留现有继承权限。F002复用这一已验方法，明确禁止tempfile0700和权限修改，并独立检查残留/不可读目录，不削弱沙箱。不是网络/Orca故障，也不更改系统或既有受限目录。

本次重新查阅官方资料用于确认机制；R1业务14/14与21/21通过但残留清理门不通过，F002仍须真实验证。源文档不是当前任务验收证据。
