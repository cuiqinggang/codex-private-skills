# Distribution Note — v2.0.0

正式技能：

```text
first-principles-physical-limit-convergence
```

正式版本：

```text
2.0.0
```

正式分支：

```text
codex/first-principles-physical-limit-convergence-v2.0.0
```

v2.0.0 继承 v1.9.0 的简洁四步法，并新增：

- 随机系统 `attempt / delivery` 双层合同；
- `T_TFVR = Time To First Valid Result`；
- verifier + reject + resample 的验证式交付；
- 控制面/执行面/业务失败分层；
- GPT-Codex-GitHub-浏览器桥接自动闭环规范；
- capacity router 与 checkpoint/idempotency 规则。

首个完整实证案例：H3-P0 delivery-system 99，20/20 最终交付 QC PASS，first-attempt pass 90%，平均 1.10 attempts，T_TFVR P50 6.076s / P95 11.974s，无效输出交付 0。

不要再把历史 `absolute-time-fireworks-optimization` 或 v1.x 分支当作当前正式母技能。
