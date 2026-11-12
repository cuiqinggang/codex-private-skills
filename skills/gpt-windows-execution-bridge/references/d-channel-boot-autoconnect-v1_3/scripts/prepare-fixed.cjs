'use strict';
// Thin adaptation of the existing, verified DevSpace startup and ensure recipes.
const fs=require('fs'),cp=require('child_process');
const root='C:/AI/DevSpace-Benchmark-20261031';
const dir=root+'/connector-fixed';
function once(source,oldText,newText){if(source.split(oldText).length!==2)throw Error('BASELINE_MISMATCH');return source.replace(oldText,newText)}
fs.mkdirSync(dir+'/config',{recursive:true});
fs.mkdirSync(dir+'/state',{recursive:true});
const endpoint={provider:'ngrok',origin:'https://ogle-grooving-skipper.ngrok-free.dev',port:17677,executable:'C:/Users/A/AppData/Local/Microsoft/WindowsApps/ngrok.exe'};
fs.writeFileSync(dir+'/endpoint.json',JSON.stringify(endpoint,null,2));
const original=fs.readFileSync(root+'/start-connector.cjs','utf8');
let start=once(original,"runtime=root+'/connector'","runtime=root+'/connector-fixed'");
start=start.replaceAll('17676','17677');
const spawnStart=start.indexOf(" cf=spawn('C:/AI/Public-Server/bin/cloudflared.exe'");
const configStart=start.indexOf(' const cfg=defaultDevspaceConfig();');
if(spawnStart<0||configStart<=spawnStart)throw Error('STARTUP_BASELINE_MISMATCH');
start=start.slice(0,spawnStart)+` const endpoint=JSON.parse(fs.readFileSync(runtime+'/endpoint.json','utf8'));
 const origin=endpoint.origin;
 const tunnelEnv={...process.env};
 for(const key of Object.keys(tunnelEnv))if(/^(http_proxy|https_proxy|all_proxy|http_proxy_env)$/i.test(key))delete tunnelEnv[key];
 cf=spawn(endpoint.executable,['http','http://127.0.0.1:17677','--url',origin,'--inspect=false','--log',logfile,'--log-format','json'],{windowsHide:true,stdio:'ignore',env:tunnelEnv});
 cf.on('error',e=>{console.error(e.message);if(server)server.close();process.exit(1)});
`+start.slice(configStart);
start=once(start,"path.join(process.env.USERPROFILE,'Desktop','DevSpace-连接资料.txt')","runtime+'/CONNECT-INSTRUCTIONS.local.txt'");
if(!fs.existsSync(dir+'/config/auth.json'))fs.copyFileSync(root+'/connector/config/auth.json',dir+'/config/auth.json');
const ensure=fs.readFileSync(fs.existsSync(root+'/ensure-connector.quick-tunnel.cjs')?root+'/ensure-connector.quick-tunnel.cjs':root+'/ensure-connector.cjs','utf8');
let fixedEnsure=once(ensure,"dir=root+'/connector'","dir=root+'/connector-fixed'");
fixedEnsure=fixedEnsure.replaceAll('17676','17677').replaceAll("root+'/start-connector.cjs'","root+'/start-connector-fixed.cjs'").replaceAll('plugin_url_can_change:true','plugin_url_can_change:false');
fixedEnsure=once(fixedEnsure,'return {ok:false,error:e.name}','return {ok:false,error:e.name,cause_code:e.cause?.code}');
fs.writeFileSync(root+'/start-connector-fixed.cjs',start);
fs.writeFileSync(root+'/ensure-connector-fixed.cjs',fixedEnsure);
for(const file of ['start-connector-fixed.cjs','ensure-connector-fixed.cjs']){const check=cp.spawnSync(process.execPath,['--check',root+'/'+file],{encoding:'utf8'});if(check.status!==0)throw Error('SYNTAX_CHECK_FAILED_'+file)}
console.log(JSON.stringify({status:'FIXED_RECIPE_PREPARED',origin:endpoint.origin,port:endpoint.port,original_recipes_unchanged:true,credential_contents_logged:false}));
