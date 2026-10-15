# F013｜Hermes 当前 Profile 与原技能目录不一致：最小官方修复冻结
项目 HERMES-ECO-20261014，方法《三人行》V2项目明确指定，桥V6 C→A→B，原Hermes专用 v2.0；承接 F012 已读云端冻结。

## 已观测事实
- 当前 Windows 实际 Hermes CLI `get_hermes_home()` 返回 `C:/Users/A/AppData/Local/hermes`，该目录中的 `skills/` 确有官方分组文件。
- 历史 Hermes 专项技能、母SKILL.md、Repair Loop 和大批安装资源在 `C:/Users/A/.hermes/skills/`，不是当前主Home。
- 2026-10-15 真正通过现有 Hermes CLI 调用内置 skills_list 得到72项，未发现 hermes-mature-supertool 和 hermes-repair-loop-adapter；skill_view 明确反馈 `Skill 'hermes-mature-supertool' not found.`，不是只根据 `hermes skills list --source local` 推理。
- CLI `hermes config get skills.external_dirs` 返回 `[]`，即该主 Profile 尚未登记老本地技能路径。
- Codex技能目录 `C:/Users/A/.codex/skills` 一级209目录、递归SKILL.md218份；老Hermes root一级85目录、递归SKILL.md161份；Knowledge Brain632文件（不是632项技能）。

## FIRST_DELTA
用户过去保存自定义SKILL在 `.hermes/skills`，当前正式CLI实际从 `AppData/Local/hermes/skills` 扫描，且外部技能路径为空。这足以解释大量本地技能没进入当前原生 skills_list 索引。先证明这个差分在单项技能上完全消除，再考虑更大的Codex技能接入。

## 官方成熟解
官方 https://hermes-agent.nousresearch.com/docs/user-guide/features/skills 支持在活动Profile config 中通过 `skills.external_dirs` 加入外部技能根，进而使技能进入同一 skills_list/skill_view 索引；不用搬运文件、不重装Hermes、不另造技能管理器。该接口不是安全沙箱：当外部路径可写时，Hermes的skill_manage可能写原文件。故这次只先加入**既存Hermes自有的 `.hermes/skills`**，不直接暴露Codex大库给自动写操作，Codex技能先走现有知识库只读索引按需读取，后续经安全门才决定如何完整接入。

## Reality合同
1. 使用官方 `hermes config path`确认活动配置，调用 `hermes config get skills.external_dirs`记录旧值；不读取/打印整个配置正文和凭据。
2. 在本机仅备份活动 config.yaml 原始字节到任务受控C盘备份目录，记录SHA，不上传配置。
3. 用官方 `hermes config set skills.external_dirs` 把唯一已有旧Hermes技能根作为路径数组；只改变此一个配置项，不改变 Provider/模型/FlClash/代理/浏览器/Docker。
4. 通过官方 `hermes config get skills.external_dirs` 回读；然后新一次性HermesCLI会话实际调用 skills_list/skill_view hermes-mature-supertool、hermes-repair-loop-adapter，确认 F011 的 CLI-first 规则可按需加载。启动新自然会话不要求重启Gateway或关闭OpenWebUI。
5. 必须比较配置只改变已授权键、不泄漏凭据；如果扫描返回0或异常，回虚最小分析，不自动重装、不会重复盲派模型；旧实际运行资产不变。成功只给动态技能发现这个子节点 PASS，不等于整站完成。

## 未展开的后续
Codex218 SKILL.md需单独兼容、同名冲突、技能权限和执行边界筛选；Knowledge Brain用INDEX→ROUTING_MAP→类别索引→Top-K原文件，不把632文件全部送进模型。原F011 YAML秘密扫描FAIL需用合规的只报数量审计处理，不能输出疑似密钥。整站5轮仍0/5，FINAL_VALID=NO。
