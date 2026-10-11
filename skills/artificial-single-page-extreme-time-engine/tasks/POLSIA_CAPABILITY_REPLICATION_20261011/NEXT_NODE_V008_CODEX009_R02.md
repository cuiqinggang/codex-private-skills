# V008 后续合法能力覆盖建议
TASK_ID=POLSIA_CAPABILITY_REPLICATION_20261011
PREVIOUS_VERSION=V008
PREVIOUS_NODE=CODEX-008_MATURE_FULL_CAPABILITY_COVERAGE
NEXT_NODE=CODEX-009_EXISTING_MATURE_WORKFLOW_SANDBOX_AND_RECOVERY
NEXT_DISPOSITION=PROPOSED_ONLY_CEO_SCOPE_DECISION_REQUIRED_NOT_EXECUTED
ENGINE=ENGINE.md@28
MOTHER_STATUS=IN_PROGRESS
MOTHER_FINAL_VALID=NO
FULL_POLSIA_EQUIVALENCE=NOT_CERTIFIED

建议优先补现成n8n测试固定流的“可核验流程身份→无副作用输入→执行原生回执→结果→现成恢复”缺口。当前health200但/rest/workflows401、Docker管道拒绝，不能读取凭据或重建HTTP桥。下一次应先确认当前已授权的正式只读/测试执行通道、流程节点及外部副作用，最多三成熟路线；合法入口仍缺则记录UNKNOWN，选择已安装官方Agent/现成测试产品的另一个业务子能力，避免重复V008财务夹具。

九类持续保留：工程需求/BUG修复可在已有明确测试仓独立复现→修复→回归；营销在既有draft/preview/test渠道验证；客服在测试工单验证真实路由且不发送；销售在现成CRM导入预览/测试空间验证去重；财务只在正式已配置sandbox/test mode和只读报表核对，无真实资金动作；多Agent补取消/超时与结果隔离；监控补原生任务权限、事件通道和主动告警测试；恢复补安全中断/现成Wait或执行记录恢复；经验在新业务上检验本次SOP是否被实际命中。没有真实客户不取消能力，没有合法权限也不编造成功。

Windows任务查询拒绝、事件通道关闭，runtime pointer3.0与live3.1差异已留证。启用日志/改系统任务或任何运行层升级需具体新授权，当前不热替换。断电、OS重启与72小时长稳尚未验证；不要按日期自动关机或停止原有观察。

下次先读 `nodes/CODEX-008/reuse/SOP.md`、`nodes/CODEX-008/CAPABILITY_MATRIX.md`、`nodes/CODEX-008/probes/MATURE_COMPONENT_PROBE.md` 和真实Freeze/Manifest/GitHub回执，再查Exactly-once。V001–V008业务事实CONFIRMED_DONE不重跑；UNKNOWN外部结果不自动重发；不重制NASA媒体。不直接运行已确认一次的V008夹具脚本。

必须另有完整定位标签和CEO批准才执行此建议。真实账户/认证/付款/退款/外联/投放/发布/生产/系统安全设置没有由V008间接授权。ROI_GATE=PAUSED_BY_USER。

【Polsia执行页｜POLSIA_CAPABILITY_REPLICATION_20261011｜CODEX-008｜实/虚按证据记录】
