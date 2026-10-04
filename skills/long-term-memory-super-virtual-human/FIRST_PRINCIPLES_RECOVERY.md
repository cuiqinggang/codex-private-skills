# 长期记忆超级虚拟人｜第一性原理故障恢复 v0.6.0

## 1. 核心原则

故障恢复默认不从“报错末端”向后堆补丁，而从**最后一个已知正确的建设起点**出发，按原始依赖链正向重放，找到第一个偏离正确状态的层级，只修这一层，再继续正向验收。

```text
现实目标 / DONE_WHEN
→ 找到最后一个已知正确起点
→ 冻结用户数据、登录态、权威状态与安全边界
→ 按原始建设链逐层重放
→ 每层立即做最小健康验收
→ 第一个偏差点 = 当前首要根因候选
→ 只做最小定点修复或受控重建
→ 从该层继续向前重放
→ 完整 Reality 验收
→ 保存新经验
```

这套方法称为：

`FIRST_PRINCIPLES_FORWARD_REBUILD_RECOVERY`
（第一性原理·正向重建恢复）

## 2. 为什么它优先

很多“修很久仍没有结果”的故障，不是因为故障本身复杂，而是因为当前执行实例已经失去成立条件。继续在末端重试，只会反复验证同一个坏状态。

典型无效模式：

```text
末端报错
→ 猜一个原因
→ 改一个参数
→ 重试
→ 再猜
→ 再改
→ 状态越来越脏
→ 不知道当前实例还剩哪些原始前提
```

默认替换为：

```text
正确建设合同
→ 正确起点
→ 层1 PASS
→ 层2 PASS
→ 层3 FAIL
→ 只处理层3
→ 层3 PASS
→ 层4...
```

这样故障定位和恢复动作合并成同一条正向链，天然服务于 `T*=min(T_VALID)`。

## 3. 与“最小定点修复”的关系

“从源头重建”不等于“大拆大改”。

它解决的是**定位顺序**；“最小定点修复”解决的是**修改范围**。

统一算法：

```text
先从源头正向重放定位
→ 找到第一个失真层
→ 判断：
   A. 当前实例可原位恢复 → 最小定点修复
   B. 当前实例已失去成立条件 → 仅重建该实例/该层
→ 禁止扩大修改面
→ 继续正向验收
```

优先级：

1. 保护数据、凭据、登录态、权威状态；
2. 重放已知正确的成熟建设链；
3. 找到首次偏差；
4. 最小定点修复；
5. 只有实例本身失效时才做受控重建；
6. 不在没有新证据时重复同一种失败尝试。

## 4. 三次经验抽象

### A. GPT/Windows 本地连接桥

历史现象：在已故障连接实例上持续修复长期无效；放弃坏实例，按原始正确接入方式重新建立连接后快速恢复。

抽象：

```text
不要把“连接对象仍存在”当成“连接链仍成立”
→ 回到连接建立条件
→ 重新验证身份/进程/传输/执行
→ 首次偏差处修复
```

### B. 专用 ChatGPT 浏览器 / CDP 9223

2026-10-04 R2 实测发现：旧 `cmd.exe` 启动壳仍在，但真正的专用 Chrome 主进程已经不存在，9223 没有监听。此前继续重连 9223 不可能恢复。

正向重建后：

- `shared-mcp` profile 保留；
- 原始 Chrome executable 存在；
- 重新以 `--remote-debugging-port=9223` 启动唯一专用浏览器；
- 9223 LISTEN PASS；
- `/json/version` PASS；
- `/json/list` 找到 ChatGPT target；
- Attach-Only runtime 恢复；
- RAW CDP 真 New chat → 提交 → GPT ACK PASS；
- `submissionCount=1`、`branchUsed=false`、`newBrowserLaunched=false`。

根因不是“9223 很难修”，而是**端口的拥有者进程已经死亡，只剩启动壳造成错误直觉**。

### C. 爱马仕升级后登录失效

用户现场确认：升级前处于登录状态；升级后出现登录页，自动填充的账号/密码无法登录。没有继续修改数据库或认证结构，而是回到最基本认证前提：从权威密码库取正确凭据重新登录，立即恢复。

抽象：

```text
认证失败
→ 先验证最原始凭据来源
→ 正确凭据可登录，则停止上升到数据库/版本/容器层
→ 只有正确凭据也失败，才继续下一层
```

这体现“最便宜的原始成立条件优先”。

## 5. 故障恢复唯一默认入口

收到“修复故障/恢复功能/为什么坏了”类任务时，除非已有明确根因和成熟一键修复，否则默认执行：

```ini
RECOVERY_DEFAULT=FIRST_PRINCIPLES_FORWARD_REBUILD
REPAIR_FROM_ERROR_TAIL_DEFAULT=NO
KNOWN_GOOD_ORIGIN_REQUIRED=YES
FORWARD_LAYER_VALIDATION=YES
FIRST_DIVERGENCE_IS_PRIMARY_REPAIR_POINT=YES
MINIMAL_POINT_REPAIR=YES
CONTROLLED_LAYER_REBUILD_WHEN_INSTANCE_INVALID=YES
REPEAT_SAME_FAILED_ATTEMPT_WITHOUT_NEW_EVIDENCE=FORBIDDEN
FULL_REALITY_REVALIDATION_REQUIRED=YES
```

## 6. 正向建设链模板

每个能力应尽量保存自己的“诞生链”：

```text
权威配置/凭据/版本
→ 依赖存在
→ 启动/创建
→ 控制面建立
→ 数据面建立
→ 上层服务接入
→ 用户功能
→ DONE_WHEN
```

发生故障时反向猜测不是默认方法；直接按这条链从最小必要起点重新走。

每层只回答三个问题：

1. 这一层的成立条件是什么？
2. 当前 Reality 是否满足？
3. 如果不满足，最小恢复动作是什么？

## 7. 停止无限“正在修复”

为避免长时间无可见进展：

- 同一失败动作没有新证据时不得机械重复；
- 每一轮必须产生至少一种新信息：新 PASS、首次 FAIL 层、根因候选收敛、修复动作结果；
- 连续两轮没有缩小故障空间，立即返回最近已知正确起点重新正向重放；
- 能低成本重建的临时实例，优先重建，不把时间消耗在保留坏实例上；
- 用户数据、账号、长期 profile、权威仓库、不可逆状态不属于“临时实例”，不得为了省事直接清空。

## 8. 与 Goal Loop 的结合

Goal Loop 遇到故障时：

```text
执行失败
→ 是否已有明确根因？
  → 是：最小定点修复 → Reality
  → 否：FIRST_PRINCIPLES_FORWARD_REBUILD
       → 找首次偏差
       → 最小修复/重建该层
       → Reality
→ 未达 DONE_WHEN 则继续循环
```

故障恢复本身也必须 obey exactly-once、lease/fencing、Checkpoint、安全权限和 FINAL_VALID 门。

## 9. 适用边界

不机械重建以下对象：

- 未备份的用户数据；
- 唯一凭据源；
- 支付/账号安全状态；
- 不可逆生产数据；
- 无法确认副作用的外部动作。

这些场景先保护状态、建立 checkpoint/备份，再从**逻辑建设起点**正向验证。

## 10. v0.6.0 冻结结论

```ini
FAULT_RECOVERY_PHILOSOPHY=FIRST_PRINCIPLES
DEFAULT_DIRECTION=ORIGIN_TO_OUTCOME
LOCAL_REPAIR_SCOPE=MINIMUM_NECESSARY
REBUILD_SCOPE=INVALID_LAYER_OR_EPHEMERAL_INSTANCE_ONLY
DONE_WHEN_UNCHANGED=YES
TSTAR_OBJECTIVE_UNCHANGED=YES
```

第一性原理在这里不是口号：它要求每次恢复都先问“这个能力成立所不可缺少的最小条件是什么”，然后从这些条件重新推导到现实结果。
