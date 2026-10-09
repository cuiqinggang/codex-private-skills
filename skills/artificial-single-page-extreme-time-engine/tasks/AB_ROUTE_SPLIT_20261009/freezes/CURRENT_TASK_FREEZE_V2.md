# 《A/B路线分叉任务冻结状态 第2版》

TASK_ID=AB_ROUTE_SPLIT_20261009
FREEZE_ID=AB-ROUTES-F002
FREEZE_VERSION=2
CONTRACT_VERSION=2
STATUS=IN_PROGRESS
METHOD_REF=315cdc78054047c75b1e177fdebc4c008fac3ab6
METHOD_A=A28/A25/A18
METHOD_B=B30/B27/B20

## 本自然节点已完成并真实落盘
- 保留共同原始第28版总纲与A28/A25/A18旧双层路线，没有拆出两个完整技能包。
- B版本继承：`routes/B/ENGINE_B_V30.md`→B29→根第28版；`routes/B/BRAIN_B_V27.md`→B26→根第25版；`routes/B/NEW_PAGE_TEMPLATE_B_V20.md`→B19→根第18版。
- 稳定标准入口 `SKILL.md` 和唯一人机引导 `START_HERE.md` 不再硬编码每轮方法版本；固定 `routes/B/ROUTE.md` 负责当前B方法的实际路径与版本指针（本次 B30/B27/B20）；固定A路线指针仍为旧A版本。用户只需一句话，不须人工查找每个版本。
- B严格一个GPT活动页面执行一个自然节点，节点内连续解决故障，结果合法冻结后才新单层页接续；自动建页尚无实测，必须提供人工最小信封降级。
- GPT是本任务的规划与执行主体，外部成熟工具视必要性调用，不强制n8n；原Windows桥 v0.3.1 保持外部独立技能入口。
- A/B量化比较方式已纠正为相同任务、相同VALID实质成果的端到端完整有效时间，不再比较A派发成本vs B上下文压力两项局部成本。
- 对比协议文件：`scenarios/IMAGE_QUALITY_AB_V2.md`（ComfyUI随机噪声精品图，结果未现实验收）。原n8n项目F002不被此任务覆盖。

## 未完成及可信性
- B当前仅为方法规则与入口修订；没有验证过GPT自动新页面建立、自动接管、关闭，未做ComfyUI全程A/B同口径Reality，也没有A/B恢复实测。
- 任务CURRENT指针尚须在本冻结文件GitHub落盘后单独写入，以真实冻结提交SHA标记；备份ZIP必须最后更新，之前的ZIP只是旧快照。
- T_A_VALID=UNKNOWN; T_B_VALID=UNKNOWN; T_BASE_REAL=UNKNOWN; T_VIRTUAL_BEST=UNKNOWN; DELTA_T=UNKNOWN; GAIN_PERCENT=UNKNOWN; SPEEDUP=UNKNOWN。
- STOP_GATE=NOT_PASSED; VIRTUAL_MATURE=NO; REALITY=NOT_AUTHORIZED; FINAL_VALID=NO。

NEXT_ACTION=按本任务状态指针恢复后验证单句调用、路由A/B当前版本、同一节点修复后继续以及断点接续；收集同结果真实时间证据，停止门未通过不得宣称最短。
