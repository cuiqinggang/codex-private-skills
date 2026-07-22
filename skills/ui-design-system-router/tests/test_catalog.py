import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestCatalog(unittest.TestCase):
 def test_archetypes(self): self.assertEqual(15,len(json.loads((ROOT/'catalog/archetypes.json').read_text(encoding='utf-8'))))
 def test_catalog(self): self.assertGreaterEqual(len(json.loads((ROOT/'catalog/catalog.json').read_text(encoding='utf-8'))),70)
if __name__=='__main__':unittest.main()

