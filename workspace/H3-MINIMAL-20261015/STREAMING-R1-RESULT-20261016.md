# H3 streaming R1 实测结果（2026-10-16 本地）
方法：SANRENXING_V2_C002；通道：Bridge V7 C。
合同：STREAMING-R1-CONTRACT-20261016.md。
仅修改 ClipProjLoader mode: dynamic -> streaming；640×352、124帧、seed3013、Turbo4及原片真实首帧保持固定。
Prompt: fc8098a9-4259-4aca-8b8b-66b07aaf69bc。

## 实际结果
未完成，未生成视频，不能认定提速或质量达标。
冷加载，无缓存命中。节点1（ClipProjLoader）约37.096秒；节点6约39.13秒开始。
服务器 execution_start=1792086895734，execution_interrupted=1792087192465，实际至中断296.731秒。
节点6连续180秒无节点/进度事件，按预设保护条件发出定向中断；中断非即时，监控进程287.96秒退出后另行核对。
最终 history 明确 execution_interrupted，node6 MiniMaxH3ImageToVideo；queue_running=0，queue_pending=0。
日志：Krea2TEModel loaded completely 4999.47MB full load True；ClipProj streaming on cuda:0 4.88GB。
末段监测 RAM64–67.3%，GPU6–10%，显存约7.3GB。未达到原来89%内存压力，但仍慢。
不代表全部使用CPU；不能仅凭GPU利用率认定模型放置错误。
日志随后出现VideoVAE加载，说明条件节点不是始终完全无活动；180秒无进度事件不证明死锁。

## 结论与下一步边界
1. streaming整体加载实际生效，但没有通过完整生成验证，不能升级为成熟默认方案。
2. 89%RAM不是唯一慢速解释；问题进一步收窄到节点6内部条件编码/图像VAE处理，仍需内部阶段计时才能分开。
3. 原有274.657秒和323.263秒是热条件缓存成绩，不能作为新图片全流程基准。
4. 本次未进入采样，不能推导完成时间、400秒达标或物理极限。
5. 此次无进一步盲跑。下轮应先给节点6的tokenize/文本视觉编码/VAE编码加只记录时间的观测，核对相同成熟方案的冷/热基准，再冻结单变量测试。
6. 保持原始工作流文件不变、普通生成锁关闭；撤销R1一次性授权。仅在确认空队列后官方/free释放本项目模型。
