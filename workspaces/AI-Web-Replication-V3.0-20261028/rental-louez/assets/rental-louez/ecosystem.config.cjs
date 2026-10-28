const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const source = path.join(root, 'source');
const runtimeEnv = Object.fromEntries(fs.readFileSync(path.join(source, '.env.local'), 'utf8').split(/\r?\n/).filter(line => line.includes('=')).map(line => { const i = line.indexOf('='); return [line.slice(0, i), JSON.parse(line.slice(i + 1))]; }));
module.exports = { apps: [{ name: 'rental-n001', script: path.join(source, 'apps/web/.next/standalone/apps/web/server.js'), cwd: path.join(source, 'apps/web/.next/standalone'), interpreter: process.execPath, instances: 1, exec_mode: 'fork', autorestart: true, restart_delay: 1000, max_restarts: 20, min_uptime: '10s', max_memory_restart: '1500M', time: true, env: { ...runtimeEnv, NODE_ENV: 'production', PORT: '4399', HOSTNAME: '127.0.0.1', MIGRATIONS_FOLDER: path.join(source, 'packages/db/src/migrations') } }] };
