# Codex 部署说明｜RC3增量集成、只读网站与不重写边界

## 固定配置

```text
运行位置：完整临时副本或独立Git Worktree
原版修改：禁止
自动merge：禁止
自动push：禁止
核心提示词重写：禁止
HTML能力验证执行器：仅允许在RC3候选中精确集成和修复，不得加入模型API或后台
```

## Codex必须执行

1. 冻结RC2全目录清单和核心提示词哈希，并复制到独立RC3候选目录。
2. 把 `A关能力形成与证据闭环_RC3/` 增量模块加入候选。
3. 将模块内增量运行规则精确插入RC3 `SKILL.md`，并保留前后差异。
4. 从正式A提示词源创建逐字节只读网站镜像，记录路径、字符数、字节数和SHA-256。
5. 运行增量包自测试、核心技能自测试、Good/Bad独立验证和站点构建。
6. 对最终RC3 ZIP做冷启动解压复核。
7. 只把通过构建的站点发布为私有Codex站点。
8. 输出集成前后对比、哈希、L3状态和真实测试前报告。

原RC2的既有部署步骤仍可用于RC2本身：

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
- 不得把模拟10/10写成真实质量通过；
- 不得在L3阶段输出 `FREEZE｜冻结为正式能力`。

## 推荐命令

```powershell
python .\scripts\self_test.py

powershell -ExecutionPolicy Bypass -File .\install_skill.ps1 `
  -Destination "C:\AI\skills\ultrafusion-v9.5"

powershell -ExecutionPolicy Bypass -File .\deploy_desktop_template.ps1 `
  -Destination "$([Environment]::GetFolderPath('Desktop'))\UltraFusion_V9.5.1_ABC运行母版_RC2"
```

## RC3候选集成完成状态

只有以下全部满足才可写：

```text
V95_RC3_STATIC_INTEGRATION_PASS
UF951_A_CAPABILITY_L3_SIMULATION_VALIDATED
```

- 自测试通过；
- 必需文件齐全；
- 禁止项为0；
- A统一提示词镜像一致；
- 部署后哈希与清单一致；
- 旧版本未修改。
- A关能力来源模块完整；
- 站点正式源只读镜像哈希一致；
- 当前成熟度保持L3；
- 私有站点版本1部署成功，10/10站点系统测试通过；
- 下一关口为L4 GPT三题真实烟雾测试。

真实质量仍必须写：

```text
V95_RUNTIME_QUALITY_PENDING
```
