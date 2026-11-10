# EXP-BLUE8-QUALITY-20261110-001｜视频原生出片与动作/口型验收不等价
类型：CASE / ERROR / CANDIDATE_RULE；核查2026-11-10。目标：24fps、8秒192帧的蓝裙数字人原片动作/原声口型/遮挡一致性，2080Ti SM75 22GB。
LAST_GOOD：复用已有MiniMax H3 Ref2VA、32B INT4、INT8 VAE及官方Turbo4，找到既有本机资产并防止重复下载；源输入/原声时轴按原冻结核对。
FIRST_DELTA：唯一56帧阶段原生成功08:44:200、可解码、无全黑/静止重复，但原片首帧低头双手合，生成首帧正站，动作和同时刻口型未达到严格合同；G3质量FAIL，完整8秒生成0、FINAL_VALID=NO。另有执行器在原生成功后KeyError('candidate')，候选赋值顺序已离线修正和分支检查，但未做新GPU回归，不能宣布运行时闭环PASS。旧5分钟预算interrupt不能当模型无进度或CUDA故障。
后续成熟方式：V1.4只读核查Wan Animate Ultimate v2的GGUF+pose+face功能完整候选、Character Swap和Viggle反例及本机缺失节点/模型；当天GPU新提交0、下载0、隔离安装0。先比原始身体姿态、pose/face遮罩、原声时间轴，代表短段质量合格再扩192帧，用户本机播放器真正验收；不能拿MuseTalk嘴修补错误身体动作底片，不能由作者3060数据估本机30分钟SLA。
原证据：GitHub main skills/video-extreme-time-engine/references/BLUE8-COMPLETE-PAIRING-V1_3-20261110.md，research/video/BLUE8-COMPLETE-STACK-AUDIT-V1_4-20261110.md，skills/visual-art-engine-performance-ladder/references/PAUSE-AND-ERROR-20261110.md。仅记录失败与现成候选，不发布合格业务配方或新的稳定规则，T_VALID=NOT_MEASURED。