# 自动化 A/B/C/D 极限工作流 v5.0

## 执行流程


### Phase -1：Search Gate 预检

1. Router 判断是否需要搜索；
2. 需要搜索则先建立 Search_Fact_Pool；
3. Search_Fact_Pool 供 A/B/C/D 四层共用；
4. B 层和 C 层默认复用 Search_Fact_Pool，不重复搜索；
5. D 层终审检查 Search_Fact_Pool 是否覆盖关键事实；
6. 若 D 层发现关键事实缺口，可追加搜索；
7. 搜索不到或结果矛盾，必须在 D_Final 中标注。

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
