# Cursor + Claude Code + DeepSeek V4 Pro 恢复检查清单

## 开工前

- [ ] 已读 `BOUNDARY-20260702.md`
- [ ] 已读 2026-07-27 完整恢复流程
- [ ] 已确认只恢复 Claude Code 工具外壳的 DeepSeek 路线
- [ ] 已确认不连接 Claude/Anthropic 官方模型
- [ ] 已核对 DeepSeek 官方 endpoint 与模型名
- [ ] 已检查 Cursor、Claude CLI、Claude Code 扩展版本
- [ ] 已运行 C 盘复用预检；未扫描 H/K

## DeepSeek 会话

- [ ] Key 通过安全输入获得
- [ ] Key 未写入日志、证明、截图或 Git
- [ ] 当前执行策略是否允许持久化已明确；不允许时使用进程级会话
- [ ] `ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic`
- [ ] `ANTHROPIC_MODEL=deepseek-v4-pro[1m]`
- [ ] 最小真实调用退出码为 0
- [ ] 返回包含 `DS_CLAUDE_CODE_OK`
- [ ] 路由证明不含 Key

## Cursor 中文化

- [ ] Cursor 版本严格匹配修复脚本支持版本
- [ ] 七项英文签名均恰好匹配一次
- [ ] 工作台 JS 和 `product.json` 已备份
- [ ] 校验和已更新
- [ ] 七项中文签名均恰好匹配一次
- [ ] Cursor 已彻底重开
- [ ] 截图可见八组中文菜单（含运行）

## Claude Code 可见验收

- [ ] Cursor 窗口句柄截图已保存
- [ ] Claude Code 页签和输入框可见
- [ ] 第一轮中文任务真实回答
- [ ] 第一轮固定标记可见
- [ ] 路由证明与 Claude Code 并排可见
- [ ] 第二轮显示 `Read` 工具调用
- [ ] 第二轮返回端点、模型、烟雾测试和官方模型禁用状态
- [ ] 第二轮固定标记可见

## 最终

- [ ] `Claude Code 工具外壳 DeepSeek V4 Pro 转接路线: PASS`
- [ ] `ACTUAL_OPEN_VERIFY_PASS`
- [ ] 失败项和回滚路径已记录
- [ ] 技能最近使用记录已更新
- [ ] 知识库条目已更新
- [ ] 秘密扫描通过
