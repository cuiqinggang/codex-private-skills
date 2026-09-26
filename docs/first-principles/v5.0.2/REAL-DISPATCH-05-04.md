【整体闭环极限时间引擎5.0.2版｜v5.0.2虚拟成熟现实认证｜05-04｜实】 极限锚00:00.494

本次 Reality 只认 05-04 完整冻结，不再引用 05-02 或 05-03 的任何基清单。

权威共同私库：
https://github.com/cuiqinggang/codex-private-skills

权威分支：
codex/first-principles-physical-limit-convergence-v5.0.2-virtual-freeze

第一步，读取唯一完整 Freeze：
docs/first-principles/v5.0.2/FREEZE-MANIFEST-05-04.json
期望 blob：
e830f9f6a517cd7faea45f68f11893cfc5eeb182

第二步，读取发布后冻结一致性收据：
docs/first-principles/v5.0.2/FREEZE-CONSISTENCY-REPORT-05-04.json
期望 blob：
25b7b9a60024f2f6ff834ce94178101dce7a2ad3
必须确认 asset_count=13、post_publish_reread_count=13、mismatches=[]、FREEZE_MANIFEST_CONSISTENT=PASS。

第三步，按完整 Manifest 读取执行合同：
docs/first-principles/v5.0.2/REAL-EXECUTION-CONTRACT-05-04-R2.json
期望 blob：
d95c7f1250ff87a7b1b572251683bed3212af0db

第四步，读取完整 Reality Capsule 源码正文，不是只读取文件名、路径、blob 或元数据：
docs/first-principles/v5.0.2/REAL-CAPSULE-SOURCE-05-04-R2.py
期望 blob：
f89519ee6e44c9df7032121bd6f1181a129f790e
期望 SHA-256：
723e622c923ff972c24cc3b739aac05a6e0ad69b5698f124b56ef57767aaa2ba

源码物化必须严格遵守冻结执行合同：
- 获取完整 UTF-8 源码文本。
- 建立一个新的 Python namespace，__name__ 不是 __main__。
- 将刚读取的完整源码在这个同一个 namespace 中编译并执行。
- 执行后先确认该同一 namespace 中 run_verifier 存在且 callable。
- 如果 run_verifier 不存在，立即返回 PAYLOAD_MATERIALIZATION_FAIL；不得在空 namespace 或其他 namespace 继续寻找。
- 只有确认 run_verifier callable 后，才开始 Reality 计时。
- 紧贴 run_verifier() 调用前记录 REAL_START，成功返回后立即记录 REAL_END。
- T_VALID_REAL_MS=(REAL_END-REAL_START)/1_000_000。

有效门：
- 冻结 Capsule 必须返回 66745/66745 PASS。
- VERIFIER_PASS=YES。
- EVIDENCE_CONSISTENT=YES。
- T_VALID_REAL_MS 必须 <= 493.886824。

只有全部成立才允许 REAL_PASS。

GitHub 正常可访问时，不扫描 C 盘，不要求本地预置副本。
只有 NETWORK_UNAVAILABLE、AUTH_UNAVAILABLE 或 REPOSITORY_UNAVAILABLE 才返回 REMOTE_REPO_UNAVAILABLE。
其他任何失败只返回最小 Reality Delta + STOP + RETURN_TO_GPT=YES；禁止现场修复、修改冻结源码、改设计或直接重跑。
