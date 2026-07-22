# 依赖与兼容性

## 必需

- Python 3.10+
- 标准库即可检查普通目录和ZIP

## 7z检查

7z冷启动需要系统安装以下任一命令：

```text
7z
7zz
7za
```

Windows通常可安装7-Zip并将其加入PATH。

环境没有7z命令时，脚本必须返回：

```text
PENDING_UNVERIFIED_7Z
```

禁止伪装为PASS。

## 可选

- Git：用于独立Worktree和原版冻结
- 浏览器：查看SVG/HTML图文说明

本技能运行时不需要联网。
