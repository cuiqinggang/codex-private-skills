# 更新和验证规则

## 更新顺序

1. 先确认用户是否要更新整包、某一级、某个主题，还是只替换失效链接。
2. 保持名称为 `AI学习资料包`。
3. 保持视频优先、文字备用。
4. 每个学习点尽量保留至少 2 个视频链接和 2 个文字链接。
5. 新链接要比旧链接更适合普通人学习，否则不要替换。
6. 同步更新微信版文档、skill reference、H 盘副本。

## 链接筛选规则

优先级：

1. 官方文档、官方帮助中心、官方教程。
2. 稳定开源项目或公开课程。
3. B站等主流视频平台上容易看懂的视频。
4. 搜索页可以作为备用视频入口，但如果找到稳定单视频，优先替换成单视频。

避免：

1. 需要复杂登录才能看的资料。
2. 标题党、营销味重、只卖课不讲内容的页面。
3. 过时工具教程。
4. 不适合中文普通用户理解的资料。

## 验证命令

验证 skill：

```powershell
python "C:\Users\A\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "C:\Users\A\.codex\skills\ai-learning-material-pack"
```

提取文档里的链接：

```powershell
Select-String -Path "C:\Users\A\Desktop\1\output\ai-learning-material-pack\AI学习资料包.md" -Pattern 'https?://\S+' -AllMatches |
  ForEach-Object { $_.Matches.Value }
```

## 自动验证注意

B站、WPS、Kimi、部分国内平台可能限制自动请求。自动请求失败时，不要直接删除链接，先人工打开确认，或等用户反馈。

## H 盘副本

默认保存位置：

```text
H:\Hermes_Skills\AI学习资料包
```

同步内容：

1. 微信可发送版资料包。
2. 讨论总结和后续计划。
3. 链接验证记录。
4. Codex skill 副本。
