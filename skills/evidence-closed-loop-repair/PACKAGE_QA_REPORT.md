# 技能包自验报告

## 1. 版本

`evidence-closed-loop-repair v1.1.0`

## 2. 脚本与夹具

- Python语法编译：PASS
- Good fixture：PASS（正确样本被接受）
- Bad fixture：PASS（错误样本被拒绝，验证进程返回非0）
- ZIP冷启动夹具：PASS
- 自测试默认只读：PASS（不再改写技能目录；只有显式 `--output` 才写结果）

## 3. 验证器独立性

- 正确真值来自独立 `CHANGE_CONTRACT.json`；
- 合同文件本身默认排除，避免合同中的Forbidden定义自触发；
- 支持每条规则独立作用域和排除范围；
- 坏样本包含“源文件正确、派生文件错误”，验证器必须拒绝。

## 4. 7z限制

当前构建环境没有7z CLI，因此没有虚构7z测试为PASS。无7z环境时脚本明确返回 `PENDING_UNVERIFIED_7Z`。

## 5. 视觉证据

- `evidence/screenshots/01_技能自测试总览.png`
- `evidence/screenshots/02_坏样本必须被拒绝.png`
- `evidence/screenshots/03_冷启动ZIP验证.png`

## 6. 最终ZIP验证

最终ZIP的冷启动解压、逐文件哈希一致性、包内自测试和MANIFEST复核结果，见压缩包旁的 `evidence-closed-loop-repair-v1.1.0_QA.json`。
