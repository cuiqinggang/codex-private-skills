# 数据契约

## source_registry.csv

固定字段：

`source_id,title,type,author_org,published_at,collected_at,version,relative_path,locator,reliability,topics,sha256,status`

- `source_id`：脚本生成的 `SRC-<SHA前12位>`。
- `type`：pdf、pptx、web、report、paper、regulation、standard、md 或 other。
- `relative_path`：相对项目根目录，必须位于项目内。
- `locator`：页码、章节、表格编号或 URL 定位。
- `reliability`：A/B/C/D。
- `status`：active、superseded、conflicted 或 rejected。

## Wiki 证据行

每条关键结论至少包含：结论、事实/推断/假设类型、source_id、locator、年份/单位/口径（如适用）、可靠性、核验状态。

## Manifest

`manifest_tool.py` 输出 schema_version、root、file_count、duplicate_count、files、duplicates 和 deleted。状态仅表示文件级变化，不替代内容审计。

## 安全边界

脚本跳过符号链接，不读取根目录外文件，不联网，不删除来源。`--force` 只允许覆盖脚手架生成的文本模板，不覆盖原始资料。

