import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { stripTypeScriptTypes } from 'node:module';
const snapshot=JSON.parse(fs.readFileSync(new URL('./virtual-v2-source.json',import.meta.url),'utf8'));
const seed=JSON.parse(fs.readFileSync(new URL('./orca-new-profile-seed.json',import.meta.url),'utf8'));
function moduleSource(suffix, context, exports) {
 const file=snapshot.files.find(x=>x.path.endsWith(suffix));
 const b=Buffer.from(file.content); assert.equal(createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${b.length}\0`),b])).digest('hex'),file.sha);
 const js=stripTypeScriptTypes(file.content).replace(/^import\s[\s\S]*?from\s+['"][^'"]+['"];?\s*$/gm,'').replace(/\bexport\s+(?=(?:async\s+)?(?:function|class|const|let))/g,'');
 return vm.runInNewContext(js+'\n;({'+exports.join(',')+'})',context,{timeout:1000});
}
const tests=[];
async function check(name, fn){await fn();tests.push({name,result:'PASS'});}
const permissions=moduleSource('tui-agent-permissions.ts',{TUI_AGENT_CONFIG:{}},['YOLO_TUI_AGENT_ARGS','YOLO_TUI_AGENT_ENV']);
const defaults=moduleSource('tui-agent-launch-defaults.ts',{...permissions,isTuiAgent:x=>x==='codex'||Object.hasOwn(permissions.YOLO_TUI_AGENT_ARGS,x)||Object.hasOwn(permissions.YOLO_TUI_AGENT_ENV,x)},['DEFAULT_TUI_AGENT_ARGS','DEFAULT_TUI_AGENT_ENV','normalizeTuiAgentArgsRecord','normalizeTuiAgentEnvRecord','resolveTuiAgentLaunchArgs']);
const migration=moduleSource('terminal-settings-migrations.ts',defaults,['migrateAgentYoloDefaults','stripRetiredGlobalSettings']);
const trust=moduleSource('agent-workspace-trust-spawn.ts',{applyAgentWorkspaceTrust:()=>{throw Error('unexpected trust write dependency reached');}},['applyAgentWorkspaceTrustToSpawn','applyStructuredCodexWorkspaceTrust']);
const home=moduleSource('host-env/codex-home.ts',{process:{env:{}}},['getLocalOrcaCodexHomeEnvKeysToDelete']);
const parse=moduleSource('profile-state-document-validation.ts',{},['parseProfileStateRoot']);
await check('官方JSON根解析接受新配置',()=>assert.equal(parse.parseProfileStateRoot(JSON.stringify(seed)).settings.agentWorkspaceTrustEnabled,false));
await check('官方迁移保留显式受限Codex参数',()=>{const v=migration.migrateAgentYoloDefaults(seed.settings);assert.equal(defaults.resolveTuiAgentLaunchArgs('codex',v.agentDefaultArgs),seed.settings.agentDefaultArgs.codex);});
await check('迁移标记缺失时仍保留显式Codex参数',()=>{const v=migration.migrateAgentYoloDefaults({...seed.settings,agentYoloDefaultsMigrated:false});assert.equal(v.agentDefaultArgs.codex,seed.settings.agentDefaultArgs.codex);});
await check('缺少参数键的负例确实返回危险默认值',()=>assert.equal(defaults.resolveTuiAgentLaunchArgs('codex',{}),permissions.YOLO_TUI_AGENT_ARGS.codex));
await check('退休设置过滤保留hooks与trust关闭',()=>{const v=migration.stripRetiredGlobalSettings(seed.settings);assert.equal(v.agentStatusHooksEnabled,false);assert.equal(v.agentWorkspaceTrustEnabled,false);});
await check('PTY预信任关闭不调用写入依赖',()=>assert.equal(trust.applyAgentWorkspaceTrustToSpawn({isFreshLaunch:true,settings:seed.settings}),null));
await check('structured预信任关闭不调用写入依赖',()=>trust.applyStructuredCodexWorkspaceTrust({settings:seed.settings}));
await check('用户自定义CODEX_HOME保留',()=>assert.deepEqual(Array.from(home.getLocalOrcaCodexHomeEnvKeysToDelete({CODEX_HOME:'C:/user/custom'})),['ORCA_CODEX_HOME']));
await check('旧Orca镜像环境仅在值匹配时清除',()=>assert.deepEqual(Array.from(home.getLocalOrcaCodexHomeEnvKeysToDelete({CODEX_HOME:'C:/task/mirror',ORCA_CODEX_HOME:'C:/task/mirror'})),['ORCA_CODEX_HOME','CODEX_HOME']));
const result={scope:'Linux Node离线执行官方函数；依赖替身只覆盖所列早退/配置分支，不是Windows、SQLite导入、实际权限或业务验收',node:process.version,platform:process.platform,commit:snapshot.commit,passed:tests.length,tests,limitations:['未执行完整Store与SQLite首次导入','未启动Orca或Codex','未证明实际Windows子进程环境','未证明整体虚拟极限或任何效率提升']};
fs.writeFileSync(new URL('./virtual-v2-result.json',import.meta.url),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));
