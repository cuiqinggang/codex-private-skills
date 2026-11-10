"""Enhanced Pi entry: keep the official 18.18 core; explicit matched archive batches reuse original programmes."""
import argparse,json,pathlib,subprocess,sys,os
R=pathlib.Path(__file__).resolve().parent
entry=pathlib.Path('C:/Users/A/Documents/DSH-Workspace/pi-rules-r64-20261108/runtime/launch_pi.py')
library=pathlib.Path(__file__).resolve().parent/'f2/snapshot'
raw=sys.argv[1:]
if '--fast-archive-batch' in raw:
    os.environ['R95_PIN']='0'
    os.environ['R95_QA']='serial'
    p=argparse.ArgumentParser(description='Explicit admitted host archive batch; original sandbox and QA retained.')
    p.add_argument('--fast-archive-batch',type=pathlib.Path,required=True)
    p.add_argument('--cwd',type=pathlib.Path,required=True)
    p.add_argument('--workers',type=int,choices=[1,2,4,8],default=4)
    p.add_argument('--library',type=pathlib.Path,default=library)
    p.add_argument('--reuse-lanes',action='store_true')
    p.add_argument('--stream-lanes',action='store_true')
    a=p.parse_args(raw)
    request_paths=json.loads(a.fast_archive_batch.read_text(encoding='utf-8-sig'))
    if not isinstance(request_paths,list) or not 1<=len(request_paths)<=128:
        p.error('This bounded fast route requires 1..128 independent archive requests')
    for name in request_paths:
        request=json.loads(pathlib.Path(name).read_text(encoding='utf-8-sig'))
        if request.get('goal')!='files.archive_exact' or request.get('context')!='host':
            p.error('Host archive contracts only; inside-OMP tasks use their original native context')
    command=[sys.executable,'-X','utf8',str(library/'scripts/deliver_archive_batch.py'),'--library',str(a.library),'--requests',str(a.fast_archive_batch),'--workers',str(a.workers),'--workspace',str(a.cwd)]
    if a.reuse_lanes:command.append('--reuse-lanes')
    if a.stream_lanes:command.append('--stream-lanes')
    raise SystemExit(subprocess.call(command,cwd=a.cwd,stdin=subprocess.DEVNULL))
raise SystemExit(subprocess.call([sys.executable,str(entry),*raw]))
