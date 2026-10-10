# 高品质图片与 H3 视频：选型记录 V1

## 当前选型
FLUX.1 Krea Dev FP8 Scaled 作为唯一优先研究候选。选择它是因为官方作品强调自然摄影细节，并有正式 ComfyUI 工作流；目前未在本机完成该模型的实际生图验收。Juggernaut XL v9 保留为成熟写实备选；FLUX.2 Klein 4B 保留为快速、Apache 2.0 许可备选，均不同时部署。

## 技术来源
- Krea 官方教程：https://docs.comfy.org/tutorials/flux/flux1-krea-dev
- 工作流：https://github.com/Comfy-Org/workflow_templates/blob/main/templates/flux1_krea_dev.json
- FP8 权重：https://huggingface.co/Comfy-Org/FLUX.1-Krea-dev_ComfyUI
- Juggernaut：https://huggingface.co/RunDiffusion/Juggernaut-XL-v9
- Klein：https://docs.comfy.org/zh-CN/tutorials/flux/flux-2-klein

## 本机条件
RTX 2080 Ti（报告 22528 MiB 显存）、32GB RAM；C 盘曾检测剩余约 324GB。已安装 CLIP-L、T5 FP8、ae VAE；Krea 主模型尚未证实安装。优先复用原有 ComfyUI，不修改网络代理、系统或健康环境。

## 许可证
官方 Krea 属于 FLUX dev 非商业、非生产许可。个人研究、测试可作为用途；不收费不等于公开运营自动获准。使用模型与生成内容后续利用是不同授权层次；公开发布及潜在商业活动前须另行审查。
权威条款：https://bfl.ai/legal/non-commercial-license-terms

## 验收与视频衔接
严格遵守 IMAGE-INDEPENDENT-GENERATION-AUDIT-V2.md。先使用官方工作流空白潜空间独立文生图，分别验证厨房静物与多人物生活摄影；保留 prompt_id、history、模型、SHA256、原图左/生成图右真实像素拼接大图。品质不通过不进入速度冠军评选。后续通过 MiniMax H3 首帧与实际视频验收，终极时间指标为有效成片端到端时间。

## 状态
MODEL_SELECTION=KREA_FIRST；DEPLOYMENT=NOT_VERIFIED；IMAGE_QUALITY=NOT_VERIFIED；H3_VALID=NOT_VERIFIED。不得将选型理解为正式品质冻结。


## 对比判断依据（可复核）
| 模型 | 核心能力证据 | 本机技术及资源 | 授权 | 定位 |
| --- | --- | --- | --- | --- |
| Krea Dev FP8 Scaled | 官方 12B 摄影美学模型；ComfyUI 完整模板；支持 FLUX.1 dev 结构 | FP8 主文件 11.9GB，现有 T5-FP8、CLIP-L、ae 可复用；RTX 2080 Ti 计算能力 7.5 无原生 FP8 推理加速 | 免费权重只限非商业/非生产 | 唯一高品质优先研究候选 |
| Juggernaut XL v9 | RunDiffusion SDXL 真实摄影专用模型，官方卡报告大规模长期社区使用 | 单权重约 7.11GB；官方建议 30–40 步，兼容多种 SDXL 控制工具 | CreativeML Open RAIL-M，付费 API 服务另需联系授权方 | 成熟写实后备，不安装 |
| FLUX.2 Klein 4B | 官方低延迟文生图及参考编辑，4 步蒸馏 | 官方报告约 8.4GB 显存（速度样例是 RTX5090，不是本机），32GB RAM 足够做研究的可能性高 | Apache 2.0；适合明确商业批量路径 | 速度与开放许可后备，不安装 |

官方模型卡与许可证：
- https://huggingface.co/RunDiffusion/Juggernaut-XL-v9
- https://huggingface.co/black-forest-labs/FLUX.2-klein-4B
- https://huggingface.co/black-forest-labs/FLUX.1-Krea-dev
- https://bfl.ai/legal/non-commercial-license-terms

## 硬件与文件证据的边界
本机核实：C: 剩余约 323.99GB；Krea 官方权重远端 HTTP 200，大小 11904639672 字节；文件官方 SHA256 为 b17a8c21703c4d6ffb0e300dd920eff3cfd35c9a72a1abaf107e3788e408b8d8。只有下载完整且本地哈希一致才允许标记 MODEL_INSTALLED=YES。T5 编码器及 VAE 既存只证明文件存在，不替代加载及采样证据。模型需要内存卸载或精度转换时实测速度会降低，不允许移植 RTX5090 的速度数字。

## 两个固定视觉验收场景
厨房：午后自然阳光，手持铁艺果篮、两枚橙子、健康的浅色条纹小南瓜、玻璃瓶、木勺和条纹棉麻布，环境朴素、真实、不塑料。
三人家庭：三个人物的肤质、面部、手指、互动触碰自然，表情可信，不要 AI 概念摄影或不稳定的人体结构。
两者均不是要求像素级复制样板，而是同等级摄影艺术品质。左右对比图只能对两份已存在的源文件做程序拼接，严格禁止用生图模型再造“验收图”。

## MiniMax H3 后续视频关卡
图片成为合格 H3 首帧，尚需验证：画幅匹配最终成片、运动空间、物体/身体接触合理、人物身份跨帧稳定、成片效果达到高品质；不能以单张图片漂亮推断 H3 成片必然合格。最终效率指标是合格成片的总耗时，而不是单张显卡推理时间。官方 H3 输入和平台条款随版本变化，执行前重读该服务当时的官方说明。

## 许可中的生产用途提醒
本人说明“不以直接盈利为目的”，作为本次私人研究的用途信息，而不是商业/公开使用的全面授权证明。BFL 2025-11-25 许可证 v2.0 明列个人研究、实验和业余项目；也列出营收性或影响最终用户的使用可能不属于允许的非商业用途。将来抖音、微信、YouTube 等平台公发或变现之前复审模型权重使用权和输出审查、AI 披露要求。此处只是对官方条款的归纳，不是法律保证。

## 成熟方案优先与回退
不安装三套，不新写模型；仅调用 ComfyUI 官方 Krea 模板及既有 ComfyUI 节点。若模型安装、静态拓扑、实际采样、品质或 H3 关卡失败，事实记录为 FAIL，不得把选择偏好升级为成功结论；必要时再启用成熟后备方案。禁止用 ImageGen 图像替代本地 ComfyUI 图像作证据。
