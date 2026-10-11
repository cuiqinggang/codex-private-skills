# 图像生成来源真实性与防作弊执行门禁 V3.0（2026-10-11）
状态：强制适用；适用于本技能接管的所有本地 ComfyUI／Krea 文生图、图生图、参考条件生成、编辑、局部修复及前后对比；取代 V2 的含糊任务分类部分，保留 V2 对独立生成的更严格源头约束。

## 0. 核心：工具选错立即终止，不能事后贴证据
- 用户指定“本机 ComfyUI／Krea／现有图像技能包／Windows 上生成或修复并出具完整来源证据”时，先锁定 `BACKEND=COMFYUI_LOCAL`。**这是工具选择前置门，不是生成完成后才看的审计说明。**
- 在该任务下，任何 ChatGPT `image_gen`／其他托管图片生成器、直接编辑或再生成的“对比海报”，均**不属于允许的正式执行路径**。不得通过它们生成正式成品、补全缺失文件、生成所谓审计对比图。看不到 ComfyUI 工具、远程设备离线或费用不足时：`BLOCKED` 或 `UNKNOWN`，不私自切换供应商。
- 用户明确改变生成后端时，必须先说明原合同已变化，建立新 TASK／新生成合同并重新计时和验收；绝不将不同后端作品沿用旧任务的 ComfyUI 认证。
- 若本轮已误调用 `image_gen`，立即记录 `ROUTE_VIOLATION=YES; RESULT=INVALID; FINAL_VALID=NO`。可以展示违规事故的原始事实用于说明，但**不可标记为经本技能生成或修复的正式作品**；也不得再调用 image_gen 伪造原图／修复图对比以“补救”。
- 与 GPT 的其他一般图片创作任务并不冲突：没有锁定 `BACKEND=COMFYUI_LOCAL` 时，可以在用户授权的其他工作流里使用相应工具，但不得声称符合本技能的 ComfyUI 证据合同。

## 1. 生成前强制锁定合同（G-1）
保存 `contract.md`，至少记载：
`TASK_ID`、`BACKEND`、`MODE`、`MODEL`、`PROMPT_VERSION`、`SOURCE_FILE_SHA256`（无来源记 NONE）、`OUTPUT_CRITERIA`、`COMP_REF`、`TOOL_ALLOWLIST`、`DENYLIST`、`STATUS`。
`MODE` 仅四种：
1. `T2I_INDEPENDENT`：纯文本与独立噪声采样；禁止图像文件输入、VAEEncode、ReferenceLatent 或参考图经 ControlNet 支路进入采样。
2. `REF_CONDITIONED`：原始图仅经明确的成熟参考条件、Depth、Canny、ControlNet、ReferenceLatent 支路使用；可从空白噪声采样；必须逐路径说明哪些条件进模型。不得声称“不参考原图”。
3. `IMG2IMG`：明确允许 `LoadImage → VAEEncode → KSampler` 或等价低噪重绘；明确记录 denoise 强度，禁止称其为独立文生图。
4. `EDIT/INPAINT`：允许经成熟编辑／遮罩／局部重绘流程修改指定输入图；保存输入图、遮罩（若有）、编辑范围，禁止把编辑作品称为完全独立创作。
未明确 `MODE` 不提交；不能为迎合某审计规则悄悄从 IMG2IMG 改成 T2I。

## 2. 执行前 G0／G1：真实节点与全链路拓扑
- G0：本机 ComfyUI API 健康、模型/编码器/VAE/所需节点真实可用；核对正式模型权重（必要时校验发布 SHA），记录服务位置及失败原因。
- G1：从正式官方模板／已验收成熟流程取得工作流；冻结 `workflow_api.json` 和 SHA256；逐节点审计源图片加载／潜空间来源／条件输入／采样器／VAE 解码／SaveImage 的可达关系，查明用户图是生成条件还是对比材料；用 JSON 与实际配置做判断，不使用自然语言保证替代拓扑检查。
- 对 `T2I_INDEPENDENT`，要求 `KSampler.latent_image` 可追踪到 EmptySD3LatentImage 或等价空白潜空间，且采样图像路径不含 LoadImage／VAEEncode／ReferenceLatent／ControlNet 输入；参考图只留在**生成结束后**的对照材料中。
- 对 `REF_CONDITIONED`、`IMG2IMG`、`EDIT/INPAINT`，相应的参考条件／编码／遮罩路径必须与合同完全一致，不能过审时假称 T2I。
- 缺少 G0 或 G1：`NO_SUBMIT`。不能以“模型选择正确”“服务端 HTTP 200”“官方教程截图”代替。

## 3. G2：一次真实执行的可核验证据，不可拼接不同运行
- ComfyUI 原生 `POST /prompt` 返回的 `prompt_id`、提交时间、`node_errors`，队列／history 的相同 `prompt_id`，`status_str=success`、`completed=true`，history 对应的完整 workflow 与 `workflow_api.json` 的采样相关字段必须一致。
- 保存 `submit.json`、原始 `history.json`、`run-log.txt`（可取得时的服务日志）、`parameters.json`、`input.sha256`、`workflow.sha256`、`output.sha256`；落盘真实 PNG 文件须与 history SaveImage 输出同名或保存有明确的原始文件到复制件的映射和 SHA 一致。
- 重新读取 history 核对 `prompt_id`、工作流节点、seed、模型、steps、CFG、分辨率、采样器、denoise、输入文件标识、输出文件名。缺关键项时记 `UNKNOWN` 或 `INVALID`，不杜撰填充。
- `prompt_id` 来自 ChatGPT `image_gen` 的 `gen_id` **绝不等价**，PNG、截图、文件 SHA、命名或两图像素差异也不能单独证明因果来源。
- 一旦任务提交后出现桥离线、响应超时或结果不明：`UNKNOWN`；只读取旧任务历史并对账，禁止在不明状态盲重发（Exactly-once）。
- 计时全程按相同 VALID 合同，错误图片不记有效最短时间；不得移植另一模型／模式的结果为当前方案成绩。

## 4. G3：真实输出的品质／合同审查及不可生成式对比
- 必须检查合同中的物体数量与位置、玻璃透明与金属结构、手部解剖、手与勺的接触/穿模、食物健康状态、摄影曝光／光影、构图、分辨率／锐度/纹理。手指与木勺融合、缺玻璃瓶、腐坏南瓜、乱码文字等是**真实缺陷**，不能只用“像素清晰”判 PASS。
- 左右对比 **只允许** 读取两张已存在的原始文件，再用 Pillow、ImageMagick 或同等非生成式像素操作（可记录的尺寸适配＋直接 paste）制作。保存 `comparison_manifest.json`，包括两输入完整路径、SHA256、尺寸、缩放裁切规则、比较图 SHA256。不得调用 image_gen 重新画“原图 vs 修复图”；展示一个画得很像的海报不属于合规证据。
- 对图像变化／相似性指标：不以“哈希不同”推断生成独立、不以 MAE 大推断画质好，也不以 MAE 小推断作弊；只使用真实拓扑＋真实历史＋原始文件交叉核验。
- 可以展示失败图片，但必须明确 `QUALITY_FAIL` 或 `INVALID`，绝不能标记为正式成功作品；用户要求最终高质量时须坚持 `FINAL_VALID=NO` 直到所有条款达标。
- 高分辨率升级不得替代结构修复；有高质量基础图时优先成熟局部 inpaint／编辑，实际修复后检查其它位置的回归缺陷；更换模型或策略必须区分新的生成任务，不回填旧任务的执行历史。

## 5. G4：认证发布前的“第二次只读复核”
在发布正式结果/写入技能成绩前，优先由独立只读路径（重新读取 ComfyUI `/history/{prompt_id}` 与 Windows 落盘文件）进行交叉复核；如果无法访问，标记 `AUDIT_STATUS=UNVERIFIED` 并只报告已得到的证据，不能制造第二来源。
输出报告必须有：
`BACKEND`、`MODE`、`PROMPT_ID`、`MODEL`、`WORKFLOW_SHA256`、`SOURCE_SHA256`、`OUTPUT_SHA256`、`HISTORY_STATUS`、`G-1/G0/G1/G2/G3/G4`、`QUALITY_ISSUES`、`T_VALID`（没有则 UNKNOWN）、`FINAL_VALID`。
没有原生证据的“下一页已执行”、由用户转述成功、只看图、只读聊天摘要都不得自动升级 PASS。

## 6. 证据包与版本层的生效定义
每次正式出图的目录至少包含：
`contract.md`、`input.sha256`、`workflow_api.json`、`workflow.sha256`、`parameters.json`、`submit.json`、`history.json`、`run-log.txt`（可取得则保存，不可取得写 UNKNOWN）、`source_original.png`（若有）、`generated.png`、`output.sha256`、`comparison.png`（若要求）、`comparison_manifest.json`（若要求）、`acceptance.md`。
必须将失败工件与成功工件分开保留，不允许在同一路径覆盖失败证据，不能将工具结果当作用户实际授权第三方的发送许可。

**重要能力边界**：技能文件中的文字无法物理阻止模型调用不合规工具，也不能单独保证防作弊。可验证的改进是“默认阻断认证／强制追溯／产生可审计失败”；若要硬性执行层禁止，还必须由支持该能力的运行器或宿主工具路由实行真正的 allowlist/denylist。不得将文档更新冒充平台级硬拦截。

## 7. 本轮违规回归用例（必须在后续测试覆盖）
- R-A：用户要求 ComfyUI，本轮调用 image_gen 产出 PNG → `ROUTE_VIOLATION`，不认可成功。
- R-B：用户要求纯文生图，工作流含 VAEEncode／ReferenceLatent → `MODE_MISMATCH`，不认可独立生成。
- R-C：只有 PNG 和 `gen_id`，没有真实 ComfyUI history → `G2_FAIL`。
- R-D：ComfyUI 图片是合法的，但左右对比海报由生成模型重绘 → `G3_COMPARE_INVALID`。
- R-E：提示词或模型声称修复手指/玻璃瓶，实际图仍手勺粘连或缺物品 → `QUALITY_FAIL`。
- R-F：桥断联且旧 `prompt_id` 结果不明 → `UNKNOWN`，禁止自动重复提交。
- R-G：型号、workflow、history、输出文件 SHA 有一项与本轮不符 → `PROVENANCE_MISMATCH`。
以上属于方法回归清单；真实跨会话执行效果尚需实际生产验证，不得把文档编写误称为回归测试通过。

## 8. 与旧规范和其他正式方法的关系
继续继承 `IMAGE-INDEPENDENT-GENERATION-AUDIT-V2.md` 的独立生成证据字段与最小证据包；V3 优先适用于模式区分、ChatGPT 工具越界、只读复核、防伪对比及错误状态报告。第28版自动化极限短时间引擎、其 REUSE_GATE／Freeze／Reality 边界、P0 性能测量规范与 H3 能力合同不因本 V3 自行改变。
