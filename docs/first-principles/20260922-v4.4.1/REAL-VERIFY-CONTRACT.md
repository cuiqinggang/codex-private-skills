# 极限短时间引擎 v4.4.1｜完整现实验证合同

## 目的

验证“现实底座 → 唯一锚定物 → 虚 → 实”在真实 Windows 主机上能够闭环；不得把仓库回读当成完整现实验证。

## 冻结输入

```text
METHOD_BRANCH=codex/first-principles-physical-limit-convergence-v4.4.1
METHOD=skills/first-principles-physical-limit-convergence/SKILL.md
FOUNDATION=skills/local-ai-reality-foundation/SKILL.md
FOUNDATION_VERSION=1.1.0
```

## 冻结现实任务

只读核验当前 Reality Foundation 的最小关键事实：

1. 方法文件明确要求现实底座为“虚/实”共同根基；
2. Foundation 版本为 1.1.0；
3. GPU 为 NVIDIA GeForce RTX 2080 Ti；
4. GPU 总显存现实读数约 22528 MiB（允许驱动展示单位产生极小格式差异，不允许换卡）；
5. 以下路径存在：
   - C:\AI\Playwright-Native-AI-Browser
   - C:\AI\OpenHands-Canvas
   - C:\AI\Bonsai2-27B-256K
6. 不修改代理、网络、系统设置，不启动 GPU 重任务。

## 冻结执行方案

```text
A. 从共同仓库指定分支读取 METHOD 与 FOUNDATION；
B. 读取 FOUNDATION VERSION；
C. 用 nvidia-smi 只读查询 GPU name + memory.total；
D. 用 Test-Path 并行/连续只读核验三个路径；
E. 一旦关键事实不符：
   输出最小 Reality Delta -> STOP；
F. 全部相符：
   输出 VALID_REAL=PASS 与 T_VALID_REAL_MS；
G. 最后执行 FOUNDATION_ABSORB_CHECK：
   只有新增现实事实对未来 min(T_VALID) 有价值才建议吸收，否则 ABSORB=NO。
```

## 禁止

- 不得现场修复 Foundation；
- 不得修改方法；
- 不得换验证路线；
- 不得修改代理；
- 不得把失败改写成 PASS。

## 完成门

```text
VALID_REAL=PASS
T_VALID_REAL_MS=有
FOUNDATION_ABSORB_CHECK=完成
```
