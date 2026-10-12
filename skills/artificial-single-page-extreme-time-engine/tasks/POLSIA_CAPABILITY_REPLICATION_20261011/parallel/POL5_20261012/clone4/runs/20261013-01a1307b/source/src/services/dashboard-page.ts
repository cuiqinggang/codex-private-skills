// The dashboard page — clean, light, document-style (NOT terminal). Geist Pixel for the brand title
// AND the section headers (served from the geist npm package via /fonts), Geist Sans body.
// Layout: sticky top (terminal log + header) · multi-column dashboard on the left · chat fixed right.
export const PAGE = String.raw`<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Polsia · 本地工作区</title>
<style>
  @font-face{font-family:'Geist Pixel';src:url('/fonts/pixel.woff2') format('woff2');font-display:swap}
  @font-face{font-family:'Geist Sans';src:url('/fonts/sans.woff2') format('woff2');font-weight:100 900;font-display:swap}
  :root{ --bg:#f6f5f2; --card:#fff; --ink:#16150f; --dim:#8c887e; --line:#e6e3db; --accent:#d6532b; --green:#1a7f37; --mono:ui-monospace,'SF Mono',Menlo,monospace; }
  *{box-sizing:border-box}
  body{ margin:0; background:var(--bg); color:var(--ink); font-family:'Geist Sans',system-ui,sans-serif; font-size:14px; line-height:1.55; }
  h2{ font-family:'Geist Pixel',monospace; font-size:13px; font-weight:400; letter-spacing:.3px; margin:0 0 11px; padding-bottom:7px; border-bottom:1px solid var(--line); }
  a{color:var(--accent);text-decoration:none}
  /* sticky top: terminal log + header */
  .topbar{ position:sticky; top:0; z-index:30; }
  #logbar{ background:#0b0b0c; color:#d6d3cb; font-family:var(--mono); font-size:12px; padding:7px 28px; cursor:pointer; }
  #logbar:hover{color:#fff}
  #logfull{ max-height:200px; overflow:auto; margin-top:6px; padding-top:6px; border-top:1px solid #222; }
  #logfull .t{color:#6a6a6a} #logfull .a{color:#e0b341}
  header{ display:flex; align-items:center; gap:16px; flex-wrap:wrap; padding:13px 28px; background:var(--bg); border-bottom:2px solid var(--ink); }
  .brand{ font-family:'Geist Pixel',monospace; font-size:26px; line-height:1; letter-spacing:.5px; }
  .co{ color:var(--dim); font-family:Georgia,serif; font-style:italic; }
  .controls{ margin-left:auto; display:flex; align-items:center; gap:8px; font-size:12px; color:var(--dim); }
  .pill{ font-family:var(--mono); font-size:11px; border:1px solid var(--line); border-radius:99px; padding:1px 9px; color:var(--dim); background:var(--card); }
  .pill.on{ color:var(--green); border-color:#bfe3c8; background:#f0faf2; }
  button{ font-family:var(--mono); font-size:11px; letter-spacing:.5px; text-transform:uppercase; background:var(--card); border:1px solid var(--ink); border-radius:5px; color:var(--ink); cursor:pointer; padding:4px 9px; }
  button:hover{ background:var(--ink); color:#fff; }
  button:disabled{ opacity:.5; cursor:default; }
  .wrap{ padding:20px 28px 40px; }
  /* layout: dashboard (multi-col) + chat (fixed right) */
  .layout{ display:grid; grid-template-columns:minmax(0,1fr) 380px; gap:28px; align-items:start; }
  .dash{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:26px; align-items:start; }
  .col{ min-width:0; }
  section{ margin-bottom:24px; }
  /* agent card */
  .agent{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:14px; }
  #face{ font-family:var(--mono); font-size:11px; line-height:1.15; margin:0 0 8px; white-space:pre; color:var(--ink); }
  .agent .nm{ font-weight:600; text-transform:capitalize; }
  .agent .md{ color:var(--accent); font-size:12px; font-family:var(--mono); }
  .agent .msg{ margin-top:7px; color:var(--dim); font-size:12.5px; max-height:80px; overflow:hidden; }
  /* business snapshot */
  .stats{ display:grid; grid-template-columns:repeat(2,1fr); gap:9px; }
  .stat{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:9px 11px; }
  .stat .k{ font-size:10.5px; color:var(--dim); text-transform:uppercase; letter-spacing:.5px; }
  .stat .v{ font-size:19px; font-family:Georgia,serif; }
  .muted{ color:var(--dim); font-size:12px; }
  /* lists */
  .row{ display:flex; align-items:center; gap:9px; padding:8px 0; border-bottom:1px solid var(--line); }
  .row:last-child{border-bottom:none}
  .row .ttl{ flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .badge{ font-family:var(--mono); font-size:9.5px; text-transform:uppercase; letter-spacing:.5px; border:1px solid var(--line); border-radius:4px; padding:1px 5px; color:var(--dim); white-space:nowrap; }
  .b-suggested{ color:var(--accent); border-color:#f0c4b4; } .b-in_progress{ color:var(--green); border-color:#bfe3c8; }
  .b-completed{ color:var(--dim); } .b-failed{ color:#c0392b; } .b-needs_continuation{ color:#b8860b; border-color:#e8d4a0; }
  .pr{ font-family:var(--mono); font-size:11px; color:var(--dim); width:20px; }
  .doc{ cursor:pointer; } .doc:hover .ttl{ color:var(--accent); }
  .doc .ic{ color:var(--dim); } .doc .arr{ color:var(--dim); font-size:11px; }
  .soon{ background:var(--card); border:1px dashed var(--line); border-radius:8px; padding:11px; color:var(--dim); font-size:12px; }
  /* chat */
  .chat{ position:sticky; top:106px; background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px; display:flex; flex-direction:column; height:calc(100vh - 126px); }
  #chatlog{ flex:1; overflow:auto; font-size:13px; }
  #chatlog .you{ margin:10px 0 2px; font-weight:600; }
  #chatlog .bot{ margin:2px 0 10px; color:#333; white-space:pre-wrap; }
  .chatin{ display:flex; gap:8px; border-top:1px solid var(--line); padding-top:10px; margin-top:10px; }
  #chatin{ flex:1; border:1px solid var(--line); border-radius:7px; padding:9px 11px; font-family:inherit; font-size:13px; outline:none; }
  #chatin:focus{ border-color:var(--ink); }
  /* onboarding overlay */
  #onboard{ position:fixed; inset:0; background:var(--bg); display:none; align-items:center; justify-content:center; z-index:40; padding:24px; }
  #onboard.show{ display:flex; }
  .ob-card{ max-width:540px; width:100%; text-align:center; }
  .ob-card .brand{ font-size:36px; }
  .ob-sub{ color:var(--dim); margin:12px 0 22px; font-size:15px; line-height:1.5; }
  #ob-idea{ width:100%; min-height:96px; border:1px solid var(--line); border-radius:10px; padding:14px; font-family:inherit; font-size:15px; outline:none; resize:vertical; background:var(--card); }
  #ob-idea:focus{ border-color:var(--ink); }
  #ob-btn{ margin-top:16px; font-size:13px; padding:10px 20px; }
  /* modal */
  #modal{ position:fixed; inset:0; background:rgba(20,18,12,.45); display:none; align-items:center; justify-content:center; z-index:50; padding:24px; }
  #modal.show{ display:flex; }
  .sheet{ background:var(--card); border:1px solid var(--line); border-radius:12px; max-width:680px; width:100%; max-height:82vh; display:flex; flex-direction:column; box-shadow:0 20px 60px rgba(0,0,0,.2); }
  .sheet header{ display:flex; align-items:center; border:none; border-bottom:1px solid var(--line); padding:16px 20px; background:var(--card); }
  .sheet h3{ font-family:Georgia,serif; font-size:18px; margin:0; text-transform:capitalize; flex:1; }
  .sheet .body{ padding:18px 20px; overflow:auto; white-space:pre-wrap; line-height:1.6; font-size:14px; }
  .x{ cursor:pointer; border:1px solid var(--line); border-radius:6px; width:26px; height:26px; line-height:24px; text-align:center; color:var(--dim); }
  .x:hover{ background:var(--ink); color:#fff; }
  .lab-field{width:100%;padding:9px;border:1px solid var(--line);border-radius:6px;margin:5px 0 12px;font:inherit;background:var(--card)}
  .lab-note{padding:10px 14px;margin-bottom:18px;border-left:3px solid var(--accent);background:#fff6ed;color:#76441d}
  .lab-cap{padding:12px 0;border-bottom:1px solid var(--line)} .lab-cap p{font-size:12px;color:var(--dim);margin:5px 0}
  .lab-nav{display:flex;gap:12px;align-items:center;font-size:12px} .lab-nav select{max-width:220px}
  .lab-result{display:flex;gap:6px;flex-wrap:wrap;margin:5px 0 10px} .lab-error{color:#a62222}
  @media(max-width:1100px){.layout{grid-template-columns:minmax(0,1fr) 320px}.dash{grid-template-columns:repeat(2,minmax(0,1fr))}}
  @media(max-width:760px){header{padding:12px 16px}.wrap{padding:16px}.layout,.dash{display:block}.chat{position:static;height:auto}.lab-nav{width:100%;flex-wrap:wrap}.controls{margin-left:0}.row{flex-wrap:wrap}.row .ttl{white-space:normal}.sheet{max-width:100%}}

  @font-face{font-family:'Suisse Intl Mono';src:url('/fonts/SuisseIntlMono-Regular.otf') format('opentype');font-display:swap}
  @font-face{font-family:'Editorial Old';src:url('/fonts/PPEditorialOld-Regular.otf') format('opentype');font-display:swap}
  :root{--bg:#fff;--card:#fff;--ink:#000;--dim:#666;--line:#ddd;--accent:#e65100;--mono:'Suisse Intl Mono',monospace}
  body{font-family:var(--mono);font-size:12px;line-height:1.6}
  h2{font-family:var(--mono);font-size:12px;letter-spacing:0}
  .brand{display:block;line-height:1}.brand img{display:block;width:auto;height:29px}
  header{background:#fff;border-bottom:1px solid #000;padding:20px}
  .wrap{padding:24px 20px 48px}.layout{gap:24px}.dash{gap:24px}
  #logbar{background:#000;color:#fff;padding:12px 15px;font-size:10px;min-height:88px;display:flex;flex-direction:column;justify-content:flex-end}
  #logbar:before{content:'>\A>\A>\A>';white-space:pre;line-height:15px}
  #logline{line-height:15px}#logfull{width:100%}
  .agent,.stat,.chat,.soon,.sheet{border-radius:0;border-color:#ccc;box-shadow:none}
  #face{display:none}.agent .nm{font-family:'Editorial Old',serif;font-size:28px;font-weight:400}
  .stat .v,.sheet h3{font-family:'Editorial Old',serif}.stat .v{font-size:25px}
  .lab-note{border:1px solid #ddd;border-left:2px solid #e65100;background:#fff;color:#333;padding:12px 14px}
  button{border-radius:3px;background:linear-gradient(#fff,#888);padding:4px 12px;letter-spacing:0;font-size:11px}
  button:hover{background:linear-gradient(#ddd,#888);color:#000}
  .lab-field,#chatin{border-radius:0;border-color:#bbb}
  .chat{top:172px;height:auto;max-height:calc(100vh - 192px);overflow:auto;padding:16px}
  .pill,.badge{border-radius:3px}.pill.on{color:#000;background:#fff;border-color:#ccc}
  .sheet header{padding:16px 20px}.sheet .body{font-family:var(--mono);font-size:12px}
  @media(max-width:760px){.chat{max-height:none;overflow:visible}.wrap{padding:20px 16px}header{padding:16px}.brand img{height:29px}.layout,.dash{display:block}}
</style></head>
<body>
  <div class="topbar">
    <div id="logbar" onclick="toggleLog()"><span id="logline">› booting…</span><div id="logfull" style="display:none"></div></div>
    <header>
      <a class="brand" href="/" aria-label="Polsia 首页"><img src="/landing/logonoir.webp" alt="Polsia"></a>
      <div class="co" id="co"></div>
      <div class="controls">
        <nav class="lab-nav"><a href="#tasks">任务</a><a href="#docs">结果</a><a href="#capabilities">能力</a>
        <select id="company-select" aria-label="选择公司" onchange="switchCompany(this.value)"></select>
        <button onclick="newCompany()">创建公司</button></nav>
        <span id="wpill" class="pill">本地验收</span>
      </div>
    </header>
  </div>

  <div class="wrap">
    <div class="lab-note" id="lab-status" role="status">把目标变成可审核的交付：创建公司、发布任务、运行本地业务并检查产物。</div>
    <div class="layout">
      <div class="dash">
        <div class="col">
          <section class="agent">
            <pre id="face"></pre>
            <div class="nm" id="aname">polsia</div><div class="md" id="amood"></div><div class="msg" id="amsg"></div>
          </section>
          <section>
            <h2>本地业务</h2>
            <div class="stats">
              <div class="stat"><div class="k">站点访问</div><div class="v" id="b-visitors">—</div></div>
              <div class="stat"><div class="k">经营收入</div><div class="v" id="b-revenue">—</div></div>
              <div class="stat"><div class="k">今日完成任务</div><div class="v" id="b-shipped">—</div></div>
              <div class="stat"><div class="k">文档</div><div class="v" id="b-docs">—</div></div>
            </div>
            <div class="muted" style="margin-top:8px">数值来自当前公司的真实记录；收款尚未接入。</div>
          </section>
        </div>

        <div class="col">
          <section><h2>任务</h2><div id="tasks"></div></section>
          <section><h2>交付物与报告</h2><div id="docs"></div></section>
          <section><h2>发布状态</h2><div id="website"></div></section>
        </div>

        <div class="col">
          <section><h2>业务能力与历史继承</h2><div id="capabilities">读取中…</div></section>
        </div>
      </div>

      <aside class="chat">
        <h2>公司与目标</h2>
        <form onsubmit="createCompany(event)"><label for="company-name">公司名称</label><input class="lab-field" id="company-name" required maxlength="80" placeholder="例如：星河工作室">
        <label for="company-goal">业务目标</label><textarea class="lab-field" id="company-goal" required maxlength="1200" placeholder="写下公司的目标"></textarea><button id="create-company" type="submit">保存公司与目标</button></form>
        <h2 style="margin-top:22px">发布业务任务</h2>
        <form onsubmit="createEvidenceTask(event)"><label for="task-mode">任务类型</label><select class="lab-field" id="task-mode" onchange="updateTaskMode()"><option value="business">新业务交付</option><option value="evidence">历史资料核验</option></select><label for="task-title">任务名称</label><input class="lab-field" id="task-title" required maxlength="160" placeholder="例如：为工作室制作报价网页">
        <label for="task-capability">能力类别</label><select class="lab-field" id="task-capability" required></select><div id="instruction-field"><label for="task-instruction">交付要求</label><textarea class="lab-field" id="task-instruction" maxlength="10000" placeholder="说明业务背景、交付内容和验收标准"></textarea></div><button id="create-task" type="submit">创建任务</button> <button type="button" id="batch-tasks" onclick="createBusinessBatch()">一次创建4项</button></form>
        <p class="muted" id="task-scope">本地交付需真实执行并核验产物；创建后点击执行，最多4项并行。外部发布、客服渠道与支付尚未接入。</p>
        <h2 style="margin-top:22px">业务执行状态</h2><p class="muted" id="business-runtime">读取当前状态…</p>
        <div id="chatlog"></div>
        <div class="chatin">
          <input id="chatin" autocomplete="off" disabled placeholder="模型配置及授权尚未验证">
        </div>
      </aside>
    </div>
  </div>

  <div id="onboard">
    <div class="ob-card">
      <div class="brand">polsia</div>
      <p class="ob-sub">Tell me your idea — I'll name the company, write the docs, set the goal,<br>and kick off the daily build.</p>
      <textarea id="ob-idea" placeholder="e.g. a monthly subscription for freshly-roasted single-origin coffee beans"></textarea>
      <div><button id="ob-btn" onclick="submitOnboard()">Build it →</button></div>
    </div>
  </div>

  <div id="modal" onclick="if(event.target===this)closeDoc()">
    <div class="sheet">
      <header><h3 id="m-title"></h3><div class="x" onclick="closeDoc()">✕</div></header>
      <div class="body" id="m-body"></div>
    </div>
  </div>
<script>
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let currentCompany=localStorage.getItem('company-lab-selection')||'demo';
let companyGeneration=0,tickSequence=0,chatSequence=0,modalSequence=0;
function changeCompany(id){currentCompany=id;companyGeneration++;modalSequence++;localStorage.setItem('company-lab-selection',id);document.getElementById('modal').classList.remove('show');}
function stillCurrent(generation,company){return generation===companyGeneration&&company===currentCompany;}
async function appFetch(path,options){const u=new URL(path,location.origin);if(!u.searchParams.has('company'))u.searchParams.set('company',currentCompany);const r=await fetch(u,options);if(!r.ok){let e;try{e=await r.json()}catch{}throw new Error(e?.error||'服务暂时不可用')}return r;}
function showLabError(e){const n=document.getElementById('lab-status');n.textContent=e.message||String(e);n.classList.add('lab-error');}
const EYES={idle:'-   -',thinking:'o   o',building:'O   O',researching:'o   o',shipped:'^   ^',stuck:'x   x'};
const MOUTH={idle:'_____',thinking:'. . .',building:'=====',researching:'-----',shipped:'vvvvv',stuck:'wwwww'};
const MOODTXT={idle:'resting',thinking:'planning',building:'building',researching:'researching',shipped:'shipped!',stuck:'needs a look'};
function face(mood){ const e=EYES[mood]||EYES.idle, m=MOUTH[mood]||MOUTH.idle;
  return '┌───────────┐\n│   '+e+'   │\n│     ▽     │\n│   '+m+'   │\n└───────────┘'; }

let logOpen=false;
function toggleLog(){ logOpen=!logOpen; document.getElementById('logfull').style.display=logOpen?'block':'none'; }
async function post(u){ await fetch(u,{method:'POST'}); tick(); }
function setWorker(on){ post('/api/worker?on='+on); }
async function runCron(btn){ btn.disabled=true; const o=btn.textContent; btn.textContent='⏰ running…';
  try{ await appFetch('/api/cron',{method:'POST'}); }catch(e){} btn.textContent=o; btn.disabled=false; tick(); }
document.addEventListener('click',e=>{
  const reportButton=e.target.closest&&e.target.closest('[data-report-id]');if(reportButton){openReport(reportButton.dataset.reportId,'任务报告');return;}
  const artifactButton=e.target.closest&&e.target.closest('[data-artifact-task]');if(artifactButton){openArtifact(artifactButton.dataset.artifactTask,artifactButton.dataset.artifactName);return;}
  const b=e.target.closest&&e.target.closest('button[data-act]'); if(b){ post('/api/'+b.dataset.act+'/'+b.dataset.id); return; }
  const rp=e.target.closest&&e.target.closest('.rep[data-report]'); if(rp){ openReport(rp.dataset.report, rp.dataset.name); return; }
  const d=e.target.closest&&e.target.closest('.doc[data-doc]'); if(d) openDoc(d.dataset.doc);
});
async function openDoc(type){
  const company=currentCompany,generation=companyGeneration,sequence=++modalSequence;
  document.getElementById('m-title').textContent=type.replace(/_/g,' ');
  document.getElementById('m-body').textContent='Loading…';
  document.getElementById('modal').classList.add('show');
  try{ const r=await(await appFetch('/api/document?type='+encodeURIComponent(type))).json();
    if(stillCurrent(generation,company)&&sequence===modalSequence)document.getElementById('m-body').textContent=r.content||'(empty)'; }
  catch(e){ if(stillCurrent(generation,company)&&sequence===modalSequence)document.getElementById('m-body').textContent='[error] '+e; }
}
async function openReport(id, name){
  const company=currentCompany,generation=companyGeneration,sequence=++modalSequence;
  document.getElementById('m-title').textContent=name||('report #'+id);
  document.getElementById('m-body').textContent='Loading…';
  document.getElementById('modal').classList.add('show');
  try{ const r=await(await appFetch('/api/report?id='+encodeURIComponent(id))).json();
    if(stillCurrent(generation,company)&&sequence===modalSequence)document.getElementById('m-body').textContent=(r&&r.content)||'(empty)'; }
  catch(e){ if(stillCurrent(generation,company)&&sequence===modalSequence)document.getElementById('m-body').textContent='[error] '+e; }
}
function closeDoc(){ modalSequence++;document.getElementById('modal').classList.remove('show'); }
document.addEventListener('keydown',e=>{ if(e.key==='Escape')closeDoc(); });

let started=false;
function newCompany(){ started=false; fetch('/api/reset',{method:'POST'}).then(()=>tick()); }
async function submitOnboard(){
  const v=document.getElementById('ob-idea').value.trim(); if(!v)return;
  started=true;
  const btn=document.getElementById('ob-btn'); btn.disabled=true; btn.textContent='Setting up…';
  document.getElementById('onboard').classList.remove('show');
  await appFetch('/api/onboard',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({idea:v})});
  btn.disabled=false; btn.textContent='Build it →'; document.getElementById('ob-idea').value='';
  tick();
}

async function tick(){
  const company=currentCompany,generation=companyGeneration,sequence=++tickSequence;
  let s; try{ s=await (await appFetch('/api/state')).json(); }catch(e){ if(stillCurrent(generation,company)&&sequence===tickSequence)showLabError(e); return; }
  if(!stillCurrent(generation,company)||sequence!==tickSequence)return;
  // onboarding overlay: show when there's no onboarded company and we're not mid-onboarding.
  const onboarding = s.busy && s.agent && s.agent.name==='onboarding';
  document.getElementById('onboard').classList.toggle('show', s.mode!=='LOCAL_TEST' && !s.onboarded && !started && !onboarding);
  document.getElementById('co').textContent = s.company;
  const w=document.getElementById('wpill'); w.textContent=s.mode==='LOCAL_TEST'?'本地验收':s.worker?(s.busy?'running':'on'):'off'; w.className='pill'+(s.worker?' on':'');

  const a=s.agent||{mood:'idle',name:'polsia',message:''};
  document.getElementById('face').textContent=face(a.mood);
  document.getElementById('aname').textContent=a.name;
  document.getElementById('amood').textContent=MOODTXT[a.mood]||a.mood;
  document.getElementById('amsg').textContent=a.message||(a.mood==='idle'?'Idle — start the worker or run the daily cron.':'');

  const b=s.business||{};
  document.getElementById('b-visitors').textContent=b.visitors??0;
  document.getElementById('b-revenue').textContent=b.revenue??'$0.00';
  document.getElementById('b-shipped').textContent=b.shippedToday??0;
  document.getElementById('b-docs').textContent=b.docs??0;

  document.getElementById('tasks').innerHTML = (s.tasks&&s.tasks.length)? s.tasks.map(t=>
    '<div class="row"><span class="pr">p'+t.priority+'</span><span class="badge b-'+t.status+'">'+t.status.replace('_',' ')+'</span>'+
    '<span class="ttl">'+esc(t.title)+'</span><button onclick="openTask(\''+t.id+'\')">详情</button>'+
    ((t.status==='todo'||t.status==='needs_continuation'||(t.status==='failed'&&t.kind!=='business'))?'<button onclick="executeTask(\''+t.id+'\',this)">'+(t.kind==='business'?'执行业务':'执行核验')+'</button>':'')+
    (t.kind==='business'&&t.status==='in_progress'?'<button onclick="cancelBusinessTask(\''+t.id+'\')">取消</button>':'')+
    (t.kind==='business'&&['failed','blocked','needs_continuation'].includes(t.status)?'<button onclick="reconcileBusinessTask(\''+t.id+'\')">核对回执</button>':'')+
    (t.status==='suggested'?'<button data-act="approve" data-id="'+t.id+'">ok</button> <button data-act="reject" data-id="'+t.id+'">x</button>':'')+
    '</div>').join('') : '<div class="muted">尚无任务。在右侧写下交付要求并创建任务。</div>';

  const docRows = (s.documents||[]).map(d=>
    '<div class="row doc" data-doc="'+esc(d.type)+'"><span class="ic">▤</span><span class="ttl">'+esc(d.type.replace(/_/g,' '))+'</span><span class="muted">'+d.updated+'</span> <span class="arr">view ›</span></div>');
  const repRows = (s.reports||[]).map(r=>
    '<div class="row doc rep" data-report="'+r.id+'" data-name="'+esc(r.name)+'"><span class="ic">◈</span><span class="ttl">'+esc(r.name)+'</span><span class="muted">'+r.created+'</span> <span class="arr">view ›</span></div>');
  document.getElementById('docs').innerHTML = (docRows.length||repRows.length)? docRows.concat(repRows).join('') : '<div class="muted">完成任务后，交付物与报告会显示在这里。</div>';

  document.getElementById('website').innerHTML = s.website
    ? '<div class="row"><span class="ttl"><a href="'+s.website+'" target="_blank">'+esc(s.website)+'</a></span><button>manage</button></div>'
    : '<div class="soon">当前运行于本机；公开发布尚未授权。</div>';

  const ev=s.events||[];
  const last=ev[ev.length-1];
  document.getElementById('logline').textContent = last? ('› '+last.actor+' · '+last.type+' '+(last.payload||'')).slice(0,160) : '› idle';
  document.getElementById('logfull').innerHTML = ev.map(e=>'<div><span class="t">'+e.ts+'</span> <span class="a">'+e.actor+'</span> '+e.type+' '+esc(e.payload)+'</div>').join('');
}

const clog=document.getElementById('chatlog');
function addmsg(who,txt){ const d=document.createElement('div'); d.className=who==='you'?'you':'bot'; d.textContent=(who==='you'?'You: ':'Polsia: ')+txt; clog.appendChild(d); clog.scrollTop=clog.scrollHeight; return d; }
async function loadChat(){
  const company=currentCompany,generation=companyGeneration,sequence=++chatSequence;
  try{ const r=await(await appFetch('/api/messages')).json();
    if(!stillCurrent(generation,company)||sequence!==chatSequence)return;
    clog.innerHTML='';
    (r.messages||[]).forEach(m=>addmsg(m.role==='user'?'you':'bot', m.content));
  }catch(e){}
}
loadChat();
document.getElementById('chatin').addEventListener('keydown',async e=>{
  if(e.key!=='Enter')return; const v=e.target.value.trim(); if(!v)return;
  e.target.value=''; addmsg('you',v); const pend=addmsg('bot','…thinking');
  let text='';
  try{
    const resp=await appFetch('/api/chat',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({message:v})});
    const reader=resp.body.getReader(); const dec=new TextDecoder(); let buf='';
    for(;;){
      const {value,done}=await reader.read(); if(done)break;
      buf+=dec.decode(value,{stream:true});
      let i; while((i=buf.indexOf('\n\n'))>=0){
        const line=buf.slice(0,i).trim(); buf=buf.slice(i+2);
        if(!line.startsWith('data:'))continue;
        const ev=JSON.parse(line.slice(5).trim());
        if(ev.type==='tool'){ if(!text) pend.textContent='Polsia: ⚙ '+ev.name+'…'; }
        else if(ev.type==='text'){ text+=ev.delta; pend.textContent='Polsia: '+text; }
        else if(ev.type==='done'){ text=ev.reply||text; pend.textContent='Polsia: '+(text||'(no reply)'); }
        clog.scrollTop=clog.scrollHeight;
      }
    }
  }catch(err){ pend.textContent='Polsia: [error] '+err; }
  tick();
});
async function loadCompanies(){
  const r=await(await appFetch('/api/companies')).json();
  if(!r.companies.some(c=>c.id===currentCompany))changeCompany(r.companies[0]?.id||'demo');
  localStorage.setItem('company-lab-selection',currentCompany);
  document.getElementById('company-select').innerHTML=r.companies.map(c=>'<option value="'+esc(c.id)+'"'+(c.id===currentCompany?' selected':'')+'>'+esc(c.name)+'</option>').join('');
}
async function switchCompany(id){changeCompany(id);await Promise.all([loadChat(),tick()]);}
function newCompany(){document.getElementById('company-name').focus();document.getElementById('company-name').scrollIntoView({behavior:'smooth',block:'center'});}
async function createCompany(event){
  const company=currentCompany,generation=companyGeneration;
  event.preventDefault();const b=document.getElementById('create-company');b.disabled=true;
  try{const r=await(await appFetch('/api/companies',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({name:document.getElementById('company-name').value,goal:document.getElementById('company-goal').value})})).json();
    if(!stillCurrent(generation,company)){await loadCompanies();return;}changeCompany(r.id);await loadCompanies();await tick();document.getElementById('lab-status').textContent='公司与目标已保存。可继续发布业务任务。';document.getElementById('lab-status').classList.remove('lab-error');
  }catch(e){if(stillCurrent(generation,company))showLabError(e)}finally{b.disabled=false}
}
let historyCatalog,businessCatalog;
function updateTaskMode(){
  const business=document.getElementById('task-mode').value==='business';
  const caps=business?businessCatalog?.capabilities:historyCatalog?.capabilities;
  document.getElementById('task-capability').innerHTML=(caps||[]).map(c=>'<option value="'+c.id+'">'+esc(c.title)+'</option>').join('');
  document.getElementById('instruction-field').style.display=business?'block':'none';document.getElementById('batch-tasks').style.display=business?'inline-block':'none';
}
async function loadCapabilities(){
  [historyCatalog,businessCatalog]=await Promise.all([appFetch('/api/capabilities').then(r=>r.json()),appFetch('/api/business').then(r=>r.json())]);updateTaskMode();
  document.getElementById('business-runtime').textContent=businessCatalog.enabled?'Codex 本地执行已启用 · 最多4项并行 · 结果需审核':'本地业务执行待启用；历史资料核验可用';
  document.getElementById('capabilities').innerHTML=businessCatalog.capabilities.map(c=>'<div class="lab-cap"><strong>'+esc(c.title)+'</strong><p>'+esc(c.output)+'</p><span class="badge">本地交付</span><p>'+esc(c.limitation)+'</p></div>').join('')+'<div class="lab-cap"><strong>并行工作流、恢复与运行审计</strong><p>持久任务、最多4项执行、取消、完整回执、结果未知时核对后接续。</p><p>监控站由已有负责人维护，当前站点提供任务与结果接口。</p></div><details><summary>继承的九类历史证据</summary>'+historyCatalog.capabilities.map(c=>'<div class="lab-cap"><strong>'+esc(c.title)+'</strong><p>'+esc(c.summary)+'</p><button onclick="openCapability(\''+c.id+'\')">查看原始证据</button></div>').join('')+'</details>';
}
async function createEvidenceTask(event){
  const company=currentCompany,generation=companyGeneration;
  event.preventDefault();const b=document.getElementById('create-task');b.disabled=true;
  try{const business=document.getElementById('task-mode').value==='business';const title=document.getElementById('task-title').value,category=document.getElementById('task-capability').value,instruction=document.getElementById('task-instruction').value.trim()||document.getElementById('company-goal').value.trim()||title;const r=await(await appFetch(business?'/api/business/tasks':'/api/tasks',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(business?{title,category,instruction}:{title,capabilityId:category})})).json();r.task=r.task||r.tasks[0];
    if(!stillCurrent(generation,company))return;document.getElementById('lab-status').textContent='任务 '+r.task.id+' 已保存，点击执行生成本次真实交付或核验报告。';await tick();
  }catch(e){if(stillCurrent(generation,company))showLabError(e)}finally{b.disabled=false}
}
async function executeTask(id,button){
  const company=currentCompany,generation=companyGeneration;button.disabled=true;try{await appFetch('/api/tasks/'+id+'/execute',{method:'POST'});if(!stillCurrent(generation,company))return;await tick();if(stillCurrent(generation,company))await openTask(id)}catch(e){if(stillCurrent(generation,company))showLabError(e)}finally{button.disabled=false}
}
async function openTask(id){
  const company=currentCompany,generation=companyGeneration,sequence=++modalSequence;
  try{const r=await(await appFetch('/api/tasks/'+id)).json();if(!stillCurrent(generation,company)||sequence!==modalSequence)return;document.getElementById('m-title').textContent=r.task.title;const t=r.task;document.getElementById('m-body').innerHTML='<p>状态：'+esc(t.status)+'</p><p>'+esc(t.result?.summary||'任务已保存，等待执行。')+'</p>'+((t.result?.artifacts||[]).map(a=>{const u=new URL(a.ref,location.origin),name=u.searchParams.get('name')||'';return '<p><button '+(a.type==='report'?'data-report-id="'+esc(u.searchParams.get('id')||'')+'"':'data-artifact-task="'+t.id+'" data-artifact-name="'+esc(name)+'"')+'>'+esc(name||(a.type==='report'?'查看报告':'查看回执'))+'</button></p>'}).join(''))+'<details><summary>完整任务回执</summary><pre style="white-space:pre-wrap">'+esc(JSON.stringify(t,null,2))+'</pre></details>';document.getElementById('modal').classList.add('show')}
  catch(e){if(stillCurrent(generation,company)&&sequence===modalSequence)showLabError(e)}
}
async function openCapability(id){
  const company=currentCompany,generation=companyGeneration,sequence=++modalSequence;
  try{const r=await(await appFetch('/api/capabilities/'+id+'/evidence')).json();if(!stillCurrent(generation,company)||sequence!==modalSequence)return;document.getElementById('m-title').textContent=r.title;document.getElementById('m-body').textContent='SHA-256: '+r.sha256+'\n历史证据只读核验：'+r.integrity+'\n\n'+r.content;document.getElementById('modal').classList.add('show')}
  catch(e){if(stillCurrent(generation,company)&&sequence===modalSequence)showLabError(e)}
}
async function createBusinessBatch(){
  const company=currentCompany,generation=companyGeneration,b=document.getElementById('batch-tasks');b.disabled=true;
  const instruction=document.getElementById('task-instruction').value.trim()||document.getElementById('company-goal').value.trim()||'为当前公司准备本地可审核交付物';
  try{const items=['engineering','marketing','support','sales'].map(category=>({category,title:({engineering:'制作报价网页',marketing:'编写营销计划',support:'准备客服FAQ',sales:'准备需求提案'})[category],instruction}));const r=await(await appFetch('/api/business/tasks/batch',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({items})})).json();if(!stillCurrent(generation,company))return;document.getElementById('lab-status').textContent='已一次保存4项业务任务。逐项点击执行，可并行观察结果。';await tick()}catch(e){if(stillCurrent(generation,company))showLabError(e)}finally{b.disabled=false}
}
async function cancelBusinessTask(id){const company=currentCompany,generation=companyGeneration;try{await appFetch('/api/business/tasks/'+id+'/cancel',{method:'POST'});if(stillCurrent(generation,company))await tick()}catch(e){if(stillCurrent(generation,company))showLabError(e)}}
async function reconcileBusinessTask(id){const company=currentCompany,generation=companyGeneration;try{await appFetch('/api/business/tasks/'+id+'/reconcile',{method:'POST'});if(stillCurrent(generation,company)){await tick();if(stillCurrent(generation,company))await openTask(id)}}catch(e){if(stillCurrent(generation,company))showLabError(e)}}
async function openArtifact(id,name){
 const company=currentCompany,generation=companyGeneration,sequence=++modalSequence;
 try{const path=name?'/api/business/tasks/'+id+'/artifact?name='+encodeURIComponent(name):'/api/business/tasks/'+id;const r=await(await appFetch(path)).json();if(!stillCurrent(generation,company)||sequence!==modalSequence)return;document.getElementById('m-title').textContent=name||'真实业务回执';document.getElementById('m-body').textContent=r.content||JSON.stringify(r,null,2);document.getElementById('modal').classList.add('show')}catch(e){if(stillCurrent(generation,company)&&sequence===modalSequence)showLabError(e)}
}
async function initializeLab(){try{await loadCompanies();await loadCapabilities();await loadChat();await tick()}catch(e){showLabError(e)}}
initializeLab();setInterval(tick,1500);
</script>
</body></html>`;
