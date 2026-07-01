# 20260528 POSA / Polsia intake report

运行类型：ad-hoc intake / light update extension

## 触发来源

用户提供 3 张中文短视频资料截图，主题为 `POSA 模式`、`Ben Broca/Brocka`、零员工 AI 公司、自动建站/支付/广告/融资、一人或零人公司。

## 本次核对结论

- 技能包已有 `Polsia` 作为候选和 watchlist 条目。
- 技能包没有收录截图里的 `POSA / Ben Broca / 零员工公司 / 融资叙事` 详细资料。
- 公开搜索和官网证据显示，截图里的 `POSA` 更可能对应 `Polsia`。
- 已新增 `CASE-008 Polsia / POSA 零员工 AI 公司模式`。

## 本次搜索和检查关键词

```text
POSA Ben Broca AI company
POSA Ben Brocka zero employee company
Polsia AI company operating system
Polsia AI That Runs Your Company While You Sleep
Polsia Ben Cera Claude Agent SDK
Polsia login dashboard live API
```

## 本次证据采集

| 类型 | 结果 |
|---|---|
| 官网 HTML | `https://polsia.com/` 保存为 `sources\web\polsia-posa-20260528\polsia_com.html` |
| 公共页面 | `/live`、`/new`、`/login`、`/terms`、`/privacy` 均保存 HTML shell |
| 前端资源 | 下载 `assets_index_DGRm7ehX_js` 和 CSS，用于只读分析功能结构 |
| 公开 API | `/api/public/live/dashboard` 可读，已保存 summary |
| 登录边界 | `/api/auth/session` 返回未登录；companies/tasks/reports/subscription 返回 401 |
| 用户截图 | 已复制到 `screenshots\polsia-posa-20260528` |

## 新增候选

| 名称 | 类型 | 当前状态 | 推荐动作 |
|---|---|---|---|
| Polsia / POSA 零员工 AI 公司模式 | 闭源一人公司操作系统产品案例 | 已成 CASE-008 | REPLAY |

## 值得吸收

- company object 作为核心容器。
- agent roster + task queue + run history + reports。
- public live dashboard 作为信任证明和运营指挥面板。
- 域名、广告、外联、支付作为能力节点，但默认进入审批门。
- 订阅/额度机制可转化为本地算力、预算、时间额度门。
- 80/20 原则：AI 执行标准化任务，人类负责品味、定位、价值判断和高风险审批。

## 暂缓观察

- 自动融资、投资人邮件、股权分配叙事。
- 真实广告投放、真实客户外联、真实域名购买。
- 平台自报 ARR/MRR/公司数量是否能被独立验证。
- 闭源后端的真实安全、权限、审计和错误恢复机制。

## 明确放弃

- 不登录真实账号。
- 不创建账号。
- 不触发真实支付、域名、广告、邮件、投资人外联。
- 不复制 Polsia 品牌和私有 UI。

## 是否更新索引

- 更新 `CASES.md`：新增 CASE-008。
- 更新 `ROUTE-MATRIX.md`：新增 Polsia/POSA 详细路线。
- 更新 `WATCHLIST.md`：补充 Polsia/POSA 行。
- 更新 `SOURCE-OF-TRUTH-MAP.md`：补充证据路径。
- 更新 `CHANGELOG.md`：记录本次 intake。

## 状态码

ONE_PERSON_AI_COMPANY_ROUTES_POSA_POLSIA_INTAKE_PASS
