# Expert Learning Synapse Skill 安装与使用说明

## 用途
这是一个给 Codex / Kilo / Claude Code 类工具使用的“专家组学习技能包”。
核心方法是：项目牵引 + AI 导师 + 递归补知识 + 作品验收。

## 推荐放置位置
按你的本地习惯，可以放到：

```text
K:\AI\skills\expert-learning-synapse-skill
```

或 Codex 技能目录，例如：

```text
C:\Users\A\.codex\skills\expert-learning-synapse-skill
```

如果你当前系统已统一使用 K 盘知识脑与技能盘，优先放：

```text
K:\AI\skills\expert-learning-synapse-skill
```

## 使用方式
在 Codex 里直接粘贴：

```text
启动 Expert Learning Synapse Skill。
我要学习【主题】。
我的目标是【目标】。
我的基础是【基础】。
时间限制是【时间】。
请用“项目牵引 + 专家组 + 递归补知识 + 作品验收”的方式教我。
不要泛泛讲课，每一步都要能操作、能检查、能产出。
```

## 最短触发语

```text
启动专家学习技能包：我要用 7 天学会【主题】，最终做出【作品】。
```

## 文件说明
- `SKILL.md`：核心技能说明，给 Codex 读取。
- `commands/启动命令.md`：可直接复制的启动提示词。
- `templates/学习计划模板.md`：学习计划输出模板。
- `templates/递归补知识模板.md`：卡点解释模板。
- `templates/项目牵引模板.md`：项目式学习模板。
- `checklists/验收清单.md`：判断是否真的学会。
- `examples/示例_学习Python本地搜索工具.md`：示范用法。
