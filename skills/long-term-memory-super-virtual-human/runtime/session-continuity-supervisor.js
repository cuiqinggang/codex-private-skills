function decide(s){
 if(s.humanVerificationRequired) return {action:'PAUSE_FOR_HUMAN_VERIFICATION',writeOwner:s.writeOwner};
 if(s.primaryRecovered && s.writeOwner==='BACKUP') return {action:'RECONCILE_BEFORE_PRIMARY_RESUME',writeOwner:'BACKUP'};
 if(!s.gptServiceAvailable) return {action:'FAILOVER_BACKUP',fencePrimary:true,nextFenceToken:s.fenceToken+1,writeOwner:'BACKUP'};
 if(s.transportDisconnected){
  if(s.finalAnswerObserved) return {action:'ACCEPT_FINAL',writeOwner:s.writeOwner};
  if(s.backendActivityObserved && !s.hardDeadlineExceeded) return {action:'WAIT_BACKEND_COMPLETION',writeOwner:s.writeOwner};
  if(!s.readOnlyProbeDone) return {action:'PROBE_PAGE',writeOwner:s.writeOwner};
  if(!s.hardDeadlineExceeded) return {action:'WAIT_WITH_PROBE',writeOwner:s.writeOwner};
 }
 if(!s.pageHealthy || (s.transportDisconnected && s.hardDeadlineExceeded)){
  if(!s.readOnlyProbeDone) return {action:'PROBE_PAGE',writeOwner:s.writeOwner};
  if(s.freshChatAvailable && s.safeCheckpoint) return {action:'ROTATE_SESSION',writeOwner:s.writeOwner};
  if(!s.freshChatAvailable) return {action:'FAILOVER_BACKUP',fencePrimary:true,nextFenceToken:s.fenceToken+1,writeOwner:'BACKUP'};
  return {action:'WAIT_SAFE_CHECKPOINT',writeOwner:s.writeOwner};
 }
 if(s.primaryPathBlocked && s.alternateValidPathAvailable) return {action:'FAILOVER_ALTERNATE_VALID',writeOwner:s.writeOwner};
 if(s.proactiveRotation){
  if(!s.safeCheckpoint) return {action:'WAIT_SAFE_CHECKPOINT',writeOwner:s.writeOwner};
  return {action:'ROTATE_SESSION',writeOwner:s.writeOwner};
 }
 return {action:'CONTINUE',writeOwner:s.writeOwner};
}
module.exports={decide};