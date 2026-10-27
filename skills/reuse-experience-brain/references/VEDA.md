# EXP-VEDA-001｜保留已验证的否决
版本V1；证据日期2026-10-24；状态：同配置筛选否决。
触发：RTX2080Ti/SM75、H3 VEDA候选、1024x576、5帧、20步、同seed、FBC Safe。
原FINAL_STATE摘录：decision=KEEP_V4_1_0_A2_DEFAULT；visual_quality=FAIL_HORIZONTAL_TILE_CORRUPTION；valid_paired_samples=1；three_pair_certification=false；baseline_seconds=109.329；candidate_seconds=283.985；attention_skipped_percent=0；T_VALID=null；full_124_frame_benefit=UNKNOWN。
行动：匹配这个配置时保持原V4.1.0 A2默认，不为重新发现同一否决而重跑；有新版本、新配置或新反证时另立隔离合同。检查实际attention跳过比例，不能只看hook已加载。
边界：只有一对五帧筛选，不是三对认证，不否定其他显卡/长视频；不能宣称124帧必然失败或已知完整节省时间。原报告next_action要求读已有证据，不重复该否决配置。
证据：`C:\AI\H3-VEDA-Trial-20261024\FINAL_STATE.json`（2026-10-27实际读回）；`C:\Users\A\.codex\obsidian-vaults\AI-COMPANY-KNOWLEDGE-OS\01_DAILY\2026-10-24-DSE-INCREMENTAL.md`。
