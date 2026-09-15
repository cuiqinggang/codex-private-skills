# P0 第一性原理四列法 99 分完整案例

## 固定任务合同

- 任务：向本机 ComfyUI `127.0.0.1:8188` 提交固定两节点工作流，得到最终 256×256 PNG 字节并完成最低结果验证。
- 输入：`p0-control-black-256.png`；工作流为 `LoadImage → P0CachedPNGWebsocket`。
- 输出：与固定 reference（参考结果）像素身份一致的完整 PNG。
- 成功条件：匹配 prompt、执行成功、获得 PNG bytes、PNG 结构有效、尺寸 256×256、完整解码、像素 SHA-256 身份匹配。
- 计时起点/终点：POST `/prompt` 前的 `REQUEST_START` 至最低验证完成的 `RESULT_READY`。
- 不计入：冷启动、证据落盘、日志整理、Git、知识同步与最终认证文件写盘。
- 冻结环境：Windows 10 build 19045；NVIDIA GeForce RTX 2080 Ti 22 GB；ComfyUI 0.9.2；认证客户端 Python 3.13.12、aiohttp 3.14.1、Pillow 12.2.0。
- 证据：`workspaces/absolute-time-fireworks-optimization/P0-EXTREME-MINIMAL-FASTPATH/certification-20260915-193531/results.json`。

## 第一列 CURRENT（当前真实状态）

初始冻结基线为 `32.55975 ms`。第一轮宏观迭代后为 `21.9215 ms`。最终相同固定任务的 P0 99 认证中位数为 `12.6782 ms`，P95 为 `16.724915 ms`，有效运行 `40/40`。

最终认证的宏观分段中位数：

| 分段 | 中位数 ms | 最小 ms | P95 ms | 最大 ms |
|---|---:|---:|---:|---:|
| REQUEST（请求） | 4.8033 | 4.2048 | 6.06325 | 9.7392 |
| QUEUE（排队） | 5.0928 | 3.5154 | 8.8674 | 9.5008 |
| EXECUTE（执行） | 0.32975 | 0.0389 | 1.07507 | 3.2574 |
| RESULT（结果） | 1.87085 | 1.7164 | 2.351425 | 2.7485 |

四个分段各自中位数相加为 `12.0967 ms`，不等于总时间中位数 `12.6782 ms`。原因是各分段中位数可能来自不同运行，中位数不具可加性；`0.5815 ms` 差值不是隐藏的第五段成本。

## 第二列 EXTERNAL FRONTIER（外部成熟前沿）

本轮实际复用或参考的成熟能力：

- `mature-replication-four-column` v4.0.0：正式第一性原理四列定义与 99 冻结门禁。
- ComfyUI 的 prompt queue（提示队列）、`LoadImage` 与 WebSocket 二进制传输能力。
- 已验证的 memory/WebSocket result path（内存/WebSocket 结果链）。
- aiohttp WebSocket/HTTP 客户端与 Pillow 完整 PNG 解码。
- ComfyUI 既有 `SaveImageWebsocket` 思路及本项目的等价缓存输出节点。

`NO_DIRECTLY_COMPARABLE_EXTERNAL_TIME`

没有找到与本任务合同、硬件、软件版本、计时起止点和最低验证完全一致的外部绝对时间，因此不伪造外部排名或数字。外部能力只作为路径库，不作为不可比的 99 约束。

## 第三列 FIRST-PRINCIPLES PHYSICAL TIME（第一性原理物理时间）

### 物理必需步骤

1. loopback HTTP 请求与响应：客户端必须把固定工作流提交给服务端并取得 prompt identity。
2. 服务端安全验证与入队：保留 ComfyUI `validate_prompt` 及队列语义。
3. 条件队列、工作线程与 OS 调度：任务必须从队列进入执行。
4. 输出节点执行：固定输入首次编码后，同一 tensor 可复用 PNG 字节；每次仍需发送结果事件。
5. WebSocket 传输：服务端把最终 PNG bytes 送到对应 client。
6. 客户端最低验证：签名、格式、256×256、完整 decode 与像素身份确认。

### 已删除的软件额外开销

- file-backed output / publish / reopen（文件输出、发布、重开）约 `10.63825 ms`；
- history HTTP polling、完整 history JSON 与重复 PNG decode 共 `4.4220 ms`；
- 固定 tensor 的重复 tensor→NumPy→uint8→Pillow→PNG encode 共 `3.3357 ms`；
- watchdog、monitor、同步 evidence、Git、统计 bookkeeping 等全部在关键路径外。

### 可以并行或后移

- 接收 WebSocket image 与 execution success 可并发等待；
- 审计、日志、证据写盘、manifest、hash inventory、知识同步全部在 `RESULT_READY` 后；
- 最终 certification 只在候选已成功后运行。

### REALITY FLOOR（当前现实下界）

`REALITY_FLOOR_MS=10.4729`

计算式：在 40 次完整有效认证运行中，最短总时间为 `10.4729 ms`。它同时包含上述所有必需步骤，因此是当前硬件、软件与固定任务下的**观测现实下界**，不是宇宙理论零开销。

`PHYSICAL_GAP_MS = FINAL_P0_99_TIME_MS - REALITY_FLOOR_MS`

`PHYSICAL_GAP_MS = 12.6782 - 10.4729 = 2.2053 ms`

中文解释：冻结中位数比同批完整有效运行的最短值多 `2.2053 ms`。从分段分布看，可变头部主要位于 REQUEST 与 QUEUE，其次是 OS/runtime 调度、短执行波动和最低解码验证。该 gap 是跨运行波动形成的整体差值，不能把各分段独立最小值相加后伪装成同一次可实现运行。

当前允许范围内，没有已证明稳定、低风险且可行的 `>=0.5 ms` 可消除块：

`LARGEST_REMAINING_REMOVABLE_BLOCK_MS=<0.5`

重复 prompt validation 物理上可能形成数毫秒机会，但绕过验证会改变安全合同，已被判为不可行候选，因此不能计入“现实可消除块”。

## 第四列 ITERATIVE CONVERGENCE（迭代收敛）

| 轮次 | PREVIOUS_BEST | TARGET_BLOCK | PHYSICAL_REASON | REMOVED_OR_REDUCED_COST | NEW_BEST | GAIN_MS | GAIN_PERCENT | NEXT_LARGEST_GAP |
|---|---:|---|---|---|---:|---:|---:|---|
| Macro R1 | 32.55975 | file-backed output / publish / reopen | 最终结果已在内存中，写盘后再打开不是任务物理必需 | 删除磁盘结果链，改为 memory/WebSocket | 21.9215 | 10.63825 | 32.6730% | history 与重复验证 |
| Armor removal | 21.9215 | history HTTP / full JSON / double decode | WebSocket 已同时给出 prompt identity、成功和最终字节 | 删除 history polling、完整 history JSON 与重复 PNG decode | 17.4995 | 4.4220 | 20.1720% | 固定输出重复编码 |
| Encode cache | 17.4995 | tensor→PNG 重复编码 | 固定任务的输入 tensor 身份不变，PNG 字节也不变 | 首次编码后以 tensor 强引用缓存 PNG bytes | 14.1638 | 3.3357 | 19.0616% | request/queue 抖动 |
| Final certification | 14.1638 candidate | 稳定性与等价性认证 | 性能候选已成功，才允许 Measurement 工具验收 | 40 次相同实现冻结分布；没有改性能代码 | 12.6782 median | 不作为新代码收益 | 不作为新代码收益 | 可行低风险项 <0.5 ms |

从正式三点看：

- `32.55975 → 21.9215`：收益 `10.63825 ms`，提升 `32.6730%`。
- `21.9215 → 12.6782`：后续宏观收敛与最终认证合计下降 `9.2433 ms`，相对提升 `42.165454%`。
- `32.55975 → 12.6782`：总绝对收益 `19.88155 ms`，总提升 `61.0617403%`。

首次宏观优化事前物理模拟约 `21.97–22.30 ms`，真实结果为 `21.9215 ms`，证明物理因果模型正确兑现了磁盘结果链的删除。

## 99 / FREEZE（99 分与冻结）

```text
FINAL_P0_99_TIME_MS=12.6782
P95_MS=16.724915
VALID=40/40
AA_95CI=[-0.247058,1.408138] ms
AA_EQUIVALENCE_BOUND=2 ms
REALITY_FLOOR_MS=10.4729
PHYSICAL_GAP_MS=2.2053
LARGEST_REMAINING_REMOVABLE_BLOCK_MS=<0.5
MACRO_SCORE=99
P0_99=YES
P0_FREEZE=YES
```

重新打开条件：出现保留安全验证且可证明至少节省 1 ms 的成熟方案，或硬件、ComfyUI、runtime、固定任务合同改变。
