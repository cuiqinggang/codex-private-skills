# 1344 Virtual-99（虚拟99）最终结果

状态：PASS

唯一冻结方案：WIN1344-NARROW-SESSION-CWD-v1

结论：
只改变 Codex workspace-write **会话级 CWD（工作目录）**：
C:\Users\A → C:\Users\A\playwright-browser-automation5-final-reality-competition-work

Virtual-99 依据：
1. Reality Anchor：1344 已 3/3 稳定复现；
2. Microsoft：1344 对 TokenDefaultDacl 表示安全信息存储空间不足；
3. Codex 0.155.1 精确源码：USERPROFILE write root 会展开为大量一级子目录；当前 active write roots 逐个形成 capability SID；所有 capability SID 继续进入默认 DACL；
4. OpenAI Codex 公开现实复现：home session CWD 会触发大量 write roots/1344，窄项目 session CWD 可消除；
5. 24/24 虚拟门禁通过；
6. 9 个候选中只有 H1 同时满足：单因素、保留 workspace-write、保留 sandbox、无系统持久修改、直接命中根因、可立即回滚。

明确排除：
清 cap_sid、改 ACL、切 elevated/unelevated、改 approval、read-only、danger-full-access、降级 0.154、切 WSL。

本 PASS 只表示“方案已虚拟成熟并冻结”；Reality Verify（现实验证）仍必须由 Codex 按 REAL-VERIFY-COMMAND.md 确定性执行。
