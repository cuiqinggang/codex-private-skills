import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
const root=join(process.cwd(),'src');const files=[];
function walk(dir){for(const n of readdirSync(dir)){const p=join(dir,n);statSync(p).isDirectory()?walk(p):files.push(p)}}walk(root);
const rules=[[/\beval\s*\(/,'dangerous eval'],[/console\.log\s*\(/,'debug console.log'],[/\bany\b/,'explicit any'],[/<img\b(?![^>]*\balt=)/,'image missing alt']];const errors=[];
for(const f of files.filter(x=>/\.(ts|tsx|js|jsx)$/.test(x))){const t=readFileSync(f,'utf8');for(const[r,m]of rules)if(r.test(t))errors.push(`${relative(process.cwd(),f)}: ${m}`)}
if(errors.length){console.error(errors.join('\n'));process.exit(1)}console.log(`STATIC_LINT=PASS files=${files.length}`);
