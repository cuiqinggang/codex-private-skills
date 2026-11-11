# EXP-VIDEO-CLEANUP-20261111-001｜65.6GB候选逐项确认，而不是整目录判废
类型：CASE / ERROR / SKILL_CANDIDATE；核查日期：2026-11-11。原任务VIDEO-STORAGE-20261110 / PI65GB；来源：GitHub main research/video/VIDEO-STORAGE-CURRENT-20261110.md、research/video/PI65GB-AUDIT-RESULT-20261111.md及其289项决策表；本日Vault 01_DAILY/2026-11-11-DSE-INCREMENTAL.md。原始审计、删除回执保留原项目，本卡仅最小脱敏导航。

触发：Pi将9临时项+167历史AI项目+113 Codex工作区标为约65.6GB待清理；旧文件无进程并不能证明无效，目录级引用也不能证明每个文件有效。LAST_GOOD：已有VoxCPM2普通话/女声/参考克隆等真实音频结果，Polsia/DeepSeek/ECC环境、冻结技能及原业务恢复记录仍被引用。FIRST_DELTA：候选同时包含旧ISO/截断下载/重复安装ZIP、可以按锁重建的node_modules，也混有约10GiB有用VoxCPM2和在用源码；旧Unit=dir误指转储目录、Grafana归档657成员未匹配、旧MSIX单文件被占用。

原项目经过定向路径、引用、SHA或压缩成员等价性和锁文件核对，实施5批精确删除：共126615文件、逻辑12675034580字节（11.8045GiB）。C盘当次可用339997364224字节（316.647GiB），与前次差+10.973GiB包含并行写入，不能混算成物理释放或记忆性能收益。失败MSIX不计删除、不自动重试；目录误判后只精确处理两份DMP，不删全目录；保留真实被引用或未证等价资产。未恢复已放弃的跨盘迁移或旧GPU intent。此复盘并未操作磁盘或扫描H/K。

回归与局限：原工具Node/npm/Codex CLI/Blender版本和Torch导入、3 junction/51保留路径通过；Etcher1.18.11仅GUI窗口启动观察，不是写盘全GUI签收；无Wan新GPU提交，旧RAM99.2%资源停止，8秒视频0、完整75%清理目标未通过。现有例子的有限成熟决策为按来源、哈希、依赖、可重建能力逐项分类并沿原清理/回执脚本执行；不将289项卡片当通用一键删除程序或正式新技能，不增加无证稳定规则。重复事件只反馈原项目，新增业务配方0，memory_T_VALID_gain=NOT_MEASURED。