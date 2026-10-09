# B33 现实基线专属无业务测试合同 V1
TASK_ID=B33_BASELINE_REAL_20261010_T02
CONTRACT_VERSION=1
ROUTE=B
METHOD_ENGINE=B33
METHOD_BRAIN=B29
METHOD_TEMPLATE=B23
MODE=MANUAL_BASELINE_REALITY_NOT_FINAL_OPTIMIZED_REALITY
SCOPE=INDEPENDENT_TEST_ONLY
ORIGINAL_B33_TASK_UNCHANGED=YES
TEST_INITIAL_WORK_START_UTC=2026-10-09T19:13:43.482Z

## 原始目的
实测B33的有真实ChatGPT模型参与的最简成熟恢复流程：第一GPT页面真实完成一个小型可复核节点→GitHub保存Freeze/CURRENT→用户在独立的新ChatGPT聊天一次手动发送唯一四字段短码→新GPT独立从网络仓库重新读合同/Freeze，继续完成固定测试结果并写入最终状态。记录能观察到的真实起止时间，不允许以模拟网页或预检秒数代替。
本轮为受控人工基线（MANUAL），不是B33要求的自动新聊天正式最终Reality。它能校准真人介入、新GPT启动/恢复/计算一段的现实开销；不等于全自动生产合同已通过。

## 唯一输入与第一节点已知事实
数据=[8,13,21,34,55,89,144,233,377,610,987,1597]，共12项，索引从1开始；需要独立计算四个可验收量：
COUNT=12
SUM=4168
WEIGHTED_SUM=sum(i*x_i)=43428
ALTERNATING_SUM=sum((-1)^(i-1)*x_i)=-984
EVEN_POSITION_SUM=2576
第一节点已由当前GPT实际完成，并读取主任务B_SINGLE_PAGE_MATURITY_20261009的CURRENT，确认为B33-VM-F015、B33/B29/B23且VIRTUAL_MATURE=NO。
下一节点不能只抄这些预期值：重新根据数组计算全部值并核对；核验CURRENT及Freeze相互一致、签发本测试任务的最新冻结号；只在当前指向F001且没有F002时按合同追加不可变F002与CURRENT，避免双写。允许对测试任务自己的GitHub文件进行写入，不操作其他TASK。

## DONE_WHEN
新GPT独立读取线上路径，计算并核验5项数值，保存本测试TASK的F002和CURRENT，输出ACK-B33-BASELINE-T02；记录T0、READY和ACK阶段的UTC时间及所有未观测延迟。若任何状态/权限错误，立即输出BLOCKED及所处阶段，不伪造ACK，不重发同一短码。
若仅完成手动恢复，本任务最终标记MANUAL_BASELINE_VALID=YES，AUTO_HANDOFF_VALID=NO，绝不改变主任务F015的VIRTUAL_MATURE和FINAL_VALID。
全程时间包含用户打开新Chat和粘贴耗时，不把GitHub每次读写原始耗时替代完整成绩。

## 边界
不修改FlClash，不启动专用浏览器，不调用n8n，不接触生产ChatGPT现有聊天，不解锁B33_Handoff.ahk --commit；不尝试通过不同工具规避此前ChatGPT自动发送安全审查。不重发历史UNKNOWN码。用户只需在自己原生ChatGPT界面合法新建一个独立聊天并发送唯一短码一次。
