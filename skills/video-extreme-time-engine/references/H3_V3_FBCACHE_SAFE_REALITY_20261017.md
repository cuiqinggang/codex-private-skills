# FirstBlockCache Safe + R2 五帧现实结果（2026-10-17）
方法：《三人行》第3版，C通道，固定原R2 1024×576 / 5帧 / 20步 / seed3013 / INT8 ConvRot / 同参考图及提示词、VAE、scheduler。仅插入FirstBlockCache Safe模型补丁，无R5分块、无TeaCache。固定开源commit d474755360cc1784df1b7c933ca28195e55e3445。
唯一prompt_id=8026d945-4dda-4562-9e2b-186a634f581f；本轮仅一次生成；独立8197端口。
结果：5/5张PNG全可解码，1024×576，SHA256见本机V3_FBCACHE_SAFE_20261017/C-result.json；文件前缀output/V3_FBCACHE_SAFE_20261017_。
完整提交→图片校验203.797秒；R2原始463.266秒，少259.469秒约56.0%。采样106.297秒；R2采样332.610秒，减少226.313秒约68.0%。首次单次测量受冷热缓存条件影响，不声称统计稳定重复或物理极限。
真实ComfyUI运行日志缓存11/20，full9/20，cached steps [3,4,6,7,9,10,12,13,15,16,18]，estimated block-stack speedup 2.17x。证实跨步复用而非单靠加载/分块。
质量：实读新生成五帧768×432缩放审查：人物面容、衣服、瀑布及构图未见严重失真或崩坏；相对于R2逐帧MAE为0.862/2.176/3.936/4.803/5.012（0-255），PSNR44.60/38.35/33.98/32.41/31.91 dB；第3-5帧偏离明显增大，新样本亮度也较原R2稍高，不能声称逐像素等价或严格同画质。仍需针对脸部、手部、衣纹做原图局部审查和人工质量准入。
资源：监控194个样本，RAM占用率峰值70.5%，guard-stop不存在。实时采样观察约20.5GB GPU占用，但缺连续显存峰值证明，资源完全PASS未认证。
当前结论：REALITY_IMAGE_OUTPUT=PASS；RUN_TIME_SPEED_GAIN=PASS_SINGLE_SAMPLE；CACHE_HITS=PASS；VISUAL_INITIAL=PASS；STRICT_EQUAL_QUALITY=NOT_VERIFIED；VRAM_PEAK=NOT_VERIFIED；STABILITY=NOT_VERIFIED；FINAL_VALID=NO（极限成熟未获认证）。不重复本次生成，不删除历史。
