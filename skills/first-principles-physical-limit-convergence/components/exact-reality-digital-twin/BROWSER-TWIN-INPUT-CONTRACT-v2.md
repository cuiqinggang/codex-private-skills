# Browser Twin 输入合同 v2

Twin：exact-reality-digital-twin@1.2.0

本文件继承 BROWSER-TWIN-INPUT-CONTRACT.md 中的现实输入字段、UNKNOWN 不猜测、Reality/Shadow 隔离与安全边界。

新增唯一时间合同：

1. T1/T2/T3 为三个预声明轻量计时运行。
2. T1/T2/T3 必须使用现实锚定包中的 browser-reality-r3-timing.mjs。
3. 计时运行禁止重观测；只保留任务身份、同一浏览器安全身份、outcome 和 duration。
4. O1 为一个预声明可观测运行，使用完整 Browser R3 collector。
5. O1 与 T1/T2/T3 的 task、selector、outcome、浏览器安全身份必须一致。
6. O1 不得替代失败的 T1/T2/T3。
7. O1 时间不进入性能指标。
8. 所有现实门禁通过后：
   T_VALID = min(T1,T2,T3)

ENGINE.py 的 canonical input 固定为：
- --timing T1
- --timing T2
- --timing T3
- --observability O1

Reality Replay 只有在：
- 三个 timing validation 全 PASS
- O1 observability validation PASS
- 3/3 timing outcome 一致
- identity 无漂移
- critical unknown = 0
时才允许执行。

现实数据不完整时必须保持：
BROWSER_TWIN_INPUT_READY=NO
FULL_BROWSER_TWIN=NO
ENVIRONMENT_99=NOT_YET
