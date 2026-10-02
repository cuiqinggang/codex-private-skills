# CHANGELOG

## v0.5

STATUS=FROZEN

首个可复用正式版本。

### 来源
由 H3-P1“首个有效图声对”极限时间收敛 Reality 提炼。

### 已冻结能力
- 同 VALID 规格下以 `T*=min(T_VALID)` 为唯一优化目标；
- GPT 连续虚拟攻击 → Freeze → Reality → GPT Final Review；
- 单本机闭环 runner；
- warm service/model/conditioning 复用；
- history/output publication race 有界同步；
- 固定有效 seed；
- 单 decode；
- 无目标提示 ASR；
- 独立 verifier 并行；
- `VALID_END` 与报告/打包分离；
- Reality 失败后的局部最小修复；
- Reality 证据反哺虚拟极限判断；
- 边际收益不足时停止主动攻击。

### 首个 Reality 成果
```
653921.787ms
→ 616191.785ms
→ 358618.442ms
→ 288281.990ms
```

最终累计改善约 55.915%，约 2.268x 加速。

### 版本语义
v0.5 表示：
- 方法已形成；
- 至少一个真实视频案例完成完整 Reality 收敛；
- 可复用为其他视频任务的极限时间优化框架。

不表示：
- 所有视频模型都已认证；
- 288281.990ms 是所有视频任务的通用极限；
- 217–257s 理论区间已被正式认证。
