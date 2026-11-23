# 自动化 A/B/C/D 极限工作流 v5.0

## 执行流程

### Phase 0：预检
1. 加载 V15_Guard_Prefix
2. 加载 V15_FULL
3. 验证 V15_SHA256
4. 确认 Core-3 模型可用性
5. 生成 run_id

### Phase 1：A 层
1. 对每个可用模型：
   - 拼装 A_prompt (V15 + Template + Question)
   - 发送给模型
   - 收集 A_<model>_Extreme
   - 标记状态码
2. 检查：至少 2 个模型 PASS

### Phase 2：B 层
1. 对每个 PASS/PARTIAL 模型：
   - 拼装 B_prompt (V15 + Template + Question + All A drafts)
   - 发送给模型
   - 收集 B_<model>_Extreme
2. B 层输入必须包含所有有效 A 层极限稿

### Phase 3：C 层
1. C_Fusion 输入 = 所有有效 B 层极限稿
2. 拼装 C_prompt (V15 + C_Template + Question + All B drafts)
3. 发送给 C 层执行模型
4. 输出 C_Fusion_Extreme

### Phase 4：D 层
1. D_Final 输入 = C_Fusion_Extreme + 用户问题
2. 拼装 D_prompt (V15 + D_Template + Question + C_Fusion)
3. 发送给 D 层执行模型
4. 输出 D_Final_Ultra_Answer_Final

### Phase 5：验收
1. 检查 V15 注入：4/4
2. 检查 D_Final 结构完整性
3. 记录评分与扣分
4. 标记 GPT 状态
5. 输出 D_Final
