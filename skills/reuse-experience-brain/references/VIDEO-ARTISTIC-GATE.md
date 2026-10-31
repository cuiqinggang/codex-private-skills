# EXP-VIDEO-ART-001｜视频技术有效不等于表演与作品质量合格
版本V1；核查日期2026-10-30；分类CASE/ERROR/CANDIDATE_RULE；证据等级=已有H3成片技术回读、音频ASR对照及审片结论。

触发：已有短片可以解码并满足帧数、长度、音画输出等机械合同，但人物语句、口型、动作触点、表演情绪与原剧本不符。环境：十几年H3 V1.4评审稿，本地10秒、240帧、24fps、576×1024竖屏。

LAST_GOOD：原渲染合成、文件哈希、解码、音轨均通过技术验收。FIRST_DELTA：原生女声的重点台词与剧本逐字不一致，耳光动作接触偏高且脸部情绪强度低于参考；原生/离线两套ASR对照暴露差异。最小返工：在已有流程内离线修正台词词面并重新检测，ASR部分改为准确文本，但生气表演、口型同步、物理触点尚未通过艺术审核；禁止以改文本后ASR通过代替真人感和情绪质量。

现实结果：2026-10-30本地评审MP4技术媒体有效（technical_media_valid=true），审片结论REVIEW_ONLY、artistic_valid=false、T_VALID=null。应回到原影视制作的布局、动作排演、演员表演、音效与镜头连续性质量门，再决定具体镜头返工；不在复盘中重拍或自行定义替代电影工序。

适用：影视生成工作流中技术门与编剧/镜头/表演门分离；H3人物动作及中文台词核查。不适用：将本地评审判为合格成片、把词面精确当口型表演精确、将此前厨房124帧图生视频历史复现当本短片艺术通过、推断完整T_VALID。

原证据：C:\AI\TenYears-H3-20261030\delivery-review.json、dialogue-review.json、final-asr-loudness-fixed.json、S03\contract.json、S04\contract.json；独立完整TASK_ID/总Freeze未在本轮核实。

## 2026-10-31新增评审候选｜R9不等于最终作品批准
本机C:\AI\TenYears-Animatic-20261030\R9\delivery-state.json与README-Review.md显示新R9已提供15秒、360帧、768×640的带声候选，原生仅384×320后做x2画面修复。内部技术和艺术审查标PASS，但状态明确READY_FOR_HUMAN_REVIEW，human_approval=false、final_approval=false；不能把30日旧10秒艺术失败简单改为作品最终成功，也不能把自动审查输出代签人工审美。R9审查还保留ASR误判“糟践”、画面左右及不存在帧号的自动审计错误，须按真实原声与有时间戳的帧核查。若人工否决，则按原工序返修；本卡不授权复拍或覆盖原Freeze。资源准入90%、运行保护95%只对本片有效。原始证据同R9目录README及delivery-state.json。
