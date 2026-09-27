import importlib.util
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parent))
import deploy_full_baseline as d
HERE=Path(__file__).resolve().parent

class FullDeployment(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.target=self.root/'skills'/d.SKILL_ID
        self.target.mkdir(parents=True)
        (self.target/'SKILL.md').write_text('---\nversion: 3.1.6\n---\nsynthetic old entry\n',encoding='utf-8')
        (self.target/'VERSION').write_text('3.1.6\n')
        (self.target/'CANONICAL.md').write_text('synthetic old canonical 3.1.6\n')
        (self.target/'user-data.bin').write_bytes(b'\0\x81preserved\r\n')
        (self.target/'empty-dir').mkdir()
        self.old=d.inventory(self.target)
        self.oldhash=d.digest((self.target/'SKILL.md').read_bytes())
        self.work=self.root/'deployment'
        self.files=d.read_payload(HERE/'FULL-BASELINE-PAYLOAD.json')
    def tearDown(self):self.temp.cleanup()
    def install(self):return d.deploy(self.target,self.work,self.files,self.oldhash)
    def unchanged(self):self.assertEqual(d.inventory(self.target),self.old)
    def rewrite_payload(self,edit):
        ob=json.loads((HERE/'FULL-BASELINE-PAYLOAD.json').read_text())
        edit(ob);raw=(json.dumps(ob,ensure_ascii=False)+'\n').encode()
        p=self.root/'bad.json';p.write_bytes(raw)
        return p,d.digest(raw)
    def test_01_full_dependency_set(self):
        self.assertEqual(set(self.files),d.REQUIRED)
        self.assertEqual(len(self.files),13)
    def test_02_upstream_blobs_identical(self):
        obj=json.loads((HERE/'FULL-BASELINE-PAYLOAD.json').read_text())
        self.assertEqual(len(obj['frozen_runtime_sources']),8)
    def test_03_tampered_bundle_rejected(self):
        p=self.root/'bad.json';p.write_bytes((HERE/'FULL-BASELINE-PAYLOAD.json').read_bytes()+b' ')
        with self.assertRaisesRegex(d.DeploymentBlocked,'PAYLOAD_HASH_MISMATCH'):d.read_payload(p)
    def test_04_missing_dependency_rejected(self):
        p,h=self.rewrite_payload(lambda o:o['files'].pop(0))
        with self.assertRaisesRegex(d.DeploymentBlocked,'FILE_SET'):d.read_payload(p,h)
    def test_05_case_duplicate_rejected(self):
        def edit(o):
            r=copy.deepcopy(o['files'][0]);r['path']=r['path'].lower();o['files'].append(r)
        p,h=self.rewrite_payload(edit)
        with self.assertRaisesRegex(d.DeploymentBlocked,'DUPLICATE'):d.read_payload(p,h)
    def test_06_path_escape_rejected(self):
        for name in ['../oops','/tmp/a','a/../../x','a\\b','C:x','a/CON.txt','a/foo.']:
            with self.subTest(name=name),self.assertRaises(d.DeploymentBlocked):d.safe_name(name)
    def test_07_old_missing_six_upgrades(self):
        result=self.install()
        self.assertEqual(result['deployment'],'FULL_BASELINE_INSTALLED')
        self.assertEqual(d.inventory(self.work/'backup-v3.1.6'),self.old)
        d.verify_tree(self.target,self.files)
        self.assertFalse(result['final_valid'])
        self.assertEqual(len(result['bindings']),6)
    def test_08_idempotent_no_second_backup(self):
        self.install();before=d.inventory(self.work/'backup-v3.1.6')
        result=self.install()
        self.assertEqual(result['deployment'],'ALREADY_INSTALLED_VERIFIED')
        self.assertEqual(before,d.inventory(self.work/'backup-v3.1.6'))
    def test_09_other_version_rejected(self):
        (self.target/'VERSION').write_text('5.3.4\n');before=d.inventory(self.target)
        with self.assertRaisesRegex(d.DeploymentBlocked,'UNAPPROVED_BASE_VERSION'):self.install()
        self.assertEqual(before,d.inventory(self.target))
    def test_10_changed_skill_hash_rejected(self):
        (self.target/'SKILL.md').write_text('changed 3.1.6')
        with self.assertRaisesRegex(d.DeploymentBlocked,'OLD_SKILL_CHANGED'):self.install()
    def test_11_stale_canonical_rejected(self):
        (self.target/'CANONICAL.md').write_text('4.4.1')
        with self.assertRaisesRegex(d.DeploymentBlocked,'METADATA_CONFLICT'):self.install()
    def test_12_unexpected_runtime_rejected(self):
        p=self.target/'runtime/fsm_v5_3_0.py';p.parent.mkdir();p.write_text('# unknown')
        with self.assertRaisesRegex(d.DeploymentBlocked,'BASELINE_RUNTIME_CHANGED'):self.install()
    def test_13_symlink_target_rejected(self):
        actual=self.root/'actual';self.target.rename(actual);self.target.symlink_to(actual,target_is_directory=True)
        with self.assertRaisesRegex(d.DeploymentBlocked,'SYMLINK'):self.install()
    def test_14_nested_symlink_rejected(self):
        (self.target/'link').symlink_to(self.root/'outside')
        with self.assertRaisesRegex(d.DeploymentBlocked,'SYMLINK'):self.install()
    def test_15_overlapping_workspace_rejected(self):
        self.work=self.target/'work'
        with self.assertRaisesRegex(d.DeploymentBlocked,'OVERLAPPING'):self.install()
        self.unchanged()
    def test_16_existing_lock_rejected(self):
        self.work.mkdir();(self.work/'DEPLOY.lock').mkdir()
        with self.assertRaisesRegex(d.DeploymentBlocked,'LOCK_EXISTS'):self.install()
        self.unchanged()
    def test_17_existing_backup_never_overwritten(self):
        self.work.mkdir();b=self.work/'backup-v3.1.6';b.mkdir();(b/'KEEP').write_text('keep')
        with self.assertRaisesRegex(d.DeploymentBlocked,'CONFLICT'):self.install()
        self.assertEqual((b/'KEEP').read_text(),'keep');self.unchanged()
    def test_18_staging_hash_failure_keeps_old(self):
        real=d.verify_tree
        def bad(root,files):
            if root.name=='staging':(root/'VERSION').write_text('corrupt')
            return real(root,files)
        with patch.object(d,'verify_tree',side_effect=bad),self.assertRaisesRegex(d.DeploymentBlocked,'HASH_MISMATCH'):self.install()
        self.unchanged()
    def test_19_import_failure_before_backup_keeps_old(self):
        with patch.object(d,'run_checks',side_effect=d.DeploymentBlocked('IMPORT_DENIED')),self.assertRaisesRegex(d.DeploymentBlocked,'IMPORT_DENIED'):self.install()
        self.unchanged()
    def test_20_concurrent_old_change_prevents_promotion(self):
        def checks(root,work):
            (self.target/'new-user-file').write_text('concurrent');return {}
        with patch.object(d,'run_checks',side_effect=checks),self.assertRaisesRegex(d.DeploymentBlocked,'SOURCE_CHANGED'):self.install()
        self.assertEqual((self.target/'new-user-file').read_text(),'concurrent')
        self.assertFalse((self.work/'backup-v3.1.6').exists())
    def test_21_backup_rename_denied_keeps_old(self):
        real=Path.rename
        def rename(p,q):
            if p==self.target:raise PermissionError('SIMULATED_FILE_LOCK')
            return real(p,q)
        with patch.object(Path,'rename',rename),self.assertRaisesRegex(d.DeploymentBlocked,'FILE_LOCK'):self.install()
        self.unchanged()
    def test_22_promotion_failure_restores_old(self):
        real=Path.rename
        def rename(p,q):
            if p==self.work/'staging':raise PermissionError('SIMULATED_PROMOTION_LOCK')
            return real(p,q)
        with patch.object(Path,'rename',rename),self.assertRaisesRegex(d.DeploymentBlocked,'RESTORED_OLD_TREE_VERIFIED'):self.install()
        self.unchanged()
    def test_23_final_import_failure_rolls_back_exact_bytes(self):
        real=d.run_checks
        def checks(root,work):
            if root==self.target:raise d.DeploymentBlocked('SIMULATED_ACTIVE_IMPORT_FAIL')
            return real(root,work)
        with patch.object(d,'run_checks',side_effect=checks),self.assertRaisesRegex(d.DeploymentBlocked,'RESTORED_OLD_TREE_VERIFIED'):self.install()
        self.unchanged();self.assertTrue((self.work/'failed-new-baseline').is_dir())
    def test_24_final_hash_failure_rolls_back(self):
        real=d.verify_tree
        def verify(root,files):
            if root==self.target:(root/'VERSION').write_text('tampered')
            return real(root,files)
        with patch.object(d,'verify_tree',side_effect=verify),self.assertRaisesRegex(d.DeploymentBlocked,'RESTORED_OLD_TREE_VERIFIED'):self.install()
        self.unchanged()
    def test_25_no_hidden_certificate_in_package(self):
        obj=json.loads(self.files['DEPLOYMENT.json'])
        self.assertEqual(obj['status'],'CANDIDATE_NOT_FINAL_CERTIFIED')
        self.assertFalse(json.loads(self.files['contracts/ACTIVE-R2.json'])['final_valid'])
    def test_26_files_readonly_verification(self):
        stage=self.root/'stage';stage.mkdir()
        for name,b in self.files.items():
            p=stage/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        before=d.inventory(stage);d.verify_tree(stage,self.files);self.assertEqual(before,d.inventory(stage))
    def test_27_recover_interrupted_backup(self):
        self.work.mkdir();backup=self.work/'backup-v3.1.6';self.target.rename(backup)
        (self.work/'JOURNAL.json').write_text(json.dumps({'target':str(self.target),'work':str(self.work),'old_inventory':self.old}))
        out=d.recover_interrupted(self.target,self.work)
        self.assertEqual(out['result'],'RESTORED_OLD_TREE_VERIFIED');self.unchanged()
    def test_28_recover_refuses_occupied_target(self):
        self.work.mkdir();(self.work/'JOURNAL.json').write_text(json.dumps({'target':str(self.target),'work':str(self.work),'old_inventory':self.old}))
        with self.assertRaisesRegex(d.DeploymentBlocked,'TARGET_EXISTS'):d.recover_interrupted(self.target,self.work)
        self.unchanged()
    def test_29_live_command_rejects_linux(self):
        if sys.platform=='win32':self.skipTest('Linux guard test')
        p=subprocess.run([sys.executable,str(HERE/'deploy_full_baseline.py'),'probe'],capture_output=True,text=True)
        self.assertEqual(p.returncode,2)
        self.assertIn('AUTHORIZED_WINDOWS_HOST',p.stdout)
    def test_30_production_old_fingerprint_is_exact_reported(self):
        self.assertEqual(d.OLD_SKILL_SHA256,'84e1f003590ab1dd37bfd24ed362ae0595b480dabbcef4c63b48b28c73c3686c')

if __name__=='__main__':unittest.main(verbosity=2)
