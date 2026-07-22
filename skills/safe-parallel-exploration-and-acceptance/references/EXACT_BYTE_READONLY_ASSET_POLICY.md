# 精确字节与只读资产策略

提示词、命令包、封存基线和其他哈希锁定资产以字节为真值，不以编辑器显示或 `git diff --check` 为真值。

## Git 属性

对锁定文件使用：

```gitattributes
path/to/locked.asset -text
```

随后运行 `scripts/acceptance/verify-exact-byte-assets.py`，同时比较工作副本 SHA-256 与 Git index blob SHA-256。

## 破坏性测试

`scripts/acceptance/test-readonly-sandbox-injection.py` 必须把源文件复制到独立临时目录。若副本继承只读属性，只允许清除副本属性；修改后再次核验源文件哈希未变化。

禁止为了通过格式检查而修改锁定资产的 CRLF、BOM、尾随空格或编码。
