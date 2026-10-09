# B32 冻结状态V6：成熟UIA动态就绪、真实只读校验

TASK_ID=B_SINGLE_PAGE_MATURITY_20261009
FREEZE_ID=B32-VM-F006
PREVIOUS_FREEZE=B32-VM-F005
FREEZE_VERSION=6
CONTRACT_VERSION=2
METHOD_ENGINE=B32
METHOD_BRAIN=B29
METHOD_TEMPLATE=B22
METHOD_REF=a2c3c99d38b034e742f81cb2292db1729b346360
STATUS=IN_PROGRESS
VIRTUAL_RULE_REPLAY=16/16_PASS
ADAPTER_PATCH_STATUS=LOCAL_AND_GITHUB_SYNCED
STATIC_REGRESSION=PASS
READONLY_UI_PREFLIGHT=PASS_WHEN_TARGET_ACTIVE
REAL_HANDOFF=BLOCKED_TARGET_CHAT_NOT_VERIFIED
VIRTUAL_MATURE=NO
FINAL_VALID=NO
T_B_VALID=UNKNOWN

## 冻结事实
用户确定：“代码对代码”语义控件访问，不靠图片，不因侧栏折叠状态或按钮尺寸开两套规则。普通Chrome、AutoHotkey v2、现有UIA-v2四步不变。
本机AHK与GitHub适配器已经实改：精准可见且可用的“新聊天”Button、动态输入框就绪、粘贴内容完整读回、一次发送、错误窗口和旧会话地址保护。旧Sleep450/Sleep350已删除。未开发新状态机，不动Codex/n8n/9223/代理。
16个虚拟故障场景是规则一致性测试，16/16_PASS而非完整虚拟成熟。无发送真实检测在正确ChatGPT前台时通过，后续当前前台变为Windows Explorer，普通Chrome当前标签非ChatGPT且14个TabItem中不能确认哪个是本任务标签，因此正式无业务烟雾交接没有执行，不能冒称FINAL_VALID。
独立无业务测试 TASK_ID=B32_UI_HANDOFF_SMOKE_20261009 的Freeze/CURRENT已真实保存；真实提交次数=0。
证据：skills/artificial-single-page-extreme-time-engine/scenarios/B32_MINIMAL_UIA_EVENT_READY_ACCEPTANCE_20261009.md

## 后续唯一事项
在可以唯一确认目标原Chrome ChatGPT标签时，用已冻结无业务测试信封做一次完整真实四步交接，分别记录新聊天路由就绪、粘贴全文核验、一次发送、会话接收证据及完整T_VALID；如目标不可确认则停止而非乱点。无需更改B32架构；GitHub冻结即时，K盘三日备份独立。
