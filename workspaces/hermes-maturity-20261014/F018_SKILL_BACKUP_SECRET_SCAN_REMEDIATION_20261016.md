# F018｜Hermes技能静态秘密模式告警：安全隔离与Reality
2026-10-16｜TASK HERMES-ECO-20261014｜《三人行》V2（仅Hermes项目）｜Windows桥 V7 C优先、B备用、A暂停

## FIRST_DELTA及冻结修复
原始完整静态检查只剩一项高置信秘密模式命中：Hermes母技能递归 evidence/backups 内一份2026-10-04的历史配置YAML快照。它不是生效配置文件，更不是技能发现故障。修复禁止查看/打印密钥、修改真实活动配置、删除历史备份字节、跳过扫描规则。
C通道真实执行：核实文件存在和SHA，确认在母技能内只有一份历史CONFIG-DELTA.json引用旧位置；按已冻结最小范围原字节复制到用户原有的 .hermes/backups 安全备份域，SHA一致后移出Hermes技能扫描树。原CONFIG-DELTA.json保持历史证据原状，精确新位置仅保存在本机F018迁移清单。没有向云端上传原配置。
原SHA256=37C5CF0FB52E21D4173C2A9232977BF9EB07949480ABFC180AF9FBDDA48298B5；迁移后校验相同。
正式原始检测器 Test-HermesMatureSuperToolSkill.ps1 完整 Reality：18/18 PASS、failure_count=0、高置信模式 hits=0，PowerShell parser、JSON及其他质量门PASS。不是靠修改或绕过检测器获得PASS。

## 同轮功能Reality及执行桥
当前正式Hermes CLI经C真实只读运行：原生skills_list=171、skill_view母技能及Repair均成功、native read_file知识库路由成功；模型配置沿用生产包装器；CLI exit0，计时26939ms（单次任务真实计时，非极限T*）。
V7官方冻结 FREEZE-GPT-WINDOWS-BRIDGE-V7-A-PAUSED-20261016，本机判路器SHA A01D22B210632FAB72F0AF84D6E3F360FCA531EB62A18F72D23360F8006727E2；PS5.1 Parser 0，C首选/B备用/A无权派单与BLOCKED三种实时测试通过。V6旧路由不得再覆盖V7。

## 认证边界
本轮F013、F014及F018限定范围功能和静态安全通过；整站FINAL_VALID=NO，综合五次验收仍0/5。F002 Runs HTTP400 原业务状态UNKNOWN不盲重发；浏览器实际UI会话、原生音视频、多模型全面质量、跨重启/登录恢复及连续稳定性尚未完成。不更改FlClash、系统代理、正在运行的服务、密钥、Docker卷、已登录浏览器。
