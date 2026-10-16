import ast,json,pathlib,tempfile,subprocess,time,uuid,threading,hashlib
from types import SimpleNamespace as NS
from unittest.mock import Mock
source=pathlib.Path('suite-ab-r3.py').read_text()
functions=ast.Module(body=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)],type_ignores=[])
ns={'subprocess':subprocess,'time':time,'uuid':uuid,'threading':threading,'hashlib':hashlib,'pathlib':pathlib,'json':json,'__file__':str(pathlib.Path('suite-ab-r3.py').resolve())}
exec(compile(functions,'recovery-functions','exec'),ns)
records=[]
ns.update(write=lambda n,x:records.append((n,x)),deadline=lambda:time.monotonic()+30)
ns['cli']=Mock(side_effect=[subprocess.TimeoutExpired('readonly',25),{'ok':True}])
assert ns['cli_read']('orchestration','task-list')=={'ok':True}
assert ns['cli'].call_count==2 and len(records)==1
ns['cli']=Mock(side_effect=subprocess.TimeoutExpired('readonly',25))
try:ns['cli_read']('orchestration','dispatch-show')
except subprocess.TimeoutExpired:pass
else:raise AssertionError('unbounded read')
assert ns['cli'].call_count==2
ns['cli']=Mock()
try:ns['cli_read']('orchestration','send')
except AssertionError:pass
else:raise AssertionError('mutation retry allowed')
assert ns['cli'].call_count==0
class Gone(Exception):pass
root=Mock();root.pid=123;root.children.return_value=[];root.is_running.return_value=True
ns['psutil']=NS(Process=lambda pid:root,NoSuchProcess=Gone,wait_procs=Mock(side_effect=TimeoutError('slow exit')))
assert ns['stop_tree'](NS(pid=123,poll=lambda:None))==[123]
assert records[-1][1]['events'][0]['stage']=='wait'
root.is_running.return_value=False
assert ns['stop_tree'](NS(pid=123,poll=lambda:None))==[]
# Run the real main failure/finally path: no runtime or business starts.
with tempfile.TemporaryDirectory() as td:
 ns.update(TEST=pathlib.Path(td)/'attempt',ARM='A',LABEL='synthetic',SPEC='synthetic',psutil=NS(virtual_memory=lambda:NS(available=0)))
 exec(compile(ast.Module(body=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name in ['write','read']],type_ignores=[]),'io-functions','exec'),ns)
 import os
 ns['os']=os
 ns['stop_tree']=Mock(side_effect=RuntimeError('cleanup failure'))
 ns['process_snapshot']=lambda p:[]
 ns['main']()
 result=json.loads((ns['TEST']/'result.json').read_text())
 assert result['passed'] is False and result['cleanup_errors'][0]['stage']=='stop_tree'
 assert (ns['TEST']/'local-acceptance.json').exists()
print('PASS 6 recovery boundaries; synthetic offline only')
