# H29-GC-R01｜混合模式现实只读协作测试记录（未完成）
日期：2026-10-10（UTC+08:00）
模式：H/GC，GPT 规划并调用授权 Windows 执行桥，Codex 原生 CLI 独立复核
任务：检查本机 E29-01.txt 至 E29-08.txt 八份审核输入的 UTF-8 可读性、定位、CASE、工具禁用表达与 SHA-256，不修改原始任务。
授权：本机只读输入；Codex `--sandbox read-only --ephemeral --ignore-user-config -c approval_policy=never`；不触碰浏览器、代理、受保护聊天或 snapshot.md。
设备：DESKTOP-4A1EGTM，在线 Desktop Commander ID=f6990966-5870-484b-bf79-409bc6fb963e
路径：C:\Users\A\Documents\Codex\ENGINE29_READONLY_20261010\E29_PARALLEL_CASES
GPT阶段实际终端测量：八份 UTF-8 读取 8/8；定位前缀 8/8；严格 `CASE=E29-XX` 7/8；严格区分大小写英文 `Do not invoke any tools` 7/8。PowerShell 内部 Stopwatch=361.775ms（不含工具连接、规划、Codex复核，不是完整 T_VALID）。
E29-01 异议：真实内容含 `PAGE=... TASK_ID=E29-01`、`CASE:` 与 `DO NOT invoke tools`，因此严格字面匹配不通过，不足以证明语义或任务合同 FAIL。独立审计待回执。
SHA256：
E29-01 B276E5CE492271804FD4EDCE53C89567D010AE02FDFA0C44CD47CCDDA85EB7E4
E29-02 BCBC168F6F22E039753F440AE11BB749A2C73E41DE709E0F7740479D4E7A65A9
E29-03 0C9E3141BDBCF4BF6FEDD0A2C170141720DD6A4BF4717DB2330429A03E61AC9E
E29-04 4CBA5E07CD5D674ABB1BAFB9C681FCA9172DE392AC660943F298035EE9A45DB1
E29-05 098ED06CAC3C1718370A032FBEEEB07283BE512D327167434C09BDC1B2494F9E
E29-06 B99330B284EDAEEFCE8BAC41672BC01EC5E8A8CCD7BB6BE9E573AC8AEB8AE12B
E29-07 846E3447CF081F89BEA1E0A5B330445E960B209AE1FD73DBF45C52B5096FC4FA
E29-08 AC39F430740791814B761D3AE9C19F4409F8386484FC305436D8DCEE5E31B54F
Codex专项：H29-GC-R01 已启动，CLI会话ID=01a125d2-b244-7831-b82a-d9a3d52de14b；输出预期写 H29-GC-R01_report.txt。启动有两项 YAML frontmatter 技能加载错误，尚未能认定对运行是否有影响。
证据状态：GPT段=REAL；Codex=STARTED_NOT_YET_VALIDATED；混合最终=UNKNOWN；G/C/H公平基准=NOT_TESTED；1/3/5/8并发=NOT_TESTED；正式公共29=NOT_ACTIVE。
注意：这里没有对现行 ENGINE.md 或 A29/B33 进行任何修改。

## 2026-10-10 追加真实回读：Codex已返回，但其只读终端遭策略拒绝
Windows 报告 H29-GC-R01_report.txt 已生成，28行，创建时间 2026-10-10T12:41:21Z。Codex报告两次尝试：PowerShell 7读取/哈希、简化 Get-Content 读取，均被执行策略返回 `rejected: blocked by policy`。独立读文件=0/8，SHA256=未取得；不应把此类安全策略拒绝与正常网络重连混为一谈，也不可将 GPT 的哈希结果冒充 Codex 独立验证。GC-R01独立审计=BLOCKED；完整GC VALID=NO。网络抖动可由原生Codex重连、查询既有会话、确认退出后有界重试，但策略明确拒绝不重复换命令规避。未修改公共引擎及A/B路线。
