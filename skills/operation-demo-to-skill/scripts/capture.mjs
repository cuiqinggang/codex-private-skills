// v2 thin bridge: existing FFmpeg and upstream desktop-record; no new recorder.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawn,spawnSync} from 'node:child_process';
const ROOT='C:\\AI\\operation-demo-to-skill-v2';
const UP='C:\\AI\\record-and-replay-evaluation\\scripts\\desktop-record.mjs';
const [cmd,slug='demo-v2'] = process.argv.slice(2);
if(!/^[a-zA-Z0-9_-]{1,50}$/.test(slug))throw Error('invalid slug');
const dir=path.join(ROOT,'sessions',slug), flag=path.join(dir,'STOP-AUDIO');
const json=(x)=>console.log(JSON.stringify(x));
const run=(args)=>spawnSync('node',[UP,...args],{encoding:'utf8',timeout:20000});
if(cmd==='start'){
 if(fs.existsSync(dir))throw Error('Session exists; choose new slug');
 fs.mkdirSync(dir,{recursive:true});
 const child=spawn(process.execPath,[process.argv[1],'worker',slug],{detached:true,stdio:'ignore',windowsHide:true});
 child.unref();
 for(let i=0;i<60;i++){if(fs.existsSync(path.join(dir,'ready.json'))){json(JSON.parse(fs.readFileSync(path.join(dir,'ready.json'))));process.exit(0)}
 if(fs.existsSync(path.join(dir,'error.txt')))throw Error(fs.readFileSync(path.join(dir,'error.txt'),'utf8'));
 Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,100)}
 throw Error('startup not confirmed: '+dir);
}
if(cmd==='stop'){
 if(!fs.existsSync(dir))throw Error('unknown session');
 fs.writeFileSync(flag,'stop');
 for(let i=0;i<100;i++){if(fs.existsSync(path.join(dir,'result.json'))){json(JSON.parse(fs.readFileSync(path.join(dir,'result.json'))));process.exit(0)}
 Atomics.wait(new Int32Array(new SharedArrayBuffer(4)),0,0,100)}
 throw Error('stop requested; result unknown, check '+dir);
}
if(cmd==='status'){json({dir,ready:fs.existsSync(path.join(dir,'ready.json')),ended:fs.existsSync(path.join(dir,'result.json'))});process.exit(0)}
if(cmd==='worker'){
 try{
 const real=process.env.SYNTHETIC_AUDIO!=='1';
 const input=real?['-f','dshow','-i','audio=麦克风 (Web Camera)']:['-f','lavfi','-i','sine=frequency=440:sample_rate=16000'];
 const outfile=path.join(dir,'narration.wav');
 const ff=spawn('ffmpeg',['-hide_banner','-nostdin','-loglevel','error',...(real?[]:['-re']),...input,'-t','1800','-ac','1','-ar','16000','-c:a','pcm_s16le','-y',outfile],{stdio:['pipe','ignore','pipe'],windowsHide:true});
 let stderr='';ff.stderr.on('data',d=>stderr+=d.toString().slice(0,2000));
 const start=Date.now();
 const desktop=real?run(['start',slug,'30']):spawnSync('node',['C:\\AI\\record-and-replay-evaluation\\scripts\\desktop-selftest.mjs','--out',path.join(dir,'synthetic-events')],{encoding:'utf8',timeout:20000});
 if(desktop.status!==0)throw Error('desktop-start '+desktop.stderr);
 fs.writeFileSync(path.join(dir,'ready.json'),JSON.stringify({status:'recording',slug,started_utc:new Date(start).toISOString(),mic:real?'Web Camera':'synthetic',events:path.join(os.homedir(),'.agents','recordings',slug),audio:outfile,ffmpeg_pid:ff.pid,desktop:desktop.stdout.trim()},null,2));
 while(!fs.existsSync(flag)&&Date.now()-start<30*60000){await new Promise(r=>setTimeout(r,200))}
 const desktopStop=real?run(['stop',slug]):{status:0,stdout:'synthetic self-test completed'};
 // ffmpeg -nostdin disables q; terminate and repair WAV header with FFmpeg copy if necessary.
 ff.kill();
 await new Promise(r=>ff.once('exit',r));
 const finalized=path.join(dir,'narration-final.wav');
 const fix=spawnSync('ffmpeg',['-v','error','-i',outfile,'-c:a','pcm_s16le','-y',finalized],{encoding:'utf8',timeout:15000});
 const ok=fix.status===0&&fs.existsSync(finalized);
 const result={status:desktopStop.status===0&&ok?'completed':'partial',slug,stopped_utc:new Date().toISOString(),started_utc:new Date(start).toISOString(),audio:ok?finalized:outfile,desktop:desktopStop.stdout.trim(),audio_error:ok?null:fix.stderr||stderr};
 fs.writeFileSync(path.join(dir,'result.json'),JSON.stringify(result,null,2));
 }catch(e){fs.writeFileSync(path.join(dir,'error.txt'),String(e))}
 process.exit(0);
}
console.error('usage: node capture.mjs start|stop|status slug');process.exit(2);