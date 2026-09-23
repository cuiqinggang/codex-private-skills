# v0.1.0 Virtual Tests

## 目标

只验证“来源 -> 成熟工具”的规则是否唯一、简短、无多余中间层。

## Cases

| Case | 输入 | 期望路由 | 结果 |
|---|---|---|---|
| V01 | Hugging Face 单文件 + revision + destination | `hf download` | PASS |
| V02 | Hugging Face 同仓库多文件 | 单次 `hf download <repo> <files...>` | PASS |
| V03 | GitHub Release asset | `gh release download` | PASS |
| V04 | 普通 HTTP/HTTPS 直链或多 URI | `aria2c` | PASS |
| V05 | 必须依赖已登录浏览器 Session 的下载 | Playwright Native AI Browser | PASS |
| V06 | HF + GitHub Release + 普通 URL 混合任务 | 拆成 3 个最少成熟工具调用；不建统一队列 | PASS |
| V07 | 官方专用工具不可用但存在直接 URL | `aria2c` fallback | PASS |
| V08 | 没有直接 URL 且必须登录 | Playwright fallback | PASS |

## 攻击检查

```text
AMBIGUOUS_ROUTE=0
CUSTOM_DOWNLOADER_REQUIRED=0
CUSTOM_ADAPTER_REQUIRED=0
CUSTOM_QUEUE_REQUIRED=0
CUSTOM_STATUS_UI_REQUIRED=0
CUSTOM_SOURCE_SEARCH_REQUIRED=0
JEV_REQUIRED=0
```

## 时间判断

本技能包不伪造现实毫秒数。

虚拟结构比较只有：

```text
旧自建方案：
分类 -> 探针 -> 自定义选源 -> 自定义控制 -> 下载器 -> 自定义状态/恢复

v0.1.0：
分类 -> 成熟工具
```

因此：

```text
PREDICTED_ROUTING_OVERHEAD=v0.1.0 最小
NUMERIC_T_VALID=REAL_TEST_REQUIRED
```

## Virtual Freeze

```text
RULE_SET_CLOSED=PASS
SINGLE_TASK_ROUTING=PASS
MULTI_TASK_ROUTING=PASS
NO_REDUNDANT_LAYER=PASS
VIRTUAL_MATURE=PASS
REAL_CERTIFIED=NO
```
