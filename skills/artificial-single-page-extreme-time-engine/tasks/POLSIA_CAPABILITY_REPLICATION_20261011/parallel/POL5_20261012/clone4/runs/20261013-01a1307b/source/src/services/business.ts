// Persistent local business jobs backed by the installed native Codex CLI.
import { randomBytes, randomUUID } from "node:crypto";
import type { IncomingMessage, ServerResponse } from "node:http";
import { db } from "../core/db.ts";
import { PgStore } from "../core/pg-store.ts";
import type { Task } from "../core/types.ts";
import { JOB_CATEGORIES, prepareCodexJob, runCodexJob, getCodexJob, readCodexJobArtifact,
  verifyCodexJobArtifacts, reconcileCodexJob, CodexJobError, type CodexJobCategory, type CodexJobStatus } from "./codex-jobs.ts";
import { readJson, selectedCompany, StagingRequestError } from "./staging.ts";

const store = new PgStore();
export const BUSINESS_ENABLED = process.env.POLSIA_CODEX_JOBS === "on";
const running = new Set<string>();
const unresolved = new Set<string>();
const controllers = new Map<string, AbortController>();
export const BUSINESS_LIMIT = 4;
export const LOCAL_BUSINESS_CAPABILITIES = [
  { id: "engineering", title: "工程开发", output: "可交互网页、代码与固定验收测试", limitation: "本地交付；公网部署另行接入" },
  { id: "marketing", title: "研究与营销", output: "商业文案、受众策略与内容计划", limitation: "生成待审核草稿；未发送、未投放" },
  { id: "support", title: "客服准备", output: "FAQ、回复建议与升级规则", limitation: "未接真实客服渠道或人工派单" },
  { id: "sales", title: "销售准备", output: "需求资格问题与提案", limitation: "未外联、未报价签约或收款" },
  { id: "finance", title: "财务核查样例", output: "新合成数据、金额计算与差异核验", limitation: "合成数据；真实银行与支付未接入" },
  { id: "learning", title: "项目经验", output: "项目 SOP 与可执行检查清单", limitation: "保存在当前项目；全局技能不变更" },
];
function send(res: ServerResponse, status: number, value: unknown) {
  res.writeHead(status, { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" });
  res.end(JSON.stringify(value));
}
function inputText(value: unknown, field: string, limit: number) {
  if (typeof value !== "string" || !value.trim() || value.length > limit || value.includes("\0")) throw new StagingRequestError(400, `${field}无效，最多${limit}字`);
  return value.trim();
}
function actionOf(task: Task): { action?: string; jobId?: string; category?: string } {
  try { return JSON.parse(task.description); } catch { return {}; }
}
async function finish(task: Task, job: CodexJobStatus) {
  if (job.taskId !== task.id) throw new StagingRequestError(409, "任务与原始业务回执关联不一致");
  if (job.state !== "succeeded" || !job.nativeCodexVerified || !(await verifyCodexJobArtifacts(job.id)).passed) {
    throw new StagingRequestError(409, "当前任务缺少完整真实执行及产物验证证据");
  }
  const sql = db();
  await sql.begin(async transaction => {
    const [locked] = await transaction`SELECT status FROM tasks WHERE id=${task.id} AND company_id=${task.companyId} FOR UPDATE`;
    if (!locked || locked.status === "completed") return;
    const [report] = await transaction`INSERT INTO reports(company_id,task_id,type,name,content)
      VALUES(${task.companyId},${task.id},'business',${task.title},${JSON.stringify(job, null, 2)}) RETURNING id`;
    const artifacts = (job.verification?.artifacts || []).map(artifact => ({ type: "local_business_artifact",
      ref: `/api/business/tasks/${task.id}/artifact?company=${task.companyId}&name=${encodeURIComponent(artifact.path)}`, note: `${artifact.path} · SHA-256 ${artifact.sha256}` }));
    artifacts.unshift({ type: "report", ref: `/api/report?company=${task.companyId}&id=${report.id}`, note: "真实 Codex 进程、结构化结果与产物核验回执" });
    await transaction`UPDATE tasks SET status='completed',ended_at=now(),result=${transaction.json({ summary: job.report?.summary || "本地交付完成", artifacts })} WHERE id=${task.id}`;
    await transaction`INSERT INTO task_events(task_id,type,actor,payload) VALUES(${task.id},'tool_result','native-codex',${transaction.json({ jobId: job.id, nativeCodexVerified: true, artifactCount: artifacts.length - 1, externalSystemsIntegrated: false })})`;
    await transaction`INSERT INTO task_events(task_id,type,actor,payload) VALUES(${task.id},'status_change','system',${transaction.json({ to: "completed" })})`;
  });
}

export async function executeBusinessTask(task: Task): Promise<{ started: boolean; job: CodexJobStatus }> {
  if (!BUSINESS_ENABLED) throw new StagingRequestError(409, "本地 Codex 业务执行尚未启用");
  const action = actionOf(task);
  if (action.action !== "CODEX_LOCAL_JOB" || !action.jobId) throw new StagingRequestError(409, "此任务没有 Codex 业务动作");
  const job = await reconcileCodexJob(action.jobId);
  if (job.taskId !== task.id) throw new StagingRequestError(409, "任务与执行回执不一致");
  if (job.state === "succeeded") { await finish(task, job); unresolved.delete(task.id); return { started: false, job }; }
  if (job.state !== "prepared") throw new StagingRequestError(409, "已执行或结果未知；请查看回执并核对，不能自动重发");
  if (running.has(task.id)) throw new StagingRequestError(409, "任务正在执行");
  if (running.size + unresolved.size >= BUSINESS_LIMIT) throw new StagingRequestError(429, "4个执行位已占用；中断且结果未知的任务也需先核对回执");
  // Reserve capacity before the first asynchronous DB claim.
  running.add(task.id);
  const abort = new AbortController(); controllers.set(task.id, abort);
  let claimedHere = false;
  try {
    const claimed = await db()`UPDATE tasks SET status='in_progress',started_at=now() WHERE id=${task.id} AND company_id=${task.companyId}
      AND status IN ('todo','needs_continuation') RETURNING id`;
    if (!claimed.length) throw new StagingRequestError(409, "任务正在执行或不能执行");
    claimedHere = true;
    await store.event(task.id, "native-codex", "status_change", { to: "in_progress", jobId: job.id });
  } catch (error) {
    if (controllers.get(task.id) === abort) { running.delete(task.id); controllers.delete(task.id); }
    // No model has started. Restore the claim where possible; a DB outage is
    // also recoverable at startup because its job receipt remains prepared.
    if (claimedHere) await store.setStatus(task.id, "todo").catch(() => {});
    throw error;
  }
  void (async () => {
    try {
      const result = await runCodexJob(job.id, { timeoutMs: 900000, signal: abort.signal, onEvent: event => {
        const item = event.item as Record<string, unknown> | undefined;
        void store.event(task.id, "native-codex", "agent_text", { type: event.type, itemType: item?.type,
          text: typeof item?.text === "string" ? item.text.slice(0, 600) : undefined }).catch(() => {});
      } });
      if (result.state === "succeeded") await finish(task, result);
      else {
        if (result.state === "unknown") unresolved.add(task.id);
        await store.setStatus(task.id, result.state === "unknown" ? "blocked" : "failed", {
        summary: `本地任务${result.state === "unknown" ? "结果待核对" : "未完成"}：${result.outcome || "请查看回执"}`,
        artifacts: [{ type: "note", ref: `/api/business/tasks/${task.id}`, note: result.recovery }] });
      }
    } catch (error) {
      unresolved.add(task.id);
      await store.setStatus(task.id, "blocked", { summary: "运行或回执写入异常，需核对后接续；不会自动重发。", artifacts: [] }).catch(() => {});
      console.error("[local-business]", error instanceof Error ? error.message : "unknown");
    } finally { running.delete(task.id); controllers.delete(task.id); }
  })();
  return { started: true, job };
}

export async function recoverBusinessTasks(): Promise<number> {
  const tasks = await db()`SELECT id FROM tasks WHERE description LIKE '%CODEX_LOCAL_JOB%' AND status IN ('in_progress','needs_continuation','blocked')`;
  let recovered = 0;
  for (const row of tasks) {
    const task = await store.get(row.id); if (!task) continue;
    const action = actionOf(task); if (!action.jobId) continue;
    try {
      const job = await reconcileCodexJob(action.jobId);
      if (job.taskId !== task.id) throw new StagingRequestError(409, "业务回执关联不一致");
      if (job.state === "succeeded") { await finish(task, job); unresolved.delete(task.id); recovered++; }
      else if (job.state === "prepared") { await store.setStatus(task.id, "todo"); unresolved.delete(task.id); recovered++; }
      else { if (job.state === "unknown" || job.state === "running") unresolved.add(task.id); await store.setStatus(task.id, "blocked", { summary: "中断任务已保留，需要核对原回执；不会重发未知结果。", artifacts: [{ type: "note", ref: `/api/business/tasks/${task.id}`, note: job.recovery }] }); }
    } catch { unresolved.add(task.id); await store.setStatus(task.id, "blocked", { summary: "执行回执暂不能核对，请检查本地任务目录。", artifacts: [] }); }
  }
  return recovered;
}

export async function handleBusiness(req: IncomingMessage, res: ServerResponse, url: URL): Promise<boolean> {
  const method = req.method || "GET";
  if (url.pathname === "/api/business" && method === "GET") {
    send(res, 200, { enabled: BUSINESS_ENABLED, provider: "NATIVE_CODEX_CLI", scope: "LOCAL_DELIVERY_ONLY", concurrencyLimit: BUSINESS_LIMIT,
      active: running.size, unknownReservations: unresolved.size, capabilities: LOCAL_BUSINESS_CAPABILITIES, fullPolsiaParity: false, externalSystemsIntegrated: false }); return true;
  }
  if (["/api/business/tasks", "/api/business/tasks/batch"].includes(url.pathname) && method === "POST") {
    const companyId = await selectedCompany(url); const body = await readJson(req);
    const items = url.pathname.endsWith("/batch") ? body.items : [body];
    if (!Array.isArray(items) || !items.length || items.length > 4) throw new StagingRequestError(400, "每次创建1至4个任务");
    const inputs = items.map(item => {
      if (!item || typeof item !== "object" || Array.isArray(item)) throw new StagingRequestError(400, "任务需要JSON对象");
      const category = inputText(item.category, "类别", 40) as CodexJobCategory;
      if (!JOB_CATEGORIES.includes(category)) throw new StagingRequestError(400, "此本地业务类别未接入");
      return { category, title: inputText(item.title, "任务名称", 160), instruction: inputText(item.instruction, "交付要求", 10000) };
    });
    const batchId = randomUUID();
    const prepared: { id: string; input: {category: CodexJobCategory; title: string; instruction: string}; job: CodexJobStatus }[] = [];
    for (const input of inputs) {
      const id = randomBytes(4).toString("hex");
      const job = await prepareCodexJob({ ...input, taskId: id });
      prepared.push({ id, input, job });
    }
    await db().begin(async transaction => {
      for (const { id, input, job } of prepared) {
        await transaction`INSERT INTO tasks(id,company_id,title,description,tag,status) VALUES(${id},${companyId},${input.title},
          ${JSON.stringify({ action: "CODEX_LOCAL_JOB", jobId: job.id, category: input.category, instruction: input.instruction, batchId })},'engineering','todo')`;
        await transaction`INSERT INTO task_events(task_id,type,actor,payload) VALUES(${id},'status_change','system',${transaction.json({ to: "todo", batchId })})`;
      }
    });
    send(res, 201, { batchId, tasks: await Promise.all(prepared.map(item => store.get(item.id))), executionStarted: false }); return true;
  }
  const match = url.pathname.match(/^\/api\/business\/tasks\/([a-z0-9]+)(?:\/(artifact|cancel|reconcile))?$/);
  if (match) {
    const companyId = await selectedCompany(url); const task = await store.get(match[1]);
    if (!task || task.companyId !== companyId) throw new StagingRequestError(404, "任务不存在");
    const action = actionOf(task); if (action.action !== "CODEX_LOCAL_JOB" || !action.jobId) throw new StagingRequestError(404, "此任务没有本地业务回执");
    const linkedJob = await getCodexJob(action.jobId);
    if (linkedJob.taskId !== task.id) throw new StagingRequestError(409, "任务与业务回执关联不一致");
    if (method === "GET" && !match[2]) { send(res, 200, { task, job: linkedJob }); return true; }
    if (method === "GET" && match[2] === "artifact") {
      send(res, 200, await readCodexJobArtifact(action.jobId, url.searchParams.get("name") || "")); return true;
    }
    if (method === "POST" && match[2] === "cancel") {
      const controller = controllers.get(task.id);
      if (!controller) throw new StagingRequestError(409, "此服务没有该任务的活动进程");
      controller.abort(); send(res, 202, { cancellationRequested: true, unknownUntilReconciled: true }); return true;
    }
    if (method === "POST" && match[2] === "reconcile") {
      const job = await reconcileCodexJob(action.jobId, { acknowledgeFailedExit: true });
      if (job.state === "succeeded") { await finish(task, job); unresolved.delete(task.id); }
      else if (job.state === "failed" && job.outcome?.startsWith("RECONCILED_CLOSED_WITHOUT_COMPLETION")) {
        if (task.status !== "completed") await store.setStatus(task.id, "failed", { summary: "已核对原进程结束；交付未完成，原回执与部分文件已保留。", artifacts: [{ type: "note", ref: "/api/business/tasks/" + task.id, note: job.recovery }] });
        unresolved.delete(task.id);
      }
      send(res, 200, { task: await store.get(task.id), job, replayed: false }); return true;
    }
  }
  return false;
}

export function businessErrorCode(error: unknown) { return error instanceof CodexJobError ? error.statusCode : undefined; }
