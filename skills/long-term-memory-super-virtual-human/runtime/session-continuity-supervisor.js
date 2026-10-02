function decide(s){
 if(!s.safeCheckpoint && s.proactiveRotation) return {action:'WAIT_SAFE_CHECKPOINT',writeOwner:s.writeOwner};
 if(!s.gptServiceAvailable) return {action:'FAILOVER_BACKUP',fencePrimary:true,nextFenceToken:s.fenceToken+1,writeOwner:'BACKUP'};
 if(!s.pageHealthy){
  if(!s.readOnlyProbeDone) return {action:'PROBE_PAGE',writeOwner:s.writeOwner};
  if(s.freshChatAvailable && s.safeCheckpoint) return {action:'ROTATE_SESSION',writeOwner:s.writeOwner};
  if(!s.freshChatAvailable) return {action:'FAILOVER_BACKUP',fencePrimary:true,nextFenceToken:s.fenceToken+1,writeOwner:'BACKUP'};
 }
 if(s.primaryRecovered && s.writeOwner==='BACKUP') return {action:'RECONCILE_BEFORE_PRIMARY_RESUME',writeOwner:'BACKUP'};
 if(s.proactiveRotation && s.safeCheckpoint) return {action:'ROTATE_SESSION',writeOwner:s.writeOwner};
 return {action:'CONTINUE',writeOwner:s.writeOwner};
}
module.exports={decide};