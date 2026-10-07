# NODE_FREEZE
NODE_FREEZE_ID=MSVM-R2-N1
TASK_ID=METHOD-SYSTEM-VIRTUAL-MATURITY-20261007
PARENT_FREEZE_VERSION=3
NODE_GOAL=成熟抖音产品的输入与执行路线
STATUS=PASS
VIRTUAL_LOOP=COMPLETE
STOP_GATE=PASS

## 冻结方案
- 用户路径：复制抖音分享链接→双击桌面入口→后台自动处理→桌面产生新MP4。
- 输入：剪贴板分享链接，短链需解析为可用抖音目标。
- Route A：优先成熟直接/公开解析路线。
- Route B：A失败时才进入既有后台浏览器/专用profile媒体捕获回退。
- 浏览器不得可见闪窗；不得预热第二套persistent browser。
- exactly-once：一次正式入口只启动一次，失败不得原地补跑同一Reality。
