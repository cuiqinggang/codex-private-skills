# B32 生产同构虚拟成熟：安全接力局部实测 V1

TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
TEST_CASE=B32_BENIGN_VIRTUAL_EXAMPLE_20261009
METHOD=B32/B29/B22；A28/共同ENGINE28不变
ENVIRONMENT=DESKTOP-4A1EGTM；普通chrome.exe；AutoHotkey v2 + 原有Descolada/UIA-v2；2026-10-09
RESULT=PARTIAL_READONLY_PASS
VIRTUAL_MATURE=NO
STOP_GATE=NOT_PASSED
FINAL_VALID=NO
REAL_SEND=NOT_RUN

## 统一案例和VALID
无真实业务副作用：校验 8+13+21=42 → 按合法TASK合同保存Freeze → 触发状态机将唯一NEXT_PAGE_PROMPT在原ChatGPT窗口的新聊天中一次发送 → 新聊天重新读取真实冻结并继续 → 最终核对。完整VALID要求不仅数学结果正确，还需真实Freeze、可靠新聊天接管和端到端耗时。本次**仅只读UI接力预检**，没有声称整案例完成。

## 可复核局部现实观察（各测试独立墙钟，不叠加为总任务耗时）
| 子案例 | 测得耗时ms | 实际证据/结论 |
|---|---:|---|
| 原B32适配器：有效虚拟信封在普通Chrome的只读预检 | 458 | BLOCKED:ACTIVE_WINDOW_NOT_CHATGPT，旧窗口标题验证误拦截；未发 |
| UIA.ElementFromChromium窗口内新聊天选择器 | 720 | 0，旧控件树入口不能定位 |
| UIA.ElementFromChromium界面结构 | 721 | Document/Edit/Button=0，失败路径 |
| 不存在的信封 | 167 | FAIL:PROMPT_NOT_FOUND；退出码12，未发 |
| 非法信封 | 178 | FAIL:UNVERIFIED_ENVELOPE；退出码13，未发 |
| UIA.ElementFromHandle窗口级控件探索 | 806 | 检出45个按钮；说明成熟UIA上游可访问 |
| UIA.ElementFromHandle地址栏/页面身份探索 | 1017 | 确认地址栏有chatgpt.com，且存在浏览器/页面控件；普通Chrome窗口非Chrome for Testing |
| 唯一“新聊天”控件选择器 | 1563 | 新聊天控件唯一匹配=1；未点击 |
| 修正最小适配后正常只读预检 | **1190** | DRY_RUN:NEW_CHAT_CONTROL_FOUND_NO_SEND；退出码0；通过 |
| 虚拟信封误带--commit参数的拦截 | **1251** | BLOCKED:TEST_ENVELOPE_COMMIT_FORBIDDEN；退出码21，未发 |
| GitHub 8个B32方法/动态状态文件并行读取 | **1962** | 8/8读取成功；是连接器调用+网络获取，不含新GPT理解/推理 |

## 已查明最小责任层和修复
GOOD=成熟 AutoHotkey v2 + 原有 Descolada/UIA-v2；BAD=旧B32适配器依赖Chrome活动窗口标题包含ChatGPT，并使用 ElementFromChromium 导致实际ChatGPT窗口误拦截。FIRST_DELTA=页面身份判断/控件树入口。
已将B32原适配器做**最小必要薄修复**：使用成熟 UIA.ElementFromHandle，不用窗口标题决定站点身份；验证有且只有一个Chrome地址栏属于chatgpt.com；原“新聊天”控件实际唯一；补齐当前输入框名称“询问 ChatGPT”；禁止虚拟测试信封走真实提交。无n8n、无9223/18931、无另开浏览器、无新通用状态机。仓库现行 `routes/B/adapter/B32_Handoff.ahk` 已更新；Windows同路径同步。初次改动有正则转义错误导致只读预检被安全拦截，修正规则后预检PASS；未曾真实发送。

## 时间模型和缺失项
唯一合法极限T*=min(T_VALID)；在完整VALID未成立前，**不能输出T_B_VALID、T_VIRTUAL_BEST、DELTA_T、SPEEDUP，也不能证明物理极限**。
可观察的局部样本：UI安全预检1190ms；同一条件的8文件并行读取1962ms；目前接力脚本在有授权的commit路径还包含450ms+350ms固定等待（800ms），未执行该路径。三部分机械相加得到3952ms**仅是不同运行条件下的条件化部件预算，不是端到端实测、也不是物理下界**。其他未知至少包含实际Freeze落盘/并发校验、新聊天创建、粘贴提交、响应接管、节点执行、质量验证、恢复与失败代价。
备选成熟方法仅在当前约束内选择：1）保留已验证的AutoHotkey v2+UIA-v2（当前优选）；2）Windows Power Automate Desktop虽提供成熟元素选择，但新增安装/工作流成本不具已测净收益；3）ChatGPT桌面快捷键属于另一客户端，不能假设能替代当前浏览器按钮。不要为节约几百毫秒提前引入新组件。
最大净收益缺口当前为**从“安全识别按钮”到“安全一次提交并确认新聊天接管”**。下一轮只针对当前成熟控件验证业务无副作用的真实一次接力，先取得冻结后授权和可靠回执；其次再做多节点含一次失败修复的完整生产同构虚拟重放。验证稳定后才考虑用成熟WaitElement替换固定Sleep；不得缩短等待而牺牲VALID。

## 冻结判断
METHOD=B32保留；SCENARIO_DESIGN=YES；READONLY_UI_PREFLIGHT=PASS；REAL_CHAT_HANDOFF=UNVERIFIED；COMPLEX_END_TO_END=UNVERIFIED；VIRTUAL_MATURE=NO；FINAL_VALID=NO。
