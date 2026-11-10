# R94｜文件精确归档·成熟节点搭配（2026-11-10）

证据级别：VERIFIED_FOR_SCOPE，限增强Oh My Pi 18.18.0、READY host文件归档、每批128独立任务×每项48文件、原始检查与独立ZIP/CRC/manifest/sha回读。NEW_DEPLOYMENT_READY=NOT_VERIFIED；不证明真实GUI交付或任意新业务READY。

## 成熟节点来源、触发合同与接口
先用现有run-batch-automation SKILL.md/R89成熟入口及executable-flows.json、assets/ready-flows、batch_handoff.py和match_flow.py。只匹配files.archive_exact，原始业务要求成员相对路径、原文件字节、CRC、manifest与输入不变，每项隔离workspace，入口上下文与原程序版本一致。文件大小、输出路径、授权根按原MATCH合同。无需另造归档算法、模型任务、数据库或调度器。对于跨workspace、ACL/时间戳备份、额外OCR和用户GUI操作，返回NOT_MATCHED/NEEDS_CONFIG，不缩减原合同。

## 调用步骤（只使用原有成熟程序）
1. 读原本机R94 FREEZE.json、SUMMARY.json、STREAM-METRICS.json核对精确输入/现时源码哈希；当前deliver_archive_batch.py源码与历史Freeze不完全一致，缺原文逐行diff，不能假定现行程序与历史相同。
2. 按既有请求JSON数组创建128项相互独立工作目录，原match()核所有输入，原batch_handoff.py以持续四lane处理，每lane32项。使用原增强CLI入口，固定worker数4仅作为本轮已测可用选择，不是跨机全局最优。具体argv、依赖、cwd以原冻结/原程序确定，不能把本说明当复制即运行的命令。
3. 每项按原归档程序完整执行，查原delivery.zip、manifest.json、delivery.json，独立对照48个文件的路径、字节、CRC、哈希，128/128有效才报本轮限定PASS；失败原工作区核账并只接续差量。
4. 用户合同要求网页/GUI时还必须从该真实入口操作及验收。历史产物签收不能代替GUI。

## Reality/反例与时间边界
来源：GitHub main reports/R94-128-Streams-Reconciliation-20261110.md；C:/Users/A/Documents/DSH-Workspace/pi-single-dual-r89-20261110/r94-cli-streams-128/ 下原冻结、八批SUMMARY、独立QA和产物。2026-11-10仅此固定文件业务1024/1024项及49,152文件检查合格。
两轮128项/批的完整原程序请求→QA读回均值，1/2/4/8路依次58.055/38.352/29.697/32.667秒；加测试数据复制则72.400/55.507/46.902/52.959秒。四路仅此两次样本均值最短，冷/热及负载漂移未隔离，不能当物理极限或模型吞吐、百席能力。槽位占用含等待，不当CPU利用率。新源码改动后成功路径等价和真实最终GUI均未认证；R89 96文件宿主PASS亦是GUI=NOT_VALIDATED。

## 回退与维护成本
环境/源码/输入变化时先只读匹配原专业包，失败保留已通过项、原Freeze与负例，按既有单路/双路或原程序同合同验收回退；禁止改ACL、代理、系统或业务核心。首次定位、模型协调、复制、维护、失败/返工/恢复与验收未统一完整用户T_VALID计量，完整净时间收益=NOT_MEASURED；跨业务新使用必须保留adopt/reject与真实结果。本页只追加已有专业包的限定配方证据，不单独建立新技能或定时器。
