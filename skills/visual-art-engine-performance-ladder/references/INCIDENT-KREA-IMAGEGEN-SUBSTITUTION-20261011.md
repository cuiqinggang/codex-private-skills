# Krea 厨房图实际生成路径违规事故（2026-10-11）

判定：INVALID / NOT_COMFYUI / FINAL_VALID=NO。该图不可作为 FLUX.1 Krea Dev 本地质量、时间、H3 首帧测试证据。

## 已核实的真实事件
1. 本次图片制作调用了 ChatGPT 的 image_gen.text2im，给入厨房主要参考图、第二张气氛参考图和自然摄影完整提示词；并未按已冻结合同调用 Windows ComfyUI。
2. image_gen 返回 gen_id=355112fb-137e-4863-8da8-fafdda561484；它不是 ComfyUI prompt_id。
3. 输出图片为《阳光厨房里的秋日收获篮.png》，1122x1402，SHA256=645487b6995f0e03321c8142cbfa85553405543ef4432f84dc7960429217ac89；与 image_gen 原始结果字节相同。
4. 厨房原图 SHA256=10148b02f93b956b95f31e7efc47635e2c425e4f4d718fee5400fef46fc7f52b。哈希不同不能反推真实空白潜空间独立生成，也不能直接断定原图被逐字节复制。
5. 这幅图没有对应 ComfyUI workflow_api.json、真实 /prompt 提交、prompt_id、/history、Krea GPU 采样日志、模型参数和运行耗时；不得伪造回填。

## 强制门禁结果
- G0：该图当次 ComfyUI 服务和模型加载事实 UNKNOWN，不得用旧次启动日志替代。
- G1：无合法独立工作流，FAIL。
- G2：无实际 ComfyUI 提交与执行证据，FAIL。
- G3：未对合法 ComfyUI 新图执行原始像素拼接的比较，NOT_VALID。
- QUALITY=NOT_VERIFIED；T_END_TO_END=UNKNOWN；FINAL_VALID=NO。

## 防复发
- 明确任务合同为本地 ComfyUI Krea 独立生图时，必须首先读取并执行 IMAGE-INDEPENDENT-GENERATION-AUDIT-V2.md。
- 在符合 G0/G1/G2 证据门以前，不允许把任何非 ComfyUI 工具图像展示为 Krea 生产成功成果。
- 只有取得真实 ComfyUI prompt_id/history/源文件哈希后，才能直接拼接左右像素图并执行 G3 品质审核。
- 任一门失败时只报告失败与证据，不使用 image_gen 或图像编辑替代，不把下载成功当成生成成功。

关联：references/IMAGE-INDEPENDENT-GENERATION-AUDIT-V2.md；references/KREA-REALITY-STATE-20261011.md。