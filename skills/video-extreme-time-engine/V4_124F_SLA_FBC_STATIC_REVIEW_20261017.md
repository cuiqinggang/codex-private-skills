# V4 124帧高清 FirstBlockCache Safe × SM75 SLA 静态核查

日期：2026-10-17

状态：静态核查部分完成；未授权Reality；新增GPU生成0次；124帧高清T_VALID未知。

设备：DESKTOP-4A1EGTM，Remote Desktop Commander在线设备 f6990966-5870-484b-bf79-409bc6fb963e 已ping且执行只读命令成功。RTX2080Ti显存22528MiB，检查时使用2206MiB。

V9规则 C>A>B，但权威路由文件未指定插件映射，因此本轮不能仅凭Remote Desktop Commander成功就认证所使用通道是C；没有切换A/B。

本地Star7节点源码存在于 C:\AI\MiniMax-H3\ComfyUI\custom_nodes\minimax-h3-chunk-star7\nodes.py。五帧FBC冻结工作流存在；未重新生成。

上游FirstBlockCache nodes.py第324-350行：已有 patches_replace.dit 的 double_block 替换会触发显式冲突异常，然后本插件为每个DiT块执行 set_model_patch_replace。第228-251行基于 extra['original_block'] 实现跳算。

本机Star7普通install_model_patch SLA路线主要通过 add_object_patch 更换各层 attn.forward；本机Star7 VSA特殊路线在约3320行又对double_block执行set_model_patch_replace，明显存在与FBC的入口冲突。

推论：Star7普通SM75 SLA object patch 与FBC整块替换可能在Star7先、FBC后顺序中共存，但还没有证明运行时object patch会通过original_block调用链生效；不能宣称兼容PASS。VSA整块替换不得直接堆叠。

候选A：已验五帧H3 INT8+CK+FBC Safe；124帧未知。候选B：A+单一Star7普通SM75 SLA QK8/PV16，仍需补丁链、显存、音画QA；未准入Reality。候选C：独立TeaCache或成熟少步路线，不与FBC叠加，需同质量证明。

未完成：实际加载FBC源码来源、Patcher中object_patches与patches_replace的注入顺序、音频guard/缓存语义、124帧资源边界和预测净收益。缺少任何关键证据继续停止GPU生成。

继承权威 V4_FREEZE_20261017.md；不更改 V4.0.0 冻结、历史文件或已完成视频。