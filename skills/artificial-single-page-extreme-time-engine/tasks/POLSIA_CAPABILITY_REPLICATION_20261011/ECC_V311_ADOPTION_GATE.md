# Polsia：ECC v3.1.1 网络成熟运行时复用门

TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
DOCUMENT_VERSION=1
SOURCE_REPO=cuiqinggang/ecc-v3.1.1
SOURCE_REF=v3.1.1
RELEASE_URL=https://github.com/cuiqinggang/ecc-v3.1.1/releases/tag/v3.1.1
METHOD_REF=skills/artificial-single-page-extreme-time-engine/ECC_V3_1_1_NETWORK_AUTHORITY.md
ENGINE=ENGINE.md@28
STATUS=REFERENCE_VERIFIED;ADOPTION_NOT_EXECUTED
MOTHER_FINAL_VALID=NO

## 使用规则
1. 先按精确路径读取本任务CURRENT.md、VERSION_CURRENT.md和最新FREEZE_Vnnn，再按标签v3.1.1读取外部ECC仓库README、loopx/contract.py、loopx/engine.py、lease.py、runners/codex_runner.py和冷恢复测试。不依赖本地旧版ECC技能文件声称新版本。
2. 评估是否以ECC现成LoopX+lease+Codex Runner能力取代目前临时的Windows调度状态判断，必须先确认副作用、账户授权、执行单例性、Exactly-once与断电/重启恢复，再做隔离小范围对照。已经执行中的Codex会话不可直接热切换执行器。
3. Checkpoint是节点内部防断电保存：成熟loopx STATE.json原子写入和RUN-LOG.jsonl追加保持真实工作进度，15分钟只是建议的最初观察频率，重要成果即时保存；不要因此递增Vnnn、不要把所有MP4和海量日志重复复制到GitHub。
4. Freeze是自然节点结束后的不可变审计；一节点一个新Vnnn，有读回的校验信息再更新网络VERSION_CURRENT/CURRENT。已通过的CODEX-001/CODEX-002不重新测试，保持证据和来源。
5. GPT接管时先检查退出码与最新冻结/CURRENT，区分正常节点完成与故障。遇到真实UNKNOWN外部操作先查原回执，不能无脑重发或绕过权限/安全拒绝。
6. 不把GitHub方法提交与「一人公司网站已经运行」混淆。面向用户的公司网站只复用现成部署平台或模板，代码变更在网上工作区版本控制，但公网功能还需另行现实部署和验收。
7. 这是源定位与复用合同，不是ECC已部署成功的结论；实际测试PASS、72小时耐力、关机恢复、网站和Polsia全能力完成仍是UNKNOWN。
