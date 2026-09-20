# MVT 浏览器部署完整性与现实竞争总装

英文：**MVT Browser Deployment Completion & Reality Competition Assembly**

版本：**1.0.0-rc1**

这不是新的浏览器引擎，而是 MVT Browser Automation 的“部署完整性技能”。

它解决的核心问题是：

> 候选路线、runner、harness、Virtual tests 都已经存在，但现实测试仍然启动不了，因为 run config、绑定、状态机、计时、结果、能力、恢复没有总装成一个可执行系统。

## 七门

1. 现实运行配置
2. 测试矩阵到 runner 的唯一绑定
3. COLD/WARM/RECONNECT 可执行状态机
4. 统一 T_VALID_FULL recorder
5. append-only 结果流水线
6. 能力矩阵机器绑定
7. 恢复执行绑定

只有 7/7 PASS 才允许现实浏览器竞争。

## 方法归属

固定属于：

**高智能虚拟成熟**

Codex 不是修复者。

现实验证失败时：
Reality Delta -> STOP -> GPT。

## 第一版来源

第一版来自 MVT Browser Automation 的一次真实现实验证阻断：

- F1/F2/F3 已程序化；
- 22/22 tests PASS；
- 26/26 simulations PASS；
- 58/58 hashes PASS；
- 但现实 attempts=0。

根因就是七门总装缺失。

因此本技能以后专门防止“组件成熟 = 系统可运行”的错误等价。
