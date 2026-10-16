# H3第3版：SM75成熟完整路径与整体虚拟成熟（2026-10-17）
## 1 合同与真实起点
本机 RTX2080 Ti 22528MiB，MiniMax H3原R2 INT8 ConvRot、1024×576、5帧PNG、20步、seed3013。R2全程463.266秒，采样332.610秒。FirstBlockCache Safe完整203.797秒，采样106.297秒，日志缓存11/20步，五帧原尺寸人脸、手部、服饰、瀑布、时序人工核验未发现明显结构退化；质量不等于逐像素同轨迹。缓存版非采样部分=97.500秒（此处总时间与采样跨度口径来自已存C-result.json）。仅一次完整实际验收，非统计稳定值。
## 2 5090最快参考路径，不直接平移
开源 https://github.com/duckyshell/ComfyUI-MiniMaxH3-FirstBlockCache/blob/main/benchmark/BENCHMARK.md ：RTX5090、960×544、124帧5秒、20步、pruned INT8 ConvRot checkpoint、res_multistep，SageAttention2.2.0，热态（同shape重跑）。Sage无缓存57.958秒，Safe46.371秒（6/20缓存），Fast40.261秒（8/20），Aggressive37.277秒（10/20）；Sage Safe相对同后端无缓存约20%总时间下降。Native attention无缓存90.644秒，Fast60.819秒。作者Safe SSIM0.8216、PSNR25.80；Fast SSIM0.6873、PSNR22.09，与未缓存结果的像素距离，非感知绝对质量。
本机203.797/40.261=5.06倍全程；简单平均“每帧速度差”=(203.797/5)/(40.261/124)=125.54倍，但两者的5帧和124帧共享同一个高固定成本及不同的注意力token预算、GPU、模型/文本/VAEs/后端、冷热态，这个125倍不得称为真实算力或可实现加速缺口。
## 3 更匹配本机的成熟完整路径
开源 https://github.com/star7code/minimax-h3-chunk-star7/blob/main/BENCHMARKS.md 在RTX2080Ti 22GB、Windows、单参考图、H3 INT8 ConvRot、10秒约243帧1MP、Turbo LoRA4步的同一任务上：KJNodes SM75 SageAttention2=190.50秒/步；Comfy Kitchen INT8=119.50；SLA SM75 QK INT8 PV FP16=96.68；SLA SM75 all INT8=60.83；Sol SM75 all INT8=88.71。SLA all INT8速度对CK约1.96倍，但作者指出旧版all INT8有可见/音频误差；修复后单任务视频音频样本通过，但质量跨seed仍需验收。R5 Chunk本机高清实测采样339.344秒对比原R2 332.610秒，并无采样提速，因此不能把分块算作速度收益。Star7全INT8注意力与FirstBlockCache的跨步缓存针对不同计算层，但模型补丁/attention hook、音频guard、算子输入布局、退化补丁行为尚需源码兼容核验。SageAttention2在2080Ti上反而更慢，不能机械复制5090路线。
## 4 第一性原理和严谨时间界限
同一次5帧缓存完整时间T=203.797=106.297采样+97.500非采样。若**不改变非采样部分**，即使将采样全部归零，T也不可能低于97.5秒；整任务最大进一步比值是2.09倍。100倍整体加速必须把已存在的97.5秒加载/条件/VAE也整体改变，不可能靠单换attention或再加缓存实现。
Amdahl模型：假设采样106.297秒中，注意力份额f，注意力内核加速倍数r，且额外开销h，则T=97.5+106.297×(1-f+f/r)+h。本机f、r未知。即使r=1.96且f=1（不合理极限），h=0，T约151.73秒；f=0.5则约177.76秒；f=0.3则约188.17秒。不是实际预测，只用于筛选收益空间。若改变后端引起缓存命中下降，净收益甚至可能为负。
真正20步的约100倍“每帧差距”错误在于当作124个彼此独立生成的一帧；H3打包联合推理，token数和f不同，各帧不单独跑一遍50块×20步。
## 5 三种候选和整体虚拟成熟
A（生产基线）：R2 INT8 + FirstBlockCache Safe 阈值0.08，20步，已有端到端203.797s、质量本例PASS、缓存11/20，单样本已冻结。不得在还没有净收益证据时降级为未使用缓存的方案。
B（当前最大净收益挑战者）：保持A所有质量、时间和模型合同不变，研究是否仅将attention后端从CK INT8替换为Star7已在SM75测试的SLA SM75 QK INT8/PV FP16（质量保守）或all INT8（性能更激进）。注意当前8197插件白名单不含Star7 chunk，需要审计其attention安装机制：是否能在不启用chunk、不覆写FBCache的double_block patch、不触发降精度其他节点行为情况下单独应用。检查SM75 CUDA核、音频guard、缓存命中变化、代码插入顺序、额外显存、官方原图视效门；不兼容则STOP，不能独立将SLA内核时间改善乘到A的墙钟数据上。
C（独立备选）：A缓存保持Safe，优化模型冷/热驻留及条件编码合法复用，守护式卸载、避免重复初始化、内存分配、VAE延迟约束；必须记录初次任务全量成本，不能把热态数字冒充首单完整耗时。若缓存换成Fast/Aggressive以追求速度，现有Safe画质合同不可直接继承，需重新审查轨迹漂移，暂不晋级。
虚拟淘汰：5090的Sage整栈照搬SM75=反例不通过；仅R5激活分块追速度=已实证采样慢；240帧/4步Turbo成绩与5帧/20步合同混比较=停止；原生缓存加TeaCache叠用=生命周期/数值冲突风险，停止。
## 6 冻结与Reality门
SOURCE_AND_THEORY=PASS；CURRENT_A_PRODUCTION_FOR_TESTED_CONTRACT=YES；B_RISK_AUDIT=INCOMPLETE；C_TIME_LEDGER=INCOMPLETE；BEST_TIME_GLOBAL=UNKNOWN；NEW_GPU_RUNS=0。
下一合法动作：先静态审查已在本地部署Star7的SM75 attention patch安装位置与FirstBlockCache的double_block hook冲突，再形成唯一可比B候选；Freeze后只有一次单任务实际验收且需通过原样本五帧原尺寸质量和显存/时间守护。首选C通道，未经权威V9映射/健康核验不得把GPT-Windows-MCP-Bridge工具名当成C通道已证实。
