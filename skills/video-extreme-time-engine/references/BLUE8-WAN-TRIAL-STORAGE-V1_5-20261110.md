# BLUE8 Wan驱动试运行与空间治理 V1.5

日期：2026-11-10（北京时间）。状态：PREPROCESS_EXECUTED / GENERATION_NOT_VERIFIED / FINAL_VALID=NO。

## 路线与已证事实
沿用[完整配套复审V1.4](../../../research/video/BLUE8-COMPLETE-STACK-AUDIT-V1_4-20261110.md)定位的作者Wan Animate Ultimate v2.0.0。选择Wan2.2 Animate GGUF＋SDPose＋面部视频分支，不混用Animate2。隔离ComfyUI v0.37.4，使用ComfyUI-GGUF；FP16/PyTorch attention适配SM75，不强套BF16/Sage2。
实际工程：`C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/BLUE8-PAIRING-20261110/WAN-TRIAL-20261110`。
新环境通过.pth复用`C:/AI/MiniMax-H3/.venv/Lib/site-packages`，UMT5引用Aaki已有模型。因此旧H3环境及Aaki编码器仍是活动依赖，清理前必须解除引用并验证，不能整目录删除。

本轮回读CURRENT.md、model-paths.yaml、主模型下载合同、prepare-events.jsonl、preprocess-review.json及service.log：
- 主GGUF=12349118272字节，官方SHA256=`2d9b55a17c2bb8eb18765e8ec10539113b080e029aa311d91d2b28e830f1dcc1`；事件记录已完成哈希认证及all_downloads_ready。不能继续沿旧聊天说仍在下载。
- SDPose、RTDETR、Turbo/Relight LoRA存在对应receipt；Wan2.1 VAE与CLIPvision已就位。资产就位不等于影片合格。
- 81帧预处理原生执行849.548秒（14:09:548），pose=748×1024/24fps/81帧，face=512×512/24fps/81帧；artistic_review=PENDING。不得把技术执行当画面审核通过。
- 目标仍为608×832、24fps、192帧、8秒，保留原声。Wan完整图采用193帧控制与末帧padding、最终裁192；不套H3的17n+5规则。
- 本轮尚未核实任何新扩散成片，不报告生成PASS或T_VALID。

## 已暴露的问题与成熟修正
1. 动态接口不能传嵌套字典冒充作者输入，按实际object_info与DynamicCombo使用点分字段映射；仅适配成熟接口，不改姿态或生成核心。
2. 缺websocket-client导致观察器无法启动；实际节点已注册仍不等于整套执行依赖齐全。
3. 多个下载器共写临时文件导致长度越界。一个资产只允许一个写入者，独立临时文件、固定revision/长度/官方SHA，全部通过才晋升正式模型。旧.download及.incomplete不加载。
4. 网络TLS错误按已验证传输方式接续；不得重复全量下载已有文件。完整失败/下载/配套/恢复时间计入总耗时。
5. RAM准入<80%，继承既有资源保护；正常进度不新增5分钟墙钟杀进程。CPU100%或初始化文字本身不能证明卡死。
6. 预处理完成后先检查首帧、偏头、嘴部覆盖和合手动作，再提交唯一短段；短段合格才扩8秒。原生queue/history/intent核账后接续，禁止盲目重投。

## 视频资产治理（用户本轮授权）
用户要求全面审计视频模型、工具、缓存、无效资料并清理，目标约75%。该目标是空间治理目标，不是强制删除有效资产的配额。
先列实际字节、活动进程、模型路径、环境共享依赖、正式结果与失败证据。分类：当前有效共享资产；已证明失败且无活动引用的残留；准确SHA重复；尚未验证候选。
删除失败传输前确认正式文件校验成功、旧下载器已退出、临时文件大小/mtime未变；保存清单和错误证据。完整模型不能仅因本任务质量未过就判全局无效。来源或用途未明的重资产优先移至非C盘隔离，保留映射与恢复办法，并与永久删除量分开报告。
技能、工作流、配置、原素材与小体积错误记录保留，去重整理入口；禁止靠删除经验与唯一素材凑75%。迁移或去重后检查被引用模型/依赖仍可解析，交付物仍需用户GUI路径验收。

## 接续
继续读取当前项目CURRENT与本轮空间清单，以实际native history为准。预处理视觉审查、81帧生成、完整8秒、播放器声画验收均未完成，不认证成熟生产配方。清理前后报告C盘实测可用空间、视频资产逻辑字节、实际回收字节和未达目标原因；硬链接不得按路径重复计入实际释放量。
