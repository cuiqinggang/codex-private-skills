# AI 化组织结构 V1.2｜父子 GPT + 轻量恢复（独立候选）
VERSION=AI_ORGANIZATION_V1.2_CANDIDATE
PARENT_VERSION=V1.1_DESIGN
DATE_LOCAL=2026-10-21
METHOD=SANRENXING_V5@SRX-V5-F001-20261020
LIGHT_STATE=LIGHT_STATE_V3_LOCAL@A5C1A1EC70725011F9B91DF258E252D5C13A41FA543E8FB22B825923797C8BDF
WINDOWS_BRIDGE=V11_C_FIRST
REUSE_ECC=ECC_V3_1_1
BACKUP=STRONG_BACKUP_V1.1.0@SB-V1.1-F001-20261021
STATUS=LOCAL_INTEGRATION_CANDIDATE; GLOBAL_AUTONOMOUS_TAKEOVER_NOT_CERTIFIED
GLOBAL_FINAL_VALID=PARTIAL

## 一、唯一目标
在固定质量、安全和完整交付门槛下最小化 T_VALID（接单、决策、工具启动、派发、核对、返工、中断恢复、人工接续、维护成本全部计入）。不把岗位数、专家数、分工复杂度当作绩效；正常简单任务 GPT 单独完成最快时不启用任何子层。

## 二、只有三个角色（而非三级企业）
1. 父 GPT（默认唯一 CEO 和任务事实裁决者）：锁定源头目标、正反约束、DONE_WHEN；读取现实环境、检索成熟方案池（历史技能、ECC V3.1.1、Codex、连接器、备援），最多比较有实质差异的三个成熟候选；基于物理状态虚拟成熟、反例攻击、Freeze，决定亲自执行还是按净收益派单；最终负责独立验收和报告。
2. 子 GPT/专业执行者（按需短期岗位）：只有真正可独立执行且有 T_VALID 净收益时启用；可为现有 GPT 子会话、Codex、Gemini、DeepSeek 或已安装专业工具。每项必须有 TASK_ID / WORK_ITEM_ID / ATTEMPT_ID / DONE_WHEN / RECEIPT；返回事实证据，不自行变更原合同；主任务仅父 GPT 接受后结束。没有证明真实启动的“子 GPT”只能标候选。
3. 独立轻量维护（不是新大脑）：使用《轻量状态持久化 V3》规则 + 已有 Windows 工具及 STRONG_BACKUP V1.1 计划任务；记录、检测、只读对账，不能代替 GPT 思考、不能替已中断的 ChatGPT 自动恢复未保存推理。n8n 只有确需跨进程 WAIT/外部唤醒并验收有益时才使用。不得重造状态机、锁、租约、浏览器或 230 个 Agent。

## 三、父 GPT 六步闭环
SOURCE（原目标、正反约束、质量/权限） -> BASE（广域成熟方案池，优先既有已测成熟路线） -> ATTACK（最多三条有区别候选、针对最强失败反例虚拟检验） -> FREEZE（唯一可验证工作包、NEXT_ACTION） -> REALITY（仅在合法授权、按实际物理环境执行，子 GPT 非必需） -> ACCEPT（独立回读验收；没通过就按 V3 最多三轮实质修复，不把中间阶段当 DONE）。
专家库230+ / ECC 3.1.1 是“按触发取能力”的候选库，不是常驻审计军团；问题指纹命中优先复用成熟修复。

## 四、控制丢失处理
CONTROL_STALL：父 GPT 仍能执行时直接针对性修复，不逐节点询问。
CONTROL_LOST：依据已落盘同一 TASK_ID、Freeze、receipt、工作进程只读恢复。原主控能恢复则原主控继续；不能恢复时交给可验证的备用 CEO，必须实际接收合同、独立判断和写入证据；旧主控撤销写权，防止双写。
UNKNOWN：只读对账；已提交不可重发，确定没提交才受控重试；涉及不可逆动作或证据缺失则 STOP_GATE。
目前现有强备份 V1.1 的 Google 网页接单/复核仍为人工复制，watchdog 仅覆盖其 own jobs，不能声称它已独立接管任意 ChatGPT 任务。不能把本文件发布等同全自动接管。

## 五、版本事实和兼容
网络权威 SANRENXING_V5.md 已冻结，当前仍引用 LIGHT_STATE_V1；本机 V3 见桌面 SRX_V3_ReadPack，源文件 SHA256 如上。用户明确指定 V3 时优先本候选 V3 规则，不覆盖 V5 冻结文件，也不把本地存在冒充主仓同步。STRONG_BACKUP_V1.1 独立运行不依赖当前 GPT，但它的 Gemini 网页规划和审核尚未端到端无人值守验证。

## 六、验收门
至少同一真实母任务的三个独立工作项：父 GPT 派单 -> 真正子端响应 -> 回执持久化 -> 独立 QA -> 失败返修 -> 汇总 -> 故障注入后同身份接管；每次测完整 T_VALID，与单 GPT 基线同质比较，含冷启动/人工介入次数/重复副作用；原主控真的死亡但没授权自动重开 ChatGPT 不能声称已解决。所有 FULL_PASS 门证据齐全才激活为默认组织方法。
