# B32 真实无发送检测与两种侧栏状态证据 V1

TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
STATE=READONLY_REALITY_OBSERVATION
METHOD=B32/B29/B22
REAL_CHAT_CLICK=NO
REAL_SEND=NO
REAL_HANDOFF_VALID=NO
VIRTUAL_MATURE=NO

## 时间顺序
先按B32无固定等待规则执行16个确定性虚拟状态场景，16/16预期决策一致，见`scenarios/B32_NO_FIXED_WAIT_VIRTUAL_REPLAY_V2.md`；冻结B32-VM-F004后，再使用已有普通Chrome与现有AutoHotkey/UIA脚本做**仅只读无发送检测**。

## 现实只读结果
- 原 `B32_Handoff.ahk` 用有效虚拟交接信封、**不带--commit**调用：`BLOCKED:AMBIGUOUS_NEW_CHAT`，`READONLY_EXIT=15`，调用墙钟`950ms`。安全阻止点击和发送，不能认定接力通过。
- 已存在的 `B32_Direct_Selector_Perf.ahk` 在同一原普通Chrome只读单个精确Button{Name=新聊天}：找到元素`X=58,Y=229,W=276,H=35`，连续三次单控件定位`32/46/32ms`，UIA根初始化`15ms`，内部总计`125ms`。该结果只证明找到**第一个**精确控件，**不能证明当前恰好一个可见目标**。前一轮收起侧栏测试曾读到一个36×36的图标控件（X60,Y129）；布局确实不同。
- 两项读操作未执行Ctrl+V/新聊天Click/Enter。进一步枚举控件的工具调用被阻拦，未冒充完成第二项确认。

## 精确根因边界
现有适配器循环多个候选名字计数；布局变化时返回AMBIGUOUS_NEW_CHAT。需要用现成UIA库按精确语义按钮名+可见属性过滤，并验证唯一性；不要靠坐标，不能仅用FindElement第一个结果代替唯一性。当前正式脚本依旧含450ms+350ms固定Sleep；更新为就绪检测的代码写入先前受限，故实装尚未完成。

## 结论
规则级虚拟场景16/16_PASS；真实只读检测已执行但发现有效的安全拦截；执行代码与“无固定等待”冻结方法还不一致。继续保留B32，不宣布VIRTUAL_MATURE/FINAL_VALID。下一真实写入/换聊必须在最小适配解决多按钮歧义、动态就绪检测已部署且用户授权后才进行。
