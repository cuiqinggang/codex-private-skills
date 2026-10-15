import json,sqlite3,pathlib,hashlib
root=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014/component-check-20261015-r1')
db=root/'profile/profiles/local-default/profile-state.db'
c=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)
settings=json.loads(c.execute("SELECT payload FROM profile_state_documents WHERE domain='settings'").fetchone()[0])
seed=json.loads((root/'profile/profiles/local-default/orca-data.json').read_text(encoding='utf-8')) if (root/'profile/profiles/local-default/orca-data.json').exists() else None
keys=['workspaceDir','agentDefaultArgs','agentDefaultEnv','agentYoloDefaultsMigrated','agentStatusHooksEnabled','agentWorkspaceTrustEnabled','experimentalNativeChat','codexManagedAccounts','activeCodexManagedAccountId','localWindowsRuntimeDefault','terminalWindowsShell']
selected={k:settings.get(k) for k in keys}
assert selected['agentStatusHooksEnabled'] is False
assert selected['agentWorkspaceTrustEnabled'] is False
assert selected['experimentalNativeChat'] is False
assert selected['codexManagedAccounts']==[]
assert selected['agentDefaultArgs']['codex']=='--sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review -c service_tier=priority'
assert pathlib.Path(selected['workspaceDir'])==root/'worktrees'
receipt=json.loads((root/'terminal-receipt.json').read_text())
result=json.loads((root/'result.json').read_text())
assert result['terminal_environment']==receipt
assert result['terminal_handle']==receipt['terminal']
assert not result['remaining_owned']
out={'settings_import_pass':True,'terminal_receipt_independent_readback':True,'settings':selected,'result_sha256':hashlib.sha256((root/'result.json').read_bytes()).hexdigest(),'harness_exit1_cause':'tuple/list JSON roundtrip comparison; component results independently verified'}
(root/'independent-verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out))
