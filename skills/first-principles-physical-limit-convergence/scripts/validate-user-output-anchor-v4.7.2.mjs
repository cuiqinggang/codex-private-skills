import fs from 'node:fs';

const path=process.argv[2];
if(!path){
  console.error('用法: node validate-user-output-anchor-v4.7.2.mjs <回答文本>');
  process.exit(64);
}
const text=fs.readFileSync(path,'utf8');
const first=(text.split(/\r?\n/).find(x=>x.trim().length>0)||'').trim();
const re=/^【状态 G\d{2}-A0[1-6]-(虚|实)｜极限锚 03:14\.419｜闭环 \d{2}:\d{2}:\d{2}\.\d{3}｜偏差 [+-]\d{2}:\d{2}:\d{2}\.\d{3}｜时间状态 (目标内|超目标)】$/;
const ok=re.test(first);
console.log(JSON.stringify({
  VALID:ok,
  执行动作:ok?'允许':'阻断',
  first_line:first,
  error:ok?null:'MISSING_OR_INVALID_HORIZONTAL_TIME_STATE_HEADER'
},null,2));
process.exit(ok?0:2);
