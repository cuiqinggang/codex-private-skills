'use strict';
const fs=require('node:fs'),path=require('node:path'),{createHash}=require('node:crypto');
const digest=x=>createHash('sha256').update(JSON.stringify(x)).digest('hex');
const dir=c=>path.join(__dirname,c.taskId);
const artifact=c=>path.join(dir(c),'artifact.json');
const read=c=>fs.existsSync(artifact(c))?JSON.parse(fs.readFileSync(artifact(c),'utf8')):null;
module.exports={
 async verify({contract:c}){const a=read(c);return {passed:a?.sum===18,contractHash:digest(c),evidence:a?[{artifact:artifact(c),sha256:createHash('sha256').update(fs.readFileSync(artifact(c))).digest('hex'),actualSum:a.sum}]:[],progressKey:String(a?.sum??'missing')};},
 async execute({contract:c,state,actionId}){fs.mkdirSync(dir(c),{recursive:true});
 const sum=c.mode==='blocked'?7:state.round===1?7:18;
 const a={actionId,sum};fs.writeFileSync(artifact(c),JSON.stringify(a));
 fs.appendFileSync(path.join(dir(c),'effects.jsonl'),JSON.stringify(a)+'\n');
 if(c.mode==='recover'&&state.round===1)throw new Error('REAL_EXCEPTION_AFTER_FILE_SIDE_EFFECT');
 return {checkpoint:a};},
 async reconcile({contract:c,actionId}){const a=read(c);return a?.actionId===actionId?{status:'COMPLETED',checkpoint:a}:{status:'UNKNOWN'};}
};