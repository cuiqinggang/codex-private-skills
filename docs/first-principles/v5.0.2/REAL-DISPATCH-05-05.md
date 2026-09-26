【整体闭环极限时间引擎5.0.2版｜v5.0.2虚拟成熟现实认证｜05-05｜实】 极限锚00:00.002

本次 Reality 使用“证明携带式”认证。VALID 定义没有变化；完整 66745 项穷举证明已在 GPT 虚阶段绑定到确切冻结 blob，Reality 只在完整 Freeze、blob 和证明收据全部一致后运行 62 项目标环境兼容性证书。

权威共同私库：
https://github.com/cuiqinggang/codex-private-skills

权威分支：
codex/first-principles-physical-limit-convergence-v5.0.2-virtual-freeze

第一步：读取唯一完整 Freeze
docs/first-principles/v5.0.2/FREEZE-MANIFEST-05-05.json
期望 blob：
15dd55a62750980c75ca2c2bf7630b6e5f8297a3

第二步：读取发布后冻结一致性收据
docs/first-principles/v5.0.2/FREEZE-CONSISTENCY-REPORT-05-05.json
期望 blob：
7af6c614e5c5ae38e3a986507a6e23d5ebc143a6

必须确认：
asset_count=11
post_publish_reread_count=11
mismatches=[]
exhaustive_virtual_proof=66745/66745 PASS
reality_certificate_virtual_test=62/62 PASS
FREEZE_MANIFEST_CONSISTENT=PASS

第三步：读取虚阶段全量证明
docs/first-principles/v5.0.2/VIRTUAL-EXHAUSTIVE-PROOF-05-05.json
期望 blob：
241ff8712217a31199c49e036eba1355c7905cf7

第四步：读取 Reality 执行合同
docs/first-principles/v5.0.2/REAL-EXECUTION-CONTRACT-05-05.json
期望 blob：
c9a7812d9cf444f40b345fc0435be3aa86eec646

第五步：读取完整 Reality Capsule 源码正文
docs/first-principles/v5.0.2/REAL-CAPSULE-SOURCE-05-05.py
期望 blob：
aec8e3addd54b677ced8843db60774841623924b

源码物化规则：
- 必须获取完整 UTF-8 源码正文，不是文件名、路径、blob 或片段。
- 建立一个新的 Python namespace，__name__='remote_capsule'。
- 将完整源码在这个同一个 namespace 中 compile + exec。
- 执行完成后确认：
  callable(namespace.get('run_verifier')) == True
  callable(namespace.get('run_reality_certificate')) == True

完整 Freeze / blob / 全量证明全部一致时：
- 不再运行 run_verifier() 的 66745 项穷举；那是该确切 blob 的虚阶段一次性证明。
- Reality 只运行 namespace['run_reality_certificate']()。
- 紧贴调用前记录 REAL_START，成功返回后立即记录 REAL_END。
- T_VALID_REAL_MS=(REAL_END-REAL_START)/1_000_000。

Reality Certificate 必须返回：
TOTAL=62
PASS=62

05-05 的目标 Windows 极限锚：
T*=2.280776761 ms

该值不是直接照搬 GPT 本机时间；它来自：
05-04 Windows 实测 / GPT 冻结基准 = 4.768616382444736×
乘以 05-05 GPT 证书最短时间 0.478289 ms。

只有以下全部成立才允许 REAL_PASS：
FREEZE_MANIFEST_CONSISTENT=PASS
EXHAUSTIVE_VIRTUAL_PROOF=66745/66745 PASS
REALITY_CERTIFICATE=62/62 PASS
EVIDENCE_CONSISTENT=YES
T_VALID_REAL_MS<=2.280776761

GitHub 正常可访问时，不扫描 C 盘，不要求本地预置副本。
只有 NETWORK_UNAVAILABLE、AUTH_UNAVAILABLE 或 REPOSITORY_UNAVAILABLE 才返回 REMOTE_REPO_UNAVAILABLE。

其他任何失败只返回最小 Reality Delta + STOP + RETURN_TO_GPT=YES。
禁止现场修复、修改冻结源码、重新设计、改 VALID 或直接重跑。
