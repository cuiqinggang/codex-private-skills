# Cursor Menubar Localization Fix - 2026-07-07

## Symptom

Cursor was launched with the mature route:

```powershell
${REDACTED_SECRET}
```

Kilo Code page text was Chinese and Kilo model state was correct, but the
Cursor top menubar still displayed:

```text
File / Edit / Selection / View / Go / Terminal / Help
```

Only `Run` displayed as Chinese.

## Root Cause

For Cursor `3.10.17` / VS Code `1.125.0`, the generated Chinese language cache
existed and contained many normal Chinese strings, but the top-level menubar in
the bundled workbench file was registered with fixed English title values:

```text
title:{value:"File",original:"File",mnemonicTitle:S(3957,null)}
title:{value:"Edit",original:"Edit",mnemonicTitle:S(3958,null)}
...
```

${REDACTED_SECRET}
the top menubar.

## Safe Repair

Back up before editing:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Patch only the top-level menubar title values:

```text
File -> 文件
Edit -> 编辑
Selection -> 选择
View -> 查看
Go -> 转到
Terminal -> 终端
Help -> 帮助
```

Also patch the Glass menu text labels in `workbench.glass.main.js`.

After editing `workbench.desktop.main.js`, update:

```text
product.json -> checksums["vs/workbench/workbench.desktop.main.js"]
```

with the new SHA256 base64 value without trailing `=`.

Do not modify:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
API keys
Windows proxy/network settings
```

## Verified Evidence

Repair output:

```text
${REDACTED_SECRET}
```

Backups:

```text
${REDACTED_SECRET}
```

Patch report:

```text
${REDACTED_SECRET}
```

Acceptance screenshots:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
```

Both screenshots show:

```text
文件(F) / 编辑(E) / 选择(S) / 查看(V) / 转到(G) / 运行(R) / 终端(T) / 帮助(H)
```

Kilo model state remained:

```json
{"providerID":"openrouter","modelID":"deepseek/deepseek-v4-pro"}
```

## Cursor 3.11.13 Incremental Repair - 2026-07-13

Cursor 3.11.13 can overwrite the 3.10.17 application-resource patch during an
update. The visible symptom is unchanged: only `Run` remains Chinese while
`File / Edit / Selection / View / Go / Terminal / Help` return to English.

For the verified mature `--classic --locale zh-cn` route, run:

```powershell
${REDACTED_SECRET}
```

3.11.13 uses `mnemonicTitle` as the visible label. Patching only `value` is no
longer sufficient. The script replaces both fields with JavaScript Unicode
escapes and uses `(F) / (E) / ...` rather than old `&F` syntax, which otherwise
renders visibly as `&amp;F`.

The script backs up the live resources, patches only
`workbench.desktop.main.js`, updates its checksum in `product.json`, and leaves
the Glass resource, Kilo model state, API keys, and network settings untouched.
After running it, restart Cursor with the mature classic shortcut and invoke
`Kilo Code: Open in Tab` if the restored Kilo webview is blank.

The Chinese response rule must also explicitly cover visible reasoning text:

```text
界面中可见的“推理”“思考”“分析”摘要也必须使用简体中文。
```

2026-07-13 acceptance evidence:

```text
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```
