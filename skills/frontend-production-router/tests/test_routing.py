import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestRouting(unittest.TestCase):
 def route(self,text):return subprocess.check_output([sys.executable,str(ROOT/'scripts/detect_task_type.py'),'--text',text],text=True,encoding='utf-8').strip()
 def test_url(self):self.assertEqual('ROUTE=clone-existing-website',self.route('克隆 https://example.com'))
 def test_new(self):self.assertEqual('ROUTE=new-product-design',self.route('为新的 AI SaaS 设计界面'))
 def test_originalize(self):self.assertEqual('ROUTE=clone-and-originalize',self.route('参考这个网站但不要照抄'))
if __name__=='__main__':unittest.main()

