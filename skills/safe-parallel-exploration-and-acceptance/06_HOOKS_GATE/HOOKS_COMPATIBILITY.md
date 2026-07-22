# Hooks Compatibility

复用全局 SessionStart、PreToolUse、PostToolUse、Stop。项目状态文件负责路线上下文；本技能不重复注册 Hook，不把 ROUTE_PASS 提升为 FINAL_PASS。

