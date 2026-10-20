# OPC 成熟能力候选：Polsia 本地核心能力复刻 V3

REGISTRY_ID=OPC-POLSIA-LOCAL-V3
PARENT_METHOD=SANRENXING_V5
CATEGORY=AI_COMPANY_BUSINESS_OPERATIONS
STATUS=AVAILABLE_FOR_SCOPED_REUSE / P2_ISOLATED_ACCEPTED / REAL_BUSINESS_NOT_CERTIFIED

## 唯一已部署入口
Windows C 通道 `C:\Users\A\.codex\skills\polsia-clone-local-foundation-v3\SKILL.md`；先执行其现有只读 `scripts/preflight_v3.py`，继承其不可变源哈希、P2 验收和授权边界。不得原地修改冻结第3版。

## 可直接复用的职责
本地虚拟公司全流程、任务依赖和逻辑角色组织、控制状态、模拟业务学习、公开UI与部分HTTP行为、异常恢复案例及证据驱动QA。由《三人行》V5 GPT CEO 按任务匹配按需调用，而非另设平行总经理/调度系统。其候选成熟度高于只有提示词的OPC方案，但仅限上述验证范围。

## 原验证证据和本次现状
V3 技能 `references/v3-p2-acceptance.md` 记载 P2 隔离门通过、163 个候选源文件、16/16测试通过、V23静态检查289 PASS/0 FAIL/3 UNVERIFIED。`references/v3-test-result.json` 报告合并隔离套件 PASS（内存SQL，无真实外部服务）。2026-10-21 新执行轮次仅只读运行 preflight_v3.py，返回 655 files PASS, 163 sourceFiles PASS, mismatched=[], unexpected=[]。历史通过不是本轮真实在线网站运行验收。

## 严格限制
未验证真实支付/收入、真实客户邮件和社交平台外发、PostgreSQL真实数据库与冷恢复、生产级浏览器/服务稳定性、原站私有后台等价、真实长期自治经营。无用户新授权不得触发真实外发/付款/发布，也不改变FlClash、代理、已有业务和 n8n。

## 使用流程
任务合同→Knowledge Brain检索旧经验/专业模板→匹配Polsia V3经验证业务工作流→最小范围安全预检→GPT CEO选择并派发到现成执行工具→证据回执与验收→必要时受控返修→写回已有知识库；跨进程恢复复用Loop/ECC/n8n，不重造。

## 升级门槛
未来须在隔离环境先做一次真实端到端网站业务操作，证明3个逻辑工作项的派单→回复→返修→汇总，再评估扩到7–8个任务。只有有证据且同等质量的总有效时间获益为正，才由候选升成默认生产路径。原Polsia公开商业指标与本地V3能力严格分开。
