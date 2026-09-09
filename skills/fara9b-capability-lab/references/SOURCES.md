# 编写时核验来源（2026-09-09）
- https://github.com/microsoft/fara/tree/a675d6d61c41c47ae87bacefeab22caad18e3e84
- https://github.com/microsoft/fara/blob/a675d6d61c41c47ae87bacefeab22caad18e3e84/pyproject.toml
- https://huggingface.co/microsoft/Fara1.5-9B
- https://learn.chatgpt.com/docs/computer-use
官方9B说明以浏览器截图为感知输入；官方CLI是可复用入口。源码Python最低3.10，模型推理依赖须另核验。
官方示例硬件不能证明用户2080Ti兼容；当前未在目标机测试。本包不承诺本机低时延，不预设原生桌面可用。
发布物是Codex执行协议与技能，不包含已测试的Windows安装器、模型权重或已完成的性能结果。
