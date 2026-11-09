# FASHN官方第一个静态换装案例：直接复现与重复

## 已测范围

复用FASHN VTON v1.5官方Space第一个镜前自拍换红裙案例。2026-11-08在本机连续两次使用原CLI完成；整图和脸/手机、左手/裙摆、红裙细节与官方对应展示相近，正常观看未见明显穿帮。未改源码、未修图、未换种子。输出576×823，不作视频换装、双人对白、古装片、新人新衣迁移或商用整体交付认证。

## 固定原资料

- 代码：https://github.com/fashn-AI/fashn-vton-1.5/tree/7c0f10af3f91ad4048fe9729c470a13ef905d25a
- Space输入/参数：https://huggingface.co/spaces/fashn-ai/fashn-vton-1.5/blob/1c49e7328d65aab0b784637275dbe17d4c0fa1b3/app.py
- 输入：assets/examples/person1.png、garment1.jpeg。两者SHA256分别为9c425d154d7bea584b4060e7e1ed28cd676e3f9ea3c475b922e986d04a48d273、8681fc59b1a7204144d9724840ed52b2a6174611a49abb20b57a3552d7d3cc84。
- 对应公开成品：https://static.fashn.ai/repositories/fashn-vton-v15/hero/concat_1.webp （官方研究页同图）；该展示图未单独披露生成种子，不声称逐像素复刻展示图。
- 主模型：https://huggingface.co/fashn-ai/fashn-vton-1.5/tree/7720683168567eb5a2a4c67f15116c6e29c83ded 。model.safetensors SHA256 d6cd38286885bc29fa487ea9383f80ffeb95862e7747c630d42c5d3c05bdd35a，与发布LFS摘要核对一致。
- DWPose版本548b5df25b84d9f4aac0611dfa1c2a7a12f15571；人物解析权重版本1f80c34dbab321c5730dda5c3fea279fd3e97498。完整哈希见本机additional-weights-manifest.json。

## 本机现有执行入口

项目根目录：C:\AI\Video-Recipe-Reproduction-20261108\FASHN-Official-R1。

复用C:\AI\MiniMax-H3\.venv\Scripts\python.exe：Python3.11.15、Torch2.9.1+cu130、torchvision0.24.1+cu130、transformers5.16.1、HFHub1.29.0、safetensors0.8.0、numpy2.4.6、Pillow12.3.0。RTX2080Ti，22528MiB。缺失依赖放在任务deps，不改原Torch环境。

已实测新增依赖：fashn-human-parser0.1.1、onnxruntime1.31.1（CPU姿态检测）、opencv-python5.0.0.93、matplotlib3.11.2及其解析出的依赖。具体列表见environment-record.json和resolved-replay-requirements.txt。

调用时设置进程PYTHONPATH为任务deps及upstream\src，HF_HOME为任务hf-cache，再执行upstream\examples\basic_inference.py。固定参数：

| 参数 | 值 |
|---|---|
| person-image | inputs\person1.png |
| garment-image | inputs\garment1.jpeg |
| category | one-pieces |
| garment-photo-type | model |
| num-timesteps | 50 |
| guidance-scale | 1.5 |
| seed | 42 |
| segmentation_free | True（不加--no-segmentation-free） |
| num-samples | 1 |

50步来自在线演示默认；CLI默认30步，必须显式传50。作者原程序在该Torch版本下选择BF16，记录实际行为，不将README的旧显卡FP32描述冒充实测。CPU ONNX提示CUDAExecutionProvider不可用后正常回落CPU；主生成使用CUDA。

## 两次证据

第一次run-R1-result.json：原CLI完整调用07:20:334，含首次人物解析权重下载；采样约04:59。第二次run-R2-result.json：05:11:605，采样约04:25。未将两次生成调用时间冒充前序检索下载安装与后序审核归档的完整T_VALID。

output-R1\output_00.png及output-R2\output_00.png均465081字节，SHA256同为460b715ecf96d8c35371a864f8c2bc1ccac715e3f4ea1e6bc1b87b1356e1fbbe。repeat-output-check.json记录原生文件字节一致、像素一致；两次均已从本机取得并核对。

复用run_original_R1.py或文档FASHN-Replay-Recipe.md中的原CLI，只换新的输出目录，保留既有结果。断线先查run-R*-result.json、日志与同一输出，不自动重投。无助手添加的任务总时限，保留原资源保护。

首次环境无pip时，使用已有MuseTalk环境的pip --python指向H3解释器，先dry-run，再将缺少的锁定依赖装到任务deps。该接入已完成；以后勿重装健康环境或重下模型。

资料总记录：https://chatgpt.com/library?file_id=libfile_fde3_f-12d10efbb39c819190b0c36ca84565bd_937029f1505c8191917e0968911c47f5&account_id=personal

详细复用配方：https://chatgpt.com/library?file_id=libfile_fde3_f-667a43def9ac81919b5e3a0b4c23b7e4_937029f1505c8191917e0968911c47f5&account_id=personal

原素材/官方成品/本机结果对照：https://chatgpt.com/library?file_id=libfile_fde3_f-c42f5015b3ec8191be583aed8c541b80_937029f1505c8191917e0968911c47f5&account_id=personal

该结果证明原案例可直接完成并重复，不证明其他案例成功率。迁移需求先找同类已合格案例与原配方，再验证，不围绕失败样片发明新修补链。
