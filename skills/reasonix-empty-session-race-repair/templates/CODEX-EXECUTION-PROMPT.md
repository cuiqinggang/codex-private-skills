# Codex 执行模板

角色：执行器，不是补丁决策者。

流程：

1. 只读复核 GPT 指定的源文件/函数。
2. 生成最小 diff。
3. 生成回归测试。
4. 执行允许的测试。
5. 通过专用 AI 浏览器把证据提交 GPT。
6. 等 GPT 返回 APPROVE + DEPLOYMENT_AUTHORIZED=YES。
7. 生成：
   - hotfix bundle
   - original bundle backup
   - source patch
   - SHA-256
8. 安装目录写入若被主机策略阻止：立即停止，不绕过策略。
9. 保存交付物，由用户普通 PowerShell 执行已审核的单文件替换。
10. 部署后进行 UI 验收。

专用浏览器：

```text
playwright-native-ai-browser
REUSE_EXISTING_OWNER=True
SECOND_OWNER=False
NEW_PROFILE=False
ISOLATED=False
CDP=False
```
