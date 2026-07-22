import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestOffline(unittest.TestCase):
 def test_runtime_has_no_external_dependency(self): self.assertEqual(0,subprocess.run([sys.executable,str(ROOT/'scripts/check_external_dependency.py')]).returncode)
if __name__=='__main__':unittest.main()

