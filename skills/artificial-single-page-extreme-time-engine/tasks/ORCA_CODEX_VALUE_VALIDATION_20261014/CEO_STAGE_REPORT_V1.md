# Orca＋Codex 实测｜阶段报告 V1（未最终验收）

TASK_ID=ORCA_CODEX_VALUE_VALIDATION_20261014
REPORT_AUTHOR=GPT_CEO_DIRECT_TOOL_READBACK
REPORT_DATE=2026-10-14
METHOD_COMMIT=4c48e249ca9c18ecde014d8b2e43f753a1f13139
LOCAL_ROOT=C:\AI\Orca-Codex-Validation-20261014
FINAL_VALID=NO
CONSECUTIVE_ORCA_FULL_RUNS=0_OF_10_NOT_STARTED
AB_PAIRED_ROUNDS=0_OF_10_NOT_STARTED
NET_TIME_SAVINGS=UNKNOWN

## 已完成的真实工作
用户明确允许GPT自行读取网上工程资料并灵活使用成熟工具。本页直接读取权威GitHub方法、现场文件、官方发行源码，实施签名/哈希校验、隔离解包和原生运行时部署，独立核验基线并直接完成恢复修复；并非只派发给另一个模型。
现场机器i5-3570/4逻辑核，31.95GB内存，首次空闲9.86GB；Codex CLI0.160.0，gpt-6.1-sol/ultra/priority，已有ChatGPT登录，workspace-write保持。
未修改FlClash/代理/DNS/ACL/全局Codex配置、原生产任务、浏览器或监控；未购买服务、未发布公网。

## Orca隔离准备：运行时通过，业务尚未验证
官方stablyai/orca稳定发行v1.4.224，源commit2bb20586ebc39d605e16d95f57420e20a16e7485。
安装包222555816字节，SHA256=d192a7f1142b58a8c9bc855275fb37cd41dff7f152fd3cbac3acdd96331ec849；实际摘要匹配，Authenticode=Valid，signer=stablyai。
采用既有7-Zip26.01解包到CEO_assets/runtime，不执行NSIS全局安装。解包文件801613383字节，4732文件/512目录。
官方物化backend版本0.1.0+9e2e3cd709d0、CLI runtime appVersion0.0.0-dev，与桌面发行tag分列，不伪装成标准桌面运行时完全等价。
捆绑Node24.21.0摘要ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32；server.js摘要bea1e0ce0f5cd40a046a40c04ef5e66c9e38ce110387f35d5b54abccf65cb8ba，启动前核验通过。
2026-10-14T12:18:07.3838805Z启动原生orcad；历史serverPID1200、daemon9376，runtime_id=8fb15ac6-5029-4af9-89eb-eb35fee7e42f。CLI status真实ok=true、ready/reachable/connected、graph=ready。
Windows独立读取监听地址仅127.0.0.1:51217与127.0.0.1:51160；pairing禁用。WSL核对Ubuntu-24.04-Restore仍Stopped、docker-desktop仍Running。
独立源码检查发现顶层orca serve为orcad硬编码--bind 0.0.0.0；--pairing-address不是绑定地址，--no-pairing不是禁止网络监听。故复用同一个官方底层orcad.js的原生--bind 127.0.0.1 --port 0 --no-pairing --json，不改源码或造服务器。
Orca进程HOME/USERPROFILE/APPDATA/LOCALAPPDATA/TEMP和profile均隔离在本任务CEO_assets，未复制凭据。待处理边界：browser_unavailable（无浏览器后台），agent-state-rules下载HTTP404；不能把健康握手当Codex业务/自动恢复通过。

## 真实任务样本与失败
公开项目llm-as-a-verifier的真实历史源commit=115de305f23ed89bc42e86e010853c40059f3f7d；本机已有源码合法只读提取到dataset/source并固定SHA。三任务：T01模型响应字段/评分解析，T02 benchmark注册到loader集成及Python3.9注解兼容，T03空数据报告/百分比/输出文件。没有真实外部API调用、没有生产业务重放；Python3.9仅静态语义检查，不冒称该解释器实跑。
GOOD_001：输入尚未交付模型，Git换行转换造成SHA不一致而拦截，723.0559ms。仅任务仓库core.autocrlf=false修复，旧失败保留。
GOOD_002：输入SHA正确，嵌套Codex初始化in-process app-server被现有沙箱拒绝，6302.0131ms；session/用量均null，无完成业务。没有放宽权限或复制凭据。
GOOD_003：GPT从已有授权执行桥直接启动独立workspace-write Codex，不使用嵌套沙箱。精确session=01a13a4e-ac29-7090-8529-a6eeb42d6bd3；开始12:05:56.756558Z；20分钟上限触发TASK_TIMEOUT，结束回执12:26:02.740466Z；1205983.9134ms，accepted=false，delivery=false。原结果8/14，不是成功基线。
独立复核6个失败发现5个是验证器AST抽取遗漏新辅助函数_openai_response_text产生的NameError，不能归因产品逻辑；1个是T03报告除零。N001随后将验证器修为传递函数依赖闭包，GPT独立读取确认并固定副本。验证器与任务均有修正，正式比较前必须冻结新SHA，不能沿用旧测试通过计数。

## GPT直接完成恢复产物：已验收限定范围
原超时工作树与回执原样保留；GPT在runs/GOOD_003_CEO_RECOVERY副本直接修复T03，保留Codex的T01/T02成果。
第一次恢复脚本因N001已修改原验证器触发防冲突断言，只创建副本未改生产代码。后续修复脚本首次调用收到桥502，读回超时，先记UNKNOWN；连接恢复后实际检查无恢复进程、无修复、无QA/回执，才受控重新发起。未盲重复已完成副作用。
2026-10-14T12:42:54.684101Z至12:42:56.599088Z，直接修复、外部检查、自测、输出SHA清单与回读完成。
外部验收14/14通过；同一修正验证器重查原始BAD仍5/14、预期非零exit2；源码回归21/21通过；产物哈希回读一致。
验证器SHA256=2d6f62b3205454ce5758c98c0160d7aa03b2820f7f05f9c1302a89651cb24979。
这是“Codex产物＋GPT独立审查/修复”的恢复成果，不是Codex单独无故障通过，不是Orca业务通过，不是10轮全流程完成。隐藏验证器位于工作树外，但不是OS强制隔绝执行者读取的盲测；独立性边界保留。

### 已回读的恢复回执摘录
```json
{"actor":"GPT_CEO_WITH_CODEX_EXISTING_OUTPUT","started_utc":"2026-10-14T12:42:54.684101+00:00","completed_utc":"2026-10-14T12:42:56.599088+00:00","exits":{"QA":0,"SELF_TESTS":0},"readback_ok":true,"accepted_recovered_artifact":true,"recovery_instrumented_ms":1914.9874,"good003_input_to_recovery_readback_ms":2219842.5331,"original_timeout_retained":true,"pure_codex_completion":false,"formal_reality":false,"ten_rounds_completed":0}
```

## 计时与效率：不能挑最快片段
- 官方下载/摘要/验签62946.0231ms；解包核心55324.0788ms，后者不含清单/哈希尾部，不能称完整部署仅118.270秒。
- HEADLESS_PREPARE_RECEIPT的810.8428ms、exit_code=null仅是Windows GUI子进程发起，父PowerShell未等待真正完成。实际准备已用后续物化文件和runtime ready回读证明，绝不能把810ms当完整成功耗时。
- 直接GPT恢复执行1914.9874ms是局部程序修复/测试/哈希回读；其脚本编写、检索和诊断时间没有被这个局部数字包含。
- 从GOOD_003原始输入交付的同机单调时钟起点到恢复产物SHA回读，实测2219842.5331ms，约36分59.843秒，包含中间失败/等待。仍不包括此前GPT研究/部署准备与最后回执写入，不是用户接单全程T_VALID。
- run_good.py原定时器在最终JSON写入/采样join/最后磁盘枚举之前结束，正式批次需要外层完整计时。配置采样间隔1秒不代表观测精确达到每秒一次；GOOD_003约1206秒仅543条资源样本，不能伪称无漏峰。
- 12:29附近一次系统CPU采样100%，同时Chrome/Defender/VM及其它任务活跃；不能据此认定Orca是原因，也不能停掉其它业务美化测试。
- 尚无Orca同合同业务时间、模型账单和10轮数据，实际净节时/回本/极限效率均UNKNOWN。目前只能证明已完成上述准备与恢复成果，不能宣布值得推广。

## 证据路径与接续
小回执：CEO_assets/DOWNLOAD_RECEIPT.json、EXTRACTION_RECEIPT.json、SERVER_LAUNCH.json、SERVER_STDOUT.log、CLI_STATUS.json（UTF16LE，按BOM读）；evidence/baseline/GOOD_001、GOOD_002、GOOD_003/TIMING_AND_ACCEPTANCE.json。
恢复证据：evidence/baseline/GOOD_003_CEO_RECOVERY/FINAL_REPAIR_RECEIPT.json、INDEPENDENT_QA.json、OUTPUT_MANIFEST.json、SELF_TESTS_STDERR.log；原始BAD复核evidence/baseline/CEO_ORIGINAL_BAD_RECHECK.json；固定验证器tools/independent_check_CEO_FROZEN.py。
本页最后给N001写CEO_N001_RECOVERY_COMPLETE.md的工具返回502，写入状态UNKNOWN；不能假定该协调者已收到。先回读N001_REPORT/RECEIPT及精确session，避免空轮询/重复启动。N001报告截至最近成功读取仍未出现。
下一节点：收尾N001→审查同合同完整计时、A/B同等GPT修复政策及产品接入/故障矩阵→具体SHA Freeze→一次N002正式Reality→通过后用户已授权A/B各10轮及容量分层验证。遇BUG修复保留历史且重置最终版本连续计数。不得把本报告14项与21项检查当10轮业务。
用户已授权后续重复测试；另设有限次数的小时级接续检查，不保证机器离线仍执行。真实源码/全部原始大日志尚未整体上传在线；本报告和合同/状态已持久化，后续需把脱敏源与完整证据按清单补齐，不冒称所有现场字节均已备份。
