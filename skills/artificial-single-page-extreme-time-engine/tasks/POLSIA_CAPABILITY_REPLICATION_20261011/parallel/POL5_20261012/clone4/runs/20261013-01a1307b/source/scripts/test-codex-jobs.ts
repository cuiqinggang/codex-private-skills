// Controlled child-process boundary tests. No real Codex model is invoked by this file.
import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { test } from "node:test";
import { CodexJobError, createCodexJobService } from "../src/services/codex-jobs.ts";

const parent = path.resolve(".pcl02"); await mkdir(parent, { recursive: true });
const testRoot = await mkdtemp(path.join(parent, "jobs-boundary-"));
const fakePath = path.join(testRoot, "controlled-child.mjs");
await writeFile(fakePath, `import {readFile,writeFile} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
const mode=process.argv[2],args=process.argv.slice(3),cwd=args[args.indexOf('-C')+1],last=args[args.indexOf('-o')+1],schema=JSON.parse(await readFile(args[args.indexOf('--output-schema')+1],'utf8'));
let prompt='';for await(const chunk of process.stdin)prompt+=chunk;
const category=schema.properties.category.const,jobId=schema.properties.jobId.const;
console.log(JSON.stringify({type:'thread.started',thread_id:'CONTROLLED_CHILD_TEST_ONLY'}));
if(mode==='delayed'){console.error('PERSISTED_WHILE_RUNNING');await new Promise(resolve=>setTimeout(resolve,1500));}
if(mode==='timeout'){setInterval(()=>{},1000);}
else if(mode==='exit'){process.exitCode=7;console.error('CONTROLLED_FAILURE');}
else if(mode==='malformed'){console.log('not-json');}
else {
let artifacts;
if(category==='engineering'){
artifacts=['index.html','quote.js'];
await writeFile('quote.js',"export function quoteTotal(q,p){if(!Number.isSafeInteger(q)||q<0||!Number.isSafeInteger(p)||p<0||!Number.isSafeInteger(q*p))throw new RangeError('invalid');return q*p;}\\n");
await writeFile('index.html','<!doctype html><html><head><meta charset="utf-8"><title>Controlled test quote</title></head><body><h1>Local quote tool</h1><p>This is an explicit controlled test artifact, not real Codex business delivery.</p><form id="quote"><input id="quantity"><input id="unit-price"><output id="total"></output></form><script type="module">import {quoteTotal} from "./quote.js";document.getElementById("quote").addEventListener("submit",event=>{event.preventDefault();document.getElementById("total").textContent=quoteTotal(2,1999);});</script></body></html>');
const checked=spawnSync(process.execPath,['--test','acceptance.test.mjs'],{cwd,encoding:'utf8'});
console.log(JSON.stringify({type:'item.completed',item:{type:'command_execution',command:'node --test acceptance.test.mjs',exit_code:checked.status,aggregated_output:checked.stdout||checked.stderr}}));
}else{artifacts=['campaign.md','content-plan.json'];await writeFile('campaign.md','# Controlled local campaign draft\\n'+('Audience and value proposition, sample copy, review criteria, no publication or performance claim. '.repeat(8)));await writeFile('content-plan.json',JSON.stringify({audience:'Controlled test audience',objective:'Draft local plan',items:[1,2,3].map(i=>({channel:'test-'+i,message:'Unsent sample '+i,status:'DRAFT_NOT_SENT'}))}));}
if(mode==='tamper'){await writeFile('AGENTS.md','changed supplied immutable rules');}
if(mode==='extra'){await writeFile('unlisted.txt','should cause rejection');}
if(mode==='missing'){artifacts=['campaign.md'];}
const report={jobId,category,status:'completed',summary:'Controlled child boundary only; no real model execution.',artifacts,externalActions:false};
if(mode==='foreign'){report.artifacts=['../outside.txt'];}
await writeFile(last,JSON.stringify(report));console.log(JSON.stringify({type:'turn.completed',usage:{input_tokens:0,output_tokens:0}}));
}
`, "utf8");

function service(mode = "success") {
  return createCodexJobService({ jobRoot: path.join(testRoot, mode), executable: process.execPath, executableArgs: [fakePath, mode], runnerKind: "CONTROLLED_CHILD_TEST" });
}
function status(code: number) { return (error: unknown) => error instanceof CodexJobError && error.statusCode === code; }

test("prepare uses a new delivery directory, fixed schema and no model execution", async () => {
  const boundary = service();
  const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "Test local draft", instruction: "Create an explicit controlled draft." });
  assert.equal(prepared.state, "prepared"); assert.equal(prepared.nativeCodexVerified, false);
  assert.equal(prepared.externalSystemsIntegrated, false); assert.ok(prepared.deliveryDirectory.startsWith(testRoot));
  assert.deepEqual(prepared.artifactPaths, ["campaign.md", "content-plan.json"]);
  assert.match(await readFile(path.join(prepared.deliveryDirectory, "AGENTS.md"), "utf8"), /Do not read credentials/);
  await assert.rejects(boundary.prepareCodexJob({ category: "monitoring" as "marketing", title: "X", instruction: "Y" }), status(400));
  await assert.rejects(boundary.getCodexJob("../escape"), status(400));
  assert.throws(() => createCodexJobService({ executable: process.execPath, runnerKind: "NATIVE_CODEX" }), status(400));
});

test("real controlled child exit, JSONL, report and actual file hashes are all required", async () => {
  const boundary = service();
  const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "Boundary success", instruction: "Unsent local draft." });
  const result = await boundary.runCodexJob(prepared.id, { timeoutMs: 10000 });
  assert.equal(result.state, "succeeded", result.outcome || "no outcome"); assert.equal(result.exitCode, 0);
  assert.equal(result.runnerKind, "CONTROLLED_CHILD_TEST"); assert.equal(result.nativeCodexVerified, false);
  assert.equal(result.outcome, "CONTROLLED_CHILD_BOUNDARY_VERIFIED_NOT_NATIVE_CODEX");
  assert.equal(result.verification?.passed, true); assert.equal(result.verification?.artifacts.length, 2);
  assert.ok((result.durationMs ?? 0) > 0); assert.equal((await boundary.getCodexJob(result.id)).state, "succeeded");
  const artifact = await boundary.readCodexJobArtifact(result.id, "content-plan.json");
  assert.match(artifact.content, /DRAFT_NOT_SENT/); assert.equal(artifact.sha256.length, 64);
  await assert.rejects(boundary.readCodexJobArtifact(result.id, "../.env"), status(404));
  await assert.rejects(boundary.runCodexJob(prepared.id), status(409));
  const start = JSON.parse(await readFile(path.join(result.receiptsDirectory, "process-started.json"), "utf8"));
  const exit = JSON.parse(await readFile(path.join(result.receiptsDirectory, "exec-exit.json"), "utf8"));
  assert.equal(start.pid, result.pid); assert.equal(exit.pid, result.pid); assert.equal(exit.processClosed, true); assert.equal(exit.exitCode, 0);
});

test("engineering uses the immutable 3-test contract and checks actual local code receipts", async () => {
  const boundary = service(); const prepared = await boundary.prepareCodexJob({ category: "engineering", title: "Controlled quote page", instruction: "Generate the prescribed test fixture." });
  const result = await boundary.runCodexJob(prepared.id, { timeoutMs: 15000 });
  assert.equal(result.state, "succeeded", result.outcome || "no outcome");
  assert.ok(result.verification?.checks.includes("PINNED_ACCEPTANCE_TEST_COMMAND_EXIT0_3_OF3"));
  assert.equal(result.nativeCodexVerified, false); // even actual fixture code testing is not native Codex certification
});

test("nonzero exit, malformed events, changed seeds and unlisted artifacts fail closed", async () => {
  for (const mode of ["exit", "malformed", "tamper", "extra", "missing", "foreign"]) {
    const boundary = service(mode); const prepared = await boundary.prepareCodexJob({ category: "marketing", title: mode, instruction: "Controlled failure boundary." });
    const result = await boundary.runCodexJob(prepared.id, { timeoutMs: 10000 });
    assert.equal(result.state, "failed", mode + ": " + result.outcome); assert.equal(result.nativeCodexVerified, false);
    await assert.rejects(boundary.runCodexJob(prepared.id), status(409));
  }
});

test("timeout stops only the owned child, preserves UNKNOWN and prohibits replay", async () => {
  const boundary = service("timeout"); const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "Timeout fixture", instruction: "Controlled hanging child." });
  const result = await boundary.runCodexJob(prepared.id, { timeoutMs: 400 });
  assert.equal(result.state, "unknown"); assert.equal(result.outcome, "TIMEOUT_OUTCOME_UNKNOWN");
  assert.equal(result.nativeCodexVerified, false); assert.ok(result.pid);
  await assert.rejects(boundary.runCodexJob(prepared.id), status(409));
});

test("simultaneous starts use a retained execution receipt and admit only one child", async () => {
  const boundary = service(); const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "No duplicate starts", instruction: "Controlled exactly-once boundary." });
  const runs = await Promise.allSettled([boundary.runCodexJob(prepared.id), boundary.runCodexJob(prepared.id)]);
  assert.equal(runs.filter((value) => value.status === "fulfilled").length, 1);
  const failed = runs.find((value) => value.status === "rejected") as PromiseRejectedResult;
  assert.ok(status(409)(failed.reason));
});

test("stdout/stderr and owned PID survive on disk while the child is still running", async () => {
  const boundary = service("delayed"); const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "Durable logs", instruction: "Controlled delayed receipt." });
  const running = boundary.runCodexJob(prepared.id, { timeoutMs: 10000 });
  let durable = false;
  for (let attempt = 0; attempt < 100; attempt++) {
    await new Promise((resolve) => setTimeout(resolve, 25));
    try {
      const state = await boundary.getCodexJob(prepared.id);
      const out = await readFile(path.join(state.receiptsDirectory, "stdout.jsonl"), "utf8");
      const err = await readFile(path.join(state.receiptsDirectory, "stderr.txt"), "utf8");
      const start = JSON.parse(await readFile(path.join(state.receiptsDirectory, "process-started.json"), "utf8"));
      if (state.state === "running" && out.includes("thread.started") && err.includes("PERSISTED_WHILE_RUNNING") && start.pid === state.pid && state.pid) { durable = true; break; }
    } catch { /* startup files need time to appear */ }
  }
  const result = await running;
  assert.equal(durable, true, "Expected logs and PID before child exit"); assert.equal(result.state, "succeeded", result.outcome || "no outcome");
});

test("reading a changed accepted artifact fails with conflict rather than returning new content", async () => {
  const boundary = service(); const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "Integrity retained", instruction: "Controlled verified draft." });
  const result = await boundary.runCodexJob(prepared.id);
  assert.equal(result.state, "succeeded", result.outcome || "no outcome");
  await writeFile(path.join(result.deliveryDirectory, "campaign.md"), "# Changed\n" + "Changed after validation. ".repeat(30), "utf8");
  await assert.rejects(boundary.readCodexJobArtifact(result.id, "campaign.md"), status(409));
  assert.equal((await boundary.verifyCodexJobArtifacts(result.id)).passed, false, "DB completion must reject changed accepted artifacts too");
});

test("reconciliation requires complete persisted owned exit evidence and preserves the test-only claim", async () => {
  const boundary = service(); const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "Recovered completed child", instruction: "Controlled crash-state simulation." });
  const result = await boundary.runCodexJob(prepared.id);
  assert.equal(result.state, "succeeded", result.outcome || "no outcome");
  const receipt = { ...result, state: "running", nativeCodexVerified: false };
  await writeFile(path.join(result.receiptsDirectory, "job.json"), JSON.stringify(receipt), "utf8");
  const restarted = service(); assert.equal((await restarted.getCodexJob(result.id)).state, "unknown");
  const reconciled = await restarted.reconcileCodexJob(result.id);
  assert.equal(reconciled.state, "succeeded", reconciled.outcome || "no outcome"); assert.equal(reconciled.nativeCodexVerified, false);
  assert.equal(reconciled.runnerKind, "CONTROLLED_CHILD_TEST");
  await assert.rejects(restarted.runCodexJob(result.id), status(409));
  await writeFile(path.join(result.receiptsDirectory, "job.json"), JSON.stringify(receipt), "utf8");
  await writeFile(path.join(result.receiptsDirectory, "stdout.jsonl"), '{"type":"turn.completed"}\n', "utf8");
  assert.equal((await restarted.reconcileCodexJob(result.id)).state, "unknown", "Edited logs must not recreate success");
});

test("reconciliation without a real process exit remains UNKNOWN and does not start another process", async () => {
  const boundary = service(); const prepared = await boundary.prepareCodexJob({ category: "marketing", title: "Unproven outcome", instruction: "Controlled missing-exit simulation." });
  await writeFile(path.join(prepared.receiptsDirectory, "job.json"), JSON.stringify({ ...prepared, state: "running", pid: 12345 }), "utf8");
  await writeFile(path.join(prepared.receiptsDirectory, "exec-started.json"), JSON.stringify({ id: prepared.id, runnerKind: "CONTROLLED_CHILD_TEST" }), "utf8");
  const reconciled = await service().reconcileCodexJob(prepared.id);
  assert.equal(reconciled.state, "unknown"); assert.equal(reconciled.nativeCodexVerified, false);
  assert.match(reconciled.outcome ?? "", /RECONCILIATION_UNPROVEN/);
  await assert.rejects(boundary.runCodexJob(prepared.id), status(409));
});
