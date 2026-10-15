# F013｜Hermes 活动Profile技能目录差分：实际修复验收 PASS
2026-10-15｜任务 HERMES-ECO-20261014｜方法《三人行》V2｜C桥V6｜Hermes现有母技能v2.0。
前置虚冻结：F013_PROFILE_SKILL_ROOT_FIRST_DELTA_FREEZE_20261015.md。

## First delta
当前 Hermes 解释器 get_hermes_home() 实际 `C:/Users/A/AppData/Local/hermes`，活动技能目录其下`skills/`；之前部署的自定义 Hermes 技能在`C:/Users/A/.hermes/skills`。活动配置 `skills.external_dirs=[]`；原生 skills_list 只72项，母技能及Repair技能均缺，skill_view返回 not found。故障属于活动Profile技能根扫描缺口，不是文件丢失、API认证或模型能力失效。

## 最小官方修复
先用 `hermes config path` 只读获取活动配置路径 `C:/Users/A/AppData/Local/hermes/config.yaml`；没有读取或输出配置正文、密钥或.env。
在本机仅备份该文件至 `C:/Users/A/.hermes/backups/hermes-f013-skills-home-20261015/config-before.yaml`，备份源字节SHA相同（TRUE）；修改前SHA256=`43526513F6B780ABA2D25FA7B54C6032A510DA9474FC104C79BDB69BF2B5AC2B`。备份没有上传GitHub。
经Hermes官方 `config set skills.external_dirs '["C:/Users/A/.hermes/skills"]'` 只更新这一项；官方 `config get skills.external_dirs`回读确认目录。没有移动旧技能或重装。

## 单次新Hermes会话 Reality
正常已验证 CLI wrapper 一次真实调用：原生 `skills_list` success=true, count=171, categories=15（修前72，独立可发现条目+99，不能当文件复制数）；
原生 `skill_view` 对 `hermes-mature-supertool` success=true/readiness_status=available，确认母版本v2.0和F011 CLI-first指令；
原生 `skill_view` 对 `hermes-repair-loop-adapter` success=true/readiness_status=available，确认v2.0和最多3轮Repair；
CLI exit0，进程runtime35.19秒。只读验证，无额外业务重派、无凭据访问、无安装。

## 保留界限
F013 才证明当前Hermes自有技能目录原生可发现及按需加载，不能把171条写成171条都能在所有环境完成业务。Codex目录C:/Users/A/.codex/skills尚未加入 external_dirs；其218份SKILL.md和Knowledge Brain632份文件未自动接入原生索引，需要另设安全的按需检索。官方提醒 external_dirs 是可读写引用，不是安全只读边界，不应不审查就暴露Codex原技能给自动改写工具。
此前F011静态包检查仍有一条YAML秘密模式告警，未泄露正文；整站 FINAL_VALID=NO、原F002五轮综合认证0/5，GUI、音视频、长期稳定待独立完成。
官方机制：https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
