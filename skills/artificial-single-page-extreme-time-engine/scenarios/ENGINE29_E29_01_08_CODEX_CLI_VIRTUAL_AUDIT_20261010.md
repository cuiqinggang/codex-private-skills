# ENGINE29｜E29-01~08：Codex 独立会话并行虚拟审核证据
日期：2026-10-10（Windows 本地 UTC+08:00）
任务批次：ENGINE29_CEO_GPT_CODEX_HYBRID_VIRTUAL_20261010
来源：用户已授权的独立 Codex CLI 审核会话与远端终端输出
仓库：cuiqinggang/codex-private-skills
CASE_COUNT=8
CLI_SESSIONS_RETURNED=8
ACTUAL_GPT_BROWSER_EXECUTION=NOT_TESTED
FULL_SAME_CONTRACT_G_C_H_BENCHMARK=NOT_TESTED
VIRTUAL_DESIGN_REVIEW=8/8_RETURNED
VIRTUAL_MATURE=NO
FINAL_VALID=NO
PUBLIC_ENGINE29_ACTIVE=NO
T_VALID_REAL=UNKNOWN

## 方法与边界
GPT 已于本次通过 GitHub 官方工具独立回读：公共 ENGINE.md=28版；A路线独立激活A29，B路线独立仍为B33。统一公共 ENGINE_V29_DRAFT.md 是未激活草案，包含G=GPT、C=Codex、H=混合与最多三级拓扑。待验收草案已增补 1/3/5/8 并行度候选并回读确认，提交 d70da9cbd8ac4b16e7e6458a970556591d34b8a3。

授权边界：Codex 本次只接收任务自身包含的事实与离线合同，明令不调用工具、不访问当前用户浏览器、不读取前次因安全策略拒绝的本地 snapshot.md、不修改GitHub，也不自动提交ChatGPT消息。其审核结论不代表实际GPT专用浏览器执行。不存在Codex已实时监控GPT任务的证据。

正式有效批次是在入口修复后依次启动E29-01单路定位校验、再并发启动E29-02至E29-08七路独立CLI会话。它们不是固定8路同时起跑的同负载竞赛，也不能证明8路比3路快。最初8路尝试均因缺四字段页面定位门禁而未做有效审核；该问题在正式批次前修复。此前还出现过stdin未关闭，已改为PowerShell标准管道向原生 codex exec 提交UTF-8任务。

## 8个独立任务的已返回结论（均为虚拟设计审核）
| 编号 | 核心合同 | 返回结论与最强反例 | Codex进程运行时间* |
|---|---|---|---|
| E29-01 | 单CEO简单问答 | 简单任务直接完成更简洁；如要求真实仓库当前状态，概念回答不能冒充实测 | 133.43秒 |
| E29-02 | 三节点/Freeze接力 | 保存失败时旧指针仍指上一节点，新旧会话并行写入应FAIL | 137.64秒 |
| E29-03 | A29 CEO +1~3 Executor标签 | 共享焦点误选与双重认领导致错标签/多写者应FAIL | 134.05秒 |
| E29-04 | 总CEO→3模块CEO→各2 Executor | 模块直接写主CURRENT、共享文件旧版本覆盖应FAIL | 139.65秒 |
| E29-05 | G/C/H同缺陷代码修复 | 统一Python区间合并函数合同；删除失败测试来伪装最快应FAIL | 137.40秒 |
| E29-06 | GPT执行、Codex监管 | 仅凭GPT自述和Codex复述不能证明外部动作成功，需授权事件源 | 136.74秒 |
| E29-07 | 公共28/A29/B33/公共29兼容 | 把A29路由激活误当公共29激活、混用method/state、双写均FAIL | 138.33秒 |
| E29-08 | 1/3/5/8+G/C/H公平计时合同 | 不能仅报最快单项或给混合组特殊缓存/免复核优惠 | 139.64秒 |

*该列来自Codex CLI最后返回的进程runtime，包含启动与严重网络重连等待，不是自然业务任务的同合同T_VALID，不能用于G/C/H排名。E29-02至08运行期间存在会话重叠，但并非7路同刻启动且负载不同，不能推出任何并行度加速比。

## 可复核现场运行环境
- Windows设备：DESKTOP-4A1EGTM；Codex CLI=0.160.0；本次模型日志显示gpt-6.1-sol、OpenAI提供方；只读沙盒；终端提示已登录ChatGPT。
- 工作目录：C:\Users\A\Documents\Codex\ENGINE29_READONLY_20261010\E29_PARALLEL_CASES\
- 独立CLI输出报告：E29-01_report.txt 至 E29-08_report.txt；独立任务输入：E29-01.txt 至 E29-08.txt；入口：run-one.ps1。
- 所有本批Codex会话报告完成，退出码0；但这只能证明有审核文本，不证明G/C/H工作流/浏览器端执行和时间目标达成。
- 每次启动均报告有2份Codex技能包缺少YAML frontmatter，另外有技能上下文预算移除警告；尚未认定这些就是高延时根因。
- 多个会话记录 Reconnecting 2/5...5/5、WebSockets回退HTTPS与 request timed out；E29-01单独启动也有此现象。故不能将重连必然归罪于8路同时运行，也不能据此得出Codex在正常网络条件下固有慢于GPT。
- 用户代理、Chrome Profile、现有聊天与B33 PROTECTED_CHAT_HARD_STOP保持不变；Codex未获得未授权的ChatGPT跨页发送/关闭能力。

## 审核后的最小待验收事项
1. 按任务相同输入、相同真实VALID、同等权限与稳定连接分别开展GPT主导G、Codex主导C、混合H的正式执行测量；先确定成熟GOOD现实基线并记录完整过程，不把此次虚拟文稿作业务成功。
2. 用E29-05同等代码缺陷、E29-02三节点接续和E29-03标签隔离等足够真实的典型任务做完整独立验证；一旦调用被拒绝，停止被拒动作，不改用其他渠道规避。
3. 用1/3/5/8并发度测真实批次墙钟、合法最终有效比例、资源争用与恢复成本；保持原生调度，不重新开发通用任务调度器。
4. 只有在授权且目标浏览器标签唯一归属的前提下才允许GPT专用浏览器现实执行；此前只能记GPT_BROWSER_REALITY=NOT_TESTED。Codex真实监控必须取得合法独立的审计日志/回执事件源。
5. 公共29版正式激活前继续按REUSE_GATE→基线现实→连续虚拟成熟→Freeze→一次最终Reality的门禁；公共ENGINE28、A29/B33指针与旧任务Freeze不动。
