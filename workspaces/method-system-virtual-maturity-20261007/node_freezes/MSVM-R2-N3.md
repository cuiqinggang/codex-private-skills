# NODE_FREEZE
NODE_FREEZE_ID=MSVM-R2-N3
TASK_ID=METHOD-SYSTEM-VIRTUAL-MATURITY-20261007
PARENT_FREEZE_VERSION=5
NODE_GOAL=合并输入路线与最终媒体合同，形成首个整体Reality Freeze
STATUS=PASS
VIRTUAL_LOOP=COMPLETE
STOP_GATE=PASS

## 整体冻结方案
1. 读取剪贴板并标准化分享链接。
2. 先Route A；仅在A失败时进入后台浏览器Route B。
3. 捕获媒体候选并分类。
4. 下载到staging。
5. 独立ffprobe验证video+audio及兼容编码。
6. 通过后atomic publish桌面；否则FAIL并返回Reality Delta。
7. 正式Reality只执行一次，不现场修复。
