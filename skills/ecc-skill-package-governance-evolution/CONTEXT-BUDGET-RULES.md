# Context Budget Rules

## Purpose

Keep skill-package work usable in bounded model context.

## Rules

1. Short Entry File（短入口文件）
   Entry files should navigate, not duplicate every rule.

2. Progressive Disclosure（渐进加载）
   Read what the current task needs, when it needs it.

3. Skills On Demand（技能按需加载）
   Specialized methods and templates are loaded only when selected.

4. Source-of-Truth Map（权威规则地图）
   Every rule category has one authoritative file.

5. Reports Archive（报告归档）
   Historical reports are evidence archives, not default context.

6. Compact Handoff（压缩交接）
   Long phases must hand off concise summaries and evidence paths.

## Forbidden Default Reads

- Do not default-read `reports/**`.
- Do not default-read `reports/**/backup/**`.
- Do not default-read backups.
- Do not read all templates when only one template is needed.
- Do not read unrelated skill packages.
- Do not scan parent skill directories unless explicitly required and authorized.

## Required Evidence

Every governance task should record:

- selected template
- source files loaded
- reports read
- reports skipped
- context-budget exceptions
- verification output
