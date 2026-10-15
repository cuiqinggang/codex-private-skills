# Hermes 生态站 F004｜F002 首轮 HTTP400 证据对账与最小修复冻结
日期：2026-10-15；任务：HERMES-ECO-20261014
状态：DIAGNOSTIC_CONFIRMED / PATCH_CANDIDATE_FROZEN / NO_REAL_RUN_DISPATCHED
上一冻结：HERMES-ECO-F003-20261015；本轮诊断冻结：HERMES-ECO-F004-20261015
Hermes 专用技能：v2.0，未升级；整站 FINAL_VALID=NO；F002 五轮认证=0/5。

## 0. 方法与执行入口
用户在本节点指定《三人行》V2（项目级显式适用；该方法在线源文件标记 REVIEW_PENDING_NOT_ACTIVE，不表示全局已正式激活）+《GPT直连Windows双路执行桥 V6.0》。
GitHub 方法源：skills/artificial-single-page-extreme-time-engine/SANRENXING_V2.md（Git blob 027229fc28ebd12811adacfe37aa857a187d3301）。
Windows V6 路由规则已实际读取：C:/AI/GPT-Windows-Bridge-B/persistence/Invoke-Three-Route-Gate-V6.ps1；其明文版本 6.0.0、policy=C_FIRST_A_SECOND_B_THIRD、advisory_only=true、no_automatic_dispatch=true。
C 实际设备 DESKTOP-4A1EGTM（本次 online+ping pong）；A、B 本次未另测。旧 F003 接续提示词中的「V5 A优先」已被当前用户明确 V6 指令替代；不回写篡改历史冻结文档。
Hermes 原始专用技能 SKILL.md、UNIFIED-EXECUTION-METHOD-V2.md 均已从 Windows 现场读取。仅沿用旧服务、既有启动器、模型和 F002 冻结源。

## 1. 原始故障不可变事实
现场：C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F002/
- R01/request-1.json 存在；R01/round-result.json: WebException HTTP400、112 ms、phase=[]、pass=false。
- R01/ack-1.json、run-1.json、grade-1.json 不存在；DISPATCH-UNKNOWN.json=UNKNOWN/RECONCILE_ONLY；BATCH-RESULT.json=NOT_ACCEPTED、0/5，禁止重发。
- 原始请求 JSON 中 input 实际是对象，具有 value、PSPath、PSParentPath、PSChildName、PSDrive、PSProvider、ReadCount 等属性，而非文本字符串。不能只看「model」字段就误判为模型路由故障。
- F002/Invoke-Acceptance.ps1 中 $Prompt=Get-Content ... -Raw -Encoding UTF8；然后 @{input=$Prompt;model='DeepSeek-V4.1-Flash';...}|ConvertTo-Json -Compress；没有序列化前类型校验。
- 真实原始 HTTP400 的响应正文没有保存在 round-result，故**HTTP400 内部分支尚不能断言百分之百已验明**。本次不重复 POST 原幂等请求。

## 2. Windows 隔离只读复现（不是 Hermes 业务测试）
在 C 通道 Windows PowerShell 中，使用 R01/prompt-1.txt 读取与脚本同形序列化；对转换所得 JSON 做类型检查：
ORIGINAL_INPUT_TYPE=PSCustomObject
ORIGINAL_HAS_PSPATH=True
CAST_INPUT_TYPE=String
CAST_HAS_PSPATH=False
进程以 exit code 0 结束。这个对照证明 PowerShell 附加的 ETS 文件元属性进入 JSON；先显式转换成普通 [string] 就不会带入。
官方 Hermes API 文档：https://hermes-agent.nousresearch.com/docs/user-guide/features/api-server/#post-v1runs ，POST /v1/runs 的 input 为简单 string；当前 payload 违反合同。结合 112ms HTTP400，属于**强证据支持的首个责任差分**，不是新模型实测。
本次无新 POST /v1/runs、无模型计费调用、无 Hermes/Gateway/Docker 重启、无代理/密钥/浏览器修改。

## 3. 最小修复候选（仅冻结差分；未写回 F002 旧固定源）
旧：
```powershell
$Prompt=Get-Content (Join-Path $Dir "prompt-$phase.txt") -Raw -Encoding UTF8
$body=@{input=$Prompt;model='DeepSeek-V4.1-Flash';instructions='...'}|ConvertTo-Json -Compress
```
新候选：
```powershell
$Prompt=[string](Get-Content -LiteralPath (Join-Path $Dir "prompt-$phase.txt") -Raw -Encoding UTF8)
$body=@{input=$Prompt;model='DeepSeek-V4.1-Flash';instructions='...'}|ConvertTo-Json -Compress
$parsed=$body|ConvertFrom-Json
if ($parsed.input -isnot [string] -or [string]::IsNullOrWhiteSpace($parsed.input)) {
    throw 'F002_INVALID_RUN_INPUT_SERIALIZATION_NO_DISPATCH'
}
```
注意上面 instructions='...' 仅为差分示意，实际版本**必须保留原完整 instructions**，不得照抄占位符覆盖真实内容。

最小进一步核验门：
1. 无任何 POST：隔离复制原脚本为候选，保持历史 F002 原始 request/round-result/LAUNCH/REALITY/Hash 不变。
2. 离线对两个 prompt 做 JSON schema 断言；input 必须是非空 string，model=既有合法别名，不能出现 PSPath；验证 PowerShell 5.1 Parser；校对下一版源 SHA、冻结配置/fixture/合同。
3. 原历史首轮先基于既有日志、返回码、官方幂等规则和运行账本做只读对账，明确旧请求 NOT_ADMITTED 或仍 UNKNOWN；找不到完整原响应时说明证据边界。
4. 然后才能在新的隔离 F003/F004 验收目录用**新的合法幂等键**做一次最小真实 admission Gate；成功必须取得 run_id/ack/status，失败记录原始脱敏响应正文与状态码。不得沿用 F002 R01 原 key 去造新工作。
5. admission Gate PASS 后，再执行已有冻结合同的真实 Repair/检索/视觉/双子代理/Gate/continuity，最后在固定配置下计算连续5次通过（修复后归零），不减少原验收项。

## 4. 非目标与余下 Gate
H-ECO-01 当前：根因候选高置信、离线复现 PASS，待最小补丁静态审查、首次合法真实 admission 验收；不得标记 RUNTIME_PASS。
H-ECO-02：原生独立多智能体、独立Gate、Repair Loop闭环未完成本阶段验收。
H-ECO-03：图片/视频/音频、长任务跨会话 checkpoint/handoff/resume 未完成。
H-ECO-04：网页端实际聊天、冷开机/恢复、长稳与五轮综合、完整冷暖 T_VALID 未完成。
过去的 DeepSeek CLI、Hermes/Open WebUI 热态、v2.0 静态30/30、合成单元42/42 均保留其各自历史证据等级；本次未重复这些检查。
112ms 是失败耗时，不是 T_VALID；旧40.002s cold和4.853s warm候选不能变成新正式 T*。

## 5. 下一唯一节点
ONLY_NEXT=H-ECO-01-F004-OFFLINE-SERIALIZATION-PATCH-AND-ADMISSION-RECONCILE
先保全旧证据与首次请求回执→在新隔离候选中做最小改动→离线验证+Freeze→获准后仅一次 Reality admission 试验。保持 C→A→B；不为验证这个错误而重新开启整套五轮或重装服务。

## 6. 本节点追加：隔离补丁已实际物化并通过离线验证
2026-10-15 通过 V6 优先 C 通道连接实际 Windows，在既有 F002 目录旁新建：
`C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F004_CANDIDATE/Invoke-Acceptance.CANDIDATE.ps1`
**只是隔离候选文件**；源 F002/Invoke-Acceptance.ps1 仍保持 SHA256=`EA285EDE3571DB4EF8C6ECF9005B3A1036D4F4FD1A4728DCA29C3D9586CD0009`，候选本机 SHA256=`C3CA109844E7020F358FFB29A93E1B535AF8DE6BDE6EA389FAFC60B25CCD04BE`。
对照变动严格限定两处：显式 [string] Get-Content + POST 前 JSON input 非空字符串断言。复用原 instructions / model / 幂等键逻辑，未碰配置。
- PowerShell 5.1 Parser：PASS。
- F002 R01–R05 每轮两段、共10份原 prompt：`OFFLINE_PAYLOADS=10/10_PASS`（断言 input 为非空 string、JSON 不含 PSPath）。
- 源文件 SHA 未变，`ORIGINAL_UNCHANGED=TRUE`。
- 全部操作没有执行候选、没有调用 Hermes POST/付费模型；因此**实际 admission Gate=NOT_TESTED，五轮仍0/5**。
- GitHub 候选：`workspaces/hermes-maturity-20261014/F004/Invoke-Acceptance.CANDIDATE.ps1`；新文件已 GitHub 回读与上传文本逐字相等，Git blob `cc1a343d0b4ddfd2511b1312af6aa29e2ed7aa18`。本机原始字节 SHA 只约束本机候选；云端文本回读相等不代替跨机器原始字节SHA。
- **重要**：此候选不是可以直接运行的完整 F004 任务目录，因为它依赖同目录的 `REALITY-F002.json`、prepare.py、fixtures 等。下次执行前应先在隔离新合同中重建相应合法目录、生成新 Freeze 和检查源哈希，绝不能直接调用候选来撞已有 F002 的哈希门。

当前结论：H-ECO-01 本次完成了 **故障结构对账→本机重现→最小隔离修复→PowerShell parser/10个请求离线负载复核→网络与本机双端冻结**。后续唯一现实准入门仍是先对账旧请求并在新合同下做一次合法 POST admission；不得冒充已完成整站成熟认证。
