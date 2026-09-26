【整体闭环极限时间引擎 4.7版2｜v5.0.2虚拟成熟现实认证｜05-03｜实】 极限锚00:00.270

本次冻结资料的权威来源不是当前工作目录，也不是 C 盘预置文件，而是已经登录可访问的共同私有 GitHub 仓库。请直接读取以下远程冻结源，不要先在 C 盘搜索：

仓库：
https://github.com/cuiqinggang/codex-private-skills

分支：
codex/first-principles-physical-limit-convergence-v5.0.2-virtual-freeze

05-03 交接冻结清单：
docs/first-principles/v5.0.2/FREEZE-MANIFEST-05-03.json
期望 blob：
e0f69362206b584a2217d94c39f092180e4c930c

基础冻结清单：
docs/first-principles/v5.0.2/FREEZE-MANIFEST.json
期望 blob：
052538814aed80507a155e5fe93e4ff34b261fb7

冻结 Reality Capsule：
docs/first-principles/v5.0.2/REAL-CAPSULE-SOURCE.py
期望 blob：
ce4d43553538580d04d80b457b7ad4f24de7f8b1
期望 SHA-256：
c7c960f74b201cf70829db9a998644f00b15dc968ca0888c4b0bdda4301f30d9

规则：
1. 使用当前已经可用的 GitHub 登录/权限直接读取上述仓库、分支和文件。
2. 只有当 GitHub 网络不可达、当前登录无权限、或仓库/分支确实不可访问时，才停止并返回 REMOTE_REPO_UNAVAILABLE；不要因此改设计，也不要自行改为扫描 C 盘。
3. 成功读取后先核对三个 blob 和 Capsule SHA-256。
4. 核对全部通过后，在已启动的 Python 解释器内，紧贴 run_verifier() 调用前记录 REAL_START，成功返回后立即记录 REAL_END。
5. 冻结胶囊必须得到 65975/65975 PASS，并记录 T_VALID_REAL_MS。
6. 只有 VERIFIER_PASS=YES、EVIDENCE_CONSISTENT=YES 且 T_VALID_REAL_MS<=269.560254 才可 REAL_PASS。
7. 任何失败只返回最小 Reality Delta、STOP、RETURN_TO_GPT=YES；禁止现场修复、重新设计或直接重跑。
