# 混合智能概率引擎 v0.3.1 — 冻结后自测与回读证据

## 继承的实际无付费执行验证

v0.3.0 与 v0.3.1 的 Reality runner 核心执行逻辑、benchmark、oracle、路由、verifier、模型合同和运行次数不变。

v0.3.0 已实际执行无付费 self-test：

```text
路由=CODE 16 / JEV 24 / GPT 8
JEV问题=32
结构自测=PASS
SQL verifier/失败注入=64/64 PASS
付费网络调用=0
```

v0.3.1 只做：
- 版本号/冻结路径升级；
- 虚拟时间校准更新；
- 攻击证据增强。

## v0.3.1 Git 回读

冻结文件已经从 v0.3.1 分支回读：

```text
HIPE-v0.3.1-real-verify.py
Git blob = 37ba028e4b15227122edf891624e27f6656147b6

HIPE-v0.3.1-reality-launcher.pyw
Git blob = 842190a328e52b3cf7d8330d34d4652342b8b43c

PUBLIC-BENCHMARK-v0.3.1.json
Git blob = 8d14d9dbe38b18388d2fe4bf1ed2554e3df4a1b6

PRIVATE-ORACLE-v0.3.1.json
Git blob = d07a130d50305348f66460eb645975f316dc29c3
```

Public benchmark 与 private oracle 的 blob 与 v0.3.0 相同，证明 benchmark/oracle 字节未改变。

## 当前环境限制

尝试在当前 GPT 执行环境从私库 raw URL 再物化 v0.3.1 文件做第二次本地执行时，容器 DNS/网络不可用。

因此：

```text
V031_POST_UPLOAD_LOCAL_RERUN=NOT_EXECUTED_ENV_NETWORK_BLOCK
```

禁止把它伪造为 PASS。

这不改变 v0.3.0 已执行 self-test 及 v0.3.1 Git blob 回读证据，但 Reality 仍必须真实执行。

## 虚拟门

```text
VIRTUAL_MATURITY=PASS_FOR_HIPE_E2E_V3_48
REALITY_CERTIFIED=NO
PAID_REALITY_CALLS_FROM_GPT=0
```
