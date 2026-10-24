# VEDA 实测筛查报告
任务编号：H3-VEDA-BENEFIT-20261024-001
日期：2026-10-24（北京时间）
结论：当前五帧高清配置不采用 VEDA；未取得同质量实际收益，V4.1.0 默认路线保持不变。

## 实测结果
固定输入为用户已有瀑布人物参考图、同一提示词、seed3014、1024×576、5帧、20步、res_multistep/simple、原INT8 ConvRot模型、ClipProj、视频VAE和FBC Safe。
本次有效开关对照统一使用隔离官方新版ComfyUI、Star7增强受保护FP16载入器、同一依赖和启动参数。A/B之间仅切换VEDA enabled。
计时从提交到PNG落盘、解码/尺寸/哈希校验及对照图生成；不含此前检索、安装和服务启动。它不是完整建设任务T_VALID。

| 项目 | 基线：VEDA关闭 | 候选：VEDA开启 |
|---|---:|---:|
| 完整五帧耗时 | 109.329秒 | 283.985秒 |
| 采样节点墙钟跨度（含初始化） | 80.766秒 | 253.922秒 |
| VAE解码节点跨度 | 26.578秒 | 23.907秒 |
| PNG可解码/尺寸正确 | 5/5 | 5/5 |
| 初步画质审查 | 主体/刺绣/瀑布整体保持 | FAIL：明显水平错块、人物及衣袖错位 |
| RAM遥测最大使用率 | 70.0% | 71.4% |

候选多用174.656秒，耗时为基线2.598倍。候选画质失败，故该耗时不能作为有效同质量T_VALID；T_VALID=null。
预热另记173.953秒，不与热态混排。显存峰值未连续完整采集，不宣称峰值认证。

## 关键运行证据
日志明确出现“Running | Star7 VEDA INT8 Tensor Core (SM75)”和“Done”，与第一轮仅注册但未生效不同。
参数为生成/参考90%稀疏；实际统计为“Attention computed: 100.0% of full attention (0.0% skipped)”。
五帧约0.2秒，被匹配到最近训练方案1344×768/5.2秒。本配置没有实际跳过注意力计算，却承担了预测与调度成本。
短序列/瓦片预算不匹配是可能的归因；没有单独因果实验，不能断言这是画面错块的唯一原因。

## 虚拟成熟与兼容性处理
1. 先读取V4.1.0冻结文件：A2 FBC Safe 20步默认；历史77.640秒只作参考，不冒充本次对照。
2. 排除已画质失败的SLA组合，不混入TE或LoRA；本轮不代表图片整套VEDA+TE+LoRA验收。
3. 原ComfyUI 0.34核心没有VEDA所需minimax_h3_layout和block_index字段。首轮开关输出逐像素相同，日志提示VEDA未使用；153.797/189.671秒只属于旁路接线观察，不作算法对照。
4. 独立下载官方核心，固定commit 7cebca52227c63b4180ceed448cbd7ad22903b6d；原生产核心和venv未升级。
5. 隔离candidate-deps使用comfy-kitchen0.2.40、comfy-aimdo0.6.0，复用现有Torch2.9.1/cu130。
6. 首次隔离配置缺原模型搜索目录，参数校验拒绝，未执行采样；修正独立目录映射后重新冻结。
7. 新核心报aimdo memory compile error。使用官方--disable-comfy-compiler开关，两侧一致，保留动态显存；未修改编译器或内存保护源码。
8. 预测器官方revision 76f202874608115408d73280be9531c4ab888242；275415648字节；SHA256=2a8d8845c5342756a2781e8e69563940e4bb573c9a40ebb534915ff8fd76573a。
9. 本机Star7 commit 8a33128f2f8c5585c57486c07de481241e70a39c；Windows10、2080Ti SM75、22528MiB、驱动591.74。

## 筛查边界与停止
原计划预热后做三对交错测试。观察到有效候选步骤明显退化后，增加“完成当前样本，若总耗时超过同seed基线1.5倍则结束筛查”的否决条件；没有把一次样本包装成三对重复认证。
本轮只完成一对有效开关对照，足以否决本次已出现画质破坏且明显更慢的配置；不证明该工具在其他任务、参数、时长或显卡上一概无效。
收益评估器返回FAIL_NOT_ADOPTABLE：重复样本不足三对；另有本次人工视觉FAIL。没有正式收益PASS或默认路线升级。
监督停止存在下一次提交的竞态：seed3015候选prompt 55e18b68-3d88-4128-93ec-775e47d2f69c已开始，随后随本轮服务清理中止，无可接受输出，排除计时，不自动重投。
完整124帧、运动连续性、音频与“VEDA+TE+LoRA”组合未测试，收益仍UNKNOWN。
没有完整计量本轮全部检索和建设耗时，不给出建设成本回本次数。

## 回执与恢复
有效基线prompt_id=e8e336b2-cebc-4a90-9ea9-686f4d7194b7。
有效候选prompt_id=7916784e-164a-4da7-8ebc-d1a777b81113。
预热prompt_id=1d9bd2c1-0c3f-44aa-9c3f-9fa218622329。
工作区：C:\AI\H3-VEDA-Trial-20261024。
有效批次：r2\batch2；原始history、workflow、receipt、PNG路径与哈希均保留。
汇总：r2\summary.json、r2\batch2\screening-verdict.json。
图像：r2\comparison.jpg、r2\roi.jpg；运行日志：r2\service3.stderr.log。
本轮试验服务PID已不存在，主运行器无残留；生产默认路线未更改，FlClash/代理未更改。
执行桥标签曾误用旧映射，已纠正：V12.0.1 A=Remote Desktop Commander，后续锁定在线设备f6990966-5870-484b-bf79-409bc6fb963e；不重投已执行生成。详见ROUTE_CORRECTION.md。
恢复时只读取现有证据，不重新执行本轮失败配置。

## 原始来源
https://github.com/star7code/minimax-h3-chunk-star7
https://github.com/Comfy-Org/ComfyUI/tree/7cebca52227c63b4180ceed448cbd7ad22903b6d
https://huggingface.co/Veda-Sparse/Minimax-H3-T2VA-Veda-8NFE-600Step-Preview/tree/76f202874608115408d73280be9531c4ab888242
