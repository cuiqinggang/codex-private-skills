// Offline fixed-source branch test. No Orca runtime, Windows, network or credentials.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { stripTypeScriptTypes } from 'node:module';
import crypto from 'node:crypto';
const snapshot=JSON.parse(fs.readFileSync(new URL('./routing-snapshot.json',import.meta.url),'utf8'));
const results=[];
function loadClass(path,name,globals){
 const file=snapshot.files[path];
 const blob=crypto.createHash('sha1').update('blob '+Buffer.byteLength(file.content)+'\0').update(file.content).digest('hex');
 assert.equal(blob,file.sha,'fixed source blob mismatch');
 const js=stripTypeScriptTypes(file.content).replace(/^import[\s\S]*?from\s+['"][^'"]+['"];?\s*$/gm,'').replace(/export\s+class\s+/, 'class ');
 const context=vm.createContext({...globals,console:{warn(){}},process:{platform:'win32'}});
 vm.runInContext(js+'\nglobalThis.testClass='+name,context);
 return context.testClass;
}
let custom=false, panes=false;
const Routing=loadClass('src/main/codex-accounts/runtime-home-service-home-routing.ts','CodexRuntimeHomeRouting',{
 CodexRuntimeHomeManagedHome:class{}, normalizeCodexRuntimeSelection:s=>({host:s.host}),
 hasCustomCodexHomeOverrideForLaunch:()=>custom, hasRecordedLegacySharedCodexPane:()=>panes,
 syncLegacySharedCodexConfigForRetainedPanes:()=>{throw Error('UNEXPECTED_CONFIG_WRITE')},
 resolveOrcaManagedCodexHomePath:()=>'/fixture/mirror'
});
const Launch=loadClass('src/main/codex-accounts/runtime-home-service-launch.ts','CodexRuntimeHomeLaunch',{
 CodexRuntimeHomeRouting:Routing, hasCustomCodexHomeOverrideForLaunch:()=>custom,
 resolveOrcaManagedCodexHomePath:()=>'/fixture/mirror',
 ManagedCodexHomeTemporarilyUnavailableError:class extends Error{}
});
function test(name,fn){fn();results.push({name,status:'PASS'});}
function fixture(provenance,runtimeAuth){
 const calls=[];
 const o=Object.create(Routing.prototype);
 Object.assign(o,{
 resolveSharedRuntimeAuthProvenanceStatus:()=>provenance,
 readRuntimeAuthForProvenance:()=>{calls.push('read_fixture_runtime_auth');return runtimeAuth;},
 writeSystemDefaultAuth:(_v,opts)=>{calls.push('write_system_if_empty');assert.equal(opts.expectedContents,null);return true;},
 persistSharedRuntimeAuthProvenance:()=>calls.push('persist_provenance'),
 captureSystemDefaultSnapshot:()=>calls.push('snapshot')
 });return {o,calls};
}
test('missing provenance: no credential write',()=>{const {o,calls}=fixture({kind:'missing'},null);o.copyMirrorLoginIntoEmptySystemHome();assert.deepEqual(calls,['read_fixture_runtime_auth']);});
test('system-default existing baseline: no credential write',()=>{const {o,calls}=fixture({kind:'committed',provenance:{owner:'system-default',authJson:'FAKE_BASELINE'}},'FAKE_RUNTIME');o.copyMirrorLoginIntoEmptySystemHome();assert.deepEqual(calls,['read_fixture_runtime_auth']);});
test('managed provenance: no system credential write',()=>{const {o,calls}=fixture({kind:'committed',provenance:{owner:'managed',authJson:null}},'FAKE_RUNTIME');o.copyMirrorLoginIntoEmptySystemHome();assert.deepEqual(calls,['read_fixture_runtime_auth']);});
test('empty runtime auth: no credential write',()=>{const {o,calls}=fixture({kind:'committed',provenance:{owner:'system-default',authJson:null}},null);o.copyMirrorLoginIntoEmptySystemHome();assert.deepEqual(calls,['read_fixture_runtime_auth']);});
test('counterexample: legacy null baseline plus mirror invokes write',()=>{const {o,calls}=fixture({kind:'committed',provenance:{owner:'system-default',authJson:null}},'FAKE_RUNTIME');o.copyMirrorLoginIntoEmptySystemHome();assert.deepEqual(calls,['read_fixture_runtime_auth','write_system_if_empty','persist_provenance','snapshot']);});
test('declined conditional write still persists provenance',()=>{const {o,calls}=fixture({kind:'committed',provenance:{owner:'system-default',authJson:null}},'FAKE_RUNTIME');o.writeSystemDefaultAuth=()=>false;o.copyMirrorLoginIntoEmptySystemHome();assert.deepEqual(calls,['read_fixture_runtime_auth','persist_provenance']);});
test('system default with no custom home selects real home',()=>{custom=false;const o=Object.create(Routing.prototype);o.store={getSettings:()=>({host:null})};assert.equal(o.isHostSystemDefaultRealHomeSelected(),true);});
test('custom home prevents real-home lane',()=>{custom=true;const o=Object.create(Routing.prototype);o.store={getSettings:()=>({host:null})};assert.equal(o.isHostSystemDefaultRealHomeSelected(),false);custom=false;});
test('no retained panes skips legacy config sync',()=>{panes=false;const o=Object.create(Routing.prototype);o.isHostSystemDefaultRealHomeSelected=()=>true;o.syncLegacySharedSystemDefaultAuthForRetainedPanes=()=>{throw Error('UNEXPECTED_AUTH_SYNC')};o.reconcileLegacySharedHomeForRetainedPanes();});
test('real-home launch still invokes both compatibility helpers',()=>{const calls=[];const o=Object.create(Launch.prototype);Object.assign(o,{getSelfContainedManagedHostAccount:()=>null,isHostSystemDefaultRealHomeSelected:()=>true,copyMirrorLoginIntoEmptySystemHome:()=>calls.push('copy_helper'),reconcileLegacySharedHomeForRetainedPanes:()=>calls.push('reconcile_helper')});assert.equal(o.prepareForCodexLaunch(),null);assert.deepEqual(calls,['copy_helper','reconcile_helper']);});
test('read-only home resolver does not invoke preparation',()=>{const o=Object.create(Launch.prototype);Object.assign(o,{getSelfContainedManagedHostAccount:()=>null,isHostSystemDefaultRealHomeSelected:()=>true,copyMirrorLoginIntoEmptySystemHome:()=>{throw Error('WRITE')},reconcileLegacySharedHomeForRetainedPanes:()=>{throw Error('WRITE')}});assert.equal(o.resolveHostCodexHomePathForLaunchReadOnly(),null);});
const out={scope:'OFFLINE_SOURCE_BRANCH_TEST_SYNTHETIC_DEPENDENCIES',ref:snapshot.ref,node:process.version,host:process.platform,simulated_branch_platform:'win32',passed:results.length,results,windows_runtime_executed:false,real_credentials_accessed:false,business_rounds_added:0,conclusion:'Conditional migration writes exist. Fresh fixture can skip them; actual startup chain and machine state remain unverified.'};
fs.writeFileSync(new URL('./routing-result.json',import.meta.url),JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));
