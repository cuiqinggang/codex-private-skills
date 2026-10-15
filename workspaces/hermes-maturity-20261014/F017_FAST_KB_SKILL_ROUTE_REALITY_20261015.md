# Hermes F017｜简洁Codex技能检索快路：单样本有效候选KEEP
2026-10-15 | HERMES-ECO-20261014 | 《三人行》第2版项目级使用 | V6 C通道 | Hermes母技能v2.0。
完整虚冻结：F017_FAST_KB_SKILL_ROUTE_VIRTUAL_FREEZE_20261015.md。性质：一项完整虚拟成熟后的一次隔离Reality，不是大量重复碰运气。

## 相同任务要求与现实路径差异
任务与F016相同：用户要求Windows PowerShell 5.1脚本变更前的成熟执行计划，需明确(1)锁定PS5.1并Parser/compat gate、(2)原字节备份+编码BOM与原子替换、(3)独立真实复验输出/退出码；均只规划，不修改或执行实际脚本。
F016策略在本项目先读KB完整INDEX/ROUTING/skills-index、搜索42处候选、再读三份Codex SKILL.md；模型进程exit0、runtime202.49s，三类质量门通过。
F017仅改变成熟资料路由，在相同已冻结KB路径下直接原生search_files查询skills-index局部，不重读已确认的全局INDEX/ROUTING；从候选选出唯一覆盖全部三质量门的powershell-reliability-guard，真实read_file精确C盘Codex技能SKILL.md（72行），不加载另两个不必要技能。已获取真实search_files返回200、read_file返回200的工具事实，并独立知道该真实技能的规则；答复列出完整三质量门，未执行任何脚本、未访问凭据、未修改文件。
正式CLI exit0、process runtime91.82s。两轮进程墙钟样本差202.49-91.82=110.67s，F017单样本较短；质量范围和Provider/Model相同，但API尾延迟随机、缓存不同，**不得**用这一轮直接宣称稳定减少54.7%或物理T*。

## 虚实收敛决定
F017保留为REALITY_OBSERVED_CANDIDATE / KEEP_FAST_PATH：此路径更少文件/模型检索，且F017同等任务质量有效；只在节点已有有效知识索引Freeze与强明确意图时使用，意图模糊或技能不覆盖需求时回退全链校验。停止继续逐点测；不为追求速度删除验收门。
已在原Hermes母技能 references/CODEX-KB-ON-DEMAND-20261015.md 新增F017快路并把后续标准流程第2条改为'只在索引来源未冻结/意图不明确/冲突时回完整INDEX+ROUTING'。改前本机只在C盘复制引用文档到 C:/Users/A/.hermes/backups/hermes-f017-kb-fast-path-20261015.md，备份SHA与原文匹配；编辑通过实际文件回读。未重建索引或复制Codex218份技能，不修改Hermes模型/代理/Windows系统/旧F002源。

## 本次局部认证边界与未完成
F013原生技能发现72→171及两个skill_view当前PASS；F014真实跨Codex/Knowledge按需文件读取、mother skill_view reference、KB健康全PASS；F016自然意图→三技能深检索PASS；F017快路单样本候选有效，但稳定性与真正完整T_VALID的重现分布未认证。
F015当前Chrome无已知9222 CDP而不能安全附着现有标签页，GUI聊天待验；旧F011一条YAML疑似凭证模式告警仍未安全解决，静态全包仍FAIL；音视频、会话重启、冷开机、综合连续5轮0/5、7–14日持续观察均未完成，FINAL_VALID=NO。
