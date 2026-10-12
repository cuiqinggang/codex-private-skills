import { spawn } from 'node:child_process';
import { createConnection } from 'node:net';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { homedir } from 'node:os';
import { createHash } from 'node:crypto';
import postgres from 'postgres';

// Task-local diagnostics. No cloud requests, credentials, seeds or Docker mutations.
const root = process.cwd();
const output = resolve(process.argv[2] ?? '.pcl01/evidence');
mkdirSync(output, { recursive: true });
const stamp = () => new Date().toISOString();
const mode = process.argv[3] ?? 'runtime';
const sha = (text) => createHash('sha256').update(text).digest('hex');
const secretNames = ['ANTHROPIC_API_KEY', 'TAVILY_API_KEY', 'GITHUB_TOKEN',
  'DAYTONA_API_KEY', 'NEON_API_KEY', 'RENDER_API_KEY', 'POLSIA_DASHBOARD_PASSWORD'];
function redact(value) {
  let text = String(value ?? '');
  for (const name of [...secretNames, 'DATABASE_URL']) {
    const secret = process.env[name];
    if (secret) text = text.split(secret).join(`[REDACTED:${name}]`);
  }
  return text.replace(/(postgres(?:ql)?:\/\/)[^\s@]+@/gi, '$1[REDACTED]@')
    .replace(/\b(?:sk-[\w-]{10,}|gh[pousr]_[\w]{15,}|github_pat_[\w]{15,})\b/g, '[REDACTED]');
}
function save(name, data) {
  writeFileSync(join(output, name), JSON.stringify(data, null, 2) + '\n');
}
function run(name, args, timeoutMs = 180000, extraEnv = {}) {
  return new Promise((resolveRun) => {
    const started_at = stamp();
    const child = spawn(process.execPath, args, {
      cwd: root, env: { ...process.env, ...extraEnv }, windowsHide: true,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    let stdout = '', stderr = '', timed_out = false, spawn_error = null;
    child.stdout.on('data', (b) => { stdout += b; });
    child.stderr.on('data', (b) => { stderr += b; });
    child.on('error', (e) => { spawn_error = { code: e.code, message: redact(e.message) }; });
    const timer = setTimeout(() => { timed_out = true; child.kill(); }, timeoutMs);
    child.on('close', (exit_code, signal) => {
      clearTimeout(timer);
      const receipt = { name, executable: process.execPath, args, cwd: root,
        pid: child.pid ?? null, started_at, finished_at: stamp(), exit_code, signal,
        timed_out, spawn_error, stdout: redact(stdout), stderr: redact(stderr) };
      save(`${name}.json`, receipt);
      console.log(JSON.stringify({ name, pid: receipt.pid, exit_code, signal, timed_out, spawn_error }));
      resolveRun(receipt);
    });
  });
}
async function tcp(port) {
  return new Promise((resolveTcp) => {
    const socket = createConnection({ host: '127.0.0.1', port });
    let done = false;
    const finish = (result) => { if (!done) { done = true; socket.destroy(); resolveTcp(result); } };
    socket.setTimeout(2500);
    socket.on('connect', () => finish({ port, reachable: true }));
    socket.on('timeout', () => finish({ port, reachable: false, error: 'TIMEOUT' }));
    socket.on('error', (e) => finish({ port, reachable: false, error: e.code }));
  });
}

const modelDir = process.env.PI_CODING_AGENT_DIR ?? join(homedir(), '.pi', 'agent');
const config = { checked_at: stamp(), node: process.version, runner_pid: process.pid,
  pi_agent_dir: modelDir, pi_agent_dir_source: process.env.PI_CODING_AGENT_DIR ? 'existing_env' : 'sdk_default',
  credential_presence: Object.fromEntries(secretNames.map((n) => [n, Boolean(process.env[n])])),
  pi_files_present: Object.fromEntries(['settings.json', 'models.json', 'auth.json'].map((n) => [n, existsSync(join(modelDir, n))])),
  local_env_exists: existsSync(join(root, '.env')), worker_override: 'off',
  credential_values_recorded: false, model_calls_made: 0 };
save(mode === 'runtime' ? 'configuration.json' : `configuration-${mode}.json`, config);

if (mode === 'tests') {
  await run('typecheck', [join(root, 'node_modules/typescript/bin/tsc'), '--noEmit']);
  await run('guard', ['--experimental-test-module-mocks', 'scripts/test-guard.ts']);
} else if (mode === 'dashboard-long') {
  // First startup budget was shorter than cold module loading. Preserve it and
  // collect a longer exact-entry receipt; this never enables the task worker.
  await run('dashboard-long', ['--env-file-if-exists=.env', '--import', 'tsx', 'src/services/dashboard.ts'], 120000,
    { POLSIA_WORKER: 'off', PORT: '4317' });
} else {
  const network = { checked_at: stamp(), results: await Promise.all([5433, 5432, 4317].map(tcp)) };
  save('tcp-before.json', network);
  const existingDefault = readFileSync(join(root, 'src/core/db.ts'), 'utf8')
    .match(/const DEFAULT_URL = "([^"]+)";/)?.[1];
  const connection = process.env.DATABASE_URL ?? existingDefault;
  if (!connection) throw new Error('BLOCKED_EXISTING_DATABASE_CONFIGURATION_MISSING');
  const u = new URL(connection);
  const isLocal = ['localhost', '127.0.0.1', '[::1]', '::1'].includes(u.hostname);
  const dbReceipt = { checked_at: stamp(), endpoint: { host: u.hostname, port: Number(u.port || 5432), database: u.pathname.slice(1) },
    source: process.env.DATABASE_URL ? 'existing_env' : 'application_default', local_only: isLocal, sql: 'SELECT 1 AS ok; read-only catalog query', success: false };
  if (isLocal) {
    const sql = postgres(connection, { connect_timeout: 3, max: 1, idle_timeout: 2, onnotice() {} });
    try {
      const result = await sql`SELECT 1 AS ok`;
      dbReceipt.success = result[0].ok === 1;
      dbReceipt.tables = await sql`SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name`;
    } catch (e) { dbReceipt.error = { code: e.code, message: redact(e.message) }; }
    finally { await sql.end({ timeout: 1 }); }
  } else { dbReceipt.error = { code: 'BLOCKED_NONLOCAL_DATABASE', message: 'No remote database access authorized.' }; }
  save('database.json', dbReceipt);
  console.log(JSON.stringify({ name: 'database', success: dbReceipt.success, error: dbReceipt.error }));
  // Start only the existing dashboard, with the worker forced off. Its boot error is evidence.
  if (isLocal) await run('dashboard', ['--env-file-if-exists=.env', '--import', 'tsx', 'src/services/dashboard.ts'], 20000, { POLSIA_WORKER: 'off', PORT: '4317' });
  const httpResults = [];
  for (const path of ['/', '/api/state', '/api/messages', '/api/document?type=mission', '/fonts/pixel.woff2', '/pcl01-not-found']) {
    try {
      const response = await fetch(`http://127.0.0.1:4317${path}`, { signal: AbortSignal.timeout(2500) });
      const body = Buffer.from(await response.arrayBuffer());
      httpResults.push({ path, http_status: response.status, bytes: body.length, body_sha256: sha(body),
        business_validated: false, reason: 'HTTP response alone does not establish app ownership or business validity.' });
    } catch (e) {
      httpResults.push({ path, http_status: null, error: { code: e.cause?.code ?? e.name, message: redact(e.message) } });
    }
  }
  save('http.json', { checked_at: stamp(), base_url: 'http://127.0.0.1:4317', results: httpResults });
  save('tcp-after.json', { checked_at: stamp(), results: await Promise.all([5433, 4317].map(tcp)) });
  console.log(JSON.stringify({ name: 'http', results: httpResults.map(({ path, http_status, error }) => ({ path, http_status, error })) }));
}
