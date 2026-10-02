const fs=require('fs');
const path=require('path');

function readJson(p){try{return JSON.parse(fs.readFileSync(p,'utf8'))}catch{return null}}
function pidAlive(pid){if(!Number.isInteger(Number(pid))||Number(pid)<=0)return false;try{process.kill(Number(pid),0);return true}catch{return false}}
function writeNew(p,v){
 fs.mkdirSync(path.dirname(p),{recursive:true});
 const fd=fs.openSync(p,'wx');
 try{fs.writeFileSync(fd,JSON.stringify(v,null,2))}finally{fs.closeSync(fd)}
}
function acquireGlobalWriterLease({leasePath,ownerRoot,inboxDir,marker='OWNER'}){
 const token=process.pid+'-'+Date.now()+'-'+Math.random().toString(16).slice(2);
 for(let attempt=0;attempt<4;attempt++){
  const record={schemaVersion:1,status:'GLOBAL_WRITER_ACTIVE',pid:process.pid,token,marker,ownerRoot,inboxDir,
   acquiredAt:new Date().toISOString(),heartbeatAt:new Date().toISOString()};
  try{writeNew(leasePath,record);return {acquired:true,token,current:record}}
  catch(e){
   if(e.code!=='EEXIST')throw e;
   const current=readJson(leasePath);
   if(current&&pidAlive(current.pid))return {acquired:false,reason:'HELD_BY_LIVE_WRITER',current};
   const stale=leasePath+'.stale-'+Date.now()+'-'+process.pid;
   try{fs.renameSync(leasePath,stale)}catch{}
  }
 }
 return {acquired:false,reason:'LEASE_CONTENTION',current:readJson(leasePath)};
}
function heartbeatGlobalWriterLease({leasePath,token,marker}){
 const current=readJson(leasePath);
 if(!current||current.token!==token)return false;
 const next={...current,heartbeatAt:new Date().toISOString(),marker:marker||current.marker};
 const tmp=leasePath+'.tmp-'+process.pid;
 fs.writeFileSync(tmp,JSON.stringify(next,null,2));
 try{fs.renameSync(tmp,leasePath)}catch{try{fs.unlinkSync(tmp)}catch{};return false}
 return true;
}
function releaseGlobalWriterLease({leasePath,token}){
 const current=readJson(leasePath);
 if(!current||current.token!==token)return false;
 try{fs.unlinkSync(leasePath);return true}catch{return false}
}
module.exports={acquireGlobalWriterLease,heartbeatGlobalWriterLease,releaseGlobalWriterLease,pidAlive};
