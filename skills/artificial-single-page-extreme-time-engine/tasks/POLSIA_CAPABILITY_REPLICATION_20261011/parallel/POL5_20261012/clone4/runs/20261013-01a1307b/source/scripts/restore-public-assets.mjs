import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {createReadStream} from 'node:fs';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const execute=promisify(execFile);

const PINNED_MANIFEST_SHA256 = 'fff8cacafb593d1320a9a375e76334a9421929b8f57155e00d8d6b8402a11681';
const ASSET_ALLOWLIST = new Set(/* GENERATED_TARGETS */["public/polsia/BlackletterBit.otf","public/polsia/PPEditorialNew-Bold.otf","public/polsia/PPEditorialNew-Italic.otf","public/polsia/PPEditorialNew-Regular.otf","public/polsia/PPEditorialOld-Italic.otf","public/polsia/PPEditorialOld-Regular.otf","public/polsia/PPEditorialOld-Ultralight.otf","public/polsia/PPEditorialOld-UltralightItalic.otf","public/polsia/SuisseIntlMono-Bold.otf","public/polsia/SuisseIntlMono-Regular.otf","public/polsia/announcement-2a637515-bb09-4f02-b5d4-24d38a98d972.webp","public/polsia/announcement-646c22cc-83d2-4188-91cc-e60702e3391c.webp","public/polsia/announcement-79d144a7-1ec2-475c-b0bc-29c7b47437a5.webp","public/polsia/announcement-7e7f565e-ed38-4f88-bae9-54d382f4c625.webp","public/polsia/background.wav","public/polsia/bencera-Di0L4Dqd.png","public/polsia/bg-clouds.webp","public/polsia/favicon-192x192.png","public/polsia/favicon.png","public/polsia/founders-tour-tee-polsia.png","public/polsia/hat-1.png","public/polsia/hat2.png","public/polsia/home-office-polsia.webp","public/polsia/home-polsia-office.webp","public/polsia/keychain-polsia.png","public/polsia/lesnuages-KkuCGfBJ.png","public/polsia/logoblanc.webp","public/polsia/logonoir.webp","public/polsia/magic-cube-polsia.png","public/polsia/mens.webp","public/polsia/pin-polsia.png","public/polsia/polsia-stickers-sheet.png","public/polsia/site.css","public/polsia/stress_cube_polsia.png","public/polsia/tee-cabo-2.png","public/polsia/tee-cabo-white.png"]);
const BASE_COMMIT = 'c62ba0be3368815dc9011848d96875ef228f1607';
const options = new Set(process.argv.slice(2));
for (const argument of options) if (!['--apply','--verify-only','--help'].includes(argument)) throw new Error(`Unsupported argument: ${argument}. Asset replacement is not supported; use a clean source directory.`);
if (options.has('--help')) {
  console.log('Run from a clean cloned open-polsia repository after applying the text source overlay.\nDefault: read-only plan. --verify-only: require all expected files. --apply: download only missing assets. Existing exact assets are reused; existing mismatched assets are BLOCKED. Replacement is not supported.\nThe adjacent pinned public-assets-restore-manifest.json is required.');
  process.exit(0);
}
if (options.has('--apply') && options.has('--verify-only')) throw new Error('--apply and --verify-only are mutually exclusive.');
const apply = options.has('--apply');
const samePath = (a,b) => process.platform === 'win32' ? path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase() : path.resolve(a) === path.resolve(b);
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const manifestPath = fileURLToPath(new URL('./public-assets-restore-manifest.json',import.meta.url));
const manifestBytes = await fs.readFile(manifestPath);
if (sha(manifestBytes) !== PINNED_MANIFEST_SHA256) throw new Error('The independent asset manifest does not match the pinned SHA-256.');
const manifest = JSON.parse(manifestBytes);
if (manifest.schema_version !== 1 || manifest.upstream.base_commit !== BASE_COMMIT || manifest.assets.length !== 36 || ASSET_ALLOWLIST.size !== 36) throw new Error('Unexpected source/manifest/allowlist contract.');
const lexicalRoot = path.resolve(process.cwd());
if (!samePath(await fs.realpath(lexicalRoot),lexicalRoot)) throw new Error('The working directory resolves through a symlink or junction.');
const assetsRoot = path.join(lexicalRoot,'public','polsia');
const publicRoot = path.dirname(assetsRoot);
const directoryIdentities = new Map();
const temporaryFiles = new Set();
const installed = new Map();
const lockPath=path.join(assetsRoot,'.polsia-restore.lock');
let lockHandle;
let lockIdentity;
let complete = false;
async function assertOrdinaryDirectory(directory) {
  const stat=await fs.lstat(directory);
  if (!stat.isDirectory() || stat.isSymbolicLink() || !samePath(await fs.realpath(directory),directory)) throw new Error(`Directory redirection rejected: ${directory}`);
  const identity={ino:stat.ino,dev:stat.dev};
  if(directoryIdentities.has(directory)&&JSON.stringify(directoryIdentities.get(directory))!==JSON.stringify(identity)) throw new Error(`Directory replaced during restoration: ${directory}`);
  directoryIdentities.set(directory,identity);
}
async function assertAssetBoundary(){await assertOrdinaryDirectory(publicRoot);await assertOrdinaryDirectory(assetsRoot);}
async function fingerprint(file) {
  let stat;
  try { stat = await fs.lstat(file); } catch(error) { if(error.code==='ENOENT') return null; throw error; }
  if (!stat.isFile() || stat.isSymbolicLink() || stat.nlink !== 1 || !samePath(await fs.realpath(file),file)) throw new Error(`Non-ordinary, redirected or hard-linked target rejected: ${file}`);
  const hash=crypto.createHash('sha256');
  let bytes=0;
  for await(const chunk of createReadStream(file)){bytes+=chunk.length;hash.update(chunk);}
  return {bytes,sha256:hash.digest('hex'),ino:stat.ino,dev:stat.dev};
}
function matches(actual,expected){return actual && actual.bytes===expected.bytes && actual.sha256===expected.sha256;}
function targetPath(target){
  if(!ASSET_ALLOWLIST.has(target)||!/^public\/polsia\/[A-Za-z0-9._-]+$/.test(target)) throw new Error(`Target is outside the pinned flat allowlist: ${target}`);
  const file=path.join(lexicalRoot,...target.split('/'));
  if(!samePath(path.dirname(file),assetsRoot)) throw new Error('Target path escaped cwd/public/polsia.');
  return file;
}
function validateUrl(value){
  const url=new URL(value);
  if(url.protocol!=='https:'||url.username||url.password||url.hash||url.port) throw new Error('Source URL is not a plain public HTTPS URL.');
  if(url.hostname==='polsia.com') return url.href;
  if(url.hostname==='cdn.shopify.com'&&url.pathname.startsWith('/s/files/1/0891/5959/8417/files/')) return url.href;
  throw new Error('Source is outside the official public asset origins.');
}
try {
  await assertAssetBoundary();
  // The clone and handed-off text files are prerequisites; this script never clones, applies code or manages processes.
  if(apply){
    const head=await execute(process.platform==='win32'?'git.exe':'git',['-C',lexicalRoot,'rev-parse','HEAD'],{windowsHide:true,timeout:10000});
    if(head.stdout.trim()!==BASE_COMMIT) throw new Error('The requested cloned repository base commit does not match.');
  }
  const handler=await fs.readFile(path.join(lexicalRoot,'src','services','public-page.ts'));
  if(sha(handler)!==manifest.provenance.handler_sha256) throw new Error('Apply the matching public-page.ts text overlay first.');
  for(const entry of manifest.required_text_overlay){
    if(!/^public\/polsia\/[A-Za-z0-9._-]+\.(?:html|css|js|json)$/.test(entry.target)) throw new Error('Text overlay target is outside the flat public folder.');
    const file=path.join(lexicalRoot,...entry.target.split('/'));
    if(!matches(await fingerprint(file),entry)) throw new Error(`Missing or mismatched required text overlay: ${entry.target}`);
  }
  if(apply){
    lockHandle=await fs.open(lockPath,'wx',0o600);
    lockIdentity=await lockHandle.stat();
    await lockHandle.writeFile(JSON.stringify({pid:process.pid,started_at_utc:new Date().toISOString(),manifest_sha256:PINNED_MANIFEST_SHA256})+'\n');
    await lockHandle.sync();
  }
  const seen=new Set();
  const plans=[];
  for(const asset of manifest.assets){
    if(seen.has(asset.target)||!Number.isSafeInteger(asset.bytes)||asset.bytes<1||asset.bytes>25*1024*1024||!/^[a-f0-9]{64}$/.test(asset.sha256)) throw new Error('Invalid or duplicate asset integrity record.');
    seen.add(asset.target);
    validateUrl(asset.source_url);
    const file=targetPath(asset.target);
    const actual=await fingerprint(file);
    if(actual&&!matches(actual,asset)) throw new Error(`BLOCKED_EXISTING_ASSET_MISMATCH: ${asset.target}. Use a clean new source directory; this script does not overwrite or remove existing mismatched assets.`);
    plans.push({asset,file,actual,action:matches(actual,asset)?'VERIFIED_EXISTING':'FETCH_MISSING'});
  }
  if(!apply){
    const missing=plans.filter(plan=>plan.action!=='VERIFIED_EXISTING');
    console.log(JSON.stringify({status:missing.length?'READ_ONLY_PLAN_MISSING_ASSETS':'PASS_ALL_ASSETS_AND_TEXT',base_commit:BASE_COMMIT,assets:36,text_files:manifest.required_text_overlay.length,missing:missing.map(plan=>plan.asset.target),network_requests:0},null,2));
    if(options.has('--verify-only')&&missing.length) process.exitCode=1;
  }else{
    // Download every needed candidate and validate it before any target is changed.
    for(const plan of plans.filter(plan=>plan.action!=='VERIFIED_EXISTING')){
      await assertAssetBoundary();
      const temporary=path.join(assetsRoot,`.polsia-restore-${crypto.randomUUID()}.tmp`);
      const handle=await fs.open(temporary,'wx',0o600);
      temporaryFiles.add(temporary);
      let reader;
      const hash=crypto.createHash('sha256');
      let position=0;
      try{
        const response=await fetch(validateUrl(plan.asset.source_url),{redirect:'manual',signal:AbortSignal.timeout(180000)});
        if(response.status!==200||!response.body) throw new Error(`Expected original asset HTTP 200: ${plan.asset.target} (${response.status})`);
        const length=response.headers.get('content-length');
        if(length!==null&&Number(length)!==plan.asset.bytes) throw new Error(`Remote Content-Length changed: ${plan.asset.target}`);
        reader=response.body.getReader();
        while(true){
          const {done,value}=await reader.read();
          if(done) break;
          if(position+value.length>plan.asset.bytes) throw new Error(`Remote body exceeds exact expected bytes: ${plan.asset.target}`);
          let offset=0;
          while(offset<value.length){const written=await handle.write(value,offset,value.length-offset,position+offset);if(!written.bytesWritten)throw new Error('Temporary file write made no progress.');offset+=written.bytesWritten;}
          position+=value.length;hash.update(value);
        }
        if(position!==plan.asset.bytes||hash.digest('hex')!==plan.asset.sha256) throw new Error(`Original asset SHA/bytes changed: ${plan.asset.target}`);
        await handle.sync();
      }finally{if(reader)await reader.cancel().catch(()=>{});await handle.close();}
      if(!matches(await fingerprint(temporary),plan.asset)) throw new Error(`Temporary asset verification failed: ${plan.asset.target}`);
      plan.temporary=temporary;
      console.log(`VERIFIED_DOWNLOAD ${plan.asset.target}`);
    }
    // Recheck all targets, and then each commit. Missing targets use atomic no-clobber publication.
    for(const plan of plans){
      await assertAssetBoundary();
      const actual=await fingerprint(plan.file);
      if(JSON.stringify(actual)!==JSON.stringify(plan.actual)) throw new Error(`Target changed during restoration: ${plan.asset.target}`);
    }
    for(const plan of plans.filter(plan=>plan.temporary)){
      await assertAssetBoundary();
      if(JSON.stringify(await fingerprint(plan.file))!==JSON.stringify(plan.actual)) throw new Error(`Target changed immediately before commit: ${plan.asset.target}`);
      const candidateIdentity=await fingerprint(plan.temporary);
      // link publishes the verified whole file and fails EEXIST if any parallel writer created the target.
      // Plain rename can replace such a target, so it is deliberately not used here.
      await fs.link(plan.temporary,plan.file);installed.set(plan.file,candidateIdentity);
      await fs.unlink(plan.temporary);temporaryFiles.delete(plan.temporary);
    }
    for(const plan of plans) if(!matches(await fingerprint(plan.file),plan.asset)) throw new Error(`Final asset verification failed: ${plan.asset.target}`);
    complete=true;
    console.log(JSON.stringify({status:'PASS_RESTORED_ALL_PINNED_ASSETS',base_commit:BASE_COMMIT,assets:36,downloaded:installed.size,bytes:manifest.assets.reduce((sum,asset)=>sum+asset.bytes,0)},null,2));
  }
}finally{
  const cleanupErrors=[];
  let safeBoundary=true;
  if(apply){try{await assertAssetBoundary();}catch(error){safeBoundary=false;cleanupErrors.push(`Asset directory changed; no cleanup paths were followed: ${error.message}`);}}
  if(!complete&&apply&&safeBoundary){
    for(const [file,identity] of [...installed].reverse()){
      try{
        if(JSON.stringify(await fingerprint(file))!==JSON.stringify(identity)) throw new Error('Target identity/content changed; rollback will not remove it.');
        await fs.unlink(file);
      }catch(error){cleanupErrors.push(`${file}: ${error.message}`);}
    }
  }
  if(safeBoundary)for(const temporary of temporaryFiles){try{await fs.unlink(temporary);}catch(error){cleanupErrors.push(`${temporary}: ${error.message}`);}}
  if(lockHandle){
    await lockHandle.close();
    if(safeBoundary)try{
      const current=await fs.lstat(lockPath);
      if(current.ino!==lockIdentity.ino||current.dev!==lockIdentity.dev||!current.isFile()||current.isSymbolicLink()) throw new Error('Lock identity changed; it was not removed.');
      await fs.unlink(lockPath);
    }catch(error){cleanupErrors.push(`${lockPath}: ${error.message}`);}
  }
  if(cleanupErrors.length) throw new Error(`Restore cleanup preserved changed/unowned files for inspection:\n${cleanupErrors.join('\n')}`);
}
