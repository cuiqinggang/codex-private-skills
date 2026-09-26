【整体闭环极限时间引擎 4.7版2｜v5.0.2虚拟成熟现实认证｜05-03｜实】 极限锚00:00.270

本次冻结资料的权威来源是共同私有 GitHub 仓库，不要求当前工作目录或 C 盘预先存在副本。

请直接使用当前已登录/已授权的 GitHub 访问能力读取：

仓库：
https://github.com/cuiqinggang/codex-private-skills

分支：
codex/first-principles-physical-limit-convergence-v5.0.2-virtual-freeze

首先读取 05-03-R2 交接冻结清单：
docs/first-principles/v5.0.2/FREEZE-MANIFEST-05-03-R2.json
期望 blob：
c1e1e658c32ecd4b7ed7f30bd017d0a66be954c9

然后按该清单读取并核对：
1. skills/first-principles-physical-limit-convergence/SKILL.md
   blob=6a78f13217dc5e579408046924ecdedaa51dc919

2. docs/first-principles/v5.0.2/FREEZE-MANIFEST.json
   blob=052538814aed80507a155e5fe93e4ff34b261fb7

3. docs/first-principles/v5.0.2/REAL-CAPSULE-SOURCE.py
   blob=ce4d43553538580d04d80b457b7ad4f24de7f8b1
   SHA256=c7c960f74b201cf70829db9a998644f00b15dc968ca0888c4b0bdda4301f30d9

规则：
- GitHub 正常可访问时，不要扫描 C 盘寻找这些文件，也不要要求先复制到工作区。
- 只有 NETWORK_UNAVAILABLE、AUTH_UNAVAILABLE 或 REPOSITORY_UNAVAILABLE 才停止，并返回 REMOTE_REPO_UNAVAILABLE + STOP + RETURN_TO_GPT=YES。
- 读取与哈希核对通过后，执行冻结 Reality Capsule。
- 在已启动 Python 解释器内，紧贴 run_verifier() 前记录 REAL_START，成功返回后立即记录 REAL_END。
- 必须得到 65975/65975 PASS，并记录 T_VALID_REAL_MS。
- 只有 VERIFIER_PASS=YES、EVIDENCE_CONSISTENT=YES 且 T_VALID_REAL_MS<=269.560254 才可 REAL_PASS。
- 其他任何失败只返回最小 Reality Delta；禁止现场修复、改设计或直接重跑。
