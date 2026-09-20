# 1344 成熟方案集群证据

## 当前现实
- Codex CLI：0.155.1
- Windows 沙盒：unelevated（非提升型）
- Reality CWD（现实会话工作目录）：C:\\Users\\A
- 失败：SetTokenInformation(TokenDefaultDacl) → 1344
- 重复：3/3
- 子进程：未成功启动

## 成熟外部证据

### OpenAI Codex #36328
同类 Windows 1344。用户主目录作为 session CWD（会话级工作目录）时，sandbox setup 会枚举大量 write roots（可写根）；窄项目目录可消除 1344。公开报告还明确指出，改变单条工具调用的 workdir 不等于改变 session CWD。

https://github.com/openai/codex/issues/36328

### OpenAI Codex #26438
1344 在 elevated / unelevated 两种 Windows 沙盒后端均可发生；read-only（只读）和 danger-full-access（完全访问）只是绕过 workspace-write 的 writable default DACL（可写默认访问控制列表），不能作为生产级最小修复。

https://github.com/openai/codex/issues/26438

### Microsoft
1344 = ERROR_ALLOTTED_SPACE_EXCEEDED；对于 TokenDefaultDacl，STATUS_ALLOTTED_SPACE_EXCEEDED 表示默认 DACL / 主组存储空间不足。

https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--1300-1699-
https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-zwsetinformationtoken

## Codex 0.155.1 精确源码闭环

Tag：rust-v0.155.1
Commit：be2951ea34f0d295ed0becf97079f92fa5f6950e

1. setup.rs：如果 write root 等于 USERPROFILE（用户主目录），expand_user_profile_root 会把它展开成用户目录下大量一级子路径。
2. spawn_prep.rs：root_capability_sids 只为当前 active roots（当前有效可写根）建立 SID。
3. token.rs：所有当前 capability SIDs（能力 SID）进入 CreateRestrictedToken，并继续进入 set_default_dacl。
4. set_default_dacl 调用 SetTokenInformation(TokenDefaultDacl)。

因此当前 Reality（现实）满足完整因果链：

C:\\Users\\A 作为宽 workspace/session root
→ USERPROFILE 展开
→ 当前 write roots 数量放大
→ capability SID 数量放大
→ TokenDefaultDacl 条目放大
→ SetTokenInformation
→ 1344

## 结论
唯一第一硬化方案不是清 cap_sid、改 ACL、改 sandbox、改 approval、降版本或切 WSL。

唯一最小变化是：

**把 Codex workspace-write 会话级 CWD 从用户主目录改为窄的真实项目目录。**

必须是 session CWD（会话级工作目录），不能只改某一条命令的 workdir。
