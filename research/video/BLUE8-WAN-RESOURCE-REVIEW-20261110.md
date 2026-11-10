# BLUE8 Wan资源适用性复审（2026-11-10）

状态：DEFER_GPU_NO_NEW_FREEZE；FINAL_VALID=NO。未提交新GPU任务。

## 本机事实
唯一POSTCLEAN-R1 prompt `0d609b22-03b1-4f69-b2cc-c5e6113323e1`在WAN22_Animate加载时RAM达到99.2%，GPU约3403MiB，0采样步完成、0视频。原RAM94保护请求interrupt未能结束加载，已核归属后终止8198服务PID4968，RAM恢复53.9%。原生history为空，不能补造execution_error。证据：工程inference-81-POSTCLEAN-R1/resource-stop-final.json与telemetry。服务保持关闭。

## 作者结果的适用范围
[作者Animate Ultimate README](https://github.com/Thefrizzy1/The_frizzy1-Workflows/blob/main/workflows/wan2.2/animate-ultimate/README.md)，所读blob c4d587e开头：RTX3060 12GB、Ryzen5600X、32GB RAM、Comfy0.37.4、Sage；GGUF Q5_K_S、81帧480×864，整体7:05、采样4:51、峰RAM24.6GB、VRAM11.7GB。明确是v1.0.0成绩，当时Relight未加载，v2才修复。
本机608×832画幅面积为其1.21975倍，Relight已加载，SM75使用PyTorch attention且存在其他业务负载。不能把该成绩视为本机同质量SLA或内存保证。24.6GB报告值也不能直接解释为新增私有RAM需求。

## 已安装源码复核
ComfyUI-GGUF/nodes.py SHA256 `16be3b08b13de6279fc432addc628320019fcb24963cbc6b52b248de8f06316e`：GGUFModelPatcher的patch_on_device默认false；量化补丁会移到offload CPU；load强制处理补丁，pin/load释放mmap路径带可能OOM的源码提示。Advanced loader支持patch_on_device/dequant_dtype/patch_dtype，只证明有接口，尚无同SM75/LoRA/RAM/画质证据，不能直接冻结。
ComfyUI/comfy/cli_args.py SHA256 `70be4fb6830ccd7e43df06330f6da31f76c0ad11ee135d04913f5d8c1d9f4cde`：lowvram对dynamic VRAM可能无效，另一模式会将文本编码器放CPU；fast-disk针对dynamic加载，并不能证明其对当前GGUF静态patcher有效。
[GGUF上游](https://github.com/city96/ComfyUI-GGUF)仍说明开发中、LoRA支持属实验性。精确RAM增长归因未测；CPU权重/补丁与共享负载是有源码依据的候选原因，不写成已确认根因。

## 决定与准入
禁止原样重投、服务启动后恢复旧intent、放宽守护或终止其他业务腾内存；不删除重下载现有Wan配套。仅在完成与当前GGUF加载路径匹配的成熟资源配置、实际可用RAM/VRAM峰值预算及LoRA/精度兼容审查后生成新Freeze。当前未满足，保持DEFER。降低画幅或去Relight会改变合同，不能暗中修改后声称原规格通过。
本机复审快照可用RAM约12.85GiB、使用59.8%；一次RAM<80准入不能确保后续加载安全。81帧未通过不得扩193控制裁192的8秒，用户GUI与原声播放均未通过。

本机汇总：K:/Video-Storage-Audit-20261110/wan-resource-static-review.json。所有此前下载、失败、清理和恢复计入任务总成本。
