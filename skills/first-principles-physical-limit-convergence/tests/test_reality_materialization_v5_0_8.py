import os, sys

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CAPSULE = os.path.join(ROOT, "docs", "first-principles", "v5.0.8", "REAL-CAPSULE-SOURCE-R2.py")

with open(CAPSULE, "r", encoding="utf-8") as f:
    source = f.read()

assert source.isascii()
for enc in ("ascii", "utf-8", "cp1252", "latin-1"):
    assert source.encode(enc).decode(enc) == source

ns = {}
compiled = compile(source, CAPSULE, "exec")
exec(compiled, ns, ns)
fn = ns.get("run_reality_certificate")
assert callable(fn)
result = fn()
assert len(result) == 18
assert all(ok for _, ok in result)

print("ASCII_ONLY_CAPSULE=PASS")
print("MULTI_ENCODING_ROUNDTRIP=PASS")
print("FRESH_NAMESPACE_MATERIALIZATION=PASS")
print("REALITY_CERTIFICATE=18/18 PASS")
