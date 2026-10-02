function pageLeaseDecision(s){
 if(s.taskFinalValid || s.explicitStop) return {action:'RELEASE_PAGE_LEASE'};
 if(s.existingUsablePage) return {action:'REUSE_EXISTING_PAGE',createPage:false,closePage:false};
 if(s.pageLeaseActive && !s.pageRecoverable) return {action:'REBUILD_ONLY_AFTER_UNRECOVERABLE',createPage:true,closePage:false};
 if(s.pageLeaseActive) return {action:'KEEP_PAGE_OPEN',createPage:false,closePage:false};
 return {action:'OPEN_ONCE_AND_ACQUIRE_LEASE',createPage:true,closePage:false};
}
function conversationRotation(s){
 if(!s.safeCheckpoint) return {action:'WAIT_SAFE_CHECKPOINT'};
 if(!s.pageLeaseActive) return {action:'ACQUIRE_PAGE_LEASE_FIRST'};
 return {action:'NEW_CONVERSATION_SAME_PAGE',createPage:false,closePage:false};
}
module.exports={pageLeaseDecision,conversationRotation};