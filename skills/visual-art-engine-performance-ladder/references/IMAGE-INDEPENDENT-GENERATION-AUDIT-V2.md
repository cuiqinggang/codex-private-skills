# 图片独立生成证据与防伪验收规范 V2.0（强制）
状态：强制适用；2026-10-10 厨房照片案例；证据不足不得出图、不得输出“已通过”的技能运行成果。
适用：要求 ComfyUI 本机独立重新生成，而非原图图生图编辑的任务。不得擅自用 ChatGPT 图片工具、图像编辑或原图轻改替代 ComfyUI。

## 工作流合同冻结
- 必须先明确任务类型：独立生成 / img2img / 编辑，合同一经确定不得暗换。
- 本案必须使用已安装、经验证的 ComfyUI 成熟节点；空白 latent（EmptyLatentImage 或等效噪声起点）进行模型采样，参考图仅可进入 ControlNet/Canny/Depth 等条件支路。
- 禁止原图进入 VAEEncode→KSampler 低噪重绘分支；禁止直接把原图像素拷贝、贴图或修图后冒充新图。
- 生成前检查工作流拓扑和参数；不满足就不提交正式任务。

## 四道门（按顺序，不允许跳过）
G0 环境：ComfyUI API 可响应、模型/节点齐全；失败只报告故障，不得称为已生成。
G1 来源：冻结输入图 SHA256、正反提示词版本、workflow API JSON 及哈希，审计所有输入节点到最终 SaveImage 的有向路径，确保采样输入为 blank latent，参考图仅控制条件；若含违规直通路径则 FAIL。
G2 实际执行：保存真实 prompt_id、ComfyUI queue/history、服务执行日志（若可取得）、模型/ControlNet/LoRA、seed、steps、CFG、采样器、分辨率、输入与生成文件的 SHA256；history 的输出文件和落盘文件必须对应。没执行、记录不全或不一致一律 NO_VALID。
G3 视觉：必须从真实原图和真实生成图两份既存图片，以不调用生成式工具的常规像素拼接脚本制成左右大图，左原图右生成图，同尺寸展示不重绘、不美颜、不混合。肉眼一眼低品质直接 FAIL，禁止展示为通过成果；合格则记录已解决/未解决项目。

## 计时
只在 G0-G3 通过后比较完整端到端 T_total，包含结构预处理、模型采样、解码、保存；分离冷启动/热运行。不得使用 LoadImage→SaveImage 的毫秒值代替生成耗时。优化不改变任务合同。

## 证据包的最小不可变目录
- contract.md（任务类型、参考图/提示词版本、质量门槛）
- input.sha256、workflow_api.json、workflow.sha256、parameters.json
- submit.json（prompt_id、提交时间）、history.json、run-log.txt、output.sha256
- source_original.png、generated.png、comparison.png（comparison 程序化拼接）、comparison_manifest.json（两份源图文件哈希、尺寸、拼接规则）
- acceptance.md（每一道门的事实与证据路径、质量判断、时间、结论）
- 证据必须写到可供复核的固定位置，不能由没有文件的口头说明代替。

## 反造假要求
- 对比海报必须禁止 image_gen/扩散模型再生成；严禁用生成工具绘制“证据照片”。
- 截图、手写文案、图片旁文字不代替 ComfyUI API 与文件证据。
- prompt_id 与 history、输出文件一一对应；工作流拓扑静态审查不可替代运行证据。
- 不可保证绝对防欺诈：SHA256 证明文件一致性，不单独证明图片因果来源，必须进行多证据交叉一致性核查。
- 历史无证据结果记 INVALID，严禁无证据 PASS 或 FREEZE。

## 事故与状态
2026-10-10 先前展示的厨房照片来自 ChatGPT 图片工具，随后其“左右对比”再由生成模型绘制；没有合格的 ComfyUI prompt_id、history 和独立采样链路记录，撤销原先 PASS。禁止将这些照片作为有效性能基线。
冻结状态：COMFY_IMAGE_INDEPENDENT_GENERATION=NOT_YET_VERIFIED；FINAL_VALID=NO。只有完整证据通过时才改状态。
