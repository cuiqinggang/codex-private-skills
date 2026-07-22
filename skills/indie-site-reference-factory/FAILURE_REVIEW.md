# FAILURE_REVIEW

## 2026-07-09 real Framer gate test: image proof must be shown per gate

### Symptom
During the real Framer-inspired clone test, the workflow could have silently treated internal screenshots as "already handled" without showing them to the user. The user correctly required every gate to publish a comparison image, a percentage score, and the pass/block decision before moving forward.

### Gate failures caught
- G30_PRIMARY_VISUAL initially scored Desktop=95%, Mobile=76%, Overall=87%; the gate script returned STATUS=GATE_BLOCKED.
- G50_FIRST_SECTION initially scored Desktop=89%, Mobile=78%, Overall=85%; the gate script returned STATUS=GATE_BLOCKED.

### Correction rule
- A visual gate is not complete until the chat contains the comparison image path, desktop/mobile/overall percentages, deduction logic, and script result.
- Blocked attempts may be documented, but the current gated score must appear before historical blocked scores so validators do not misread stale failure values.
- Target cookie banners and other capture pollution must be documented in G00 and excluded from scoring; they must not be cloned.
- Visually valuable reference sites require rich lower-section/card evidence, not only a good hero.

## 记录入口
- 真实 URL 访问失败
- 截图缺失
- build 失败
- 移动端布局崩坏
- 保留参考站品牌资产
- QA 任一项低于 7

## 2026-07-09 失败复盘：自由发挥导致不像

### 现象
真实测试中，目标站 Framer 是黑色沉浸式居中 hero、蓝色发光 prompt、chips、canvas UI；生成站第一版却是浅色左右分栏 SaaS 站。用户复核指出“完全不是一个东西”，复核成立。

### 根因
1. 技能包没有强制 `outputs/progress/` 执行进度包。
2. 没有先生成目标站几何规格，就开始编码。
3. 没有按组件分段截图对比，而是一次性写完整页面。
4. 把 build、合规、工程完整混入视觉相似度，导致错误高分。
5. 移动端没有独立复刻，直接继承桌面结构。

### 修正规则
1. 缺 `00_TARGET_BASELINE.md`、`01_GEOMETRY_SPEC.md`、`02_COMPONENT_SPECS_INDEX.md`、`03_BUILD_PLAN.md` 时，禁止编码。
2. 每轮必须发目标截图、生成截图、桌面/移动/综合相似度百分比。
3. 低于 95% 只能是 `PARTIAL_SIMILARITY` 或 `FAIL_SIMILARITY`。
4. 缺进度包或截图证据时，必须是 `INVALID_TEST`。
5. 不能再使用“参考结构”掩盖“克隆不像”。

## 2026-07-09 失败复盘追加：只有最终验收不够

### 现象
用户指出技能包虽然有流程说明，但没有足够强的逐关门禁，执行者仍可能随意探索、最后才截图打分，导致低相似度结果冒充通过。

### 修复
新增同级制阶段门禁：G00/G01/G02/G03/G10/G20/G30/G40/G50/G60。每一关必须有独立证据、截图、百分比、扣分逻辑和脚本判定。任一视觉关低于 95% 必须停留当前关，不能进入下一关。

### 验证
G10 低分烟测 Desktop=78%、Mobile=42%、Overall=64%，脚本输出 STATUS=GATE_BLOCKED。最终门禁现在要求所有阶段报告并复查视觉关分数。
