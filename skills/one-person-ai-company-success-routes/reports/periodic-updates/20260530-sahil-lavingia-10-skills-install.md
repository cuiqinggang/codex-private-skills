# 20260530 Sahil Lavingia 10 skills install report

运行类型：install / validation

## 目标

检查 `slavingia/skills` 的 10 个 The Minimalist Entrepreneur skills 是否已经安装到 Codex 可发现目录；如果未安装且有必要，则安装到本机 Codex skills 目录，便于后续直接触发使用。

## 安装判断

有必要安装。

原因：

- 已有 `H:\AI\skills\minimalist-entrepreneur-10-skills` 是总览型中文技能包，适合复盘和整理。
- 用户要求“可以让你直接调用”，这需要把 10 个 skill 分别安装到 Codex 的可发现目录。
- 这 10 个 skill 的触发场景不同，分别安装后更容易按 `/find-community`、`/pricing`、`/minimalist-review` 等具体任务触发。

## 安装位置

```text
C:\Users\A\.codex\skills
```

## 已安装技能

| Skill | 路径 | 校验 |
|---|---|---|
| find-community | `C:\Users\A\.codex\skills\find-community` | PASS |
| validate-idea | `C:\Users\A\.codex\skills\validate-idea` | PASS |
| mvp | `C:\Users\A\.codex\skills\mvp` | PASS |
| processize | `C:\Users\A\.codex\skills\processize` | PASS |
| first-customers | `C:\Users\A\.codex\skills\first-customers` | PASS |
| pricing | `C:\Users\A\.codex\skills\pricing` | PASS |
| marketing-plan | `C:\Users\A\.codex\skills\marketing-plan` | PASS |
| grow-sustainably | `C:\Users\A\.codex\skills\grow-sustainably` | PASS |
| company-values | `C:\Users\A\.codex\skills\company-values` | PASS |
| minimalist-review | `C:\Users\A\.codex\skills\minimalist-review` | PASS |

## 兼容修正

`minimalist-review/SKILL.md` 原始 frontmatter 带有 Claude 专用字段：

```text
argument-hint
```

Codex 的 `quick_validate.py` 不接受该字段。已只删除这个 frontmatter 字段；技能正文未改。

## 验证命令

```powershell
$validator='C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py'
$names=@('find-community','validate-idea','mvp','processize','first-customers','pricing','marketing-plan','grow-sustainably','company-values','minimalist-review')
foreach($n in $names){ python $validator "C:\Users\A\.codex\skills\$n" }
```

结果：10 个 skill 全部 `Skill is valid!`

## 使用说明

新安装的技能需要重启 Codex 后才会出现在自动发现列表中。本会话仍可按路径手动读取；后续新会话可以直接触发。

## 状态码

ONE_PERSON_AI_COMPANY_ROUTES_MINIMALIST_10_SKILLS_INSTALLED_PASS
