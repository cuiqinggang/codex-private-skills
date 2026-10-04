# LTMVH v0.6.0｜第一性原理故障方法语义修正

## 冻结结论

第一性原理不是“重建法”。

第一性原理是所有故障处理的唯一分析与定位方法：

1. 先问：这个能力成立最不可缺少的条件是什么？
2. 从源头因果关系开始验证。
3. 前面正确的部分全部保持不动。
4. 找到第一个逻辑或 Reality 不成立点。
5. 只修这个最小断点。
6. 继续沿原因果链验证直到 DONE_WHEN / Reality。

重建只是一种局部动作：若断点可原位修复，就最小定点修复；若断点对应的临时实例已经失去成立条件，才只重建该实例；前面已 PASS 的层级禁止重建。

## 唯一故障方法

FAULT_ANALYSIS_METHOD=FIRST_PRINCIPLES_ONLY
FAULT_REASONING_DIRECTION=CAUSE_TO_OUTCOME
TAIL_SYMPTOM_TRIAL_AND_ERROR=FORBIDDEN
PRESERVE_CONFIRMED_GOOD_LAYERS=YES
FIRST_INVALID_CAUSAL_LINK=PRIMARY_REPAIR_POINT
REPAIR_SCOPE=MINIMUM_NECESSARY
REBUILD_IS_A_METHOD=NO
REBUILD_ALLOWED_AS_LOCAL_REPAIR_ACTION=YES
FULL_REALITY_REVALIDATION_REQUIRED=YES

## 初级错误例外

所谓“初级错误”不是另一套方法。下载目录无权限、编码错误、明确的 A 路径不可用而 B 路径等价可用，也仍然先做最小因果判断，只是因果链很短，所以可以立即修复。

因此不存在“简单错误用一种方法、复杂错误用另一种方法”。只有一套：第一性原理 → 最小原因 → 最小动作。区别只是链条长度不同。

## 9223 示例

9223 的修复不是“大面积重建”。正确逻辑是：为什么需要 9223？因为专用 Chrome 启动时开放 CDP。继续检查：Chrome executable 存在，PASS；shared-mcp profile 存在，PASS；专用 Chrome 主进程存在，FAIL。到这里首次断裂已经出现，因此 executable、profile、登录态全部不动，只恢复 Chrome 主进程这个断点，然后继续验证 9223 LISTEN → CDP → ChatGPT target → Attach-Only runtime → GPT ACK。

所以它证明的不是“重建有效”，而是：从第一性原理因果链出发，可以很快找到最小错误点，并只修那个点。

## 三次经验的共同规律

1. Windows/GPT 本地连接：回到连接成立条件，找到失效环节。
2. CDP 9223：回到“端口为什么存在”的因果源头，发现 Chrome 主进程死亡。
3. 爱马仕登录：回到“认证成立首先需要什么”，先验证权威正确密码，问题立即结束。

共同规律：故障出现的位置，不等于故障原因所在的位置。因此不得从末端症状出发无限枚举修复方案。

## 与 T*=min(T_VALID) 的关系

第一性原理路径不是形式上的“从头检查更多东西”，而是用因果链快速压缩搜索空间：因果链 → 首次不成立点 → 最小修复 → VALID。它天然避免多个未经约束的故障假设并行扩散，因此作为 LTMVH 的默认且唯一故障分析方法。
