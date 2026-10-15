# Orca + Codex：配置与派发 Windows 实测 V3
日期：2026-10-15 UTC。方法仍为三人行 V2 C002；不是方法 V3 或正式融合包。
本报告不是整体验收通过。FINAL_VALID=NO；WHOLE_VIRTUAL_MATURITY=NOT_PASSED。

## 本轮实际完成
- C 实时设备 Online，Windows 命令实际以 A 用户运行；home C:\Users\A；Node v24.14.0；环境未设置 CODEX_HOME / ORCA_CODEX_HOME。单次可用内存 9,333,645,312 bytes，满足 4 GiB 保留线。
- 用 psutil 只输出进程归属、PID 和创建时间；首次检查无不可读取候选进程。原 N001 历史 PID 不在当前列表，三个其他 Codex 的命令不匹配本项目；没有停止它们。历史会话最终退出码仍 UNKNOWN，不能因此把原失败改成成功。
- 固定官方 Orca 二进制、捆绑 Node 通过原 SHA 校验；新目录首次 JSON→SQLite 完整启动导入实际执行成功。只使用 ORCA_USER_DATA 隔离状态，真实 home 保留。
- 独立只读查询新 SQLite settings，确认 hooks=false、自动预信任=false、native chat=false、无托管账号、Windows cmd 终端和任务内 workspaceDir；Codex 受限参数与 priority/auto_review 均保留。
- 官方 repo add → worktree create → terminal create → 真正子进程写回执 → terminal read 完成，home/cwd/真实 ORCA_TERMINAL_HANDLE 一致。
- Codex --version 实测 0.160.0；没有读取/复制登录凭据。
- 新业务测试创建了真实协调终端，run-create 与 worker-start 身份匹配；Orca 已实际创建 Codex 子进程。R2 argv 包含 --no-daemon、--sandbox workspace-write、--ask-for-approval on-request、approvals_reviewer=auto_review、service_tier=priority、-m gpt-6.1-sol、model_reasoning_effort=ultra。后端实际服务 tier 仍 UNKNOWN。

## 三个冻结及结果
1. 组件脚本 analysis/component-check-r1.py@71df25320b49ea45a2089b86e1cd69ed94e89306，blob6898a47f64ed301b7d0053b7c1c24d0327246bd8。实测组件链通过；测试器最终把 SQLite tuple 与 JSON list 直接比较，导致 exit1。保留原失败，不重跑组件。verify-component-r1.py 独立核验数据库配置及回执通过，原 result SHA256=0efb8b573d625b9218cb9050e2389df65fc0afd469442fa1f56f383a38d6b835。后续脚本改为 JSON 规范化后比较。
2. 单任务业务 R1 analysis/business-smoke-r1.py@db03c39c6ac081f89ee334f17bc88537084f7e38，blob8419e339baea3a7702cb7e1c101fa819d35e711a。run_5b3939eb3ad9 / task_42815db4ed37 / ctx_a5b4ebb6277a。明确 failed: agent_readiness / agent-trust-workspace；任务正文未执行，按回执回到虚拟修正。
3. 单任务业务 R2 analysis/business-smoke-r2.py@69b825c1709563698dcb7cc7e2fae8c76956c19a，blobe4c5ee978f3b1dfbf1420d2db7b037c25765034b。复用 Codex 0.160.0 官方 projects 配置，仅命令行信任用户已授权的新 fixture 与工作树两精确路径，不调用全局配置写入接口；保留原沙箱与审批。run_cd1b0557ab0e / task_3ab643edbc70 / ctx_9a05c725c022。Orca 返回 ready/input_accepted/turn_started，但180秒等待后无 DELIVERY.md，终端仍显示任务文本、Context 100%，worker-show liveness=unverifiable/missing_status。独立固定验证器确认空报告仍 ZeroDivisionError；T03两项加编译=2/3，原始 BAD 同样2/3。业务验收拒绝。

“Codex 已开始处理”此前进度表述依据 Orca turn_started；后续独立证据不足，纠正为“派发 API 报告已开始，业务执行未证明”。不能拿 ready 冒充完成，也不能断言必然没有发生模型请求。未取得完整模型用量，缺测为 UNKNOWN。

## 清理、计时与副作用
三次测试都只停止各自启动进程的实际后代，回执 remaining_owned=[]；不按进程名称杀全机进程，不停止其他 Codex/浏览器/桥。保留隔离目录、SQLite 和失败日志，不删除保护性迁移/锁记录以强行启动。
R1 scope局部15.811秒、R2局部222.448秒是启动脚本至清理前后记录的测试墙钟，不含前面研究、后续独立QA和网上归档，不是 T_VALID，更不是效率提升。
外部验证器会产生 __pycache__；R2 git状态仅见该缓存，无业务修复。既有 GOOD_003_CEO_RECOVERY 没有重做。
本轮无新平台拒绝；没有创建/重发历史被拒 GitHub 预检工作流，没有将旧拒绝解释为全平台不可用。最小有界组件测试、新业务测试分别记录，未执行旧恢复预检。
桥当前入口 V7 用户暂停 A，实际沿 C；未恢复 A，未改系统代理/网络/全局模型配置。
没有全局配置写操作是本轮命令范围陈述，不是对所有同时运行应用做全盘无写入认证。

## 确切停点与下一差分
输入提交/执行观测尚未闭合，不能宣布整套虚拟成熟。上游 issue https://github.com/stablyai/orca/issues/22703 与 draft PR https://github.com/stablyai/orca/pull/22705 描述 Windows Codex 多行输入编码差异；它是调查线索，不是本机已证根因，不直接安装未验补丁。
下一节点先审查固定版本 headless prompt submission 的 Windows 换行、粘贴完成与 Enter 提交及 turn_started 判定；不能把桌面 renderer 修复直接套入 headless，也不能盲目补 Enter 或重发同一 UNKNOWN 请求。另一成熟候选是官方非交互 Codex 执行入口/Orca structured 通道，须核对其原生身份、权限、回执和既有登录兼容后再选择。
按三人行 V2 同页最多三次 Freeze，本轮达到上限，不启动第四次变更实测。这项限制不阻断证据保存与只读分析。本轮明确未完成用户的全部目标；接续无需再下载 Orca、调查已解决的 home/priority 参数或重做已验恢复 T03。
正式三任务 Reality=0；连续全套=0/10；完整AB=0/10；极限效率与融合包未认证。

## 已归档可复核证据
- evidence/component-check-r1-result.json@9f9271e683f657eab99f32b95ed8478acdd62553
- evidence/component-check-r1-independent.json@3ac584655f73d27dbea173b18d7cdc9249e4a855
- evidence/business-smoke-r1-result.json@be1a94f1df271fca4256fe8c2e4814a969ee9651
- evidence/business-smoke-r2-result.json@0887967b13e99b429ab2512e6a08e5d3637bd61e
- evidence/business-smoke-r2-qa.json@fb6870bc1edb602ecbc9f923e07f97ea48279700
上述五份均已独立按提交回读一致。脚本亦先保存固定提交并回读后执行。
