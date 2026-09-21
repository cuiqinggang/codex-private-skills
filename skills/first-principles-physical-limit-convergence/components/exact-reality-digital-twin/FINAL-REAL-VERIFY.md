# 最终正式技能包现实验收

只允许 VERIFY；禁止修改、修复、发布、重新设计、重新采集 R3、重新运行 T1/T2/T3/O1。

## 关键约束

正式技能包已自包含冻结的 safe Reality/Twin 证据。
最终验收禁止依赖或访问旧 task-local 工作区：
`C:\Users\A\playwright-browser-automation5-final-reality-competition-work`

不得重新生成 Reality Profile；只验证正式包中的冻结证据。

## 从仓库根执行

1. 核对 VERSION：
   - 母技能 = 3.1.9
   - Reality Anchor = 1.3.0
   - Exact Twin = 1.3.0

2. 运行 Legacy selftest：
   `python skills/first-principles-physical-limit-convergence/components/exact-reality-digital-twin/ENGINE.py selftest --output-dir <仓库内临时目录>`
   必须 24/24 PASS；完成后删除该临时目录。

3. 运行正式自包含 Browser Twin tests：
   `python -m unittest discover -s skills/first-principles-physical-limit-convergence/components/exact-reality-digital-twin/tests -p test_browser_twin.py -v`
   必须 6/6 PASS。

4. 只读核对：
   `REALITY-AUTHORITY.json`
   与
   `reality-profiles/playwright-golden/`

   必须：
   - Browser R3 fingerprint = 9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd
   - Material Delta = 0
   - Shadow Isolation = PASS
   - Reality Mutated = NO
   - frozen evidence count = 6

5. 本轮 git diff/status 必须无修改。

最终只回：
```text
FINAL_FORMAL_SKILL_VERIFY=
MOTHER_VERSION=
REALITY_ANCHOR_VERSION=
EXACT_TWIN_VERSION=
LEGACY_SELFTEST=
BROWSER_TWIN_TESTS=
BROWSER_R3_FINGERPRINT_SHA256=
MATERIAL_REALITY_TWIN_DELTA_COUNT=
SHADOW_ISOLATION=
REALITY_MUTATED=
SELF_CONTAINED_FORMAL_PACKAGE=
FULL_BROWSER_TWIN=
ENVIRONMENT_99=
REALITY_MUTATION=0
ACTION=STOP
```

任一失败只记录 REALITY_DELTA 并 STOP；执行器不得修复。
