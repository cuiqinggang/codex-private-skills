# Hermes F005｜原生 Repair Loop 最小现实验证合同（Reality 前冻结）

任务：HERMES-ECO-20261014 / NODE=H-ECO-02-REPAIR-F005
日期：2026-10-15；继承 HERMES-ECO-F004-20261015。
方法：《三人行》第2版（仅本项目明确选用）＋《GPT直连Windows双路执行桥 V6.0》C>A>B＋Hermes专用技能v2.0＋hermes-repair-loop-adapter v2.0。
状态：VIRTUAL_MATURE_FROZEN，待此节点现实验证；原整站 FINAL_VALID=NO，五轮=0/5。

### 既有可复用成熟基线
原本机路径：C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F002/R01。
现成 requirements.md, invoice.py, test_invoice.py, run-tests.cmd 组成已冻结的故障注入合同。不对原路径写入；复制到完全独立 F005_REPAIR 目录。Hermes正式CLI调用原有 ltmvh-hermes-formal.ps1 和 OpenRouter DeepSeek V4.1 Flash，不改模型设置。既有 Repair Loop SKILL.md 规定 FAIL→根因→最小修复→回归测试→独立复核，最多3次同类失败。

### TASK_INVARIANT
仅修 F005_REPAIR/invoice.py；不得改 requirements.md、test_invoice.py、run-tests.cmd 及 F002 任何文件；不访问密钥、代理、浏览器、私人对话或其他任务。不安装依赖，不启动新服务。严格按照 requirements.md 只累加 status 恰为 paid 的整数 cents（排除 bool），错误值 ValueError，允许负数、大整数。
独立验收固定 Windows Python unittest；外部复核脚本应比较 tests/contracts SHA 前后完全一致、原 F002 invoice SHA 未变。模型自称 PASS 无效。

### 正确执行顺序
1. 在隔离目录复制四份原有合成文件，计算基线 SHA、审查只写权限。
2. 外部运行 run-tests.cmd，确定出现预期失败，保存 exit code / 用例数量；失败不能写成 PASS。
3. 单次真实调用已存在 Hermes 正式 CLI，明确要求读取两份文件、遵守限制、定位 FIRST_DELTA、仅修 invoice.py、执行同项 unittest；允许一次自然模型任务，不盲重发未知进程。
4. 外部独立再次运行 run-tests.cmd，核实所有测试，复核测试和需求 SHA 完全未变及源原 F002 不变；记录模型实际退出码、输出和总墙钟。失败保存 UNKNOWN/FAIL，按 Repair 回虚，而非不断碰碰试。
5. 通过后才考虑独立 delegate_task Gate 验收；该能力单独节点，不因本项通过自动标记整个生态站 PASS。

### 状态及停止
F002 Runs API HTTP400 故障没有被此 CLI Repair 节点修复，仍等待经过授权的单次新隔离 admission Gate。此节点的成功只证明CLI修复+终端+单元测试的当前范围；多智能体/视觉/恢复/网页端/冷启动和长稳都不能由此继承。
