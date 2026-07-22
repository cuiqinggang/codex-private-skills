# 05_NEXTJS_BUILD_PIPELINE

默认输出工程：`test_projects/<project_name>/`

优先技术栈：Next.js、React、TypeScript、Tailwind、组件化目录结构。

必须创建：`app/`、`components/`、`lib/`、`public/`、`package.json`、`README.md`。

## 编码前硬门禁

写页面代码前必须按顺序通过：

1. `G00_TARGET_CAPTURE`
2. `G01_GEOMETRY_SPEC`
3. `G02_COMPONENT_SPECS`
4. `G03_BUILD_PLAN`

每关必须运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\validate_stage_gate.ps1 -WorkRoot <workroot> -Gate <GATE_ID>
```

只有输出 `STATUS=PASS` 才能继续。缺任一项，禁止编码。

## 分段实现硬门禁

不得一次性写完整页面后才截图。必须按顺序执行并逐关验收：

1. `G10_NAVBAR`
2. `G20_HERO_TEXT`
3. `G30_PRIMARY_VISUAL`
4. `G40_CTA_SCROLL`
5. `G50_FIRST_SECTION`
6. `G60_MOBILE`

每一关流程：

1. 只实现当前关允许的组件。
2. 运行本地站点。
3. 截取该关目标桌面/生成桌面/目标移动/生成移动 4 张截图。
4. 写 `outputs/progress/stage-gates/<GATE_ID>.md`。
5. 运行 `validate_stage_gate.ps1`。
6. 分数未达 95%，停留本关继续修复，不得进入下一关。

## 工程验收

必须运行：

- `npm install`
- `npm run lint`
- `npm run typecheck`
- `npm run build`

若没有 lint/typecheck 脚本，需要补充合理脚本或记录原因。

工程通过只证明可运行，不证明视觉相似。最终 PASS 仍由阶段门禁和 `FINAL_SIMILARITY_GATE.md` 决定。
