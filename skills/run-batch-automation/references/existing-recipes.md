# 已有专业配方与精确调用条件

这些是原能力的路由卡；本包不复制原业务程序或旧依赖环境。当前Windows环境未重新检查。命中卡片后读取原合同，按原任务当前输入执行其原验收。

## orders-four-artifacts

**订单CSV一次生成四种报表并独立核对**

- 原包：`dsh-mature-capabilities`；入口：`C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/business_pack.py`。
- 匹配：UTF-8 CSV精确表头row_id,order_id,customer,amount_cents,quantity；整数分金额、非负整数数量；输入≤16MiB且不超Excel精确整数范围。
- 批次：一份CSV整表处理，生成details.csv、summary.json、report.docx、ledger.xlsx；不逐行调用模型。
- 验收：原独立verify_order_pack.py读取输入及四个成品，20项内容/排序/汇总/公式/缓存检查；返回CONTENT_ACCEPTED且qa.pass=true。
- 边界：CONTENT_ACCEPTED不含所有视觉和外部重算；金额/行数/字段不匹配先拒绝或改选现有完整配方。未取得实际付费客户生产验收证明。

```json
{
  "kind": "CLI",
  "windows_path": "C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/business_pack.py",
  "call": "python \"C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/business_pack.py\" --input <orders.csv> --out <new_output_dir>"
}
```

原证据：dsh-mature-capabilities/references/business-acceptance.json：PASS_LIMITED_BUSINESS_SCOPE，订单2配对夹具各20检查、新输入20检查。；dsh-mature-capabilities/references/holdout-acceptance.json：240行、14客户、20项检查，真实LibreOffice重算及3视图复核。

## office-multi-file-extraction

**Word/Excel/PPT等多文件同进程提取**

- 原包：`local-capability-index`；入口：`C:/Users/A/Documents/DSH-Workspace/capability-index-20261024/data_fastlane.py`。
- 匹配：已解析的本地普通文件；docx/pptx/xlsx/txt/md/html/csv/pdf；每文件≤64MiB；Office ZIP有展开大小/成员数/穿越检查。
- 批次：MarkItDown同一进程转换多文件，JSON结果含source与markdown；插件、LLM和URL输入关闭。
- 验收：原FASTLANE-ACCEPTANCE.json/BATCH-ACCEPTANCE.json登记了本地格式和批量接入验证；本轮仅读技能/源码，未重新打开该Windows回执。
- 边界：提取不是高保真成品导出，也不是扫描件OCR或全部格式安全认证。必须复用原环境，不把脚本移走后假设依赖仍可用。

```json
{
  "kind": "CLI",
  "windows_path": "C:/Users/A/Documents/DSH-Workspace/capability-index-20261024/data_fastlane.py",
  "call": "python \"C:/Users/A/Documents/DSH-Workspace/capability-index-20261024/data_fastlane.py\" convert <file1> <file2> --root <authorized_input_root>"
}
```

原证据：local-capability-index/references/external-capabilities.md：Windows既有MarkItDown0.1.6与多文件入口。；local-capability-index/scripts/data_fastlane.py：convert input nargs=+，MarkItDown(enable_plugins=False)。

## integer-cents-csv-aggregate

**整数分CSV固定聚合**

- 原包：`local-capability-index`；入口：`C:/Users/A/Documents/DSH-Workspace/capability-index-20261024/data_fastlane.py`。
- 匹配：本地授权根内CSV≤64MiB；金额列必须为显式整数分字符串，非法值不丢行、不静默舍入。
- 批次：DuckDB固定SQL一次GROUP BY/count/sum(HUGEINT)，输入all_varchar，返回分组key/rows/total_cents。
- 验收：原隔离DuckDB1.5.6 wheel来源/哈希与固定聚合接入有登记；40万行合成对照没有优于Pandas。
- 边界：可选SQL缺口入口，不替换默认Pandas，也不承诺通用提速；沿用原脚本旁python-packages隔离依赖，不复制成无依赖单文件。内部2线程不是2条Pi＋GPT整链。

```json
{
  "kind": "CLI",
  "windows_path": "C:/Users/A/Documents/DSH-Workspace/capability-index-20261024/data_fastlane.py",
  "call": "python \"C:/Users/A/Documents/DSH-Workspace/capability-index-20261024/data_fastlane.py\" aggregate <input.csv> --root <authorized_root> --group <column> --cents <integer_cents_column>"
}
```

原证据：local-capability-index/references/external-capabilities.md：DUCKDB-PROVENANCE/INSTALL、FASTLANE/BATCH验收位置。；local-capability-index/scripts/data_fastlane.py：锁定配置，禁自动/未签名扩展，threads=2，memory_limit=256MB。

## source-pack-fetch-and-verify

**官方原文取回与整包引用核对**

- 原包：`dsh-mature-capabilities`；入口：`C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/`。
- 匹配：已结构化有限事实、实际来源原文和evidence.json中的url/file/sha256；GitHub小适配器只支持公开单ref文本≤1MiB。
- 批次：一次核对整包sources/连续引文/事实覆盖及brief正文一致；GitHub必要时官方Contents API取正文并验blob SHA。
- 验收：原2份简报、每份4事实/2来源；混合240行报表＋4事实/2官方来源验收保留了错引文和篡改拒绝证据。
- 边界：不代替联网事实研究、中文语义判断或动态事实更新；verify通过不等于模型结论语义正确；分支名含斜杠、私有仓库和二进制不在fetch小适配器合同内。

```json
{
  "kind": "existing_CLI_composition",
  "windows_path": "C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/",
  "calls": [
    "python \"C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/fetch_github_source.py\" --url <public_github_blob_url> --out <source.md>",
    "python \"C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/verify_source_pack.py\" --folder <artifact_dir> --input <fact_contract.json> --evidence <evidence.json>"
  ]
}
```

原证据：dsh-mature-capabilities/references/business-recipes.md：来源合同/CLI及base64、原字节哈希。；dsh-mature-capabilities/references/business-acceptance.json、holdout-acceptance.json。

## bounded-original-session-recovery

**本地成品任务有界原会话恢复**

- 原包：`dsh-mature-capabilities`；入口：`C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/run_resumable.py`。
- 匹配：仅本地成品、无外部副作用；原DSH headless、Tenacity、continuity资源齐备，显式工作区状态根。
- 批次：复用官方session-id与已有检查点，对账后差量接续，最多两次。
- 验收：原recovery记录实际终止进程、同session恢复、2次尝试、已提交产物不变。
- 边界：不要捏造python run_resumable.py命令。不是守护进程/任务队列；权限拒绝和活写句柄冲突不重试；不外推OS重启、24小时、付款/外发或GPT自动唤醒。

```json
{
  "kind": "existing_python_library",
  "windows_path": "C:/AI/DeepSeek-Harness-Trial/dsh-home-mature-agent/skills/dsh-mature-capabilities/scripts/run_resumable.py",
  "function": "execute(task,cwd,patch,home,binary,log_root,session_id=None,max_attempts=2,timeout_seconds=240)"
}
```

原证据：dsh-mature-capabilities/references/business-acceptance.json/recovery。；dsh-mature-capabilities/scripts/run_resumable.py确为库函数，无独立CLI入口。
