【整体闭环极限时间引擎5.0.2版｜v5.0.2虚拟成熟现实认证｜05-05｜实】 极限锚00:00.002

本次只认 05-05-R2 完整冻结。05-05-R1 已在 REAL_START 前被更低 T* 的确切字节复测结果取代，不得使用。

权威共同私库：
https://github.com/cuiqinggang/codex-private-skills

权威分支：
codex/first-principles-physical-limit-convergence-v5.0.2-virtual-freeze

1. 读取唯一完整 Freeze：
docs/first-principles/v5.0.2/FREEZE-MANIFEST-05-05-R2.json
期望 blob：
4197518fcd2334c27a5d3fa91280540ba04b8efb

2. 读取发布后冻结一致性收据：
docs/first-principles/v5.0.2/FREEZE-CONSISTENCY-REPORT-05-05-R2.json
期望 blob：
47e619072f6706064b84416cf67a41e47c52c02c

必须确认：
asset_count=11
post_publish_reread_count=11
mismatches=[]
FREEZE_MANIFEST_CONSISTENT=PASS

3. 读取确切字节虚拟证明：
docs/first-principles/v5.0.2/VIRTUAL-EXACT-PROOF-05-05-R2.json
期望 blob：
2eaa2ded44b91c775110927e63d25903e6907d02

必须确认：
capsule blob=aec8e3addd54b677ced8843db60774841623924b
capsule SHA256=4baf7d00c1921cd85bf8117d325e22772a1372e6946750045504befc1c9881ee
run_verifier=66745/66745 PASS
run_reality_certificate=62/62 PASS

4. 读取执行合同：
docs/first-principles/v5.0.2/REAL-EXECUTION-CONTRACT-05-05-R2.json
期望 blob：
6e8496fd8edbab5e795409f508cf6939d53976d5

5. 读取完整 Reality Capsule 源码正文：
docs/first-principles/v5.0.2/REAL-CAPSULE-SOURCE-05-05.py
期望 blob：
aec8e3addd54b677ced8843db60774841623924b
期望 SHA-256：
4baf7d00c1921cd85bf8117d325e22772a1372e6946750045504befc1c9881ee

源码物化：
- 获取完整 UTF-8 源码正文。
- 建立一个 fresh Python namespace，__name__='remote_capsule'。
- 在同一个 namespace 中 compile + exec 完整源码。
- 先确认：
  callable(namespace.get('run_verifier')) == True
  callable(namespace.get('run_reality_certificate')) == True

完整 Freeze、blob、SHA-256、虚拟全量证明全部一致以后：
- 不运行 run_verifier() 的 66745 项穷举；它已经是该确切 blob 的冻结虚证明。
- Reality 只运行 namespace['run_reality_certificate']()。
- 紧贴调用前记录 REAL_START。
- 成功返回后立即记录 REAL_END。
- T_VALID_REAL_MS=(REAL_END-REAL_START)/1_000_000。

Reality Certificate 必须返回：
TOTAL=62
PASS=62

05-05-R2 目标 Windows 极限锚：
T*=2.266199101 ms

该值来自：
GPT 确切 blob 证书最短时间 0.475232 ms
×
05-04 已实测 Windows/GPT 同类全量 verifier 比率 4.768616382444736

只有以下全部成立才允许 REAL_PASS：
FREEZE_MANIFEST_CONSISTENT=PASS
EXACT_CAPSULE_BLOB_MATCH=YES
EXACT_CAPSULE_SHA256_MATCH=YES
EXHAUSTIVE_VIRTUAL_PROOF=66745/66745 PASS
REALITY_CERTIFICATE=62/62 PASS
EVIDENCE_CONSISTENT=YES
T_VALID_REAL_MS<=2.266199101

GitHub 正常可访问时，不扫描 C 盘，不要求本地预置副本。
只有 NETWORK_UNAVAILABLE、AUTH_UNAVAILABLE 或 REPOSITORY_UNAVAILABLE 才返回 REMOTE_REPO_UNAVAILABLE。

其他任何失败只返回最小 Reality Delta + STOP + RETURN_TO_GPT=YES。
禁止现场修复、修改冻结源码、改变 VALID、重新设计或直接重跑。
