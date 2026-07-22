【任务：视觉修复循环】

输入：

```text
WORKROOT=<工作目录>
GATE_ID=<当前关卡>
```

执行：

1. 只修当前 `GATE_ID` 对应的组件或布局。
2. 重新截取当前关 4 张截图：
   - `<GATE_ID>_target_desktop.png`
   - `<GATE_ID>_generated_desktop.png`
   - `<GATE_ID>_target_mobile.png`
   - `<GATE_ID>_generated_mobile.png`
3. 更新 `outputs/progress/stage-gates/<GATE_ID>.md`。
4. 给出桌面/移动/综合百分比和扣分逻辑。
5. 运行 `scripts\validate_stage_gate.ps1 -Gate <GATE_ID>`。
6. 若 `STATUS=PASS`，才允许进入下一关。
7. 若 `STATUS=GATE_BLOCKED`，继续修当前关或停止，不得跳关。

禁止：

- 不得跳到后续组件继续做。
- 不得等最终页面完成后再回填当前关截图。
- 不得用 build 通过替代视觉分。
- 不得设固定 3 轮上限；低于 95% 就不能过关。
