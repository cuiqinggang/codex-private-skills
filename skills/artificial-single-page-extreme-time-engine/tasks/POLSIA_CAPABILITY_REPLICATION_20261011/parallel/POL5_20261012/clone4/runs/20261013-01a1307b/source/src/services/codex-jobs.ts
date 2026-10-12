// Business-specific native Codex jobs; this does not replace AgentRuntime or its JS tool boundary.
import { spawn, type ChildProcessWithoutNullStreams } from "node:child_process";
import { createHash, randomUUID } from "node:crypto";
import { mkdir, open, readFile, realpath, readdir, rename, writeFile, type FileHandle } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { performance } from "node:perf_hooks";

export const CODEX_EXECUTABLE = "C:\\Users\\A\\AppData\\Local\\OpenAI\\Codex\\bin\\2e5e00daee91c61d\\codex.exe";
export const CODEX_JOBS_ROOT = fileURLToPath(new URL("../../workspaces/codex-jobs", import.meta.url));
export const JOB_CATEGORIES = ["engineering", "marketing", "support", "sales", "finance", "learning"] as const;
export type CodexJobCategory = typeof JOB_CATEGORIES[number];
export type CodexJobState = "prepared" | "running" | "succeeded" | "failed" | "unknown";
type RunnerKind = "NATIVE_CODEX" | "CONTROLLED_CHILD_TEST";
const MAX_FILE_BYTES = 128 * 1024;
const MAX_ARTIFACT_BYTES = 256 * 1024;
const MAX_LOG_BYTES = 8 * 1024 * 1024;
const MAX_RESULT_BYTES = 64 * 1024;

export class CodexJobError extends Error {
  constructor(public readonly statusCode: 400 | 404 | 409 | 502, message: string) {
    super(message); this.name = "CodexJobError";
  }
}

export interface PrepareCodexJobInput { category: CodexJobCategory; title: string; instruction: string; taskId?: string; }
export interface JobArtifact { path: string; bytes: number; sha256: string; contentType: string; }
export interface ArtifactVerification { passed: boolean; checks: string[]; errors: string[]; artifacts: JobArtifact[]; scope: "LOCAL_DELIVERY_ONLY"; }
interface FinalReport { jobId: string; category: CodexJobCategory; status: "completed" | "blocked"; summary: string; artifacts: string[]; externalActions: false; }
export interface CodexJobStatus {
  id: string; category: CodexJobCategory; title: string; taskId?: string;
  state: CodexJobState; runnerKind: RunnerKind; createdAt: string;
  startedAt?: string; finishedAt?: string; durationMs?: number;
  exitCode?: number | null; pid?: number; threadId?: string;
  directory: string; deliveryDirectory: string; receiptsDirectory: string;
  artifactPaths: string[]; pinnedSeedHashes: Record<string, string>;
  nativeCodexVerified: boolean; externalSystemsIntegrated: false;
  outcome?: string; recovery: string; verification?: ArtifactVerification; report?: FinalReport;
}
export type CodexJob = CodexJobStatus;
export type CodexJobResult = CodexJobStatus;
export interface RunCodexJobOptions { timeoutMs?: number; signal?: AbortSignal; onEvent?: (event: Record<string, unknown>) => void; }

const ARTIFACTS: Record<CodexJobCategory, string[]> = {
  engineering: ["index.html", "quote.js"], marketing: ["campaign.md", "content-plan.json"],
  support: ["faq.md", "support-routing.json"], sales: ["proposal.md", "qualification.json"],
  finance: ["reconciliation.md", "reconciliation.json"], learning: ["sop.md", "checklist.json"],
};
const CATEGORY_CONTRACTS: Record<CodexJobCategory, string> = {
  engineering: "Create a complete, polished, self-contained local business quote webpage index.html and an ES module quote.js exporting quoteTotal(quantity, unitPriceCents). Use nonnegative safe integers and reject invalid/overflow values. The page must have a form id=quote, input id=quantity, input id=unit-price, and output id=total, and use quoteTotal for working interaction. No remote scripts/fonts/assets/network requests. Read the provided acceptance.test.mjs and run exactly: node --test acceptance.test.mjs . Fix your new code until those tests pass; do not edit the supplied tests/package/AGENTS files.",
  marketing: "Write a substantive campaign.md (at least 400 UTF-8 characters), including audience, value proposition, sample copy, measurable review criteria and explicit publication limitations. Create content-plan.json: {audience:string,objective:string,items:[{channel:string,message:string,status:'DRAFT_NOT_SENT'}]}; at least 3 distinct plan items. No sending, publishing, advertising spend, invented performance or unverified claims.",
  support: "Write faq.md (at least 400 characters) and support-routing.json: {faq:[{question:string,answer:string,escalationRole:string,status:'DRAFT_NOT_SENT'}]}; at least 3 useful FAQ entries. Draft answers and role recommendations only; no actual customer sends, assignments, closure or SLA claims.",
  sales: "Write proposal.md (at least 400 characters) and qualification.json: {scope:string,assumptions:string[],questions:string[],outboundStatus:'NOT_SENT'}; at least 3 assumptions and 3 qualification questions. No real outreach, invented identity, prices, accepted contract, customer or revenue claims.",
  finance: "Prepare NEW local SYNTHETIC financial review documents; do not read or rerun old V008 fixtures. Write reconciliation.md (at least 400 characters) and reconciliation.json: {inputKind:'SYNTHETIC',currency:'CNY',invoices:[{id:string,expectedMinor:integer,receivedMinor:integer,differenceMinor:integer,status:'MATCHED'|'PARTIAL'|'UNPAID'|'OVERPAID'}]}. At least 3 uniquely identified invoices; integer minor units, differenceMinor=expectedMinor-receivedMinor and status must match those amounts. No bank/payment/refund API, credentials, real money or actual accounting closure.",
  learning: "Write project-local sop.md (at least 400 characters) and checklist.json: {reuseScope:'PROJECT_LOCAL_ONLY',checks:[{id:string,step:string,evidence:string,passCriteria:string}]}; at least 3 distinct checks. Describe triggers, inputs, procedure, failure/recovery and concrete acceptance evidence. Do not install or modify global/FROZEN Skills, memories or indexes, and do not claim cross-task learning success.",
};

const ENGINEERING_TEST = `import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { quoteTotal } from './quote.js';
test('integer minor-unit quote: normal, free and zero quantity',()=>{assert.equal(quoteTotal(2,1999),3998);assert.equal(quoteTotal(0,1999),0);assert.equal(quoteTotal(3,0),0);assert.equal(quoteTotal(1,1),1);});
test('reject invalid inputs and overflow',()=>{for(const [q,p] of [[-1,1],[1,-1],[1.5,1],[1,1.5],[NaN,1],[1,Infinity],['2',1],[1,'2'],[Number.MAX_SAFE_INTEGER,2]])assert.throws(()=>quoteTotal(q,p));});
test('local webpage contract',async()=>{const html=await readFile('index.html','utf8');assert.match(html,/<html[\\s>]/i);assert.match(html,/id=["']quote["']/);assert.match(html,/id=["']quantity["']/);assert.match(html,/id=["']unit-price["']/);assert.match(html,/id=["']total["']/);assert.match(html,/quoteTotal/);assert.doesNotMatch(html,/(?:src|href)\\s*=\\s*["'](?:https?:)?\\/\\//i);});
`;

function sha(bytes: Uint8Array | string): string { return createHash("sha256").update(bytes).digest("hex").toUpperCase(); }
function requireText(value: unknown, name: string, max: number): string {
  if (typeof value !== "string" || !value.trim() || value.length > max || value.includes("\0")) throw new CodexJobError(400, `Invalid ${name}.`);
  return value.trim();
}
function validateJobId(id: string): void { if (!/^[a-f0-9]{8}-[a-f0-9-]{27}$/.test(id)) throw new CodexJobError(400, "Invalid job ID."); }
function samePath(a: string, b: string): boolean { return process.platform === "win32" ? path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase() : path.resolve(a) === path.resolve(b); }
function typeFor(name: string): string { return name.endsWith(".json") ? "application/json; charset=utf-8" : name.endsWith(".html") ? "text/html; charset=utf-8" : name.endsWith(".js") ? "text/javascript; charset=utf-8" : "text/plain; charset=utf-8"; }
function hasText(value: unknown): value is string { return typeof value === "string" && value.trim().length > 0; }
function object(value: unknown): Record<string, unknown> { if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error("Expected a JSON object."); return value as Record<string, unknown>; }
function atLeastThree(value: unknown): unknown[] { if (!Array.isArray(value) || value.length < 3) throw new Error("At least three entries are required."); return value; }

/** Controlled-child injection is used only by direct tests, never accepted from HTTP input. */
export function createCodexJobService(config: { jobRoot?: string; executable?: string; executableArgs?: string[]; runnerKind?: RunnerKind } = {}) {
  const root = path.resolve(config.jobRoot ?? CODEX_JOBS_ROOT);
  const executable = config.executable ?? CODEX_EXECUTABLE;
  const runnerKind = config.runnerKind ?? "NATIVE_CODEX";
  if (runnerKind === "NATIVE_CODEX" && (executable !== CODEX_EXECUTABLE || (config.executableArgs?.length ?? 0) > 0)) throw new CodexJobError(400, "Native verification is restricted to the fixed verified Codex executable.");
  const live = new Map<string, ChildProcessWithoutNullStreams>();

  function directories(id: string) {
    validateJobId(id); const directory = path.join(root, id);
    return { directory, deliveryDirectory: path.join(directory, "delivery"), receiptsDirectory: path.join(directory, "receipts") };
  }
  async function checkDirectory(directory: string) {
    const relative = path.relative(root, directory);
    if (relative.startsWith("..") || path.isAbsolute(relative)) throw new CodexJobError(409, "Job path escaped its workspace.");
    const [realRoot, actual] = await Promise.all([realpath(root), realpath(directory)]);
    if (!samePath(root, realRoot) || !samePath(directory, actual)) throw new CodexJobError(409, "Job path redirection is not allowed.");
  }
  async function writeState(job: CodexJobStatus) {
    const pending = path.join(job.receiptsDirectory, `job-${randomUUID()}.pending.json`);
    const handle = await open(pending, "wx");
    try { await handle.writeFile(JSON.stringify(job, null, 2), "utf8"); await handle.sync(); }
    finally { await handle.close(); }
    // Windows can briefly deny replacing a receipt while a status reader has it open.
    // This retries only the atomic file replacement; it never re-executes a business job.
    for (let attempt = 0; ; attempt++) {
      try { await rename(pending, path.join(job.receiptsDirectory, "job.json")); break; }
      catch (error) {
        if (process.platform !== "win32" || !["EPERM", "EACCES", "EBUSY"].includes((error as NodeJS.ErrnoException).code ?? "") || attempt >= 9) throw error;
        await new Promise((resolve) => setTimeout(resolve, 10 * (attempt + 1)));
      }
    }
  }
  async function getCodexJob(id: string): Promise<CodexJobStatus> {
    const dirs = directories(id);
    try {
      await checkDirectory(dirs.directory); await checkDirectory(dirs.receiptsDirectory);
      const bytes = await readFile(path.join(dirs.receiptsDirectory, "job.json"));
      if (bytes.length > MAX_RESULT_BYTES) throw new CodexJobError(409, "Job receipt exceeds its limit.");
      const value = JSON.parse(bytes.toString("utf8")) as CodexJobStatus;
      if (value.id !== id || value.directory !== dirs.directory || value.deliveryDirectory !== dirs.deliveryDirectory || value.receiptsDirectory !== dirs.receiptsDirectory || value.runnerKind !== runnerKind || !JOB_CATEGORIES.includes(value.category)) throw new CodexJobError(409, "Job receipt identity mismatch.");
      if (value.state === "running" && !live.has(id)) return { ...value, state: "unknown", nativeCodexVerified: false, outcome: "PROCESS_OUTCOME_REQUIRES_RECONCILIATION", recovery: "Read saved JSONL, final report and artifacts before any new job; do not replay this job automatically." };
      return value;
    } catch (error) {
      if (error instanceof CodexJobError) throw error;
      if ((error as NodeJS.ErrnoException).code === "ENOENT") throw new CodexJobError(404, "Unknown local Codex job.");
      throw new CodexJobError(409, "Job receipt is not safely readable.");
    }
  }
  async function prepareCodexJob(input: PrepareCodexJobInput): Promise<CodexJob> {
    if (!input || typeof input !== "object" || !JOB_CATEGORIES.includes(input.category)) throw new CodexJobError(400, "Unsupported local business category.");
    const title = requireText(input.title, "title", 200);
    const instruction = requireText(input.instruction, "instruction", 16000);
    const taskId = input.taskId === undefined ? undefined : requireText(input.taskId, "taskId", 100);
    await mkdir(root, { recursive: true }); await checkDirectory(root);
    const id = randomUUID(); const dirs = directories(id);
    await mkdir(dirs.directory); await mkdir(dirs.deliveryDirectory); await mkdir(dirs.receiptsDirectory);
    const rule = `# This new local business job\nWork only in this delivery directory. Authorized outputs: ${ARTIFACTS[input.category].join(", ")}. Existing supplied files are immutable. Do not read credentials/auth/tokens or unrelated history. Do not login, change accounts/system/proxy/network, install packages, publish, send, pay, deploy externally or access production. Retain existing approval rules. Use only built-in local tools and Node built-ins. Results describe LOCAL_DELIVERY_ONLY; external systems are not integrated.\n`;
    const seeds: Record<string, string> = { "AGENTS.md": rule };
    if (input.category === "engineering") { seeds["acceptance.test.mjs"] = ENGINEERING_TEST; seeds["package.json"] = '{"type":"module","private":true}\n'; }
    for (const [name, value] of Object.entries(seeds)) await writeFile(path.join(dirs.deliveryDirectory, name), value, "utf8");
    const schema = { type: "object", properties: { jobId: { type: "string", const: id }, category: { type: "string", const: input.category }, status: { type: "string", enum: ["completed", "blocked"] }, summary: { type: "string" }, artifacts: { type: "array", items: { type: "string", enum: ARTIFACTS[input.category] } }, externalActions: { type: "boolean", const: false } }, required: ["jobId", "category", "status", "summary", "artifacts", "externalActions"], additionalProperties: false };
    await writeFile(path.join(dirs.receiptsDirectory, "result.schema.json"), JSON.stringify(schema, null, 2), "utf8");
    const prompt = `Authorized new LOCAL business job ${id} (${input.category}).\n${rule}\nBusiness-specific contract: ${CATEGORY_CONTRACTS[input.category]}\nTitle: ${title}\nUser requirements (within the above local scope):\n${instruction}\nProduce only the allowed artifact files; preserve supplied files. Finish with JSON exactly matching the supplied output schema, jobId=${id}, category=${input.category}, externalActions=false. Do not claim success unless the new files exist and required tests have actually passed. If authorization or runtime prevents the task, use status=blocked with the real reason.\n`;
    await writeFile(path.join(dirs.receiptsDirectory, "prompt.txt"), prompt, "utf8");
    const job: CodexJob = { id, category: input.category, title, taskId, state: "prepared", runnerKind, createdAt: new Date().toISOString(), ...dirs, artifactPaths: [...ARTIFACTS[input.category]], pinnedSeedHashes: Object.fromEntries(Object.entries(seeds).map(([name, value]) => [name, sha(value)])), nativeCodexVerified: false, externalSystemsIntegrated: false, recovery: "Prepared only; no model or business process started." };
    await writeState(job); return job;
  }
  async function readBounded(directory: string, name: string, limit = MAX_FILE_BYTES, allowEmpty = false): Promise<Buffer> {
    if (path.basename(name) !== name || name.includes("\\") || name.includes("/") || name.includes("\0")) throw new CodexJobError(400, "Invalid artifact path.");
    await checkDirectory(directory);
    const target = path.join(directory, name);
    if (!samePath(await realpath(target), target)) throw new CodexJobError(409, "Artifact redirection is not allowed.");
    const handle = await open(target, "r");
    try { const stat = await handle.stat(); if (!stat.isFile() || stat.size < (allowEmpty ? 0 : 1) || stat.size > limit) throw new CodexJobError(409, "Artifact size is invalid."); const bytes = await handle.readFile(); if (bytes.length !== stat.size || bytes.length > limit) throw new CodexJobError(409, "Artifact changed while reading."); return bytes; }
    finally { await handle.close(); }
  }
  async function verifyCodexJobArtifacts(id: string): Promise<ArtifactVerification> {
    const job = await getCodexJob(id);
    const checks: string[] = [], errors: string[] = [], artifacts: JobArtifact[] = [];
    const contents: Record<string, string> = {};
    try {
      const allowed = new Set([...ARTIFACTS[job.category], ...Object.keys(job.pinnedSeedHashes)]);
      for (const entry of await readdir(job.deliveryDirectory, { withFileTypes: true })) if (!entry.isFile() || !allowed.has(entry.name)) throw new Error("Unexpected file/directory in delivery allowlist.");
      for (const [name, expected] of Object.entries(job.pinnedSeedHashes)) if (sha(await readBounded(job.deliveryDirectory, name)) !== expected) throw new Error(`Supplied acceptance/rule file changed: ${name}`);
      checks.push("IMMUTABLE_SEEDS_MATCH");
      let total = 0;
      for (const name of ARTIFACTS[job.category]) {
        const bytes = await readBounded(job.deliveryDirectory, name); total += bytes.length;
        contents[name] = new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes);
        artifacts.push({ path: name, bytes: bytes.length, sha256: sha(bytes), contentType: typeFor(name) });
      }
      if (total > MAX_ARTIFACT_BYTES) throw new Error("Total artifact bytes exceed the limit.");
      checks.push("ALLOWLIST_UTF8_SIZE_AND_HASH");
      if (job.verification?.passed) {
        for (const accepted of job.verification.artifacts) {
          const current = artifacts.find((item) => item.path === accepted.path);
          if (!current || current.bytes !== accepted.bytes || current.sha256 !== accepted.sha256) throw new Error("Previously accepted artifact has changed since verification.");
        }
        checks.push("PREVIOUSLY_ACCEPTED_ARTIFACT_HASHES_MATCH");
      }
      if (job.category === "engineering") {
        const html = contents["index.html"]!;
        if (html.length < 300 || !/<html[\s>]/i.test(html) || !/id=["']quote["']/.test(html) || !/id=["']quantity["']/.test(html) || !/id=["']unit-price["']/.test(html) || !/id=["']total["']/.test(html) || !/quoteTotal/.test(html)) throw new Error("Webpage contract is incomplete.");
        if (/(?:src|href)\s*=\s*["'](?:https?:)?\/\//i.test(html) || /fetch\s*\(|XMLHttpRequest|WebSocket|import\s*\(?\s*["']https?:/i.test(html + contents["quote.js"])) throw new Error("Webpage/code requests external resources.");
        if (!/export\s+(?:function\s+quoteTotal|\{[^}]*\bquoteTotal\b)/.test(contents["quote.js"]!)) throw new Error("quoteTotal export is missing.");
        const lines = (await readBounded(job.receiptsDirectory, "stdout.jsonl", MAX_LOG_BYTES)).toString("utf8").split(/\r?\n/).filter(Boolean);
        const passed = lines.some((line) => { const event = JSON.parse(line); const item = event.item; return event.type === "item.completed" && item?.type === "command_execution" && item.exit_code === 0 && /\bnode(?:\.exe)?["']?\s+--test\s+["']?(?:\.\/)?acceptance\.test\.mjs\b/i.test(item.command ?? "") && /(?:#|ℹ)\s*pass\s+3\b/.test(item.aggregated_output ?? "") && /(?:#|ℹ)\s*fail\s+0\b/.test(item.aggregated_output ?? ""); });
        if (!passed) throw new Error("No successful native command receipt for the fixed engineering acceptance tests.");
        checks.push("LOCAL_WEBPAGE_CONTRACT", "PINNED_ACCEPTANCE_TEST_COMMAND_EXIT0_3_OF3");
      } else {
        const [md, jsonName] = ARTIFACTS[job.category];
        if (contents[md!]!.trim().length < 400) throw new Error("Business document is too short for the delivery contract.");
        const data = object(JSON.parse(contents[jsonName!]!));
        if (job.category === "marketing") { if (!hasText(data.audience) || !hasText(data.objective)) throw new Error("Campaign audience/objective missing."); for (const row of atLeastThree(data.items)) { const item = object(row); if (!hasText(item.channel) || !hasText(item.message) || item.status !== "DRAFT_NOT_SENT") throw new Error("Campaign items must be unsent drafts."); } }
        if (job.category === "support") for (const row of atLeastThree(data.faq)) { const item = object(row); if (!hasText(item.question) || !hasText(item.answer) || !hasText(item.escalationRole) || item.status !== "DRAFT_NOT_SENT") throw new Error("FAQ routing is incomplete or not a draft."); }
        if (job.category === "sales") { if (!hasText(data.scope) || data.outboundStatus !== "NOT_SENT" || !atLeastThree(data.assumptions).every(hasText) || !atLeastThree(data.questions).every(hasText)) throw new Error("Qualification contract is incomplete."); }
        if (job.category === "finance") { if (data.inputKind !== "SYNTHETIC" || data.currency !== "CNY") throw new Error("Finance must be explicit local synthetic CNY."); const ids = new Set<string>(); for (const row of atLeastThree(data.invoices)) { const item = object(row); const expected = item.expectedMinor as number, received = item.receivedMinor as number; if (!hasText(item.id) || ids.has(item.id) || !Number.isSafeInteger(expected) || expected < 0 || !Number.isSafeInteger(received) || received < 0 || item.differenceMinor !== expected - received) throw new Error("Invoice identity or minor-unit arithmetic is invalid."); ids.add(item.id); const status = expected === received ? "MATCHED" : received === 0 ? "UNPAID" : received < expected ? "PARTIAL" : "OVERPAID"; if (item.status !== status) throw new Error("Invoice status differs from amounts."); } }
        if (job.category === "learning") { if (data.reuseScope !== "PROJECT_LOCAL_ONLY") throw new Error("Learning scope must stay project local."); const ids = new Set<string>(); for (const row of atLeastThree(data.checks)) { const item = object(row); if (!hasText(item.id) || ids.has(item.id) || !hasText(item.step) || !hasText(item.evidence) || !hasText(item.passCriteria)) throw new Error("Learning checklist lacks unique executable criteria."); ids.add(item.id); } }
        checks.push("BUSINESS_DOCUMENT_AND_STRUCTURED_CATEGORY_CONTRACT");
      }
    } catch (error) { errors.push(error instanceof Error ? error.message : "Artifact verification failed."); }
    return { passed: errors.length === 0, checks, errors, artifacts, scope: "LOCAL_DELIVERY_ONLY" };
  }
  async function readCodexJobArtifact(id: string, name: string): Promise<JobArtifact & { content: string }> {
    const job = await getCodexJob(id);
    if (!ARTIFACTS[job.category].includes(name)) throw new CodexJobError(404, "Artifact is not in this job's allowlist.");
    try {
      const bytes = await readBounded(job.deliveryDirectory, name), actualSha = sha(bytes);
      if (job.state === "succeeded") {
        const accepted = job.verification?.artifacts.find((artifact) => artifact.path === name);
        if (!job.verification?.passed || !accepted || accepted.sha256 !== actualSha || accepted.bytes !== bytes.length) throw new CodexJobError(409, "Accepted artifact has changed since verification.");
      }
      return { path: name, bytes: bytes.length, sha256: actualSha, contentType: typeFor(name), content: new TextDecoder("utf-8", { fatal: true, ignoreBOM: true }).decode(bytes) };
    }
    catch (error) { if (error instanceof CodexJobError) throw error; throw new CodexJobError(job.state === "succeeded" ? 409 : 404, "Artifact is missing or not safely readable."); }
  }
  async function validateCompletedDelivery(job: CodexJobStatus, stdout: string): Promise<"succeeded"> {
    const events = stdout.split(/\r?\n/).filter((line) => line.trim()).map((line) => object(JSON.parse(line)));
    let completedIndex = -1;
    for (let index = 0; index < events.length; index++) if (events[index].type === "turn.completed") completedIndex = index;
    const invalidEvent = events.some((event, index) => event.type === "turn.failed" || (event.type === "error" && !(index < completedIndex && typeof event.message === "string" && /^Reconnecting\.\.\. [1-5]\/5 \(request timed out\)$/.test(event.message))));
    if (completedIndex < 0 || invalidEvent) throw new Error("No verified completed Codex turn receipt; only recovered timeout reconnect notices are permitted before completion.");
    const report = object(JSON.parse((await readBounded(job.receiptsDirectory, "last-message.json", MAX_RESULT_BYTES)).toString("utf8")));
    if (Object.keys(report).sort().join(",") !== "artifacts,category,externalActions,jobId,status,summary" || report.jobId !== job.id || report.category !== job.category || report.status !== "completed" || !hasText(report.summary) || report.summary.length > 12000 || report.externalActions !== false || !Array.isArray(report.artifacts) || [...report.artifacts].sort().join(",") !== [...ARTIFACTS[job.category]].sort().join(",")) throw new Error("Final result does not meet the exact completed local job contract.");
    job.report = report as unknown as FinalReport;
    const accepted = job.verification;
    job.verification = await verifyCodexJobArtifacts(job.id);
    if (!job.verification.passed) throw new Error(job.verification.errors.join("; "));
    if (accepted?.passed && accepted.artifacts.some((item) => { const current = job.verification!.artifacts.find((artifact) => artifact.path === item.path); return !current || current.bytes !== item.bytes || current.sha256 !== item.sha256; })) throw new Error("Previously accepted artifacts changed before reconciliation.");
    job.state = "succeeded"; job.nativeCodexVerified = runnerKind === "NATIVE_CODEX";
    job.outcome = runnerKind === "NATIVE_CODEX" ? "NATIVE_CODEX_LOCAL_DELIVERY_VERIFIED" : "CONTROLLED_CHILD_BOUNDARY_VERIFIED_NOT_NATIVE_CODEX";
    return "succeeded";
  }
  async function reconcileCodexJob(id: string, options: { acknowledgeFailedExit?: boolean } = {}): Promise<CodexJobStatus> {
    if (live.has(id)) throw new CodexJobError(409, "The owned process is still running; it cannot be reconciled yet.");
    const job = await getCodexJob(id);
    const reviewRejectedCompletion = options.acknowledgeFailedExit === true && job.state === "failed" && job.exitCode === 0 && job.outcome?.startsWith("VERIFICATION_FAILED:");
    if (job.state !== "unknown" && job.state !== "running" && !reviewRejectedCompletion) return job;
    if (reviewRejectedCompletion) {
      const previous = await open(path.join(job.receiptsDirectory, `verification-review-${Date.now()}-${randomUUID()}.json`), "wx");
      try { await previous.writeFile(JSON.stringify({ reviewedAt: new Date().toISOString(), previousJob: job, action: "REVERIFY_EXISTING_RECEIPTS_ONLY", executionStarted: false }, null, 2)); await previous.sync(); }
      finally { await previous.close(); }
    }
    job.nativeCodexVerified = false;
    try {
      const receipt = object(JSON.parse((await readBounded(job.receiptsDirectory, "exec-exit.json", MAX_RESULT_BYTES)).toString("utf8")));
      if (receipt.id !== id || receipt.runnerKind !== runnerKind || receipt.pid !== job.pid || !Number.isInteger(receipt.pid) || (receipt.pid as number) <= 0 || receipt.processClosed !== true || !(receipt.exitCode === null || Number.isInteger(receipt.exitCode)) || !hasText(receipt.finishedAt) || !Number.isFinite(Date.parse(receipt.finishedAt)) || typeof receipt.durationMs !== "number" || !Number.isFinite(receipt.durationMs) || receipt.durationMs < 0) throw new Error("No complete owned-process exit receipt.");
      const stdout = await readBounded(job.receiptsDirectory, "stdout.jsonl", MAX_LOG_BYTES, true);
      const stderrPath = path.join(job.receiptsDirectory, "stderr.txt");
      if (!samePath(await realpath(stderrPath), stderrPath)) throw new Error("Stderr receipt was redirected.");
      const stderrHandle = await open(stderrPath, "r"); let stderr: Buffer;
      try { const stat = await stderrHandle.stat(); if (!stat.isFile() || stat.size > MAX_LOG_BYTES) throw new Error("Stderr receipt exceeds its limit."); stderr = await stderrHandle.readFile(); if (stderr.length !== stat.size) throw new Error("Stderr receipt changed while reading."); }
      finally { await stderrHandle.close(); }
      if (stdout.length !== receipt.stdoutBytes || stderr.length !== receipt.stderrBytes || sha(stdout) !== receipt.stdoutSha256 || sha(stderr) !== receipt.stderrSha256) throw new Error("Captured process logs differ from the owned-process exit receipt.");
      job.exitCode = receipt.exitCode as number | null; job.finishedAt = receipt.finishedAt; job.durationMs = receipt.durationMs;
      if (receipt.forced || receipt.processError || receipt.exitCode !== 0) {
        if (!options.acknowledgeFailedExit) throw new Error("Explicit review required for a closed incomplete process.");
        job.state = "failed"; job.outcome = "RECONCILED_CLOSED_WITHOUT_COMPLETION: " + String(receipt.forced || receipt.processError || receipt.exitCode);
        job.recovery = "Explicit review verified the owned process ended and logs match. This delivery is failed, never completed or replayed; partial files remain for inspection.";
      } else {
        job.state = await validateCompletedDelivery(job, stdout.toString("utf8"));
        job.recovery = "Reconciled from persisted owned-process exit, logs, report and artifacts; never replay this job. External systems remain unintegrated.";
      }
    } catch (error) {
      job.state = "unknown"; job.outcome = `RECONCILIATION_UNPROVEN: ${error instanceof Error ? error.message : String(error)}`;
      job.recovery = "Preserve existing receipts and investigate; no clean complete exit proof, so no success claim and no automatic replay.";
    }
    await writeState(job); return job;
  }
  async function runCodexJob(id: string, options: RunCodexJobOptions = {}): Promise<CodexJobResult> {
    const job = await getCodexJob(id);
    if (job.state !== "prepared") throw new CodexJobError(409, "This job has already started; reconcile its receipts instead of replaying it.");
    const timeoutMs = options.timeoutMs ?? 300000;
    if (!Number.isInteger(timeoutMs) || timeoutMs < 100 || timeoutMs > 900000) throw new CodexJobError(400, "Invalid job timeout.");
    if (options.signal?.aborted) throw new CodexJobError(409, "Job was cancelled before execution.");
    // An immutable execution receipt, not a retry/queue/lease mechanism. It is never removed.
    try { const marker = await open(path.join(job.receiptsDirectory, "exec-started.json"), "wx"); await marker.writeFile(JSON.stringify({ id, runnerKind, startedAt: new Date().toISOString() })); await marker.close(); }
    catch { throw new CodexJobError(409, "An execution receipt already exists or cannot be created; do not replay unknown results."); }
    job.state = "running"; job.startedAt = new Date().toISOString(); job.recovery = "Execution in progress; no automatic replay.";
    await writeState(job);
    const prompt = await readFile(path.join(job.receiptsDirectory, "prompt.txt"), "utf8");
    const args = [...(config.executableArgs ?? []), "-a", "on-request", "exec", "--sandbox", "workspace-write", "--skip-git-repo-check", "-C", job.deliveryDirectory, "--json", "--ephemeral", "--output-schema", path.join(job.receiptsDirectory, "result.schema.json"), "-o", path.join(job.receiptsDirectory, "last-message.json"), "-"];
    const environment: NodeJS.ProcessEnv = {};
    // Inherit OS/runtime and existing routing values; do not copy server DB/API credentials.
    for (const key of ["PATH", "Path", "PATHEXT", "SystemRoot", "SYSTEMROOT", "WINDIR", "TEMP", "TMP", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "HOMEDRIVE", "HOMEPATH", "CODEX_HOME", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "all_proxy", "no_proxy"]) if (process.env[key] !== undefined) environment[key] = process.env[key];
    const begin = performance.now(); let stdout = "", stderr = "", lineBuffer = "", logBytes = 0, forced: string | undefined, processError: string | undefined;
    const stdoutFile = await open(path.join(job.receiptsDirectory, "stdout.jsonl"), "wx");
    let stderrFile: FileHandle;
    try { stderrFile = await open(path.join(job.receiptsDirectory, "stderr.txt"), "wx"); await stdoutFile.sync(); await stderrFile.sync(); }
    catch (error) { await stdoutFile.close(); throw error; }
    let logWrites = Promise.resolve(), processClosed = false;
    let child: ChildProcessWithoutNullStreams | undefined;
    const stopOwned = (reason: string) => {
      if (forced) return; forced = reason;
      if (!child || child.exitCode !== null || child.signalCode !== null) return;
      // Only this newly spawned process and its descendants are eligible for termination.
      if (process.platform === "win32" && child.pid) {
        try {
          const killer = spawn(path.join(environment.SystemRoot ?? environment.SYSTEMROOT ?? "C:\\Windows", "System32", "taskkill.exe"), ["/PID", String(child.pid), "/T", "/F"], { shell: false, windowsHide: true, stdio: "ignore" });
          killer.once("error", () => { if (child?.exitCode === null && child?.signalCode === null) child.kill(); });
          killer.once("close", (code) => { if (code !== 0 && child?.exitCode === null && child?.signalCode === null) child.kill(); });
        } catch { if (child.exitCode === null && child.signalCode === null) child.kill(); }
      } else child.kill();
    };
    const appendLog = (handle: FileHandle, chunk: string, stream: NodeJS.ReadableStream) => {
      stream.pause();
      logWrites = logWrites.then(async () => { await handle.appendFile(chunk, "utf8"); await handle.sync(); }).catch((error) => { processError = `Process log persistence failed: ${error instanceof Error ? error.message : String(error)}`; stopOwned("LOG_PERSISTENCE_OUTCOME_UNKNOWN"); }).finally(() => { stream.resume(); });
    };
    const timer = setTimeout(() => stopOwned("TIMEOUT_OUTCOME_UNKNOWN"), timeoutMs);
    const onAbort = () => stopOwned("CANCELLED_OUTCOME_UNKNOWN"); options.signal?.addEventListener("abort", onAbort, { once: true });
    let exitCode: number | null = null, closedPromise: Promise<number | null> | undefined;
    try {
      child = spawn(executable, args, { cwd: job.deliveryDirectory, env: environment, shell: false, windowsHide: true, stdio: ["pipe", "pipe", "pipe"] });
      live.set(id, child); job.pid = child.pid;
      child.stdout.setEncoding("utf8"); child.stderr.setEncoding("utf8");
      child.stdout.on("data", (chunk: string) => { logBytes += Buffer.byteLength(chunk); if (logBytes > MAX_LOG_BYTES) { stopOwned("LOG_LIMIT_OUTCOME_UNKNOWN"); return; } stdout += chunk; appendLog(stdoutFile, chunk, child!.stdout); lineBuffer += chunk; const lines = lineBuffer.split(/\r?\n/); lineBuffer = lines.pop() ?? ""; for (const line of lines) { if (!line.trim()) continue; try { const event = object(JSON.parse(line)); if (event.type === "thread.started" && typeof event.thread_id === "string") job.threadId = event.thread_id; try { options.onEvent?.(event); } catch { /* observers cannot change job outcome */ } } catch { processError = "Malformed JSONL event stream."; } } });
      child.stderr.on("data", (chunk: string) => { logBytes += Buffer.byteLength(chunk); if (logBytes > MAX_LOG_BYTES) { stopOwned("LOG_LIMIT_OUTCOME_UNKNOWN"); return; } stderr += chunk; appendLog(stderrFile, chunk, child!.stderr); });
      child.stdin.on("error", () => { /* close/error event supplies the final process outcome */ });
      closedPromise = new Promise<number | null>((resolve) => { child!.once("error", (error) => { processError = error.message; }); child!.once("close", (code) => { processClosed = true; resolve(code); }); });
      await writeState(job);
      const ownership = await open(path.join(job.receiptsDirectory, "process-started.json"), "wx");
      try { await ownership.writeFile(JSON.stringify({ id, runnerKind, pid: job.pid, startedAt: job.startedAt, executable, deliveryDirectory: job.deliveryDirectory })); await ownership.sync(); }
      finally { await ownership.close(); }
      child.stdin.end(prompt); exitCode = await closedPromise;
    } catch (error) { processError = error instanceof Error ? error.message : String(error); if (child && closedPromise) { stopOwned("PROCESS_RECEIPT_ERROR_OUTCOME_UNKNOWN"); exitCode = await closedPromise; } }
    finally { clearTimeout(timer); options.signal?.removeEventListener("abort", onAbort); live.delete(id); }
    job.exitCode = exitCode; job.durationMs = performance.now() - begin; job.finishedAt = new Date().toISOString();
    await logWrites;
    try { await stdoutFile.sync(); await stderrFile.sync(); }
    finally { await stdoutFile.close(); await stderrFile.close(); }
    if (processClosed) {
      const exitReceipt = await open(path.join(job.receiptsDirectory, "exec-exit.json"), "wx");
      try { await exitReceipt.writeFile(JSON.stringify({ id, runnerKind, pid: job.pid, processClosed: true, exitCode, finishedAt: job.finishedAt, durationMs: job.durationMs, forced, processError, stdoutBytes: Buffer.byteLength(stdout), stderrBytes: Buffer.byteLength(stderr), stdoutSha256: sha(stdout), stderrSha256: sha(stderr) }, null, 2)); await exitReceipt.sync(); }
      finally { await exitReceipt.close(); }
    }
    if (forced) { job.state = "unknown"; job.outcome = forced; }
    else if (processError || exitCode !== 0) { job.state = "failed"; job.outcome = processError ? `PROCESS_ERROR: ${processError}` : "CODEX_EXIT_NONZERO"; }
    else {
      try {
        job.state = await validateCompletedDelivery(job, stdout);
      } catch (error) { job.state = "failed"; job.outcome = `VERIFICATION_FAILED: ${error instanceof Error ? error.message : String(error)}`; }
    }
    job.recovery = job.state === "succeeded" ? "Confirmed done locally; never replay this job. External systems remain unintegrated." : "Read execution JSONL, stderr, final report and actual artifacts. Unknown results must be reconciled; this adapter never retries or resumes automatically.";
    await writeState(job); return job;
  }
  return { prepareCodexJob, runCodexJob, getCodexJob, verifyCodexJobArtifacts, readCodexJobArtifact, reconcileCodexJob };
}

const service = createCodexJobService();
export const prepareCodexJob = service.prepareCodexJob;
export const runCodexJob = service.runCodexJob;
export const getCodexJob = service.getCodexJob;
export const verifyCodexJobArtifacts = service.verifyCodexJobArtifacts;
export const readCodexJobArtifact = service.readCodexJobArtifact;
export const reconcileCodexJob = service.reconcileCodexJob;
