# Codex 一键部署指令

把下面这一行交给 Codex：

```text
从 GitHub 私库 cuiqinggang/codex-private-skills 的 main 分支，把 skills/reasonix-empty-session-race-repair 保护性部署到 C:\Users\A\.codex\skills\reasonix-empty-session-race-repair；如目标已存在先完整备份，再覆盖，随后校验 SKILL.md、MANIFEST.json、VERSION=1.0.0，并只输出 DEPLOY=PASS/FAIL、BACKUP_PATH、INSTALLED_VERSION。
```

部署仅安装技能包，不修改 Reasonix 程序、用户历史、代理、网络或模型配置。
