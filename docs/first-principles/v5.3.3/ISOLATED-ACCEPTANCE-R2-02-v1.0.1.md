# R2 第02号独立页面验收合同 — 修补 v1.0.1

## 范围与状态

母引擎 v5.3.3；本次只修验收来源入口接入，并冻结独立页面测试安排。不是整版最终认证。唯一目标 T*=min(T_VALID)。原 R2 业务、C3 成熟路径、旧第01轮原始证据保留。旧人工1次归因为争议待核，不能继承为新轮事实，也不能改写为已认证零次。

本次 GPT 宿主实跑：原22项+新增正式监督器入口28项=50/50通过；6个最终证据布尔门64/64组合正确；绕过入口门、信任裸标签、忽略回执绑定3/3变异均被回归检出。100次合成入口测量：最小0.009713ms、中位0.0103375ms、P95 0.01434ms、最大0.52508ms，仅为GPT宿主局部代码耗时，绝不是浏览器或完整闭环T_VALID。完整闭环虚拟工程目标保留60000ms，不是失败阈值。

截至冻结：本机安装、新对话创建、生产同构完整真实闭环均未运行。虚拟成熟范围是本修补代码和执行合同；本机能力与最终成功必须现实验收。

## 页面定位（本轮用户已明确要求）

控制页/命令Locator使用：极限短时间 v5.3.3冒烟 R2。
控制会话ID：6ab94118-27c8-83ea-93c3-599270775902。
新测试页命名：极限短时间 v5.3.3冒烟 R2｜独立测试02。

使用既有 playwright-native-ai-browser 专用浏览器；不得打开旧地址冒充新会话、仅改旧标题、复用用户日常浏览器配置或编辑旧讨论页。无需安装不同品牌浏览器。新建动作、专用浏览器上下文标识、真实新对话ID和标题必须回读绑定。新对话ID在真实创建/首条提交后取得；取得前写NOT_CREATED，不能编造。新ID必须不同于控制页。若标题已有，先核对是否本次创建；不是则用本轮RUN_ID后缀新建，不按同名搜索选旧会话。

## 加载与备份（Codex仅执行已冻结改动）

从本合同同一冻结提交读取技能目录 skills/first-principles-physical-limit-convergence。读取本机现有技能入口并解析真实加载目录，不猜第二套入口。先备份后仅安装本修补所需的 acceptance_supervisor_v5_3_3.py、acceptance_review_v1_0_1.py、acceptance_isolation_guard_v1.py 及对应测试；不重构FSM、不改浏览器脚本、不改系统/代理/FlClash/Git全局配置。

旧监督器允许基线blob c520152633e168fd418ac545d73e9c941f691b37，目标35af5dd5e7478898f5f1f7a751a3365daf858aed。目标review模块600bbbe3c997efc5d2dadc0cbb7fe1f90c600db2，来源门dc86a5d70f6449f13d417d2cb0e46c7472b342b6。新增模块不存在可创建；已存在相同字节可幂等使用；存在不同未冻结版本则停止报告VERSION_CONFLICT，不覆盖并行项目。Git对象字节为权威，不修改autocrlf。

核心三文件保持原版：FSM d79661d478793cd183ae6559ac01d0aba387ad51；Scope 5208d600060bef0cdcab10681f82e5cd6ab034fd；Renderer 2a56e186ec94d912fa4d6b461657bdfd9c2fb068。若实际正式加载版本不同，回报差异，禁止现场适配。

使用冻结的两份测试文件复核50项，仅作加载门；必须继续真实用户路径测试，不能把测试脚本通过当最终认证。回报实际模块路径、哈希、调用记录。新测试页的GPT与执行器均应读取同一冻结合同；正式裁决必须调用已修补的 acceptance_result，不能仍用旧函数或手工写FAIL/PASS绕过。

## 正常任务与完整闭环

建立新的独立试验 TASK_ID=ESTE-v5.3.3-SUPER-SMOKE-R2-ISO02；在真实启动时生成唯一RUN_ID并记录来源。该试验继承母任务ESTE-v5.3.3-SUPER-SMOKE-R2及原Timeline ESTE-v533-R2-20260927T162319Z。02是同一项目第02号派发，不把第01轮重置。

先记录本指令收件与安装/建页准备耗时；再由专用浏览器在全新对话提交普通任务：使用整体闭环极限短时间引擎v5.3.3和本冻结修补，在隔离目录 C:\Users\A\Documents\Codex\2026-09-27\este-super-smoke-v533-r2-02 内新建 result.txt，内容精确为 V5.3.3_SMOKE_OK，其他业务文件不动；按正常方式完成GPT虚拟成熟、Freeze、完整派发、Codex真实执行、回GPT与最终收口。

预先声明该独立试验的正常任务入口：上述新页普通任务被实际受理。新页GPT建立真实TASK_ACCEPTED时间线，不得事后补造。此前安装/建页/转交时间另记并保留母任务整体耗时，不藏入零成本；不能把真实受理后的人工转交改名为首次提交豁免。

业务文件UTF-8无BOM无末尾换行，15字节，SHA256=0a9e171cb0f1f5114b81b0878a8a8a52b3ebf604cddf54d1539c134367fd44ef。旧第01轮文件不得改动。新目录若已有相同结果只报告幂等先存，不能冒称新建；不同内容停止并报冲突。

测试全过程必须走正式网页入口与真实Codex，不由测试器补状态、补证据或代执行业务。新页里实际GPT负责虚拟成熟和通过原FSM生成完整派发；Codex只读取、执行、验证、回传。子试验结果先回同一新页并取得匹配确认，完成后才向控制页报告摘要；不能将仅回控制页冒称子试验闭环。

## 来源门和等待门绑定

正式入口 acceptance_result(result, fail_source, expected=..., evidence=...)；等待入口 acceptance_wait(expected=..., observation=...)。expected来自冻结任务和实际回读的task_id/timeline_id/run_id/conversation_id；不能取待验证回报替代权威绑定。evidence事件逐一关联相同四ID、原始evidence_ref、source_kind、actor、purpose、within_loop、stage和verified。仅在独立读到原始动作记录后才填verified=True，禁止由模型摘要自证。

四个自动环节证据为TASK_SUBMISSION、COMMAND_RECEIPT、BUSINESS_EXECUTION、RESULT_RETURN。最终还需business_verified、delivery_verified、scope_verified、runtime_binding_verified、closed_loop_verified、timeline_verified均有实际核验依据。示例/测试里的synthetic数据不得进入真实证据。

USER角色、自动粘贴、双窗口显示、页面标题和报告数字都不能认定人工。实际人工接管有同任务原始证据才计数；未知/争议写待核，不转人工FAIL；缺完整证据也不自动PASS。HOLD/REVIEW是验收证据待核状态，不新增顶层FSM状态、不自动恢复重发。

确认/进展必须匹配四ID。匹配ACK已经出现即送达，不再重发；有可核实生成或工具进展继续等；工具等待到时先查实际状态，不自动判失败。保持既有有界工具等待，不修改全局超时；60000ms不作超时。明确真实传输错误才用既有成熟恢复一次与R2的C3→C2→C1→C5策略；不拿旧监督器默认A/B/C末端代表本轮全部路径失败。

## 副作用、回报、边界

必要业务和本轮证据只写新业务目录。允许现有浏览器技能正常机制产生自身日志，但必须回读其预定日志位置并记录；非预定目录写入不可自动豁免。不要因已确认的标准日志机制本身判业务失败，也不改日志配置强行隐藏。

Codex回报RESULT=PASS|FAIL|BLOCKED，另列ACCEPTANCE_REVIEW、真实人工已核验次数或UNKNOWN、报告次数及证据来源，不签发FINAL_VALID/DONE/REAL_T*。缺证据可报BLOCKED_EVIDENCE而不是人为失败。保留实际起止UTC、局部单调时钟耗时、自动路径、回执、版本、目录、恢复次数、阶段时间与原始引用。新页GPT只有完整证据经正式入口返回FSM_PASS_TO_FINAL_VALID才使用FSM收口；收口时间/已用时间真实生成。最多01–06；不能无限新增派发。

固定回执控制标记：CODEX_RETURN_ESTE_v533_R2_ISO02_02。尚未送达执行器、尚未新建页面时必须明确写NOT_RUN，不把命令发布当成这些动作已完成。
