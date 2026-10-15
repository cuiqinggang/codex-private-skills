import importlib.util,pathlib,json,hashlib,subprocess
root=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
validator=root/'tools/independent_check_CEO_FROZEN.py'
assert hashlib.sha256(validator.read_bytes()).hexdigest()=='2d6f62b3205454ce5758c98c0160d7aa03b2820f7f05f9c1302a89651cb24979'
spec=importlib.util.spec_from_file_location('qa',validator);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
attempt=root/'business-smoke-20261015-r2'
work=attempt/'worktrees/fixture/component'
def selected(path):return [r for r in m.check(path) if r['name'].startswith('T03_') or r['name']=='ALL_source_compile']
bad=selected(root/'dataset/source')
good=selected(work)
diff=subprocess.run(['git','status','--porcelain'],cwd=work,capture_output=True,text=True)
result={'scope':'T03_ONLY_EXTERNAL_QA','baseline':bad,'candidate':good,'accepted':len(good)==3 and all(r['passed'] for r in good) and any(not r['passed'] for r in bad),'git_status':diff.stdout,'delivery_exists':(work/'DELIVERY.md').exists()}
(attempt/'independent-qa.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
