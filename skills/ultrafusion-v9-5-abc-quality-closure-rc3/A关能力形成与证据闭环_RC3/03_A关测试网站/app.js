
const pressureDefs=[
["defect",15,"定位最高价值缺陷"],
["fix1",25,"第一轮定向修复"],
["rescore1",15,"第一轮重新评分"],
["fix2",20,"第二轮定向修复"],
["probe",15,"极限探针/反例/边界挑战"],
["history",10,"历史最佳比较与保留/回退"]
];
const stages=[
["q0","Q0｜零流程基线"],
["qr","QR｜压力前原始"],
["q1","Q1｜第一轮修复"],
["q2","Q2｜第二轮修复"],
["qf","QF｜最终极限"]
];
const dims=[["F","事实与证据可靠性",.25],["L","逻辑闭合性",.20],["C","完备性与任务相关性",.20],["D","深度、反例与路径价值",.15],["U","清晰度与可执行性",.20]];
const gateNames=[
"前置测试合同完整","关键变量已记录","原版保持只读","正式源提示词已锁定",
"测试输入装配一致","必须内容完整","禁止内容清零","镜像内容一致",
"独立验证三类齐全","冷启动复现通过","量化计算完整且硬闸门通过","证据矩阵完整并形成发布决定"
];
const evidenceNames=[
"原始问题","零流程直接回答","V15.1-A发送内容","模型完整原始回复","自动拆分结果","各阶段质量评分",
"压力值计算","时间与操作记录","匿名交换顺序评审","压力—质量曲线","性价比计算","最终验收结论"
];
const promptManifest={
 asset:"assets/V15.1-A_正式只读提示词.txt",
${REDACTED_SECRET}
 expectedCharacters:1260,
 expectedBytes:2890,
 expectedSha256:"1E85CF5234527B7F491823EF8755C6940D4FD96C608B0D0866A0CFE8D0BF4EDE"
};
let promptVerified=false;
let currentDecision={code:"REVISE",label:"继续修订",nextGate:"L4｜GPT三题真实烟雾测试"};

async function init(){
 document.getElementById("pressureActions").innerHTML=pressureDefs.map(x=>`<label><input type="checkbox" id="p_${x[0]}" onchange="calculateAndSave()"> ${x[2]}（${x[1]}分）</label>`).join("");
 let h="<table><tr><th>阶段</th>"+dims.map(d=>`<th>${d[0]}｜${d[1]}</th>`).join("")+"<th>总质量分</th></tr>";
 for(const s of stages){h+=`<tr><td>${s[1]}</td>`+dims.map(d=>`<td><input id="${s[0]}_${d[0]}" type="number" min="0" max="100" step="0.1" value="0" onchange="calculateAndSave()"></td>`).join("")+`<td id="${s[0]}_total">0.00</td></tr>`}
 h+="</table>";document.getElementById("scoreTable").innerHTML=h;
 document.getElementById("gates").innerHTML=gateNames.map((g,i)=>`<div class="gate"><label><input type="checkbox" id="gate${i+1}"> 关口${i+1}：${g}</label></div>`).join("");
 document.getElementById("evidenceMatrix").innerHTML=evidenceNames.map((e,i)=>`<div class="evidence"><label><input type="checkbox" id="ev${i+1}"> 图片证据${i+1}：${e}</label></div>`).join("");
 await loadPrompt();loadState();calculateAll();
 document.getElementById("validSampleMetric").textContent=val("validSamples");
 const restoredEvidence=evidenceNames.filter((_,i)=>document.getElementById("ev"+(i+1)).checked).length;
 document.getElementById("evidenceMetric").textContent=`${(restoredEvidence/12*100).toFixed(1)}%`;
}
async function sha256Hex(bytes){const digest=await crypto.subtle.digest("SHA-256",bytes);return [...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,"0")).join("").toUpperCase()}
async function loadPrompt(){
 const status=document.getElementById("promptStatus");
 try{
  const response=await fetch(promptManifest.asset,{cache:"no-store"});
  if(!response.ok)throw new Error(`HTTP ${response.status}`);
  const bytes=await response.arrayBuffer();
  const text=new TextDecoder("utf-8").decode(bytes);
  const hash=await sha256Hex(bytes);
  promptVerified=text.length===promptManifest.expectedCharacters&&bytes.byteLength===promptManifest.expectedBytes&&hash===promptManifest.expectedSha256;
  document.getElementById("officialPrompt").value=text;
  document.getElementById("promptSourcePath").textContent=promptManifest.sourcePath;
  document.getElementById("promptCharacters").textContent=text.length;
  document.getElementById("promptBytes").textContent=bytes.byteLength;
  document.getElementById("promptHash").textContent=hash;
  status.textContent=promptVerified?"哈希核验通过":"哈希不一致";
  status.className=`status-badge ${promptVerified?"pass":"fail"}`;
 }catch(error){
  promptVerified=false;status.textContent="正式源加载失败";status.className="status-badge fail";
  document.getElementById("copyStatus").textContent=`无法加载只读源：${error.message}`;
 }
}
async function copyText(text,message){
 if(!promptVerified){document.getElementById("copyStatus").textContent="哈希未通过，已阻止复制。";return}
 try{await navigator.clipboard.writeText(text);document.getElementById("copyStatus").textContent=message}catch(_){document.getElementById("copyStatus").textContent="浏览器未授予剪贴板权限，请手动复制只读正文。"}
}
function copyOfficialPrompt(){copyText(document.getElementById("officialPrompt").value,"已复制哈希锁定的正式原文。")}
function copyAssembledPrompt(){
 const q=document.getElementById("question").value.trim();
 if(!q){document.getElementById("copyStatus").textContent="请先填写原始问题。";return}
 const source=document.getElementById("officialPrompt").value;
 const marker="<<<在这里完整粘贴原始问题、资料、硬约束和输出要求>>>";
 const assembled=source.includes(marker)?source.replace(marker,q):`${source}\n\n## 原始用户问题\n\n${q}`;
 copyText(assembled,"已装配当前问题并复制；正式源原文未被修改。")
}
function val(id){return Number(document.getElementById(id).value||0)}
function stageScore(stage){return dims.reduce((s,d)=>s+val(stage+"_"+d[0])*d[2],0)}
function calculatePressure(){
 let p=pressureDefs.reduce((s,x)=>s+(document.getElementById("p_"+x[0]).checked?x[1]:0),0);
 document.getElementById("pressureScore").textContent=p;return p
}
function parseReply(){
 const t=document.getElementById("fullReply").value;
 const raw=t.match(/【A_RAW_BEGIN】([\s\S]*?)【A_RAW_END】/)||t.match(/【A_Raw[^】]*】([\s\S]*?)(?=【A_Final|$)/);
 const fin=t.match(/【A_FINAL_BEGIN】([\s\S]*?)【A_FINAL_END】/)||t.match(/【A_Final[^】]*】([\s\S]*?)(?=【A层极限压力记录|$)/);
 const log=t.match(/【A_PRESSURE_RECORD_BEGIN】([\s\S]*?)【A_PRESSURE_RECORD_END】/)||t.match(/【A层极限压力记录】([\s\S]*)/);
 if(raw)document.getElementById("raw").value=raw[1].trim();
 if(fin)document.getElementById("final").value=fin[1].trim();
 if(log)document.getElementById("pressureLog").value=log[1].trim();
 const missing=[];if(!raw)missing.push("A_Raw");if(!fin)missing.push("A_Final");if(!log)missing.push("A层极限压力记录");
 const echo=/请确认是否开始|尚未执行|已收到文件|完整提示词|系统提示词/.test(t);
 document.getElementById("parseStatus").innerHTML=missing.length?`<span class="fail">解析失败：缺少 ${missing.join("、")}</span>`:`<span class="pass">三个区块解析成功</span>${echo?'<br><span class="fail">检测到疑似未执行或命令回显</span>':''}`;
}
function calculateAll(){
 const scores={};for(const s of stages){scores[s[0]]=stageScore(s[0]);document.getElementById(s[0]+"_total").textContent=scores[s[0]].toFixed(2)}
 const times={q0:val("t0"),qr:val("tr"),q1:val("t1"),q2:val("t2"),qf:val("tf")};
 const stagePressure={q0:0,qr:0,q1:55,q2:75,qf:100};
 const budget=val("budget"), noise=val("noise"), pressure=calculatePressure();
 const valid=stages.map(s=>({id:s[0],name:s[1],q:scores[s[0]],t:times[s[0]]})).filter(x=>x.t<=budget);
 let best=valid.sort((a,b)=>(b.q-a.q)|| (a.t-b.t))[0]||null;
 const external=scores.qf-scores.q0, internal=scores.qf-scores.qr, extra=times.qf-times.q0;
 const ratio=extra>0?external/extra:null;
 const marginal=[];
 const order=["q0","qr","q1","q2","qf"];
 for(let i=1;i<order.length;i++){const a=order[i-1],b=order[i],dt=times[b]-times[a],dq=scores[b]-scores[a];marginal.push({from:a,to:b,dq,dt,rate:dt>0?dq/dt:null})}
 let effective="q0";
 for(const m of marginal){if(m.dq>=noise) effective=m.to}
 const effectivePressure=Math.min(stagePressure[effective],pressure);
 const bestPressure=best?Math.min(stagePressure[best.id],pressure):null;
 const hard=val("factErrors")+val("logicBreaks")+val("criticalOmissions")+val("hallucinations")===0;
 let html=`<b>实际最大压力：</b>${pressure}/100<br><b>有效最大压力：</b>${effectivePressure}/100（${effective}）<br><b>最佳性价比压力：</b>${bestPressure===null?'无法计算':bestPressure+'/100'}<br><b>外部提升：</b>${external.toFixed(2)}分<br><b>内部提升：</b>${internal.toFixed(2)}分<br><b>最终时间性价比：</b>${ratio===null?'无法计算':ratio.toFixed(2)+'分/额外分钟'}<br>`;
 html+=`<b>固定${budget}分钟内最佳版本：</b>${best?best.name+'，'+best.q.toFixed(2)+'分，'+best.t.toFixed(1)+'分钟':'无有效版本'}<br>`;
 html+=`<b>硬性质量闸门：</b>${hard?'<span class="pass">通过</span>':'<span class="fail">失败</span>'}<br><br>`;
 html+="<table><tr><th>阶段变化</th><th>质量增量</th><th>新增时间</th><th>边际收益</th></tr>"+marginal.map(m=>`<tr><td>${m.from}→${m.to}</td><td>${m.dq.toFixed(2)}</td><td>${m.dt.toFixed(2)}</td><td>${m.rate===null?'无法计算':m.rate.toFixed(2)+'分/分钟'}</td></tr>`).join("")+"</table>";
 document.getElementById("calculation").innerHTML=html;
 return {scores,times,budget,noise,pressure,effective,effectivePressure,best,bestPressure,hard,external,internal,ratio,marginal};
}
function calculateAndSave(){calculateAll();saveState(false)}
function evaluateGates(){
 const c=calculateAll();const reply=document.getElementById("fullReply").value;
 const parsed=document.getElementById("raw").value.trim()&&document.getElementById("final").value.trim()&&document.getElementById("pressureLog").value.trim();
 const echo=/请确认是否开始|尚未执行|已收到文件/.test(reply);
 const auto=[
 document.getElementById("caseId").value&&document.getElementById("model").value&&document.getElementById("promptVersion").value,
 document.getElementById("networkStatus").value&&document.getElementById("reviewer").value&&document.getElementById("orderPolicy").value,
 true,
 promptVerified,
 promptVerified&&document.getElementById("question").value.trim(),
 parsed,
 !echo,
 promptVerified,
 document.getElementById("independentReview").checked&&document.getElementById("humanReview").checked,
 val("coldStartPasses")>=3,
 c.hard&&c.pressure>0&&c.scores.q0>0&&c.scores.qf>0,
 false
 ];
 auto.forEach((x,i)=>{if(i<11)document.getElementById("gate"+(i+1)).checked=!!x});
 const evDone=evidenceNames.every((_,i)=>document.getElementById("ev"+(i+1)).checked);
 document.getElementById("gate12").checked=evDone;
 const passed=gateNames.filter((_,i)=>document.getElementById("gate"+(i+1)).checked).length;
 const evidence=evidenceNames.filter((_,i)=>document.getElementById("ev"+(i+1)).checked).length;
 const evidenceRate=evidence/12*100,samples=val("validSamples"),regressions=val("decisiveRegressions");
 const reviewed=document.getElementById("independentReview").checked&&document.getElementById("humanReview").checked;
 if(regressions>0){currentDecision={code:"ROLLBACK",label:"回退：存在决定性回退",nextGate:"定位失败关口并建立新候选版本"}}
 else if(passed<12||evidence<12||!reviewed){currentDecision={code:"REVISE",label:"继续修订：关口、证据或独立复核尚未闭环",nextGate:"L4｜GPT三题真实烟雾测试"}}
 else if(samples<12){currentDecision={code:"REVISE",label:"继续修订：真实有效样本不足12个",nextGate:samples<3?"L4｜GPT三题真实烟雾测试":"L5/L6｜三模型一致性与12个有效组合"}}
 else if(samples<24){currentDecision={code:"LIMIT",label:"限制适用场景：已达候选样本门槛，未达正式冻结建议样本",nextGate:"L7候选｜补足24个以上有效组合"}}
 else{currentDecision={code:"FREEZE",label:"冻结候选：仍需人工发布批准并更新能力账本",nextGate:"人工批准正式冻结"}}
 const status=`${currentDecision.code}｜${currentDecision.label}`;
 document.getElementById("gateSummary").innerHTML=`十二道关口：${passed}/12（${(passed/12*100).toFixed(1)}%）<br>图片证据：${evidence}/12（${(evidence/12*100).toFixed(1)}%）`;
 document.getElementById("finalStatus").textContent=status;
 document.getElementById("validSampleMetric").textContent=samples;
 document.getElementById("evidenceMetric").textContent=`${evidenceRate.toFixed(1)}%`;
 document.getElementById("requiredOutput").innerHTML=`<strong>当前成熟度等级：</strong>L3｜模拟验证通过<br><strong>十二道关口通过数：</strong>${passed}/12<br><strong>证据完整率：</strong>${evidenceRate.toFixed(1)}%<br><strong>有效样本数：</strong>${samples}<br><strong>Q0 / QR / Q1 / Q2 / QF：</strong>${c.scores.q0.toFixed(2)} / ${c.scores.qr.toFixed(2)} / ${c.scores.q1.toFixed(2)} / ${c.scores.q2.toFixed(2)} / ${c.scores.qf.toFixed(2)}<br><strong>实际最大压力：</strong>${c.pressure}/100<br><strong>有效最大压力：</strong>${c.effectivePressure}/100<br><strong>最佳性价比压力：</strong>${c.bestPressure===null?'无法计算':c.bestPressure+'/100'}<br><strong>固定时间最佳版本：</strong>${c.best?c.best.name:'无'}<br><strong>决定性回退数：</strong>${regressions}<br><strong>最终状态：</strong>${status}<br><strong>下一关口：</strong>${currentDecision.nextGate}`;
 saveState(false);return {passed,evidence,status}
}
function collect(){
 const obj={meta:{caseId:caseId.value,taskType:taskType.value,model:model.value,strength:strength.value,networkStatus:networkStatus.value,reviewer:reviewer.value,orderPolicy:orderPolicy.value,promptVersion:promptVersion.value,budget:val("budget"),noise:val("noise"),validSamples:val("validSamples"),decisiveRegressions:val("decisiveRegressions"),coldStartPasses:val("coldStartPasses")},maturity:"L3_SIMULATION_VALIDATED",reviews:{independent:independentReview.checked,human:humanReview.checked},releaseDecision:currentDecision,question:question.value,fullReply:fullReply.value,raw:raw.value,final:final.value,pressureLog:pressureLog.value,pressureActions:{},scores:{},times:{q0:val("t0"),qr:val("tr"),q1:val("t1"),q2:val("t2"),qf:val("tf"),active:val("activeTime")},hardGates:{factErrors:val("factErrors"),logicBreaks:val("logicBreaks"),criticalOmissions:val("criticalOmissions"),hallucinations:val("hallucinations")},gates:[],evidence:[]};
 pressureDefs.forEach(x=>obj.pressureActions[x[0]]=document.getElementById("p_"+x[0]).checked);
 stages.forEach(s=>{obj.scores[s[0]]={};dims.forEach(d=>obj.scores[s[0]][d[0]]=val(s[0]+"_"+d[0]))});
 gateNames.forEach((g,i)=>obj.gates.push({name:g,passed:document.getElementById("gate"+(i+1)).checked}));
 evidenceNames.forEach((e,i)=>obj.evidence.push({name:e,complete:document.getElementById("ev"+(i+1)).checked}));
 obj.calculated=calculateAll();return obj;
}
function saveState(show=true){localStorage.setItem("uf951_a_site",JSON.stringify(collect()));if(show)alert("已保存在当前浏览器")}
function loadState(){const s=localStorage.getItem("uf951_a_site");if(!s)return;try{const o=JSON.parse(s);for(const [k,v] of Object.entries(o.meta||{})){const e=document.getElementById(k);if(e)e.value=v}question.value=o.question||"";fullReply.value=o.fullReply||"";raw.value=o.raw||"";final.value=o.final||"";pressureLog.value=o.pressureLog||"";if(o.reviews){independentReview.checked=!!o.reviews.independent;humanReview.checked=!!o.reviews.human}if(o.releaseDecision)currentDecision=o.releaseDecision;for(const [k,v] of Object.entries(o.pressureActions||{})){const e=document.getElementById("p_"+k);if(e)e.checked=v}for(const [s,ds] of Object.entries(o.scores||{}))for(const [d,v] of Object.entries(ds)){const e=document.getElementById(s+"_"+d);if(e)e.value=v}for(const [k,v] of Object.entries(o.times||{})){const map={q0:"t0",qr:"tr",q1:"t1",q2:"t2",qf:"tf",active:"activeTime"};if(map[k])document.getElementById(map[k]).value=v}for(const [k,v] of Object.entries(o.hardGates||{})){const e=document.getElementById(k);if(e)e.value=v}(o.gates||[]).forEach((x,i)=>document.getElementById("gate"+(i+1)).checked=x.passed);(o.evidence||[]).forEach((x,i)=>document.getElementById("ev"+(i+1)).checked=x.complete)}catch(e){}}
function resetState(){localStorage.removeItem("uf951_a_site");location.reload()}
function download(name,text,type){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;a.click();URL.revokeObjectURL(a.href)}
function exportJSON(){const o=collect();download(o.meta.caseId+".json",JSON.stringify(o,null,2),"application/json")}
function exportMarkdown(){const o=collect();let t=`# ${o.meta.caseId}｜A关量化测试报告\n\n- 当前成熟度：L3｜模拟验证通过\n- 模型：${o.meta.model}\n- 工作强度：${o.meta.strength}\n- 提示词版本：${o.meta.promptVersion}\n- 时间预算：${o.meta.budget}分钟\n- 有效样本数：${o.meta.validSamples}\n- Q0/QR/Q1/Q2/QF：${o.calculated.scores.q0.toFixed(2)} / ${o.calculated.scores.qr.toFixed(2)} / ${o.calculated.scores.q1.toFixed(2)} / ${o.calculated.scores.q2.toFixed(2)} / ${o.calculated.scores.qf.toFixed(2)}\n- 实际最大压力：${o.calculated.pressure}/100\n- 有效最大压力：${o.calculated.effectivePressure}/100\n- 最佳性价比压力：${o.calculated.bestPressure===null?"无法计算":o.calculated.bestPressure+"/100"}\n- 外部提升：${o.calculated.external.toFixed(2)}分\n- 内部提升：${o.calculated.internal.toFixed(2)}分\n- 固定时间最佳版本：${o.calculated.best?o.calculated.best.name:"无"}\n- 决定性回退数：${o.meta.decisiveRegressions}\n- 硬闸门：${o.calculated.hard?"通过":"失败"}\n- 最终状态：${o.releaseDecision.code}｜${o.releaseDecision.label}\n- 下一关口：${o.releaseDecision.nextGate}\n\n## 原始问题\n${o.question}\n\n## A_Raw｜压力前原始答案\n${o.raw}\n\n## A_Final｜压力后最终强化答案\n${o.final}\n\n## A层极限压力记录\n${o.pressureLog}\n`;download(o.meta.caseId+".md",t,"text/markdown")}
window.onload=init;
