# 整体闭环极限短时间引擎 v5.0.5｜状态机保持 + 时间总控虚拟冻结 R1

- VERSION: 5.0.5
- FREEZE_ID: ESTE-v5.0.5-STATE-MACHINE-PRESERVED-TIME-MASTER-VIRTUAL-FREEZE-R1
- STATUS: VIRTUAL_MATURE_FROZEN
- UNIQUE_OBJECTIVE: `T*=min(T_VALID)`
- TOP_LEVEL_T_VALID: `T_CLOSED_LOOP_VALID`

## 本版只修一件事

v5.0.4 的时间总控不得改写已经在 v4.7.x / v5.0.3 固定的状态机动作。

正式关系：

```text
原状态机 = 决定允许发生什么动作、按什么顺序发生
时间总控 = 验证这些动作是否始终服从唯一时间锚
来源守卫 = 保证冻结资产按共同私库主路径直接进入 Reality
```

三者不是并列流程，时间总控和来源守卫都没有权限重写原状态机。

## 不可改写的原动作

```text
虚
→ 完整虚拟成熟
→ Freeze
→ FREEZE_TO_REAL
→ 自动形成 Reality / Codex CHAT 派发
→ 实只执行冻结方案

REAL PASS
→ DONE

REAL FAIL
→ Reality Delta
→ STOP
→ 回虚
→ 新 Freeze
→ 再实
```

同一 FREEZE_ID 只允许一次正式 REAL；Codex 在实阶段不得现场修复、重新设计、换路线。

## 共同私库主路径

正常状态固定：

```text
共同私库可访问
→ 直接按 repository / branch / path / blob 读取冻结资产
→ 不下载
→ 不要求用户重新确定位置
→ 不扫描本地磁盘
```

只有：
`NETWORK_UNAVAILABLE / AUTH_UNAVAILABLE / REPOSITORY_UNAVAILABLE`

才允许当前 Reality：
`STOP -> Reality Delta -> RETURN_TO_GPT`

若要使用下载/本地/内联备用物，必须回到“虚”后显式形成一个新的 Freeze；不得在当前 REAL 中切换。

## 时间总控

时间总控保留 v5.0.4 的：
- 唯一锚 `T*=min(T_VALID)`
- 顶层 `T_VALID=T_CLOSED_LOOP_VALID`
- N/A / NULL / MISSING 非法
- PENDING / SOLVING / VIRTUAL_FROZEN / REAL_CERTIFIED 连续求解
- 虚拟成熟时间收口
- 局部极限服从整体极限

但它只能：
`ALLOW / BLOCK`

不能：
- 改状态顺序
- 改执行器
- 改 Freeze 消耗规则
- 改远程源优先级
- 插入“下载包→人工找位置→再执行”动作

## 虚拟测试

- 原状态机允许/阻断等价：12/12 PASS
- 虚转实守卫矩阵：64/64 PASS，仅 1/64 允许
- 远程源/备用路径矩阵：64/64 PASS
- 失败回虚随机链：20,000/20,000 PASS，Timeline 重建 0
- 01-06 / 结构性失败代际语义：12/12 PASS
- 非法时间锚：18/18 全部阻断

虚拟验证 5 次：
MIN=420.966167ms
P50=426.243914ms
MAX=429.704564ms

结论：
`VIRTUAL_MATURE=YES`
`FREEZE=PASS`
`ANCHOR_STATE=VIRTUAL_FROZEN`
