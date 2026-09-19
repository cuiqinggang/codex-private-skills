# 成熟态验收门禁

只有各层都有真实证据，项目才能从 `MATURE_CANDIDATE` 升级为 `MATURE_VERIFIED`。

## A 产品能力
网站导入/生成；Design System/组件一致性；页面/内容/图像编辑；live preview；CMS/DB/forms；Analytics + GA4/GSC；SEO/AEO；Audience/visitor insight；integrations/OAuth；workflow/scheduled actions；publish/domain/SSL/CDN；immutable deploy/version/rollback。

## B Agent 主动闭环
必须证明 `OBSERVE → THINK → ACT → MEASURE → LEARN` 可连续运行：发现问题/机会、给出可解释建议、权限内执行、高风险审批、安全边界、动作后测量并更新策略。

## C 可靠性
build/deploy/retry/queue、token/OAuth expiration、第三方 API failure、partial failure/recovery、rollback、state/data consistency、scheduled jobs、long-running agent actions。

## D 安全
secret isolation、least-privilege OAuth、tenant/workspace isolation、auditability、destructive-action protection、prompt/tool injection boundary tests。

## E 测试证据
unit/component、integration、E2E/browser、regression、load/performance、chaos/failure injection、agent eval、security、long-run stability。

## F 商业可运行
onboarding、billing/usage accounting、support/error visibility、monitoring/alerts、data export/delete、目标市场要求的基本 legal/privacy surfaces。

## 状态码
- REFERENCE_MATURE_ROUTE：外部成功路线已整理
- VIRTUAL_MATURE_99：虚拟方案收敛，未真实实现
- MATURE_CANDIDATE：核心能力运行，成熟证据不足
- MATURE_VERIFIED：真实验收全部通过

禁止从 VIRTUAL_MATURE_99 直接跳到 MATURE_VERIFIED。
