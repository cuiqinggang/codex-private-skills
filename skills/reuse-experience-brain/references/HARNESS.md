# EXP-HARNESS-001｜原生Windows兼容门
版本V1；证据日期2026-10-23；状态：NATIVE_WINDOWS_TEST_FAILED。
触发：LongHorizon Harness0.1.8在原生Windows，os.killpg/secure control bus相关报错。
原回执摘录：upstream_commit=fb7e1b677d85b8dd7a03368f6c7d976c1d0c54bd；native_test_result=56 passed,17 failed,14 errors,pytest exit1；Windows缺少POSIX进程组/secure control bus能力；A_T_VALID_seconds=null；B_T_VALID_seconds=null；original_untouched=true。
行动：先查官方支持环境与首个兼容失败，隔离修复/适配后才运行原同合同业务对照；不默认替换现有三人行V5+轻状态V3+执行桥。
内部冲突：同文件旧evidence仍写dependency pending，但status/native_test_result给出后续实际失败；不得拿旧安装中描述覆盖新测试结果。
边界：这些单测失败不证明Linux运行结果，也不证明两套方案业务A/B已完成，更不能判新工具全面无效或已更快。
证据：`C:\AI\LongHorizon-AB-20261023\AB_CONTRACT_STATUS.json`（2026-10-27实际读回）；`C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_DAILY\2026-10-23-DSE-INCREMENTAL.md`。
