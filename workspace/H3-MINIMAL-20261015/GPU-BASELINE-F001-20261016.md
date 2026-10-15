# H3 GPU成熟基线与暂停规则 F001

Freeze ID：H3-GPU-BASELINE-F001-20261016
日期：2026-10-16（北京时间）
方法：用户指定《三人行》V2 C002；连接桥V7，C唯一日常入口、A暂停。
状态：方法/配置防漂移已冻结；生成暂停；资源瓶颈根因未完全确认；目标质量和400秒均未通过；物理极限UNKNOWN。

## 承认并纠正的执行偏差
此前出现系统响应变慢、GPU低利用率和明显页面读入后，仍继续跑完，异常停止纪律不足。低分辨率热缓存成绩又被拿来与新输入高分辨率比较，比较口径不一致。核对旧GOOD与新BAD合同，主模型、编码器、VAE、LoRA、4步采样与启动参数没有变成CPU方案；不能将CPU内存89%或单次GPU4–11%直接等同于CPU推理。

## 固定成熟基线
来源：https://github.com/IvenKooLab/minimax-h3-turing ，同2080Ti22G的W4A8兼容成片路线。
- CUDA cuda:0；torch2.9.1+cu130；comfy-kitchen原生CUDA量化算子；W4A8 mixed主模型；Qwen4B ClipProj；Turbo4；simple/res_multistep；原生视频/音频VAE。
- 既有启动参数保留：--reserve-vram 2.5 --vram-headroom 0.5 --disable-pinned-memory；只允许ComfyUI-ClipProj自定义节点。
- 不为追求GPU利用率强制gpu-only、全局FP16、T8、减少步数或擅改模型。FP32计算dtype不等同于CPU设备。
- 单卡串行，不新启第二服务；服务地址127.0.0.1:8196。
- 640×352/124帧只作诊断基线。目标清晰度、作者LMS工作流与分镜是独立未通过门；不能把降质当提速成功。
- 同一质量合同固定图片、提示词、种子、尺寸、帧数、模型、步数、缓存边界和音频范围。新图片/新条件与同条件热缓存分别计时；禁止只报最快样本。

## 资源异常处理规则
先只读检查任务队列、实际CUDA路径、可用内存及系统响应；检查运行阶段，不能要求加载/保存期间GPU永远满载。若出现用户可感的卡顿并伴随持续页面读入/低GPU进展，停止新增任务；当前任务只通过既有ComfyUI接口受控中断并保存证据，不等到整体长超时。仅在确认空队列时使用官方/free释放本项目模型/条件缓存；不关闭浏览器或其他项目，不改代理、FlClash、杀毒、分页文件或Windows全局设置。
本规则是操作合同；尚未实现并验证实时自动资源监控，因此恢复生成前须冻结具体观测与中断计划，不能宣称自动防卡死已经认证。

## 本次已实际完成
- 空队列确认后，官方POST /free {unload_models:true,free_memory:true} 返回200；8秒后系统RAM占用88.1%→72.0%，可用内存4098674688→9600507904字节；GPU显存16347→2170MiB。没有重启服务，条件缓存已清空，下一次属于重新加载，不能叫热运行。
- 现有run_reference_once.py、benchmark_warm.py、run_5f_once.py增加GPU-BASELINE-LOCK.json检查：缺锁失败；generation_allowed=false时生成前退出；允许执行时核对冻结文件SHA。三个入口暂停负例3/3通过，未提交视频。
- 备份保留为原脚本名.before-F001。约束覆盖这三个入口，不是平台/API全局禁令；禁止内存改写脚本绕过暂停。

## 未解决与下一步
保持generation_allowed=false，先定位条件编码/模型加载的资源等待并核对官方成熟内存生命周期；内存释放只能证明闲置资源回收，不能证明根因已修复。完成整体候选虚拟审查、同质量合同与观测/中断方案后，再更新任务锁并进行一次Reality。不得恢复逐点盲跑。
旧结果：厨房首次567.177秒；厨房热缓存274.657/323.263秒；原片1024×576为1473.885秒；原片640×352对照838.265秒。末次prompt_id=36e2f816-8b04-4db2-b7b8-b03bc5b086ff已完成，不重发。

## 本机定位与完整锁
项目C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015；GPU-BASELINE-LOCK.json、GPU-BASELINE-GUARD-RESULT.json、RESOURCE-RELEASE-20261016.json。

```json
{
  "policy": {
    "freeze_id": "H3-GPU-BASELINE-F001-20261016",
    "status": "HOLD_RESOURCE_DIAGNOSIS",
    "generation_allowed": false,
    "method": "SANRENXING_V2_C002",
    "bridge": "V7_C_ONLY_A_PAUSED",
    "comfy_commit": "8a33128f2f8c5585c57486c07de481241e70a39c",
    "files_sha256": {
      "launch_comfy.py": "4e6d426befdf1d7c81d760e95b15a83c1c02167d875b78846789b7a6565c43eb",
      "workflow_5f_api.json": "fbaf87d4304d349803f3dab278243c2f9e992a9eb513a5822c5b492ebd52a448",
      "workflow_reference_api.json": "40834830c435edb3ae9955c4c70fc37afa07e4a332b606eec1ecd5a7fbb1049c",
      "extra_model_paths.yaml": "8abb615373224f9837d5e801bd088ec1c7d7c0555011bdd2f0725f8a90f76f4c"
    },
    "route": "cuda:0 / native comfy-kitchen cu130 / W4A8 mixed / Qwen4B ClipProj / Turbo4 / simple+res_multistep / native audio",
    "precision": "existing default; FP32 fallback on sm75 is not proof of CPU compute; no forced FP16 or gpu-only",
    "quality_status": "TARGET_NOT_PASSED",
    "resume_requires": "Diagnose conditioning/loading wait, restore responsive resource state, freeze complete same-quality contract and observation/abort plan; no blind rerun; no treating warm cache as fresh-input timing"
  },
  "guards": [
    {
      "file": "run_reference_once.py",
      "sha256": "c8630a72e18b5d5517c88b421b62200750b38ad186d62c179f1f990d8a1e1de2",
      "hold_test": "PASS_NO_SUBMISSION"
    },
    {
      "file": "benchmark_warm.py",
      "sha256": "e544c02df226d3d189b9e483e3c339a2e63dce440e1cf9ab059845ad7efbf90a",
      "hold_test": "PASS_NO_SUBMISSION"
    },
    {
      "file": "run_5f_once.py",
      "sha256": "081f632c7acbb2c2b6bc211325dc79183f38c8871678c8db9c79a0eaa9e88a77",
      "hold_test": "PASS_NO_SUBMISSION"
    }
  ]
}
```
