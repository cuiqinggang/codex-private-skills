// PCL-02: inherited business documents are exposed through a bounded read-only adapter.
// These receipts do not certify live business integration or replay any historical workflow.
import { createHash } from "node:crypto";
import { open, realpath } from "node:fs/promises";
import path from "node:path";

export const HISTORICAL_ASSET_ROOT = "C:\\AI\\Polsia-Codex-20261011";
const MAX_EVIDENCE_BYTES = 128 * 1024;

export class CapabilityRequestError extends Error {
  constructor(public readonly statusCode: 400 | 404 | 409, message: string) {
    super(message);
    this.name = "CapabilityRequestError";
  }
}

interface EvidenceSource {
  id: string;
  title: string;
  relativePath: string;
  bytes: number;
  expectedSha256: string;
}

interface CapabilitySource {
  id: string;
  title: string;
  historicalStatus: string;
  summary: string;
  implementedEntryPoints: string[];
  siteAction: string;
  input: string;
  output: string;
  gaps: string[];
  evidence: EvidenceSource[];
}

export interface CapabilityEvidenceDocument extends EvidenceSource {
  capabilityId: string;
  evidenceId: string;
  contentType: string;
  content: string;
  sha256: string;
  integrity: "PINNED_SHA256_MATCH";
  operation: "READONLY_EVIDENCE_READ";
  functionalIntegrated: false;
  readAt: string;
}

export interface CapabilityEvidenceStatus extends EvidenceSource {
  status: "READABLE_PINNED" | "MISSING" | "INTEGRITY_ERROR";
  url: string;
}

export interface Capability extends Omit<CapabilitySource, "evidence"> {
  availability: "OFFLINE_READONLY" | "EVIDENCE_UNAVAILABLE";
  integration: "READONLY_EVIDENCE_ADAPTER";
  functionalIntegrated: false;
  evidence: CapabilityEvidenceStatus[];
}

export interface CapabilityCatalog {
  batchId: "PCL4_20261012";
  parentFreeze: "POLSIA-MOTHER-V008-F001";
  integration: "READONLY_EVIDENCE_ADAPTER";
  functionalIntegrated: false;
  monitorOwnership: "EXTERNAL_OWNER_UNCHANGED";
  historicalReplay: "DISABLED";
  capabilities: Capability[];
}

const source = (id: string, title: string, relativePath: string, bytes: number, expectedSha256: string): EvidenceSource =>
  ({ id, title, relativePath, bytes, expectedSha256 });

// Byte counts and hashes come from the existing sealed node manifests, not new business runs.
const MATRIX = source("matrix", "V008 九类事实矩阵", "nodes/CODEX-008/CAPABILITY_MATRIX.md", 19108, "B5F1AB2893E55C107F56B316BBBEAD6993EB2154FFAD9039E57ACCF607595502");
const SOURCES: CapabilitySource[] = [
  {
    id: "engineering", title: "工程开发与 BUG 修复",
    historicalStatus: "HISTORICAL_LOCAL_VALIDATION_WITH_SCOPE_LIMIT",
    summary: "继承文件校验、验收草稿和独立审查。完整研发需求、BUG 修复与受控交付仍有缺口。",
    implementedEntryPoints: ["Codex 原生工程工具与子 Agent", "原生 Git", "V007 离线验收和变更草稿"],
    siteAction: "读取历史验收标准和变更模板；新工程任务由现有任务执行入口另行执行。",
    input: "只接受能力 ID 与证据 ID，不接受本机路径或执行命令。",
    output: "V007 验收/变更正文、冻结字节数与 SHA-256 校验回执。",
    gaps: ["历史文件恢复不证明完整 BUG 闭环。", "新失败复现、代码修复、独立回归与部署回执需另案验证。"],
    evidence: [
      source("acceptance", "V007 本地验收标准", "nodes/CODEX-007/delivery/LOCAL_ACCEPTANCE_ZH_EN.md", 12858, "6B2E8BDE9DF72DDA6593CDE7E4BEED3E38757016CD7AA2A36F09D24EAF21382A"),
      source("change-request", "V007 变更请求模板", "nodes/CODEX-007/delivery/CHANGE_REQUEST_ZH_EN.md", 9317, "3A8B0BE81898AF00A551DBF9A9430F0773EC70A2B4B67F18DA9C0EDF811E129C"),
      MATRIX,
    ],
  },
  {
    id: "marketing", title: "研究、营销及内容发布",
    historicalStatus: "HISTORICAL_LOCAL_DRAFT_DELIVERY_NOT_PUBLISHED",
    summary: "继承 V002 成片与 V004 内容运营草稿，只读查看既有内容计划和文案。",
    implementedEntryPoints: ["V004 离线内容包", "现成媒体 CLI/技能的历史成果", "公开研究工具"],
    siteAction: "读取内容计划和渠道草稿；不重新渲染、下载、探测旧媒体。",
    input: "冻结的 V004 内容目录与渠道草稿。",
    output: "只读内容计划/文案与 SHA-256 回执；发送状态保留 NOT_SENT。",
    gaps: ["未上传、排期、投放或验证真实获客。", "真实发布、账户连接、付费广告和商业清权需明确授权。"],
    evidence: [
      source("content-pack", "V004 内容交付说明", "nodes/CODEX-004/delivery/README.md", 2058, "0E58AF36379EED8F7B7DA14B8E72D40736CA6202C9B8E0869EC51CE122805CC6"),
      source("content-plan", "V004 离线内容计划", "nodes/CODEX-004/delivery/operations/CONTENT_PLAN.csv", 2688, "170BC2A3AE27D47541D0749AF367979A0F7ACB641C1D6CEFF489F7CFE8520087"),
      source("douyin-draft", "V004 抖音未发布草稿", "nodes/CODEX-004/delivery/channels/douyin.txt", 457, "F924511FACF8DE07FDAD8FED9CD454E422C6694888E675043B7D3E2046EC2625"),
    ],
  },
  {
    id: "support", title: "客服及人工升级",
    historicalStatus: "HISTORICAL_LOCAL_SUPPORT_DRAFTS_NOT_SENT",
    summary: "继承 V005 的 18 组双语 FAQ/回复宏和升级清单；全部是未发送草稿。",
    implementedEntryPoints: ["V005 FAQ 和回复宏", "V005 人工升级/未知项清单", "Codex 原生离线分析"],
    siteAction: "读取 FAQ、回复宏与人工升级说明，交操作员审核。",
    input: "既有 FAQ/宏 ID 和合成支持材料；不收集或发送真实客户信息。",
    output: "冻结客服文件正文和 SHA-256 回执。",
    gaps: ["未连接真实客服渠道、派单或人工升级发送。", "真实工单关闭、SLA 和人工决定仍 UNKNOWN。"],
    evidence: [
      source("faq", "V005 双语 FAQ", "nodes/CODEX-005/delivery/FAQ_ZH_EN.md", 26708, "208C4EE86DFBF4F6AA76F18DD105106C078644ADFCBCBEED8706C36DACDE1212"),
      source("reply-macros", "V005 未发送回复宏", "nodes/CODEX-005/delivery/REPLY_MACROS_ZH_EN.md", 37115, "C1CA7C1D15EA45482FF172A97A4054DB73F00D373D765FB4D58800AFC9641E4A"),
      source("escalation", "V005 人工升级与未知项", "nodes/CODEX-005/delivery/ESCALATION_AND_UNCERTAINTY_ZH_EN.md", 15979, "7BB4FB8FE9862BEAD507B2236245C876713F5A4F9DCCD0D78E48CEB6A619B374"),
    ],
  },
  {
    id: "sales", title: "销售获客",
    historicalStatus: "HISTORICAL_OFFLINE_PRESALES_NOT_SENT",
    summary: "继承 V006 的需求资格判断、双语提问和提案模板，未外联、未交接、未成交。",
    implementedEntryPoints: ["V006 需求发现与资格模板", "V006 未发送提案模板"],
    siteAction: "读取售前提问、资格字段和提案模板，保留人工审批缺口。",
    input: "冻结离线模板与 12 条历史合成需求的事实范围。",
    output: "售前模板正文/JSON 与 SHA-256 回执。",
    gaps: ["CRM 测试空间、去重导入和真实线索身份未联通。", "实际外联、价格、合同、订单和收入没有完成证据。"],
    evidence: [
      source("discovery", "V006 双语需求发现", "nodes/CODEX-006/delivery/DISCOVERY_ZH_EN.md", 10371, "0C54D9260BB8E0B9225B706080CB0A396B0A99BC315BBD8779542F67C45AE5F1"),
      source("proposal", "V006 未发送提案模板", "nodes/CODEX-006/delivery/PROPOSAL_TEMPLATE_ZH_EN.md", 13926, "3D6B696C529B6B4E0572F75A18B2B5F6BD37020F8F7F86FDAA58BEC0840D20D1"),
      source("qualification", "V006 资格字段模板", "nodes/CODEX-006/delivery/QUALIFICATION_TEMPLATE.json", 2006, "7A328B0E41B4AA113770BBC5FFB0C046A58909DC743D1C584DCC9016DE8D2848"),
    ],
  },
  {
    id: "finance", title: "财务、支付与对账",
    historicalStatus: "HISTORICAL_LOCAL_EXECUTED_SYNTHETIC_NO_REAL_MONEY",
    summary: "继承 V008 七张合成账单、九行合成流水的真实本地对账输出；业务只执行一次。",
    implementedEntryPoints: ["V008 原生 PowerShell 对账的已冻结输出", "V008 官方 Agent 离线人工核查建议"],
    siteAction: "只读查看已有账本、流水去向与核查建议，不重跑财务夹具。",
    input: "已冻结的 V008 合成输出；不读取银行账户、凭据或真实资金。",
    output: "只读账本/路由/核查建议与 SHA-256 回执。",
    gaps: ["真实银行、付款、退款及支付接口 UNKNOWN/UNAUTHORIZED。", "本地合成对账不证明生产财务联通。"],
    evidence: [
      source("ledger", "V008 合成账本", "nodes/CODEX-008/scenario/output/ledger.csv", 839, "79E80E1A9C1F66E508A6B4EA86DBFB44CD33CAE9B5E22EAA2E3FB93006959756"),
      source("payment-routing", "V008 合成流水去向", "nodes/CODEX-008/scenario/output/payment-routing.csv", 710, "28E01AEA5C0589E10B1FF6888D20A3B5E57A6EC3E63B4EE169AB474C3A0DD35A"),
      source("finance-escalation", "V008 未发送核查建议", "nodes/CODEX-008/scenario/agent/FINANCE_ESCALATION.md", 4247, "E6FB9FDD7C4D5817FD6B38002A7FBBF2A30751E77F525E07D328272C53F83069"),
    ],
  },
  {
    id: "agents", title: "多 Agent、并发及工作流",
    historicalStatus: "HISTORICAL_NATIVE_AGENT_DELEGATION_WITH_SCOPE_LIMIT",
    summary: "继承 V005–V008 的不同 Agent 编写、分析与非作者审查事实；并发性能未认证。",
    implementedEntryPoints: ["Codex 官方内建子 Agent", "V008 原输入绑定的委派/分析回执", "n8n 仅有健康和权限探测"],
    siteAction: "读取真实委派回执，区分分派成功、执行成功和独立审核。",
    input: "只读历史委派记录与输入 SHA 绑定回执。",
    output: "Agent 回执正文/JSON 与 SHA-256 回执。",
    gaps: ["n8n 工作流管理 401、Docker 管道拒绝，V008 业务执行 0 次。", "取消、超时、资源争抢、跨会话恢复和多公司调度仍 UNKNOWN。"],
    evidence: [
      source("delegation", "V008 委派记录", "nodes/CODEX-008/evidence/AGENT_DELEGATION_RECORD.json", 833, "718C112D10E032A65C0246A1699738823EC42DD64F7DECA1ABDECC385F1B112A"),
      source("finance-agent", "V008 财务 Agent 输入绑定回执", "nodes/CODEX-008/scenario/agent/AGENT_FINANCE_RECEIPT.json", 7279, "3119184A40B2593FBD6ADD8ABE34F66039BF505060D6A5C436B53C5864B707EF"),
      MATRIX,
    ],
  },
  {
    id: "monitoring", title: "智能运营监控与审计",
    historicalStatus: "HISTORICAL_SIX_DIMENSION_RECONCILIATION_EXTERNAL_MONITOR_OWNER",
    summary: "继承运行、业务、告警、证据、Exactly-once 与恢复决策六维对账；监控网站由外部负责人接手。",
    implementedEntryPoints: ["V008 六维证据对账", "既有工具/运行日志与 GitHub 哈希回执"],
    siteAction: "只读提供业务证据和遥测事实；不建设、启动或修改监控网站。",
    input: "已冻结的监控/恢复对账和成熟入口探测记录。",
    output: "六维事实与权限缺口正文/JSON，供既有监控方引用。",
    gaps: ["Windows 任务查询拒绝、Operational 日志关闭，未改变权限或系统配置。", "主动告警发送、断电恢复及 72 小时长稳未验证；状态窗不是智能经营监控。"],
    evidence: [
      source("reconciliation", "V008 六维监控与恢复对账", "nodes/CODEX-008/evidence/MONITORING_RECOVERY_RECONCILIATION.json", 2756, "84A18372539E98B761F200E745CAC93F124A8B5E785364EB638FAEB3DA297A99"),
      source("mature-probe", "V008 成熟入口/权限探测", "nodes/CODEX-008/probes/MATURE_COMPONENT_PROBE.md", 8980, "04AD802CDFE8C7DC8C4AB894836BF055380E7EC2F3FAA67ED0E196C3041988B9"),
      MATRIX,
    ],
  },
  {
    id: "recovery", title: "异常恢复、意外中断与冷恢复",
    historicalStatus: "HISTORICAL_FILE_RECOVERY_ONLY_NOT_COLD_RECOVERY",
    summary: "继承 V001 文件冲突恢复、V002 来源读取恢复及 V008 原生 Git 单文件恢复；不重放旧测试。",
    implementedEntryPoints: ["既有 safe-file-demo 历史成果", "原生 Git restore 的 V008 隔离回执", "非作者独立场景审查"],
    siteAction: "读取原故障、恢复和独立审查回执，按三态决策核对。",
    input: "已确认 DONE 的历史恢复事实；未知外部执行先对账。",
    output: "冻结恢复回执/审查正文和 SHA-256 回执。",
    gaps: ["文件内容恢复不证明进程崩溃、半提交、断电或冷启动恢复。", "UNKNOWN 外部结果不可自动重发；不触发系统关机或旧恢复脚本。"],
    evidence: [
      source("functional-result", "V008 原业务/故障/恢复回执", "nodes/CODEX-008/evidence/FIN008_FUNCTIONAL_RESULT.json", 1234, "46AE44C92DDC5DC72662EB4BB56EEA659CA0B6C00445718D3A34AF4DD1795551"),
      source("independent-review", "V008 非作者独立场景审查", "nodes/CODEX-008/evidence/INDEPENDENT_SCENARIO_REVIEW.md", 3371, "7F691039603603D956D6C72AFFA6291C9C52FF8D5D375B3819481BC99BC0BA55"),
      MATRIX,
    ],
  },
  {
    id: "learning", title: "经验学习与技能沉淀",
    historicalStatus: "HISTORICAL_PROJECT_REUSE_ASSETS_NOT_GLOBAL_DEPLOYMENT",
    summary: "继承 V008 项目 SOP、验收清单和复用顺序；冻结 Skill 保持不可变。",
    implementedEntryPoints: ["V008 项目级 SOP/checklist", "C 盘现成 Knowledge Brain 与版本化证据"],
    siteAction: "读取下一任务可复用步骤和验收清单，不安装或修改全局 Skill。",
    input: "现有项目经验和明确失败/恢复入口。",
    output: "SOP、checklist、顺序说明正文与 SHA-256 回执。",
    gaps: ["全局 Skill 部署、长期索引更新和自动跨任务学习未执行。", "复用有效性需新任务实际命中证据，不能从文件存在推导学习成功。"],
    evidence: [
      source("sop", "V008 项目复用 SOP", "nodes/CODEX-008/reuse/SOP.md", 2058, "87FD4EED755DA51B694F0EE7D007E81FD49261EF45510789E5ED0252092FC541"),
      source("checklist", "V008 独立验收清单", "nodes/CODEX-008/reuse/CHECKLIST.md", 992, "4CA9B397C2EDBAC203E637CCB3B6427C177264CFE0DF883F58929843D381D73A"),
      source("reuse-order", "V008 执行与复用顺序", "nodes/CODEX-008/ORDER_AND_REUSE.md", 3474, "8732CAAC2E99214AD1DDE0F419D269BD3C26974441AD85718D05EDCD305FD825"),
    ],
  },
];

function validateId(value: unknown): asserts value is string {
  if (typeof value !== "string" || !/^[a-z][a-z0-9-]{0,63}$/.test(value)) {
    throw new CapabilityRequestError(400, "Invalid capability or evidence ID.");
  }
}

function normalized(value: string): string {
  const result = path.resolve(value);
  return process.platform === "win32" ? result.toLowerCase() : result;
}

function contentType(relativePath: string): string {
  return relativePath.endsWith(".json") ? "application/json; charset=utf-8" : "text/plain; charset=utf-8";
}

/** Explicit local root injection is for isolated integrity tests; HTTP callers never supply it. */
export function createCapabilityService(assetRoot = HISTORICAL_ASSET_ROOT) {
  const root = path.resolve(assetRoot);

  async function readPinned(ref: EvidenceSource): Promise<{ content: string; sha256: string }> {
    const target = path.resolve(root, ref.relativePath);
    const relative = path.relative(root, target);
    if (relative.startsWith("..") || path.isAbsolute(relative) || !/\.(md|txt|csv|json)$/.test(ref.relativePath)) {
      throw new CapabilityRequestError(409, "Evidence path is outside the allowlist.");
    }
    let handle: Awaited<ReturnType<typeof open>> | undefined;
    try {
      const [realRoot, realTarget] = await Promise.all([realpath(root), realpath(target)]);
      // Reject symlink/junction redirection, including to another unlisted file inside the root.
      if (normalized(realRoot) !== normalized(root) || normalized(realTarget) !== normalized(target)) {
        throw new CapabilityRequestError(409, "Evidence path redirection is not allowed.");
      }
      handle = await open(target, "r");
      const stat = await handle.stat();
      if (!stat.isFile() || stat.size !== ref.bytes || stat.size > MAX_EVIDENCE_BYTES) {
        throw new CapabilityRequestError(409, "Evidence byte count differs from the frozen source.");
      }
      const bytes = await handle.readFile();
      const sha256 = createHash("sha256").update(bytes).digest("hex").toUpperCase();
      if (bytes.length !== ref.bytes || sha256 !== ref.expectedSha256) {
        throw new CapabilityRequestError(409, "Evidence SHA-256 differs from the frozen source.");
      }
      // Preserve a possible UTF-8 BOM so a stored report can reconstruct the pinned bytes.
      const content = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
      return { content, sha256 };
    } catch (error) {
      if (error instanceof CapabilityRequestError) throw error;
      const code = (error as NodeJS.ErrnoException).code;
      if (code === "ENOENT" || code === "ENOTDIR") {
        throw new CapabilityRequestError(404, "BLOCKED_C_SOURCE_MISSING: Historical evidence is missing from the C-drive source.");
      }
      throw new CapabilityRequestError(409, "Historical evidence is not safely readable.");
    } finally {
      await handle?.close();
    }
  }

  async function readCapabilityEvidence(capabilityId: string, evidenceId?: string): Promise<CapabilityEvidenceDocument> {
    validateId(capabilityId);
    if (evidenceId !== undefined) validateId(evidenceId);
    const capability = SOURCES.find((item) => item.id === capabilityId);
    if (!capability) throw new CapabilityRequestError(404, "Unknown capability.");
    const ref = evidenceId === undefined ? capability.evidence[0] : capability.evidence.find((item) => item.id === evidenceId);
    if (!ref) throw new CapabilityRequestError(404, "Unknown evidence for this capability.");
    const value = await readPinned(ref);
    return {
      ...ref, capabilityId, evidenceId: ref.id, contentType: contentType(ref.relativePath),
      content: value.content, sha256: value.sha256, integrity: "PINNED_SHA256_MATCH",
      operation: "READONLY_EVIDENCE_READ", functionalIntegrated: false, readAt: new Date().toISOString(),
    };
  }

  async function getCapabilities(): Promise<CapabilityCatalog> {
    const capabilities = await Promise.all(SOURCES.map(async (item): Promise<Capability> => {
      const evidence = await Promise.all(item.evidence.map(async (ref): Promise<CapabilityEvidenceStatus> => {
        let status: CapabilityEvidenceStatus["status"] = "READABLE_PINNED";
        try { await readPinned(ref); } catch (error) {
          status = error instanceof CapabilityRequestError && error.statusCode === 404 ? "MISSING" : "INTEGRITY_ERROR";
        }
        return { ...ref, status, url: `/api/capabilities/${item.id}/evidence?evidence=${ref.id}` };
      }));
      return {
        ...item, implementedEntryPoints: [...item.implementedEntryPoints], gaps: [...item.gaps], evidence,
        availability: evidence.every((ref) => ref.status === "READABLE_PINNED") ? "OFFLINE_READONLY" : "EVIDENCE_UNAVAILABLE",
        integration: "READONLY_EVIDENCE_ADAPTER", functionalIntegrated: false,
      };
    }));
    return {
      batchId: "PCL4_20261012", parentFreeze: "POLSIA-MOTHER-V008-F001",
      integration: "READONLY_EVIDENCE_ADAPTER", functionalIntegrated: false,
      monitorOwnership: "EXTERNAL_OWNER_UNCHANGED", historicalReplay: "DISABLED", capabilities,
    };
  }

  return { getCapabilities, readCapabilityEvidence };
}

const service = createCapabilityService();
export const getCapabilities = service.getCapabilities;
export const readCapabilityEvidence = service.readCapabilityEvidence;
