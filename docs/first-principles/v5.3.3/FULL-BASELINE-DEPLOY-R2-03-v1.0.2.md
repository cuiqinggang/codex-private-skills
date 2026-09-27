# R2 第03号完整基线部署合同 v1.0.2

## 本轮修复什么

用户回传第02号 RESULT=BLOCKED / REASON=VERSION_CONFLICT：正式目录 C:\Users\A\.codex\skills\first-principles-physical-limit-convergence 是普通目录，SKILL.md、VERSION、CANONICAL.md 均声明 v3.1.6；六个目标运行时均缺失。入口 SKILL.md SHA256=84e1f003590ab1dd37bfd24ed362ae0595b480dabbcef4c63b48b28c73c3686c。该结果来自用户提供的本机 Codex 回报，GPT 未独立读取该本机目录。

GPT重新读取第02号冻结 a6149ea00aca2ffc77373df7dcd790cc215b66ef，确认原合同只授权已有v5.3.3上的三文件修补，不授权不同版本全量安装。因此停止是符合合同的；错误是部署前提未经证实。另实际读取同一源提交发现 VERSION=5.3.3，而 CANONICAL.md 仍指向 v4.4.1。本轮同时修复活动入口/版本说明不一致。

第02号安装、回归、建页、业务均 NOT_RUN；不能记成已运行失败，也不能记成人工失败。ISO02子任务尚未受理，保留这一事实。

## 冻结范围

母引擎=5.3.3，验收修补=1.0.1，完整部署包=1.0.2；不是将引擎升为1.0.2。

包路径：deployments/este-v533-r2-full-baseline-v1.0.2/。

完整活动载荷13文件：六运行时、两份50项回归测试、SKILL.md、VERSION、CANONICAL.md、DEPLOYMENT.json、contracts/ACTIVE-R2.json。六运行时及两份测试与a6149ea源冻结的Git blob字节完全一致；本轮不修改FSM、监督器、来源/等待算法或浏览器。新入口明确当前使用规则，历史仓库说明不再作为第二活动入口。

这是R2使用所需完整可加载基线，不包含全部历史工具或外部浏览器/Codex程序。旧目录完整保留，不删除历史技能资产。外部浏览器、已有Python与真实Codex/GPT通道仍须现场验证，不把“内包依赖齐全”当作“全环境已验证”。

FULL-BASELINE-SPEC.json固定八个已有Git对象和五份入口/合同内容；materialize_payload.py从Git对象读取原始字节，重建FULL-BASELINE-PAYLOAD.json。最终payload SHA256必须为469567e166f2dedcf8d97c06969092f3ce0630585070aa7f6b7bb3c9a8be7a20。已生成的交付ZIP含全部13文件与同一payload，无需用户手工补源码。

权威源文件blob：SPEC=f891f1ba92e5ed6f66e80fea75b4411ae2338e41；部署器=c104a5ee2c1f7e40273c067f4c5e33ba20ae40d4；物化器=caf05ee99be03027dee72883248c18c58f85a344；部署测试=43eacee59d147989c84a2d1d410bf2672a100808；物化测试=f2b118227eae3765887591cb9e279acecd14e588。

## 唯一安装路径与新授权

本第03号合同明确授权：仅在再次核验本次回报的v3.1.6版本、普通目录、入口SHA256和六运行时缺失均吻合时，执行备份后完整替换；这取代第02号“不同版本禁止安装”的前提，不授权任意版本覆盖或现场设计适配。

目标：C:\Users\A\.codex\skills\first-principles-physical-limit-convergence。
部署工作区：C:\Users\A\Documents\Codex\2026-09-27\este-baseline-v533-r2-03。
旧目录备份：部署工作区\backup-v3.1.6，位于技能搜索路径之外。

用已授权的Git共同仓库通道按冻结提交获取上述部署目录，使用现有checkout作为只读对象源；只读核对其remote确为cuiqinggang/codex-private-skills，不切换或清理用户在用分支。不具备已有对象源时，只在部署工作区内准备独立源目录，获取本冻结所需对象，不扫描全盘、不拉取无关历史。登录/权限失败原样回报，不改代理、密钥或Git全局配置。

使用当前执行通道已允许的Python3.10+运行冻结物化器；无既有合法Python则BLOCKED，不安装系统组件、不绕过子进程权限。按参数传已确认的对象仓库路径，不把PowerShell文本管道用于原始源码写入。得到payload后，运行冻结部署器的probe动作，核对批准基线；再执行install动作。禁止改动脚本常量、指纹、目标路径或跳过门禁。

部署器顺序：准备全部文件→逐文件哈希和依赖检查→暂存目录新进程加载六模块及50项测试→再次确认原目录未被并行修改→完整旧目录改名备份并核对所有文件→暂存目录提升到正式路径→正式路径哈希、新进程模块__file__和50项测试复核。不是将零散新文件覆盖进旧树，也不是只改版本号。

安装故障按冻结代码恢复旧目录、核对原始字节、保留失败新目录及日志；发生目标占用或无法恢复时STOP并报告具体路径，禁止盲目删除。recover动作仅用于日志证明目标缺失且完整备份仍在的中断恢复；目标已存在时不得自动覆盖。任何真实权限拒绝不扩权、不换通道绕过。已完整安装同一payload可幂等核验，不重新覆盖备份。

新进程导入成功后，Codex还必须实际重读正式SKILL.md/VERSION/CANONICAL.md，回报当前会话采纳的版本；仅磁盘安装不能证明旧会话缓存已切换。无法确认使用新规则时记录SESSION_BINDING_UNCONFIRMED，不代签成功。

## 本轮虚拟验证

GPT Linux沙箱实际运行：原运行时50/50，完整部署30/30，Git对象物化5/5，共85/85。六最终证据门64/64组合正确，3/3防绕过变异被检出。包含旧版缺六文件的模拟基线、备份保真、幂等、版本/哈希/目录/链接冲突、模拟权限拒绝、提升失败、最终加载失败与回滚、中断备份恢复。

模拟基线只复现本轮已知版本/缺失形态，不是用户完整目录克隆。Windows文件锁、重解析点、当前权限和真实浏览器未在GPT宿主复现，不写Windows部署已通过。VIRTUAL-VALIDATION.json记录范围。唯一T*=min(T_VALID)不变；60000ms仍是闭环工程目标，不是本地测试耗时、失败门或超时设置。

## 安装通过后继续同一个未受理的独立页测试

不让用户再次发“继续”。完成本机正式加载门后，继续第02号合同的ISO02新页任务。沿用控制页名称“极限短时间 v5.3.3冒烟 R2”，真正新建“极限短时间 v5.3.3冒烟 R2｜独立测试02”，回读新conversation_id/context_id，必须不同于控制会话6ab94118-27c8-83ea-93c3-599270775902。不能改旧页标题、复制标签或按同名选旧页。

新普通任务：在C:\Users\A\Documents\Codex\2026-09-27\este-super-smoke-v533-r2-02创建result.txt，内容V5.3.3_SMOKE_OK，UTF-8无BOM无换行15字节，SHA256=0a9e171cb0f1f5114b81b0878a8a8a52b3ebf604cddf54d1539c134367fd44ef。不同先存文件不覆盖；同内容只记幂等先存；旧第01轮结果不动。

新页GPT与执行器都读取本完整部署合同和活动规则；真正沿普通任务→GPT虚→冻结完整派发→真实Codex→回同一新页→GPT裁决。必须用正式FSM/Scope/Renderer和经来源门的acceptance_result；测试器不得补字段、伪造四ID或代执行业务。判定证据、独立来源核查、真实人工接管与正常等待规则继续采用第02号验收合同；本合同仅覆盖其安装基线条款，不能回到旧裸PASS/FAIL入口。

人工次数依据原始同任务动作，不凭USER角色、标题、自动粘贴、浏览器种类或双窗口同步推断；不继承第01轮争议“1次”。未知写UNKNOWN，不强行FAIL或零人工PASS。有匹配ACK不重发，正常生成继续观察；确认等待到时先查状态，不把60000ms当超时或用部署器的本地测试等待值控制GPT生成。

## 时间、输出与停止

母Timeline=ESTE-v533-R2-20260927T162319Z，原点=2026-09-27T16:23:19.729Z，不重置、不扣除准备等待。03是第03号外层执行包，02阻断记录保留；不是清零派发计数。新子Timeline仅在ISO02普通任务实际受理时建立，不把旧准备改名豁免。部署计时由已许可Python内的UTC和perf_counter_ns记录；缺少更早收件时间如实UNKNOWN，不能用首次时钟观测冒充。

固定控制回执CODEX_RETURN_ESTE_v533_R2_BASELINE03_03。回报基线核验、payload/六模块哈希、完整备份路径与核验、暂存/正式50项结果、真实加载路径与会话采纳版本、安装起止和耗时、新页ID/上下文/创建证据、子任务RUN_ID与时间线、业务文件证据、来源门结果、匹配ACK、已核验人工次数或UNKNOWN、Reality Delta。安装PASS、业务PASS、闭环验收必须分列。

RESULT=PASS|FAIL|BLOCKED；RETURN_TO_GPT=YES；NO_FINAL_VALID_DONE=YES。Codex不签发FINAL_VALID/DONE/REAL_T*；真实新页GPT经完整证据裁决。任何尚未运行项写NOT_RUN。本轮部署器不负责启动浏览器、不自动伪造新页，必须由现有授权Codex/浏览器执行链继续。禁止修改代理、系统、FlClash、权限策略和浏览器脚本。项目最多01–06，不能另起编号规避上限。
