# Hermes F016｜自然语言任务→知识库索引→Codex技能按需加载，当前真实PASS
2026-10-15 | HERMES-ECO-20261014 | 《三人行》V2（Hermes项目显式使用） | V6桥C | Hermes母技能v2.0。
前置完整虚拟冻结：F016_NATURAL_TASK_SKILL_ROUTER_FREEZE_20261015.md；结果SCOPED_RUNTIME_PASS，用户的原Codex技能与Knowledge文档都未修改。

## 实际输入与能力主张
新正式CLI一次性隔离只读任务，模型只知道目标：Windows PowerShell 5.1代码变更要保证编码/Parser、原文件字节备份与独立接受，不给具体Codex技能名、禁止执行任何技能脚本、修改系统或额外工具。需先用原生母技能和Knowledge Brain索引自主寻找最适合的技能。

## Hermes原生回执与真实轨迹（本轮stdout可证）
1) 调用技能发现与 native skill_view 加载 hermes-mature-supertool SKILL.md，readiness_status=available；同时用read_file读取 F014/CODEX-KB-ON-DEMAND-20261015.md 引导规则。
2) 原生read_file真实按次序读取 C:/Users/A/.codex/knowledge-brain/INDEX.md（176行）、ROUTING_MAP.md（189行）、indexes/skills-index.md；对索引进行关键字检索powershell/encoding/backup/verification/parse，42处匹配，定点阅读对应局部行段。
3) 从候选选3项并实际用read_file读对应Codex SKILL.md：
   a. powershell-reliability-guard（72行，主匹配，freeze host 5.1、PowerShell parser、UTF8 BOM与安全fail-closed gate）；
   b. evidence-closed-loop-repair（315行，byte backup、不可变GOOD/BAD夹具与独立验收门）；
   c. verification-before-completion（120行，未见本轮真实验收及exit code不得宣称PASS）。
4) 识别索引内codex-cli-windows-sandbox-fix在Reasonix技能根而非Codex目录，未臆造文件/验收。
5) 输出的可执行Plan符合三个技能的冻结与改动前备份、5.1与7分流、明确UTF8解析、独立同项测试，且未创建/写入/执行任何代码或脚本。native tools=skills_list、skill_view、read_file、search_files，CLI exit0，进程runtime=202.49s。

## 有效性与性能判断
当前可以正式说：Hermes已能根据**任务意图**自己经过成熟知识库选择并读取多个真实Codex技能，并形成符合安全边界的建议。这是跨技能库自然任务路由RUNTIME_PASS，而不是218项逐一性能PASS。
但是202.49s较长，可能包含索引加载/3份SKILL.md/多轮模型与工具。与F014的指定路径30.28s任务不等价，禁止声称确定慢6.7倍或获利何值；对于用户已给定具体技能/常见轻任务应跳过读整个Knowledge INDEX和查多个候选，只打开已知精确SKILL.md，最多必要的1-3文件，不搞大规模工具堆叠。
F011/F014母技能已保留 CLI-first 和知识库按需引用，参考文件中已加入《三人行》V2网络方法权威源及真实blob 027229fc28ebd12811adacfe37aa857a187d3301（仅Hermes项目级方法使用，不全局激活）。

## 整站剩余
F015已有Chrome不提供9222 CDP，因此WebUI当前标签页未做GUI真实聊天；本节点没有另开浏览器。F011原整包秘密扫描仍有1项YAML命中，该安全质量门FAIL，未读取/传播凭据。Hermes五轮正式综合验收0/5、FINAL_VALID=NO，模型多路由/视频/音频/Hermes新会话恢复/长期观察均待验。
