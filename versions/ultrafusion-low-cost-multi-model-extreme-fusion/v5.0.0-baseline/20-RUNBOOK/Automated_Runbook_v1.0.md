# UltraFusion 自动化执行手册 v1.0

**版本**: v5.0
**最后更新**: 2026-06-17 00:33:24
**定位**: 此文件是 UltraFusion 正式自动化执行手册

---

## 🚫 硬规则

**UltraFusion 正式执行禁止用户手工粘贴 A/B/C/D。**

旧版手工流程（Phase 0 — 手工运行 RUNBOOK v2.0）已归档至：
`90-ARCHIVE/legacy_manual_runbooks/Legacy_Manual_Runbook_ARCHIVE_ONLY.md`

用户不应手动执行以下被废止的操作：
- ❌ 手工打开多个 AI 模型网页
- ❌ 手工复制 V15 到多个模型
- ❌ 手工粘贴 A/B/C/D 模板
- ❌ 手工拼接多个模型答案
- ❌ 手工评分

---

## 正式执行方式

### 方式一：Hermes Agent 自动化编排

```bash
# Hermes 加载 UltraFusion 技能后自动执行
"Use ultrafusion-low-cost-multi-model-extreme-fusion to answer: <user question>"
```

Hermes 自动完成：
1. 加载 V15_Guard_Prefix + V15_FULL
2. 对 Core-3 模型逐层执行 A/B/C/D
3. 每层自动拼装 prompt
4. 验证 V15 注入
5. 输出 D_Final_Ultra_Answer_Final

### 方式二：Codex CLI 自动化编排

```bash
codex exec --skill ultrafusion-low-cost-multi-model-extreme-fusion "回答: <question>"
```

### 方式三：Provider Adapter API 调用

通过各 Provider Adapter 直接调用模型 API：
- GPT: 官网套餐浏览器自动化
- DeepSeek: 官方 API
- MiniMax: 官方 API
- Qwen: DashScope API (观察位)

---

## 自动化执行流程

### Phase 0：预检
1. 加载 `10-SPEC/V15_Guard_Prefix_v1.0.md`
2. 加载 `10-SPEC/V15_FULL_v1.0.md`
3. 计算 V15_SHA256 并记录
4. 确认 Core-3 模型可用性
5. 生成 run_id

### Phase 1：A 层
对每个可用模型自动：
- 拼装 A_prompt = V15_Guard + V15_FULL + A_Template + Question
- 发送给模型（GPT/DeepSeek/MiniMax）
- 收集 `A_<model>_Extreme.md`
- 记录模型状态码（PASS/PARTIAL/EMPTY/...）
- 检查至少 2 个模型 PASS

### Phase 2：B 层
对每个 PASS/PARTIAL 模型自动：
- 拼装 B_prompt = V15_Guard + V15_FULL + B_Template + Question + All_A_Drafts
- 发送给模型
- 收集 `B_<model>_Extreme.md`

### Phase 3：C 层
融合层自动：
- 拼装 C_prompt = V15_Guard + V15_FULL + C_Template + Question + All_B_Drafts
- 发送给 C 层执行模型
- 输出 `C_Fusion_Extreme.md`（V15 驱动的融合极限稿）

### Phase 4：D 层
最终层自动：
- 拼装 D_prompt = V15_Guard + V15_FULL + D_Template + Question + C_Fusion
- 发送给 D 层执行模型
- 输出 `D_Final_Ultra_Answer_Final.md`（V15 驱动的最终稳定极限稿）
- D_Final 是唯一最终报告，不再生成 E 层

### Phase 5：验收
自动执行：
- 检查 V15 注入：4/4 层
- 检查 D_Final 结构完整性
- 记录评分与扣分
- 标记 GPT 状态（PASS/UNAVAILABLE）
- 输出 D_Final

---

## 自动保存内容

每次运行自动保存以下制品：
- A 层极限稿（每个模型的）
- B 层极限稿（每个模型的）
- C_Fusion_Extreme.md
- D_Final_Ultra_Answer_Final.md
- prompt manifest（每层的 assembled prompt）
- V15 注入验证结果（每层）
- 模型状态记录
- 扣分与贡献记录

---

## 模型失败处理

按 `35-MODEL-ROSTER/Model_Failure_And_Skip_Rules_v1.0.md` 自动处理：
- EMPTY → 跳过
- LOW_QUALITY → 不进入 C_Fusion
- ERROR/RATE_LIMITED/AUTH_FAILED → 启用替补模型
- GPT UNAVAILABLE → D_Final 标注"GPT 质量锚点缺失"
- <2 模型 PASS → D_Final 标注"受限融合"

## 关键约束
- D_Final 是最终报告，不生成 E 层
- A/B/C/D 全部自动注入 V15_FULL
- C_Fusion 是 V15 驱动融合极限稿，不是普通合并
- D_Final 是 V15 驱动最终稳定极限稿
- 禁止伪造缺失模型的回答

## 2026-06-28 Runtime Parameter Rule: Full ABCD Test

Current default for actual UltraFusion-style testing is full A/B/C/D.

`A_ONLY_CORE2_FUSION_TEST` is paused as default and should only be used when explicitly requested.

Runtime temperature/token policy:

`45-RUNTIME/ABCD_Temperature_And_Token_Strategy_v1.0.md`

Do not modify V15 source text. Temperature is a runtime parameter only.

Temperature descends from A to D:

`A/B maximize independent divergence; C/D maximize correctness and stability.`

Defaults:
- A = 0.70
- B = 0.60
- C = 0.35
- D = 0.20

B is one layer. It reads all valid A extreme drafts and each participating model directly generates its own B-layer extreme draft. Do not split B into sublayers or two-step variants.

`max_tokens` is not fixed yet. Record settings, actual output length, truncation, verbosity, and V15 impact during full-flow tests.
