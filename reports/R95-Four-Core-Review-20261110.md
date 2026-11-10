# R95：四路成熟配置对照与物理时间参照

日期：2026-11-10（北京时间）。任务：PI-R95-FOUR-CORE-20261110-F2。

**结果：四路固定归档与默认四路CLI入口均验收通过；本轮没有找到可信的新极限时间，也没有取得稳定的新提速。保留A：四路由Windows调度、原串行最终核验，内存按需使用。**

## 方法与固定合同

已读取[《三人行》V5原文](https://github.com/cuiqinggang/codex-private-skills/blob/main/skills/artificial-single-page-extreme-time-engine/SANRENXING_V5.md)，Freeze SRX-V5-F001-20261020，blob 87480d7c4937facbaaec53ac4e44b26379ddb3dd。实际有主控执行、资料、独立审计三个上下文与回传；不把ECC历史版本或另一套第一性引擎冒充本方法，不扩大原方法PARTIAL认证边界。

同R94的128项唯一标记输入，每项48文件；4个持续worker，每路32项。原完整match、原归档算法、原workspace-write沙箱、原QA及固定4线程外部QA保留。仅比较两个成熟配置因素：worker亲和性、CLI内部最终逐项QA的串行/4线程执行。聚合签收仍由单控制者写入。

预注册顺序A/B/C/D/D/C/B/A，每档2批；完整源码在F2前冻结，18项指纹最终独立复核全部一致。没有删除慢样本。

## 8批结果

主计时：输入和请求就绪，CLI启动前→执行→原QA→独立QA→结果写入读回。数据复制另列；不是用户发出需求到最终答复的整体时间。

| 配置 | 第1批 | 第2批 | 平均 | 含输入复制平均 |
|---|---:|---:|---:|---:|
| A 自动调度＋串行最终QA | 01:18:622 | 00:58:729 | 01:08:676 | 01:33:586 |
| B 每核一路＋串行最终QA | 01:43:372 | 00:56:742 | 01:20:057 | 01:46:781 |
| C 每核一路＋并行最终QA | 01:27:021 | 00:48:221 | 01:07:621 | 01:36:582 |
| D 自动调度＋并行最终QA | 03:39:511 | 00:36:094 | 02:07:802 | 02:33:905 |

8批1024/1024合格，49152份文件检查通过。各批确有4个不同worker PID与各32项；绑核组实际读回核0/1/2/3，自动组每worker可用0/1/2/3。

按预注册输入就绪后的均值，**C暂优**；原ANALYSIS.selected=C完整保留。C仅比A少1.055秒、约1.54%，两轮比较方向反转，D单次从219.511变到36.094秒，性能明显时变。不能把均值差都归因配置，更不能把最短一次封为稳定极限。

**采用决定另记A。** 没有稳定净收益证据时保留简单已验基线；含复制口径A均值也更低。没有把A改写成本轮主口径最快。

## 第一性参照与内存

本机实读i5-3570、4物理核/4逻辑线程，约32GB内存。固定总工作量的时间参照应考虑CPU工作/可用核数、必经依赖链、必要I/O及协调；四个worker不意味着独占四个核，绑核也不创造独立磁盘吞吐。

实测各批worker job累计CPU时间÷4为**00:06:277—00:07:008**。这只是既有实现的局部CPU理想并行参照，排除了Node、控制器、OS其他工作、I/O等待、最终QA；不是整批物理下界，也不是可承诺交付时间。I/O带宽、元数据延迟和完整关键链尚未建立足够证据，整批物理极限保持NOT_PROVEN。

每worker峰值工作集**26.070—27.676MiB**，系统各批开始时可用内存约6.78—8.48GiB。不是整个进程树同步峰值。没有容量不足证据支持硬分或预占每路8GB；保留独立进程/目录，内存按需使用。

本轮最短合格单次为D的00:36:094。旧R94四路最短00:24:040是另一轮环境观测，保留历史，不跨轮相除宣称提速。

## 失败、成熟修正与投入

F1 A合格69.566秒；F1 B在业务前失败3.922秒，原因是psutil setter调用OpenProcess被原沙箱拒绝。失败及输入准备投入保留，不参与F2成功排名。

按微软文档改用GetCurrentProcess→SetProcessAffinityMask→GetProcessAffinityMask；先在原workspace-write沙箱内验证掩码1/2/4/8及恢复15，再创建F2新快照、从基线重跑完整矩阵。不提升权限、不改ACL/沙箱/代理。F1源码和回执未覆盖。

从F1 A已记录起点到F2末批读回的跨度为**19:43:259**，含失败、诊断、修正、等待及全部F2批次；不含更早检索和后续审计发布，不冒充完整TASK_ACCEPTED→FINAL_VALID。

## 实际CLI入口验收

本机入口：
C:/Users/A/Documents/DSH-Workspace/pi-single-dual-r89-20261110/r95-four-core/four_lane_entry.py

仅显式固定归档快路默认4路，采用A；未改全局Pi的任意自然语言任务默认分派。由GPT/Pi生成合同和独立lane目录后调用：

```text
<固定Python> <上述入口> --fast-archive-batch <绝对requests.json> --cwd <本批工作区> --stream-lanes
```

实际验收未传--workers，仍为4个worker，各32项，退出全部0；128/128、6144文件通过全部原检查及外部读回。版本入口另实测返回omp/18.18.0。

原始功能验收耗时：
- 输入复制准备10:46:324。
- 输入就绪至最终独立读回09:48:378。
- 含准备20:34:702。

该批处于宿主慢响应和额外复读并行阶段，仅作功能验收，不加入8批速度榜，不能隐藏长耗时或称获得提速。目录命令也曾明显延迟；后续原始目录读回显示请求持续写入、EXECUTION生成、最终签收完成。共享资源/宿主负载波动有证据，尚不能断定唯一磁盘根因。

## 最终独立审计与资源仲裁

独立审计PASS：18项源码、1024项原QA/ZIP/manifest/产物哈希、49152个ZIP成员；另抽查64项原输入，共3072文件。其余原输入由各批外部全量QA验证，本独审没有再次全部读取。

额外复读与入口验收并行时宿主明显变慢。仅暂停并恢复本审计进程PID9664，核对创建时间和命令标记；不终止、不重跑、不改变标准，不碰其他任务。暂停北京时间21:15:05.050，恢复21:23:32.727，暂停08:27:677。恢复前后CPU和I/O计数一致，之后原session432退出0。

独审完整墙钟22:14:890，包含暂停。它和入口验收有重叠，不能简单相加为总耗时。完整用户任务T_VALID未统一计量，保持NOT_MEASURED。收尾经验：额外全量复读与大批输入复制应先按共享资源审查是否并行，不把上下文独立当作资源独立。

## 证据与停止裁决

- [比较机器证据](assets/r95/R95-Comparison-Evidence.json)（完成比较时快照；当时附加审计/入口尚在运行）。
- [最终独审回执](assets/r95/R95-Final-Audit.json)。
- [CLI入口验收](assets/r95/R95-Entry-Acceptance.json)。
- [实际执行源码快照](assets/r95/R95-Source-Snapshot.json)（重建时优先于历史适配脚本）。
- [独审源码](assets/r95/r95_independent_audit.py)、[四路入口源码](assets/r95/four_lane_entry.py)。

原始本机目录：C:/Users/A/Documents/DSH-Workspace/pi-single-dual-r89-20261110/r95-four-core；F1在run，正式F2在f2/run，入口验收在f2/acceptance。全部Freeze、RESULT、EXECUTION、DELIVERY、trace及实际文件保留。

**本轮停止扩搜和追加速度试验：已验成熟候选没有形成足够可信的整批净收益。四路程序与入口内容验收PASS；稳定新增提速、整批物理极限未认证。**

成熟依据：[Windows当前进程句柄](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentprocess)、[进程亲和性](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setprocessaffinitymask)、[Python线程池](https://docs.python.org/3.13/library/concurrent.futures.html)。沿用已装依赖，没有升级工具。
