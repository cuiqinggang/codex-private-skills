# 千问3.8 27B1 — 01｜实现实认证合同

四定位：
【千问3.8 27B1｜本地智能体能力边界现实认证｜01｜实】

TASK_TIME_ID=QWEN38-27B1-20260923-182700+0800
TASK_SEQUENCE=01
T_CLOSED_REAL_START=2026-09-23T18:27:00+08:00
GPT_DISPATCH_TIMESTAMP=2026-09-23T23:14:10+08:00

现实唯一执行物：
QWEN38-AGENT-REALITY-RUNNER-v4.7.1.py
SHA256=d727112ac292f166f7509553bc96dea321025cec72d28916e78049c00e25e6f0

发布方式：GPT 本轮内联 gzip+base64 bootstrap；不依赖 GitHub 下载。

现实顺序：
1. 在 C:\AI\Bonsai2-27B-256K 物化 runner 并校验 SHA256；
2. --self-test，必须 PASS；
3. --real；
4. runner 只允许使用冻结的本地模型/runtime/安全沙箱工具绑定；
5. 输出 RESULT.json；
6. STOP，返回 GPT 最终判断。

任何基础设施/模型/工具边界失败：
REALITY_DELTA=<minimum evidence>
VALID_REAL=FAIL
ACTION=STOP_RETURN_TO_VIRTUAL

禁止：
- 现实现场改 runner；
- 换模型；
- 改代理/FlClash；
- 自动修方案；
- 自动降 128K；
- 把 FAIL 用速度抵消；
- 重置 TASK_TIME_ID 或序号。
