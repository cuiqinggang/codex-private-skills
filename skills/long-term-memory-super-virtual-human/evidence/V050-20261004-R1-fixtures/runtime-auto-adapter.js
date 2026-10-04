const fs=require('node:fs'),path=require('node:path');
const base=require('./runtime-file-adapter');
module.exports={...base,async recover({contract,state,actionId,error}){
 const artifact=path.join(__dirname,contract.taskId,'artifact.json');
 const actual=fs.existsSync(artifact)?JSON.parse(fs.readFileSync(artifact)):null;
 fs.appendFileSync(path.join(__dirname,'auto-recovery-log.jsonl'),JSON.stringify({taskId:contract.taskId,actionId,error,actual})+'\n');
 return {available:actual?.actionId===actionId,reason:'ACTUAL_SIDE_EFFECT_RECONCILIATION_REQUIRED'};
}};