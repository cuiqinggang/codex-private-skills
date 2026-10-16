# T01 交付结果

已完成 requests/T01.md：恢复 OpenAI-compatible 响应中有效评分字母和真实概率分布的解析，离线回归全部通过。

## 改动

- `llm_verifier/fine_grained_reward.py`：新增 `_openai_choice_text`，供初始响应和 prefill 共用。保留非空 content 的优先级，再读取 reasoning、reasoning_content；消息字段均为空时，按原顺序拼接 logprobs 的 sampled token。
- `_find_tag_logprobs`：空或纯空白 token 继续参与文本拼接，但不重复触发 tag 匹配，避免将已捕获的字母分布覆盖为 closing-tag 分布。保留拆分 tag、融合 `>字母`、最后一次匹配和文本回退语义。
- `tests/test_t01_offline.py`：新增 15 个标准库 unittest 测试方法，使用 mock 客户端验证普通内容、content 优先级、两个 reasoning 字段、logprobs 回退、prefill 字母与双标签分布、空白 token、文本评分、请求重试及首次／后续 prefill 失败回退。

## 验证

最后一次执行：

```text
python -B tests/test_t01_offline.py -v
```

结果：`Ran 15 tests in 0.068s`，`OK`，退出码 0。

此前还通过以下发现模式运行同一组测试：

```text
python -B -m unittest discover -s tests -p test_t01_offline.py -v
```

修复前，同一组测试产生 21 个失败断言（含 subTest），复现字母丢失与分布覆盖；修复后 15 个测试方法全部通过。验证环境为 Python 3.13.12；两个改动 Python 文件的 AST 语法检查通过，均无行尾空白。

测试直接加载目标模块，固定使用 mock 客户端和离线模型名称，不导入模型 SDK；测试期间禁止凭据加载、客户端创建和 socket 连接。未调用模型服务，未读取 .env 或凭据。

## 范围与限制

仅修改目标解析文件，新增测试文件与本报告；未实现或读取 T02/T03，未读取工作树外父目录、隐藏检查或历史方案，未联网、调用额外模型或执行 Orca 生命周期命令。已有请求参数、概率期望计算和失败回退流程保持不变。本次只做离线验证，未进行真实服务集成测试；T01 无剩余实现事项。

CodeGraph usage:

- MCP available: 未探测；仓库无 .codegraph，未进行外部工具发现。
- CLI available: 未探测；同上。
- .codegraph index present: 否。
- status checked before work: 是，修改前已检查索引是否存在。
- callers/callees/impact checked where relevant: 是，通过定向 rg 与阅读检查 call_openai → prefill，以及 extract_score → tag 分布查找的调用关系。
- sync/refresh run after meaningful code changes: 未运行，仓库不存在索引。
- if not used, reason: 无 .codegraph，按项目规则使用定向 rg 与代码阅读。

Knowledge Brain usage:

- INDEX checked: 否。
- ROUTING_MAP checked: 否。
- Relevant indexes checked: 否。
- CodeGraph used where relevant: 未使用，原因见上。
- OpenHuman reference used where relevant: 不适用。
- Sync run before/after: 均未运行。
- If not used, reason: 本次明确限定在隔离工作树完成 T01，不读取外部资料，不涉及知识库或长期记忆维护。
