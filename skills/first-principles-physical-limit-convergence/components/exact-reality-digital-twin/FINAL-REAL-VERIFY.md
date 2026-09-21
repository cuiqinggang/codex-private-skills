# 最终正式技能包现实验收

只允许 VERIFY；禁止修改、修复、发布、重新设计、重新采集 R3、重新运行 T1/T2/T3/O1。

从仓库根：

1. 核对 VERSION：母技能 3.1.9；Reality Anchor 1.3.0；Exact Twin 1.3.0。
2. 运行：
   `python skills/first-principles-physical-limit-convergence/components/exact-reality-digital-twin/ENGINE.py selftest --output-dir <临时目录>`
   必须 24/24 PASS。
3. 运行：
   `python -m unittest discover -s skills/first-principles-physical-limit-convergence/components/exact-reality-digital-twin/tests -p test_browser_twin.py -v`
   必须 6/6 PASS。
4. 只读核对 `REALITY-AUTHORITY.json`：
   - Browser R3 fingerprint = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
   - Material Delta = 0
   - Shadow Isolation = PASS
   - Reality Mutated = NO
5. 本轮 git diff/status 必须无修改。

最终只回：
FINAL_FORMAL_SKILL_VERIFY / 三个版本 / 24/24 / 6/6 / Fingerprint / Delta / Shadow / FULL_BROWSER_TWIN / ENVIRONMENT_99 / REALITY_MUTATION=0 / ACTION=STOP。

任一失败只记录 REALITY_DELTA 并 STOP；执行器不得修复。
