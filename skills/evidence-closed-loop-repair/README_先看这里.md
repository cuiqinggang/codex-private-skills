# 全量证据闭环修复技能包 V1.1.0

这个技能用于解决一种高频且高损耗的问题：

> 文件、命令包或压缩包被宣布“已经改好”，但用户下载、解压或真正运行时，旧错误仍然存在。

## 推荐部署路径

```text
C:\AI\skills\evidence-closed-loop-repair\
```

也可以部署到你的 Codex skills 根目录下，只要最终目录中直接存在：

```text
SKILL.md
scripts\
templates\
tasks\
examples\
```

## 安装方式

### 方式一：手工复制

1. 解压本压缩包；
2. 把整个 `evidence-closed-loop-repair-v1.1.0` 文件夹复制到 Codex skills 目录；
3. 可将文件夹重命名为 `evidence-closed-loop-repair`；
4. 在 Codex 新任务中要求读取该技能；
5. 运行：

```powershell
python .\scripts\self_test.py
```

### 方式二：PowerShell安全安装

```powershell
powershell -ExecutionPolicy Bypass -File .\install_skill.ps1 -Destination "C:\AI\skills\evidence-closed-loop-repair"
```

默认不会静默覆盖现有技能；已有目录会先备份。

## 使用方式

向 Codex 说明：

```text
使用 evidence-closed-loop-repair 技能执行本次修复。
先建立 CHANGE_CONTRACT 和全量影响图；
修改真源头和生成器；
全量重建所有派生文件；
对最终ZIP/7z冷启动解压、递归扫描、正向必需项和负向禁止项双重核验；
没有E3证据不得宣称完成。
```

## 先读哪些文件

1. `SKILL.md`：技能执行规则；
2. `FULL_LOGIC_EXPLANATION.md`：完整逻辑和为什么前几次会失败；
3. `examples/ultrafusion-qwen-case/CASE_STUDY.md`：真实案例；
4. `templates/CHANGE_CONTRACT.template.json`：先定义独立真值；
5. `scripts/self_test.py`：验证技能本身。

## 最重要的规则

```text
正确内容存在，不等于错误内容已经消失。
工作目录正确，不等于最终压缩包正确。
验证脚本PASS，不等于验证真值正确。
没有最终交付物的独立证据，就视为未完成。
```
