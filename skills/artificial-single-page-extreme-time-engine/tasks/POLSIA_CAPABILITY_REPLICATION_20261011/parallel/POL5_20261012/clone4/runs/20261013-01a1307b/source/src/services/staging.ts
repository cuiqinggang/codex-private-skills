// Local, persistent acceptance flows on the existing Postgres/PgStore plane.
// The only executable action here reads an allowlisted historical evidence file.
import { randomUUID } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import { db, ensureCompany } from "../core/db.ts";
import { PgStore } from "../core/pg-store.ts";
import { CapabilityRequestError, getCapabilities, readCapabilityEvidence } from "./capabilities.ts";
import { BUSINESS_ENABLED, executeBusinessTask, businessErrorCode } from "./business.ts";

const store = new PgStore();
export const STAGING = process.env.POLSIA_STAGING !== "off";

export class StagingRequestError extends Error {
  constructor(public statusCode: number, message: string) { super(message); }
}

export async function readJson(req: IncomingMessage): Promise<Record<string, unknown>> {
  const chunks: Buffer[] = [];
  let bytes = 0;
  for await (const chunk of req) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    bytes += buffer.length;
    if (bytes > 16384) throw new StagingRequestError(413, "请求过大");
    chunks.push(buffer);
  }
  const body = Buffer.concat(chunks).toString("utf8");
  let value: unknown;
  try { value = JSON.parse(body || "{}"); } catch { throw new StagingRequestError(400, "需要有效 JSON"); }
  if (!value || typeof value !== "object" || Array.isArray(value)) throw new StagingRequestError(400, "需要 JSON 对象");
  return value as Record<string, unknown>;
}

function text(value: unknown, field: string, limit: number): string {
  if (typeof value !== "string" || !value.trim() || value.trim().length > limit) {
    throw new StagingRequestError(400, `${field}不能为空，最多${limit}字`);
  }
  return value.trim();
}

export async function selectedCompany(url: URL): Promise<string> {
  const id = url.searchParams.get("company") || "demo";
  if (!/^[a-zA-Z0-9-]{1,64}$/.test(id)) throw new StagingRequestError(400, "公司编号无效");
  const rows = await db()`SELECT id FROM companies WHERE id=${id}`;
  if (!rows.length) throw new StagingRequestError(404, "公司不存在");
  return id;
}

function send(res: ServerResponse, code: number, value: unknown) {
  res.writeHead(code, { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" });
  res.end(JSON.stringify(value));
}

export async function handleStaging(req: IncomingMessage, res: ServerResponse, url: URL): Promise<boolean> {
  const method = req.method || "GET";
  if (url.pathname === "/api/runtime" && method === "GET") {
    send(res, 200, { mode: STAGING ? "LOCAL_TEST" : "UPSTREAM", workerAllowed: !STAGING,
      modelExecution: BUSINESS_ENABLED ? "LOCAL_CODEX_JOBS_ENABLED" : "NOT_ENABLED_IN_LOCAL_TEST", publicPublication: "NOT_AUTHORIZED",
      parentFreeze: "POLSIA-MOTHER-V008-F001", finalValid: false }); return true;
  }
  if (url.pathname === "/api/capabilities" && method === "GET") {
    send(res, 200, await getCapabilities()); return true;
  }
  const evidence = url.pathname.match(/^\/api\/capabilities\/([a-z0-9-]+)\/evidence$/);
  if (evidence && method === "GET") {
    send(res, 200, await readCapabilityEvidence(evidence[1], url.searchParams.get("evidence") || undefined)); return true;
  }
  if (url.pathname === "/api/companies" && method === "GET") {
    send(res, 200, { companies: await db()`SELECT id,name,slug,created_at FROM companies ORDER BY created_at` }); return true;
  }
  if (url.pathname === "/api/companies" && method === "POST") {
    const input = await readJson(req);
    const name = text(input.name, "公司名称", 80);
    const goal = text(input.goal, "目标", 1200);
    const id = "local-" + randomUUID();
    await ensureCompany(id, name, id, { goal, mode: "LOCAL_TEST", modelExecution: "UNAVAILABLE" });
    send(res, 201, { id, name, goal, mode: "LOCAL_TEST", note: "已真实保存；尚未启动模型经营" }); return true;
  }
  if (url.pathname === "/api/tasks" && method === "GET") {
    send(res, 200, { tasks: await store.list(await selectedCompany(url)) }); return true;
  }
  if (url.pathname === "/api/tasks" && method === "POST") {
    const input = await readJson(req);
    const companyId = await selectedCompany(url);
    const title = text(input.title, "任务名称", 160);
    const capabilityId = text(input.capabilityId, "能力编号", 64);
    const evidenceId = input.evidenceId === undefined ? undefined : text(input.evidenceId, "证据编号", 64);
    // Validate the exact allowlist entry before creating a persistent task.
    await readCapabilityEvidence(capabilityId, evidenceId);
    const task = await store.create({ companyId, title, tag: "research", status: "todo",
      description: JSON.stringify({ action: "READ_HISTORICAL_EVIDENCE", capabilityId, evidenceId, mode: "LOCAL_TEST" }) });
    send(res, 201, { task, execution: "LOCAL_READONLY_EVIDENCE", modelExecution: false }); return true;
  }
  const match = url.pathname.match(/^\/api\/tasks\/([a-z0-9]+)(?:\/(execute))?$/);
  if (match && (method === "GET" || (method === "POST" && match[2] === "execute"))) {
    const companyId = await selectedCompany(url);
    const task = await store.get(match[1]);
    if (!task || task.companyId !== companyId) throw new StagingRequestError(404, "任务不存在");
    if (method === "GET") { send(res, 200, { task }); return true; }
    if (task.status === "completed") { send(res, 200, { task, replayed: false }); return true; }
    let action: { action?: string; capabilityId: string; evidenceId?: string };
    try { action = JSON.parse(task.description); } catch { throw new StagingRequestError(409, "此任务没有本地证据动作"); }
    if (action.action === "CODEX_LOCAL_JOB") {
      const execution = await executeBusinessTask(task);
      send(res, execution.started ? 202 : 200, { task: await store.get(task.id), started: execution.started, jobId: execution.job.id }); return true;
    }
    if (action.action !== "READ_HISTORICAL_EVIDENCE") throw new StagingRequestError(409, "此任务动作未启用");
    const claimed = await db()`UPDATE tasks SET status='in_progress',started_at=now()
      WHERE id=${task.id} AND status IN ('todo','failed','needs_continuation') RETURNING id`;
    if (!claimed.length) throw new StagingRequestError(409, "任务正在执行或不能执行");
    try {
      await store.event(task.id, "local-evidence-adapter", "status_change", { to: "in_progress" });
      const document = await readCapabilityEvidence(action.capabilityId, action.evidenceId);
      const sql = db();
      // Save report + completion + evidence receipt in one native Postgres transaction.
      // A crash cannot leave a persisted report attached to a resumable unfinished task.
      await sql.begin(async transaction => {
        const [report] = await transaction`INSERT INTO reports(company_id,task_id,type,name,content)
          VALUES(${companyId},${task.id},'evidence',${task.title},${JSON.stringify(document, null, 2)}) RETURNING id`;
        const result = { summary: "已实际读取历史证据并保存核验报告；仅此只读动作完成。",
          artifacts: [{ type: "report", ref: `/api/report?company=${companyId}&id=${report.id}`, note: "实际文件内容与摘要；未重跑历史业务" }] };
        await transaction`UPDATE tasks SET status='completed',ended_at=now(),result=${transaction.json(result)} WHERE id=${task.id}`;
        await transaction`INSERT INTO task_events(task_id,type,actor,payload) VALUES(${task.id},'tool_result','local-evidence-adapter',
          ${transaction.json({ action: action.action, reportId: report.id, modelCalled: false })})`;
        await transaction`INSERT INTO task_events(task_id,type,actor,payload) VALUES(${task.id},'status_change','system',${transaction.json({ to: "completed" })})`;
      });
    } catch (error) {
      await store.setStatus(task.id, "failed", { summary: "证据读取失败；请检查原始资产及回执。", artifacts: [] });
      throw error;
    }
    send(res, 200, { task: await store.get(task.id), replayed: false, modelCalled: false }); return true;
  }
  // These existing upstream routes call models, publish, reset data, or enable workers.
  // Local acceptance never reaches them, including the upstream mutation on GET /run.
  if (STAGING && (url.pathname.startsWith("/run/") || url.pathname.startsWith("/api/proxy/") ||
      ["/api/worker", "/api/reset", "/api/onboard", "/api/cron", "/api/chat"].includes(url.pathname) ||
      /^\/api\/(approve|reject)\//.test(url.pathname))) {
    send(res, 409, { error: "此操作在本地验收模式未启用", code: "UNAVAILABLE_LOCAL_TEST", modelCalled: false }); return true;
  }
  return false;
}

export function requestErrorCode(error: unknown): number {
  return error instanceof StagingRequestError || error instanceof CapabilityRequestError ? error.statusCode : businessErrorCode(error) || 500;
}
