# Attempt 2 — Clean Replay 全流程轨迹

任务：DOUYIN-DOWNLOADER-VIRTUAL-MATURITY-20261008
起点：TASK_ACCEPTED
方法固定：ENGINE 22 / BRAIN 18 / NEW_PAGE_TEMPLATE 17
METHOD_REF=e64f7593a732a99c82c8d4e36b30e25f89d00aa7

本次从头重放，不把 Attempt 1 的“PASS”作为本次结论前提。

## A. TASK_ACCEPTED → CONTRACT

- 读取用户目标：复制抖音分享文本/短链 → 双击桌面入口 → 自动得到桌面 MP4。
- 目标与正反约束可明确验收。
- 不需要新增范围。
- CONTRACT_VERSION=1 足够，无目标漂移。

结果：PASS

## B. PAGE_TOPOLOGY_GATE

为覆盖跨页恢复：
PAGE_TOPOLOGY=CEO_EXECUTOR

只虚拟两个语义阶段：
1. 虚拟成熟节点
2. Reality 重放节点

不增加第三类执行器。

结果：PASS

## C. BASELINE → VIRTUAL_LOOP → STOP_GATE

BASELINE 使用成熟 direct API first-valid 路线：
clipboard → deterministic URL extract → direct API → staged verify → atomic publish → independent final verify。

最大净收益判断：
- 浏览器/model 不进入 hot path；
- 本地 mature downloader/browser 仅 fallback；
- 3-provider race 属于可选后续优化，不是首次 VALID 必需，并会扩大 failure surface。

刷新完整方案后再次 NET_GAIN 检查，没有已知、确定、值得在 first-valid 前新增的正净收益变化。

STOP_GATE=PASS
NODE_FREEZE=PASS

## D. CEO_PAGE_ROTATION_GATE

从虚拟成熟进入 Reality 验收，语义改变：
REPLAN_REQUIRED=YES

必须生成 handoff，使用：
- 方法固定 ref
- 动态任务状态 ref
两者分离。

结果：待机械验证。

## E. Reality Replay 预期

只允许重放历史 R1 Reality：
- FINAL_VALID=YES
- EXACTLY_ONCE=PASS
- video+audio+duration>0
- runner exit 后 independent ffprobe PASS
- 未执行 fallback 不冒充已认证

本轮仍不执行新的真实下载。
