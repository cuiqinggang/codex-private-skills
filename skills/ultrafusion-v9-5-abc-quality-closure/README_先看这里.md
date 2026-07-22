# UltraFusion V9.5.1 ABC 极限质量闭环技能包 RC2

## 当前状态

```text
静态结构：已构建并可校验
真实质量：等待端到端测试
HTML最小运行页：尚未实现
旧V9.1与旧V9.5草案：不修改
```

这次版本把过去分散的长讨论整理成两套内容：

1. **设计与证据层**：完整保存为什么要做、为什么这样做、数学关系、研究数据、成立条件、成本门槛和失败边界。
2. **轻量运行层**：真正复制给模型的 A/B/C/最终评测提示词，删除重复论证和无关公式。

## 版本核心

```text
A：一个统一极限提示词 × GPT/Qwen/DeepSeek
B：GPT选择性吸收三份A中的独有强点
C：新GPT会话做局部、可撤销、非回退强审核
最终评测：匿名评答案，再揭示阶段、时间和成本审核整个流程
```

## 最先阅读

1. `00_设计演进与逻辑总览.md`
2. `01_V9.5逻辑与量化合同.md`
3. `CODEX_部署说明.md`
4. `运行提示词/`

## Codex部署原则

Codex只负责：

```text
解压；
运行自测试；
复制技能目录；
复制桌面执行母版；
报告哈希和测试结果。
```

Codex不得：

```text
重新生成或改写提示词；
把一个A提示词改成三个版本；
自动加入HTML、API或后台；
修改旧版；
merge或push。
```

## 快速部署

在 PowerShell 中：

```powershell
python .\scripts\self_test.py
powershell -ExecutionPolicy Bypass -File .\install_skill.ps1 -Destination "C:\AI\skills\ultrafusion-v9.5"
powershell -ExecutionPolicy Bypass -File .\deploy_desktop_template.ps1
```

两个 PowerShell 脚本遇到同名目录会先备份，不会静默覆盖。

## 本版本没有做什么

- 没有实现 HTML 测试页；
- 没有连接 GPT、Qwen 或 DeepSeek API；
- 没有声称真实答案质量已通过；
- 没有取代后续多题实验；
- 没有生成英文版。

## 正确使用方式

从 `桌面执行版模板/1号文件夹_稳定运行母版_V9.5.1` 复制出新的 2号测试副本。母版内已经包含 A_Initial、统一A、B、C和最终评测提示词；1号母版不得直接使用。
