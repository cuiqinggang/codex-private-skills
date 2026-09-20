const nodes=[]; const add=(id,kind,deps=[])=>nodes.push({id,kind,deps});
add("BIND","local"); add("J_SPEC","model",["BIND"]);
for(let i=1;i<=20;i++) add("A"+String(i).padStart(2,"0"),"action",["J_SPEC"]);
for(let i=21;i<=24;i++){const p=i-4; add("A"+i,"action",["J_SPEC","A"+p]);}
add("VERIFY","verify",nodes.filter(n=>n.kind==="action").map(n=>n.id)); add("OUT","local",["VERIFY"]);
const byId=new Map(nodes.map(n=>[n.id,n]));
const md=new Map(); function mdepth(id){if(md.has(id))return md.get(id);const n=byId.get(id);const b=n.deps.length?Math.max(...n.deps.map(mdepth)):0;const d=b+(n.kind==="model"?1:0);md.set(id,d);return d;}
const ad=new Map(); function adepth(id){if(ad.has(id))return ad.get(id);const n=byId.get(id);const b=n.deps.length?Math.max(...n.deps.map(adepth)):0;const d=b+(n.kind==="action"?1:0);ad.set(id,d);return d;}
for(const n of nodes){mdepth(n.id);adepth(n.id);}
const result={benchmark:"PE-P0-GENERAL-01",version:"0.2.0",model_barrier_depth:Math.max(...md.values()),action_dependency_depth:Math.max(...ad.values()),dependent_edges:[["A17","A21"],["A18","A22"],["A19","A23"],["A20","A24"]]};
result.pass=result.model_barrier_depth===1&&result.action_dependency_depth===2;
console.log(JSON.stringify(result,null,2)); if(!result.pass) process.exit(1);
