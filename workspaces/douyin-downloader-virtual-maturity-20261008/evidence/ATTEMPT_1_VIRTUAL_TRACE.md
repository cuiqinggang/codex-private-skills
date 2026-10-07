# Attempt 1 — 虚拟节点生产同构重放

任务：DOUYIN-DOWNLOADER-VIRTUAL-MATURITY-20261008
方法：ENGINE 22 / BRAIN 18 / NEW_PAGE_TEMPLATE 17
METHOD_REF=e64f7593a732a99c82c8d4e36b30e25f89d00aa7

## 1. TASK_ACCEPTED

读取本任务《当前任务目标与正反约束 第1版》与 Freeze V1 后，目标未漂移。

## 2. BASELINE

采用历史已证明可进入 VALID 的成熟最小组合：

```text
clipboard
→ deterministic URL extraction
→ mature direct API
→ staged download
→ ffprobe(video>=1,audio>=1,duration>0)
→ atomic publish
→ runner exit
→ independent final ffprobe
→ FINAL_VALID
```

fallback 继续保留为失败路径，但不把未执行 fallback 写成 Reality-certified。

## 3. VIRTUAL_LOOP

### 最大净收益点
避免把浏览器、模型判断或自研协议放入正常 hot path。

### 成熟候选
1. direct API hot path + local deterministic verifier
2. local mature content-downloader as fallback
3. browser only as mature fallback internal path

### 虚拟替换与整体刷新
选 1 为 primary，2/3 仅失败时进入。

刷新后：
- 用户操作仍是“复制 → 双击”；
- deterministic 工作全部 CODE；
- Reality 前方案可完整 Freeze；
- VALID 判定有 staged + independent 双验证；
- 复杂度没有为了架构完整而上升。

### 第二轮 NET_GAIN 检查
可选的“3 provider resolver race”属于后续性能优化，不是首次进入 VALID 的必要条件；在没有新 Reality 前会增加取消、winner arbitration 和新 failure surface。

对本任务当前目标，继续引入它的净收益不确定且会增加重放复杂度，因此不进入本轮 first-valid Freeze。

STOP_GATE=PASS

## 4. NODE_FREEZE

VIRTUAL_NODE_RESULT=PASS
FROZEN_CANDIDATE=historical R1 architecture
NEXT_STAGE=REALITY_REPLAY

## 5. CEO_PAGE_ROTATION_GATE

REPLAN_REQUIRED=YES

理由：从虚拟成熟阶段进入 Reality 验收阶段，语义明显不同。按 BRAIN 18 / TEMPLATE 17，Freeze 后应 handoff 到新的 CEO。

本轮实际页面仍为单个 ChatGPT 页面，只虚拟模拟 True New Chat；验证重点是 handoff 状态是否可无歧义恢复。
