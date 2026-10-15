# H3 五帧最小验证冻结

方法：《三人行》第2版；Windows桥V6 C优先。

- 真实任务：d2989192-30e6-44ee-b117-926acb736d95，单次提交成功。
- 路线：IvenKooLab/minimax-h3-turing W4A8 i2v compat，4B ClipProj + Lightx2v Turbo4，无T8缓存；640×352、5帧、24FPS、原生音频。
- 全部依赖已SHA256核对通过；主模型Python整文件校验96.56秒，编码器25.43秒。
- ComfyUI history success；执行377.91秒，客户端至检测成功380.36秒。均不含下载和哈希校验。
- 日志：模型初始化149.22秒；随后采样进度计时约56.94秒。不能将该分段日志当作精确独立阶段性能。
- 实际输出5帧，640×352，24FPS，解出7个音频帧；视频长度约0.208秒。
- 视频SHA256：c3daaea1a6c35d0642d369e7ec6b132264a027e10c23ca8f10b22cc087a71ea9。
- 已实际查看全部5张解码图：第2、3帧明显模糊、重影，瓶身与篮子边缘不稳定；第1、4、5帧较清晰。场景及主要物体可辨识，手部有连续变化。

结论：真实生成→保存→解码→逐帧检查流程PASS；商业画质NOT_PASSED；约5秒视频300–400秒目标NOT_PROVEN。本次377.91秒是5帧冷启动测试，不是5秒视频成绩。

## 定位

Windows项目：C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015

桌面交付：C:/Users/A/Desktop/H3_5F_Test_20261015（MP4、decoded_frames、验收说明.txt、output-validation.json）。

证据：submit-receipt.json、generation-contract.json、history.json、generation-timing.json、output-validation.json、comfy.log、decoded_frames。

ComfyUI服务127.0.0.1:8196，已有模型缓存；任务已结束，勿重复提交原任务。下一阶段先核对成熟案例与当前精度/冷启动差异（本机日志manual cast float32），最小5帧处在节点支持范围但低于训练常见124帧范围。不要把5帧缺陷直接外推到124帧，也不要直接启动长视频。
