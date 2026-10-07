# 《当前任务目标与正反约束 当前版》

状态：STOPPED  
更新时间：2026-10-07  
当前任务：方法极简化完成；不执行旧抖音 Reality

## 当前方法基线

- 《人工单页面极限短时间引擎 第14版》
- 《极限短时间执行大脑 第9版》
- 《新页面运行模板 第6版》

## 权威来源

权威来源=网络共同工作区  
REPO=cuiqinggang/codex-private-skills  
PATH=skills/artificial-single-page-extreme-time-engine/

禁止先去 C 盘找方法。

## 当前核心

成熟 BASELINE  
→ 计算下一轮 EXPECTED_GAIN / OPT_COST / NET_GAIN  
→ 不划算：STOP  
→ 划算：选择最大净收益点  
→ ≤3 个成熟候选  
→ 选 1 个  
→ 虚拟刷新完整数据  
→ 再算下一轮  
→ 直到下一轮不划算  
→ Freeze  
→ 1 次正式 Reality  
→ 验收

停止条件只是一笔成本账：

EXPECTED_GAIN = 预计未来运行次数 × 每次预计节省时间  
NET_GAIN = EXPECTED_GAIN - OPT_COST

NET_GAIN 不为正或收益太小，就停止。

不存在“关键未知所以提前 Reality”的默认分支。

## 硬规则

禁止自研  
禁止从零重建  
禁止中途逐点 Reality  
禁止把最大耗时点自动当成最大价值点  
禁止收益小于成本还继续优化

## 强制保留

四字段定位：页面名｜任务名｜序号｜虚/实  
状态机  
时间锚：TASK_ACCEPTED / CURRENT / ELAPSED / T_VALID / T*

## 当前停止项

DOUYIN-ONECLICK-METHOD-V1 及旧 R3 / 后续 Reality 继续 STOP。

下一步：等待新的现实任务，按第14版 + 第9版执行。
