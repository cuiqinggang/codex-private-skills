项目：《家庭作业江湖：功夫式 AI 辅导短片》

当前任务：根据 v1.6 Remotion 执行包，把已完成的 30 张正确关键帧实现为 15 秒竖屏 Remotion 原型。

必须读取：
1. H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包\SKILL.md
2. H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包\remotion\timeline_v1.6.csv
3. H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包\remotion\keyframes_manifest_v1.6.json
4. H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包\remotion\subtitle_rules_v1.6.md
5. H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包\remotion\audio_nodes_v1.6.md
6. H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.6_Remotion执行包\references\禁止事项_v1.6.md

图片源目录：
H:\Hermes_Skills\家庭作业江湖_功夫式AI辅导短片技能包_v1.5_正确关键帧图\images_full30_backup\

执行要求：
- 建立或使用一个 Remotion 项目。
- 输出 15 秒、1080×1920、30fps 竖屏原型。
- 严格按 timeline_v1.6.csv 使用 30 张关键帧。
- 加轻微 Ken Burns、硬切/快切/少量淡入，增强视频感。
- 字幕和文字严格按 subtitle_rules_v1.6.md。
- 音效节点按 audio_nodes_v1.6.md 写入计划或占位实现。
- 不重新发明导演方案，不改故事，不添加广告词。

成功判定：
1. Remotion 项目能启动预览。
2. 15 秒完整播放，不缺图。
3. 30 张图按时间线出现。
4. 14-15 秒只出现：17371044790 / 资料和教学全免费。
5. 生成 report.md，写明：项目路径、运行命令、预览方式、导出方式、未完成项、问题与建议。

失败停止条件：
- 找不到 v1.5 图片目录。
- 找不到 v1.6 执行包关键文件。
- Remotion 环境无法安装或启动。
- 发现必须修改导演方案才能继续。

完成后输出状态码：
CODEX_REMOTION_V16_REPORT_READY
