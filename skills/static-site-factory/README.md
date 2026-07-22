# Static Site Factory Skill V1.0

这是一个“静态网站总路由与交付技能”，用于连接现有的网站设计、网页克隆和 URL 转代码技能。

## 安装原则

- 不覆盖任何现有 Skill；
- 默认先 dry-run；
- 正式复制到 C 盘运行 Skills；
- 知识条目写入 K 盘知识库；
- 实际路径不一致时先改参数；
- 安装后仍需在你的本机完成三轮真实验证。

## Dry-run

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

## 确认路径后安装

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -RuntimeSkills "C:\AI\skills" -KnowledgeRoot "K:\AI\knowledge-brain" -Apply
```
