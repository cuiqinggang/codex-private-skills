# Codex执行命令包｜全量证据闭环修复

```text
执行平台：OpenAI Codex App for Windows 或 Codex CLI
模型：GPT-5.6 Sol（或当前可用的最强稳定编码模型）
工作强度：High
运行位置：独立Git Worktree或完整临时副本
并行：只读盘点可并行；同一文件写入禁止并行
自动merge：禁止
自动push：禁止
原版修改：禁止
失败回退：保留证据后删除候选Worktree
```

请读取并完整执行 `evidence-closed-loop-repair/SKILL.md`。

本次任务必须：

1. 根据用户明确要求建立独立 `CHANGE_CONTRACT.json`；
2. 盘点所有源文件、派生文件、生成脚本、验证脚本、母版、报告、网页、截图、文件名和嵌套压缩包；
3. 冻结原版及关键SHA-256；
4. 修正真源头和所有会重新引入旧值的生成/同步逻辑；
5. 从真源头全量重建派生物，禁止只修表面成品；
6. 对Required做100%正向验证，对Forbidden做严格0残留验证；
7. 验证派生关系、镜像字节一致和锁定哈希；
8. 使用独立验证器运行Good fixture和Bad fixture；
9. 对用户最终下载的ZIP和7z分别在全新目录冷启动解压；
10. 递归打开并验证所有嵌套包；
11. 生成截图、JSON日志、哈希清单和证据矩阵；
12. 只有E3证据完整时才允许输出 `FINAL_ARTIFACT_EVIDENCE_PASS`；
13. 真实运行质量、真实时间收益等无法静态证明的内容必须标记 `RUNTIME_VALIDATION_PENDING`；
14. 未经用户授权不得merge、push、覆盖原版或删除旧版本。

最终报告必须逐项列出：实际修改、影响链、Required计数、Forbidden计数、锁定哈希、派生/镜像结果、ZIP/7z冷启动结果、嵌套包结果、Good/Bad测试、截图路径、PENDING项和唯一下一步建议。
```
