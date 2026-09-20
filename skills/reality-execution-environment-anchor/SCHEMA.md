# 字段结构

## R1/R2 历史
34=证据元数据盘点；35=关键缺口；36=全部非 PASS 模块；37=V2 总指纹；38=逐项恢复；39=发布分类；40=实际配置层与规则源；41=官方规则解释器验证；42=实际生效规则模型；43=TARGET 父/子进程执行边界；44=关键与辅助双覆盖率；45=最终权威总锚点；46=V3 总指纹。

来源枚举：TARGET、COLLECTOR、TARGET_AND_COLLECTOR、RUNTIME_REPORTED、SOURCE_FILE。
`PROVEN_NON_BLOCKING` 不等于 PASS；R2 中网络对 1344 预启动失败“非阻断”不得外推到浏览器 E2E。

## Browser R3 新结构
每次真实 R3 使用新目录：
`snapshots/YYYY-MM-DD-r3-browser-<run-id>/`

安全镜像目标结构：
- 00-R3-MANIFEST.json
- 01-HOST-BROWSER.json
- 02-CONTEXT-CONFIG-SAFE.json
- 03-AUTH-STORAGE-SAFE.json
- 04-PAGE-GRAPH.json
- 05-DOM-ACTIONABILITY.json
- 06-NETWORK-SAFE.jsonl
- 07-RUNTIME-ERRORS.jsonl
- 08-ARTIFACT-HASHES.json
- 09-GOLDEN-TASK-RESULT.json
- 10-BROWSER-REALITY-ANCHOR-R3.json
- 11-BROWSER-REALITY-FINGERPRINT-V1.json

`raw/` 只存在本机，不属于远端安全镜像。
