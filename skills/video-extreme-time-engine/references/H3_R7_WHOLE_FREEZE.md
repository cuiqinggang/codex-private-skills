# H3 R7 整体虚拟成熟与唯一批次冻结
日期2026-10-16。目标在固定厨房640×352/124帧/24FPS/Turbo4合同下改善完整首次，保留热态成果与全部旧证据；用户授权继续成熟和必要实测。
## 新证据
R6在主模型创建阶段RAM96.4%，原生锁页政策未保护住32GB内存；不重复启用。ClipProjFree移回CPU而非销毁权重，不可当RAM释放；作用仅对resident注册表且dynamic并不一定在其中。Comfy RAMPressureCache跳过本轮all_outputs_dynamic，调cache-ram不能保证主动释放当前编码器。C盘Disk1 Great Wall GT6 1TB SATA，非NVMe，fast-disk不准入。
读取本机main.py、cli_args.py、model_management.py、model_patcher.py、caching.py、ClipProj节点/释放实现及固定Star7源码。main.py原生支持--disable-dynamic-vram，保留CoreModelPatcher=ModelPatcher；正常显存模式load_models_gpu在模型加载前按model_memory+extra_mem调用free_memory，对非dynamic模型实际卸载，再按容量部分加载。不是gpu-only/highvram。
## 全流程候选比较
A R4：首次469.167/热172.128保底。
B R5：首次490.504/热49.707，保留热态候选且同质量未认证。
C R7：R5完整图不变，R5服务命令只增加--disable-dynamic-vram；保留--disable-pinned-memory、reserve2.5/headroom0.5、原生异步2流。整体从按需分页转为原生估算和加载前卸载，覆盖编码器/主模型/VAE生命周期；不改变权重文件/LoRA/计算精度策略/注意力/步数/输出。
## 反例攻击后的取舍
1 resident编码器永久占显存影响后续采样：拒绝，不改ClipProj mode字段；全局传统调度生效时实际patcher为传统，字段名dynamic不等于真实分页路径，必须记录启动与加载日志。
2 全局锁页挤压RAM：保留禁用，R6不复用。
3 全驻留模型+激活越界：不设置highvram/gpu-only，保留原生部分加载及容量余量。W4A8主模型约12GB只是原观察，不把LoRA反量化峰值当已知可容纳。
4 丢失CUDA图/增多权重搬运：是实质可能，整套首次与热态都必须实测，不预加收益；若热态变慢分列，不宣称全面胜出。
5 LoRA常驻补丁可能改变量化路径与数值：保持既有保护层和标准LoRA原语，但输出仍需对照，不能默认同质量。
6 fast-disk、cache-ram、Free节点叠加：无净收益证据或释放对象不符，均不加入。
7 分段结果取最好拼接：禁止。只认新完整输出和服务器整段时间。启动另记，不隐藏预热。
## 准入与测试
基线文件哈希核对；空队列且内存<75%，单服务定向替换。R7独立日志/manifest/runner；启动必须节点注册且没有DynamicVRAM启用、没有Enabled pinned memory。不升级依赖，不改代理或其它项目。
从无节点缓存PREP seed3013，成功才MEASURE seed3014，各唯一prompt_id；900秒单任务上限，RAM>=94或RAM>=88且GPU<20持续30秒定向中断。不是断电冷启动，OS文件缓存不清。
原成熟runner复用，完整解码124帧、音频有限值、图像初验与同seed数值差异记录；同质量未证不晋级。监控脚本退出0不等业务成功。
首次对469.167与490.504；热态对172.128与49.707；不能只报局部改进。失败不试参、不提高保护阈值；归档后/free，清授权，恢复R4并检查空队列。
虚拟结论：R7有明确原生实现及生命周期差异支持，允许一次完整批次验证；不是已证更快，不是全局最优或物理极限。
