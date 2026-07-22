# FAILURE-HISTORY-20260528

## 保存原因

本技能包必须保存这次探索的失败、纠偏与成功路径。价值不只是最终结论，而是流程如何从“模型自称完成”升级为“可验证、可返修、可最终验收”的长任务体系。

## 第一轮问题

GPT 输出的是 Claude-style 12 层说明书，不是完整任务包。

问题：章节化、介绍化、不能直接执行，缺少完整 gate、产物、验证、repair、final acceptance。

纠偏：GPT P1 只能作为 control specification；不能伪装成最终本地执行包。

## 第二轮问题

GPT 发布的是“制作任务包”任务。Codex 制作了任务包，大约 16 分钟完成，但没有真实执行 2 小时 endurance run。

问题：任务本质是 package creation，不是 real endurance run。

纠偏：必须明确区分“制作任务包”和“执行真实长任务”。

## Codex 反向指出缺口

缺少：

```text
minimum_elapsed_minutes >= 120
start_time / end_time
elapsed_minutes
15 分钟 checkpoint
真实 workload
independent verifier 校验耗时
bad-case must-fail
positive-case after 120 minutes
```

纠偏：ENDURANCE_VALIDATION 必须具有最低耗时、checkpoint、bad-case、positive-case 与 independent verifier。

## 第三轮成功

GPT 根据 Codex 指出的缺口补齐硬条件。Codex 完成真实 124.12 分钟 endurance run，生成 9 个 checkpoint，bad-case 和 positive-case 均通过，final-acceptance 完成。

成功沉淀：

1. 不要一步从目标跳最终执行包。
2. GPT 必须先做详细总控设计。
3. Codex 必须做准备阶段，不执行。
4. Codex 准备阶段包括草案、自审、修正版、skills 搜索准备。
5. GPT 再最终整合。
6. Codex 最后执行。
7. L4/L5 必须有 subagent evidence gate。
8. Endurance 才强制最低时间。
9. Production / mature replay 用 time budget，不强制空耗。
