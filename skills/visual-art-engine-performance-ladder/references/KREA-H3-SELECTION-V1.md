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
