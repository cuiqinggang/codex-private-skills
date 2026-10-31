# EXP-N8N-001｜安全升级后的镜像、业务定义与探针分层核验
版本：V1；核查：2026-10-31 21:00前（北京时间）；分类：CASE/CANDIDATE_RULE；证据：既有Windows升级回执及独立HTTP时点检查。

触发：n8n发布安全通告，要求既有生产实例采用成熟升级方法，且不能把容器启动成功等同业务完成。
环境：原C盘既有n8n Docker/Compose实例，原始工作流与原备份目录均保留。**复盘未执行升级**，只读取原项目11:16回执。
LAST_GOOD：升级前2.45.5及原业务工作流集合。
FIRST_DELTA/修正：正式升级为2.45.7，镜像digest固定为sha256:9a8d8dcea75667496695d7810d7e1fe018a65efb36cc499d347f3931b3957b5d；记录13个工作流及3个active身份、workflowHash=3db3cbb7d29c4474ee1a64b7ebb9f185dca72fa2c14051ce4fa543b39eccbe63和C盘备份定位。后续HTTP /healthz、/healthz/readiness、/signin均200、healthy、restartCount=0。
适用：同一既有实例做安全版本变更后，将版本/digest、工作流数量与Hash、数据备份、HTTP就绪分开核账。
不适用：认为此版本必为全网最新，或已独立证明所有公告被缓解、每个业务工作流完整E2E、以后自动重启长期稳定。不得从本卡自行进行生产升级或复制配置中的凭据。
原回执：C:\AI\n8n\updates\20261031-2457\upgrade-result.json、final-http-qa.json（本机11:16）。现有生产任务CURRENT/Freeze优先；本卡仅是历史时点经验。