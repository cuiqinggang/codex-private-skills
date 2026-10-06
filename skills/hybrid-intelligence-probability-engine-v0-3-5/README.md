# 混合智能概率引擎 v0.3.5 — 简洁生产成熟版

STATE=FULLY_SEALED
FREEZE_ID=HIPE-v0.3.5-FULLY-SEALED-20261006-R1

本目录是用户授权保存到共同工作区的 v0.3.5 冻结副本。
原正式包 14 个文件逐字节保存，freeze/ 保存已有封存包与完整清单。
原 release notes 中 13/13 发布哈希匹配，完整正式包/冻结 ZIP 14/14。

## 网上与本地位置

- 共同私库：cuiqinggang/codex-private-skills
- 网上目录：https://github.com/cuiqinggang/codex-private-skills/tree/main/skills/hybrid-intelligence-probability-engine-v0-3-5
- 使用入口：[SKILL.md](SKILL.md)
- 发布状态：[CURRENT_STATE.json](CURRENT_STATE.json)
- 文件清单：[SHA256-MANIFEST.json](freeze/SHA256-MANIFEST.json)
- 冻结 ZIP：[HIPE-v0.3.5-FROZEN.zip](freeze/HIPE-v0.3.5-FROZEN.zip)
- 本地正式源：`C:\Users\A\Documents\Codex\2026-09-29\5-hipe-v0-3-5-01\outputs\hipe-v0.3.5`
- 本地封存目录：`C:\Users\A\Documents\Codex\2026-10-06\v0-3-5-x20\outputs\HIPE-v0.3.5-FROZEN-20261006`

## 冻结约束

禁止原地编辑、替换或隐式升级本冻结版本。需要变更时返回 NEEDS_VERSIONED_UPGRADE，另建版本。
使用前验证清单；不同版本/旧 v0.3.0 不得覆盖本冻结基线。
本次仅保存已验证的冻结资产，没有重跑引擎远端认证，不扩大原有常用场景 21/21 的认证范围。
冻结是版本治理和哈希证据，不宣称管理员不可修改的文件系统锁。

freeze/ 中原《定位与冻结记录》保留首次封存时的历史措辞（当时尚未上传）；
本 README 及本次远端保存回执补充当前保存事实，不修改已封存历史文件。

【页面名1｜任务名1｜序号1】

## 网上副本核验

在本目录运行 `python -B verify_cloud.py`，核验正式文件、ZIP 和封存附件。
冻结记录：[location-and-freeze.md](freeze/location-and-freeze.md)；长期定位条目：[durable-location-note.md](freeze/durable-location-note.md)。
这两份元数据使用英文文件名，内容保持原字节；原本地封存回执中的中文名称通过 verify_cloud.py 中的固定映射核对。
