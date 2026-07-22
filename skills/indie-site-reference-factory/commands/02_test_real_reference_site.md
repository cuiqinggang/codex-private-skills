【任务：真实参考站拆解与独立站生成测试】

输入：

```text
TARGET_URL=<填写目标网址>
PROJECT_NAME=<填写项目名>
MODE=reference_to_indie_site
```

执行顺序：

1. 合规检查。
2. 环境预检。
3. 截图目标站：桌面、移动、全页。
4. 创建 `outputs/progress/00_TARGET_BASELINE.md`。
5. 创建 `outputs/progress/stage-gates/G00_TARGET_CAPTURE.md`。
6. 运行 `validate_stage_gate.ps1 -Gate G00_TARGET_CAPTURE`，未 PASS 停止。
7. 创建 `outputs/progress/01_GEOMETRY_SPEC.md`。
8. 创建 `outputs/progress/stage-gates/G01_GEOMETRY_SPEC.md`。
9. 运行 `validate_stage_gate.ps1 -Gate G01_GEOMETRY_SPEC`，未 PASS 停止。
10. 生成组件规格和 `outputs/progress/02_COMPONENT_SPECS_INDEX.md`。
11. 创建 `outputs/progress/stage-gates/G02_COMPONENT_SPECS.md`。
12. 运行 `validate_stage_gate.ps1 -Gate G02_COMPONENT_SPECS`，未 PASS 停止。
13. 创建 `outputs/progress/03_BUILD_PLAN.md`。
14. 创建 `outputs/progress/stage-gates/G03_BUILD_PLAN.md`。
15. 运行 `validate_stage_gate.ps1 -Gate G03_BUILD_PLAN`，未 PASS 停止。
16. 按 `G10/G20/G30/G40/G50/G60` 逐关构建、截图、评分、运行门禁。
17. 任一视觉关低于 95%，停留当前关修复，不得进入下一关。
18. 所有关卡 PASS 后，运行 lint/typecheck/build。
19. 输出 `FINAL_SIMILARITY_GATE.md`。
20. 输出测试报告和 ZIP。

完成标准：

有真实 URL、目标截图、生成截图、进度包、每关截图对比、桌面/移动/综合相似度百分比、门禁脚本输出、build、QA、ZIP，才算完成。

克隆能力通过标准：

所有视觉关和最终桌面/移动/综合相似度全部 >= 95%，且 build 通过。否则只能标记 `GATE_BLOCKED` / `PARTIAL_SIMILARITY` / `FAIL_SIMILARITY` / `INVALID_TEST`。
