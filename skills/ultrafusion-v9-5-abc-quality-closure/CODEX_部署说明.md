# Codex 部署说明｜只部署，不重写

## 固定配置

```text
运行位置：完整临时副本或独立Git Worktree
原版修改：禁止
自动merge：禁止
自动push：禁止
核心提示词重写：禁止
HTML开发：本轮禁止
```

## Codex必须执行

1. 解压本技能包到独立目录。
2. 运行 `python scripts/self_test.py`。
3. 确认输出 `overall = PASS`。
4. 使用 `install_skill.ps1` 将整个技能目录复制到用户指定的 Codex skills 目录。
5. 使用 `deploy_desktop_template.ps1` 将已经生成好的 0号与1号模板复制到桌面或用户指定目录。
6. 对部署前后的 `MANIFEST_SHA256.txt` 进行核验。
7. 输出部署路径、备份路径、自测试结果和哈希结果。

## Codex不得执行

- 不得根据自己的理解重新写 A、B、C 提示词；
- 不得替换评分权重；
- 不得把 A 提示词拆成 GPT/Qwen/DeepSeek 三个不同版本；
- 不得将 A_Initial 暴露给 A、B、C；
- 不得为“方便”删除 Raw、Final、压力记录或回退标记；
- 不得增加英文版；
- 不得自动开始真实测试。

## 推荐命令

```powershell
python .\scripts\self_test.py

powershell -ExecutionPolicy Bypass -File .\install_skill.ps1 `
  -Destination "C:\AI\skills\ultrafusion-v9.5"

powershell -ExecutionPolicy Bypass -File .\deploy_desktop_template.ps1 `
  -Destination "$([Environment]::GetFolderPath('Desktop'))\UltraFusion_V9.5.1_ABC运行母版_RC2"
```

## 部署完成状态

只有以下全部满足才可写：

```text
V95_SKILL_DEPLOY_PASS
```

- 自测试通过；
- 必需文件齐全；
- 禁止项为0；
- A统一提示词镜像一致；
- 部署后哈希与清单一致；
- 旧版本未修改。

真实质量仍必须写：

```text
V95_RUNTIME_QUALITY_PENDING
```
