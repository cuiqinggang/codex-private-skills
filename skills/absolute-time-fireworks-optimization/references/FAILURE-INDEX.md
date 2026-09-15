# FAILURE INDEX

正常任务不要通读本文件；只在对应 TRIGGER 命中时查。

## FI-01 本机服务未运行

PROBLEM：首个 WebSocket 连接被 127.0.0.1:8188 拒绝。

ROOT_CAUSE：旧证据日志存在，但 ComfyUI 进程已停止。

TIME_COST：一次无效启动。

WRONG_PATH：把历史日志当当前运行状态；把 readiness polling 放入 runner。

FAST_PATH：benchmark 外调用现有启动脚本；等待冷启动后只查 object_info 一次。

TRIGGER：ClientConnectorError / WinError 1225。

EVIDENCE：P0-EXTREME-MINIMAL-FASTPATH/service-logs。

## FI-02 aiohttp 单连接死锁

PROBLEM：runner 无输出，服务日志没有 got prompt。

ROOT_CAUSE：TCPConnector(limit=1) 的唯一连接被 WebSocket 占用，POST 无连接可用。

TIME_COST：一次卡住与一次精确进程终止。

WRONG_PATH：WebSocket 与 HTTP POST 共用 limit=1。

FAST_PATH：使用默认池或 TCPConnector(limit=0)；WebSocket 长驻时至少允许第二条连接。

TRIGGER：WS 已连接、POST 未到服务端、无超时输出。

EVIDENCE：run.py 的 connector 配置修复。

## FI-03 inference tensor 没有 version counter

PROBLEM：读取 images._version 抛出 RuntimeError。

ROOT_CAUSE：torch.inference_mode 生成的 inference tensor 不跟踪 version counter。

TIME_COST：一次失败 warmup 和一次服务重启。

WRONG_PATH：用 _version 作为 ComfyUI inference tensor 缓存键。

FAST_PATH：固定不可变任务保存 tensor 强引用并用 is 比较；输入对象变化即重编码。

TRIGGER：Inference tensors do not track version counter。

EVIDENCE：candidate-r2 服务与节点源码。

## FI-04 PowerShell 宿主与 quoting

PROBLEM：用 pwsh -File 运行 .py 被拒；嵌套命令中的 PowerShell 变量被外层提前展开。

ROOT_CAUSE：入口类型错误与多层字符串解析。

TIME_COST：三次无效只读命令。

WRONG_PATH：pwsh -File script.py；在双引号嵌套命令中使用未保护的变量/foreach。

FAST_PATH：Python 脚本直接用 python path；简单查询写精确 LiteralPath，不引入变量。

TRIGGER：没有 .ps1 扩展名、LiteralPath 缺参数、foreach 缺变量。

## FI-05 递归复用扫描被安全拒绝

PROBLEM：preflight_reuse_check.py 因递归读 .codex/.hermes/Documents 被阻断。

ROOT_CAUSE：范围可能触及凭据或会话。

TIME_COST：一次被拒执行。

WRONG_PATH：在受保护根做自动递归预检。

FAST_PATH：INDEX → ROUTING_MAP → 一个 category index → 明确 Top-K 文件。

TRIGGER：安全审查提示扫描范围过宽。

## FI-06 Windows apply_patch 多行参数

PROBLEM：内置补丁后端 DACL 失败；apply_patch.bat 的 %* 破坏多行尾行。

ROOT_CAUSE：Windows token/DACL 与 batch 多行参数传递。

TIME_COST：多次失败补丁调用。

WRONG_PATH：把多行 UTF-8 patch 经 apply_patch.bat 的 %* 传递。

FAST_PATH：直接调用包装器背后的 Codex executable，使用 --codex-run-as-apply-patch 和单一 UTF-8 参数。

TRIGGER：SetTokenInformation 1344、last line must be End Patch。

## FI-07 大范围 rg 污染输出

PROBLEM：在整个 comfy 目录搜索 encode 命中巨大 tokenizer/vocab 文件。

ROOT_CAUSE：没有限定文件类型和明确源文件。

TIME_COST：约 730k 原始输出和一次无效搜索。

WRONG_PATH：对大型依赖树做宽泛关键词搜索。

FAST_PATH：先限定 server.py/execution.py/main.py；必要时加 -g "*.py"。

TRIGGER：输出突然出现词表、模型或数十万行。

## FI-08 启动负担不等于稳态负担

PROBLEM：只加载白名单 custom nodes 后 P50 从 14.1638 退化到 16.9494 ms。

ROOT_CAUSE：大量扩展主要影响冷启动，没有证据证明其进入稳态固定任务关键路径。

TIME_COST：一次重启和 2+5。

WRONG_PATH：仅凭启动日志很长推断稳态会更慢。

FAST_PATH：先证明 hook 位于 T_START/T_END，再改启动集合；未兑现立即回滚。

TRIGGER：建议用 disable-all-custom-nodes 提升稳态任务。

EVIDENCE：白名单候选 results JSON。

## FI-09 安全边界阻止无校验快速端点

PROBLEM：固定快速提交端点方案被安全审查拒绝。

ROOT_CAUSE：新增 HTTP 接口并绕过 validate_prompt 改变网络/校验边界。

TIME_COST：一次被拒补丁。

WRONG_PATH：用换名、monkeypatch 或缓存绕过同一安全拒绝。

FAST_PATH：把重复 validation 记录为当前约束成本；只有保留安全校验的成熟方案才重开。

TRIGGER：优化建议涉及新网络端点、跳过 prompt validation。

## FI-10 中文参数编码

PROBLEM：初始化器命令行传入的中文 openai.yaml 变成乱码。

ROOT_CAUSE：Windows 命令行编码链未保持 UTF-8。

TIME_COST：一次重写 metadata。

WRONG_PATH：通过多层 PowerShell 参数直接传中文生成文件。

FAST_PATH：初始化时用 ASCII，占位后使用 UTF-8 apply_patch 写中文；运行
quick_validate.py 时显式使用 python -X utf8，不用嵌套 PowerShell 环境变量赋值。

TRIGGER：生成文件出现 replacement/乱码字符，或 validator 报 GBK UnicodeDecodeError。
