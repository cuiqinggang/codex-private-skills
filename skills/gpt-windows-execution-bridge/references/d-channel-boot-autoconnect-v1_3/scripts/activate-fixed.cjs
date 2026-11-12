'use strict';
// Activate only after ChatGPT's new native entry has passed its actual checks.
const fs=require('fs'),cp=require('child_process');
const root='C:/AI/DevSpace-Benchmark-20261031';
const proof=JSON.parse(fs.readFileSync(root+'/fixture/d-channel-fixed-native-acceptance.json','utf8'));
if(proof.status!=='NATIVE_RECONNECTED_PASS'||proof.entry!=='Windows D 20261110-02'||proof.hostname!=='DESKTOP-4A1EGTM'||proof.exit_code!==0)throw Error('NATIVE_ACCEPTANCE_REQUIRED');
const origin='https://ogle-grooving-skipper.ngrok-free.dev';
const s=JSON.parse(fs.readFileSync(root+'/connector-fixed/status.json','utf8'));
if(s.mcp_url!==origin+'/mcp')throw Error('FIXED_ENDPOINT_MISMATCH');
const current=root+'/ensure-connector.cjs',backup=root+'/ensure-connector.quick-tunnel.cjs';
if(!fs.existsSync(backup))fs.copyFileSync(current,backup);
const shim="'use strict';\nconst fs=require('fs');\nconst root='C:/AI/DevSpace-Benchmark-20261031';\nconst fixed=fs.existsSync(root+'/connector-fixed/active.json');\nif(fixed)process.on('exit',()=>{try{for(const file of ['status.json','autostart-health.json'])if(fs.existsSync(root+'/connector-fixed/'+file))fs.copyFileSync(root+'/connector-fixed/'+file,root+'/connector/'+file)}catch(e){console.error('CANONICAL_STATUS_PUBLISH_FAILED');process.exitCode=2}});\nrequire(fixed?root+'/ensure-connector-fixed.cjs':root+'/ensure-connector.quick-tunnel.cjs');\n";
fs.writeFileSync(root+'/connector-fixed/active.json',JSON.stringify({activated_at:new Date().toISOString(),entry:proof.entry,origin},null,2));
fs.writeFileSync(current,shim);
const result=cp.spawnSync(process.execPath,['--check',current],{encoding:'utf8'});
if(result.status!==0){fs.copyFileSync(backup,current);fs.unlinkSync(root+'/connector-fixed/active.json');throw Error('ROLLED_BACK_BAD_SYNTAX')}
const config=root+'/connector/config/config.jsonc';
if(!fs.existsSync(config+'.before-fixed'))fs.copyFileSync(config,config+'.before-fixed');
fs.copyFileSync(root+'/connector-fixed/config/config.jsonc',config);
fs.writeFileSync(root+'/connector/CONNECT-URL.txt',origin+'/mcp\n');
console.log(JSON.stringify({status:'EXISTING_STARTUP_RECIPE_ROUTED_TO_FIXED',entry:proof.entry,task_definition_changed:false,rollback:backup}));
