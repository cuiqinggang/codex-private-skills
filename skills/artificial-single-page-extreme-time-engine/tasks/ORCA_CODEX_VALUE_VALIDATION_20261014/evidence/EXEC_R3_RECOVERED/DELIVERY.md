# T03 交付记录

已完成 `requests/T03.md`。改动仅涉及 `scripts/run.py`、`tests/test_run_report_offline.py` 与本文件。

`report()` 为三种方法共用百分率格式化函数：`n_tasks=0` 时在原有七字符 Rate 列右对齐显示 `--`，避免除零；非空数据仍使用原有 `>6.1f` 格式和 `%` 后缀。分数、报告其他内容及结果文件选择逻辑保持原样。

离线测试覆盖：

- 空数据的三个不可用百分率及默认结果文件保存。
- 非空报告全文、分数、百分率、舍入、间距及 token 用量格式。
- 非空数据的 `0.0%`、`50.0%`、`100.0%`。
- stdout 报告正文与保存文件一致；保留 stdout 原有附加换行和 `Results saved:` 提示。
- `results_file` 相对路径、绝对路径、覆盖配置路径及嵌套目录创建。
- 空 benchmark 完成两个模拟评分阶段后，将 `results_file` 传入报告并成功保存。

测试只使用 Python 标准库。导入时屏蔽 `.env` 加载，客户端创建与访问均设为失败保护；评分阶段使用 mock，未启动真实 verifier 后端、未访问凭据或网络，未启动其他模型。

测试中修正了两类本地断言错误：Verifier / Oracle 预期文本多出一个空格；统计 `--` 时误将横线分隔符计入。未为通过测试改变原有非空报告格式。

## 执行命令与结果

工作目录为本 worktree，使用 `C:\Program Files\PowerShell\7\pwsh.exe` 宿主执行：

```text
python -B -m unittest discover -s tests -p test_run_report_offline.py -v
```

本次续接首次运行：退出码 1，`Ran 5 tests in 0.078s`，`FAILED (failures=4)`；空数据已不再除零，失败均来自上述两类本地测试断言错误。

修正断言后的最终结果：

```text
test_empty_benchmark_completes_phases_and_saves_requested_file ... ok
test_empty_report_saves_all_unavailable_rates ... ok
test_nonempty_report_preserves_complete_format_and_values ... ok
test_nonempty_zero_and_full_rates ... ok
test_results_file_overrides_config_for_relative_and_absolute_paths ... ok

Ran 5 tests in 0.055s

OK
```

退出码：0。通过后未重复或扩大测试。本文件在上述测试完成后写入。

## 已保留的旧测试目录

前一轮使用 `TemporaryDirectory` 创建的以下目录因 Windows 沙箱权限拒绝而未能清理；按续接指令保留，本次不再尝试删除，也未修改 ACL：

- `tests/t03-offline-tjau3w1y`
- `tests/t03-offline-e6hx86vh`
- `tests/t03-offline-d2o7g9cy`
- `tests/t03-offline-3d81xfog`
- `tests/t03-offline-lc4fixtx`

现有测试改用继承权限的独立测试目录，并仅清理各次测试自己创建的目录。旧目录不影响五项测试通过。

## CodeGraph usage

- MCP available: 未检查；仓库无 `.codegraph`，无需使用。
- CLI available: 未检查；仓库无 `.codegraph`，无需使用。
- .codegraph index present: 否。
- status checked before work: 是，初始工作目录列表无该索引。
- callers/callees/impact checked where relevant: 已定向阅读 `report()`、`main()` 与 `run_benchmark()`；验证结果路径传递和保存行为。
- sync/refresh run after meaningful code changes: 否，无索引。
- if not used, reason: 无 `.codegraph`，本次为局部报告格式修复。

## Knowledge Brain usage

- INDEX checked: 否。
- ROUTING_MAP checked: 否。
- Relevant indexes checked: 否。
- CodeGraph used where relevant: 否，原因见上。
- OpenHuman reference used where relevant: 不适用。
- Sync run before/after: 无。
- If not used, reason: 本任务明确限定当前 worktree，禁止读取父目录或历史方案；未访问外部知识库，未进行长期记忆治理。