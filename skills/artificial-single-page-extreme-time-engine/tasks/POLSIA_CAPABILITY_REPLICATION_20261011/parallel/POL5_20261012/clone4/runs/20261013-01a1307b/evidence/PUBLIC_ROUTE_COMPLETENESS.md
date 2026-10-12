# 当前 Polsia canonical 公开路由库存

当前下载的 `visual-reference/index-CsJ1Yu6P.js` 为 3,224,224 字节，SHA-256 `85f71d50a1518fae95246fc694e4efa28212609c573f9d8d43ea05927e623d67`。全文件只用可信 TypeScript parser 解析文本，未 import/eval 或启动浏览器。0 语法诊断；136 个含 path/component/guard 的路由对象与旧 `index-VMJx2-_h.js` metadata、守卫源及位置相同，69 个公开组件/交互/主域选择/守卫符号源码 SHA 均相同，0 未分类路由。两个 bundle 的字节 SHA 不同，差异窗口中包括静态依赖 hash；不把“路由相同”扩张为整个站点字节相同。

完整机器证据见 `CURRENT_PUBLIC_ROUTE_AUDIT.json`。旧版本组件片段及主域/help 域选择证据见 `PUBLIC_ROUTE_AUDIT.json`、`public-route-audit/`。DOM、原资产和实际请求验证分别见 `PUBLIC_PAGE_BUILD_RECEIPT.json`、`PUBLIC_PAGE_ROUTE_OBSERVATIONS.json`。

## canonical 主域 Yrt 的 13 个路由模式

| 路由 | 当前源码组件 / 守卫 | 实测源行为与本地实现 |
|---|---|---|
| `/` | xrt / YH | 匿名首页，四屏及语言菜单；本地真实 DOM |
| `/giftshop` | nrt / Bn | 10 商品、原图、ASCII hover；第三方购买未接入 |
| `/changelog` | kst / Bn | 真实列表四条公告；当前捕获分页容器无其他公告入口 |
| `/changelog/:id` | Tst / Bn | 仅四个已捕获真实 ID 的完整桌面 DOM/原图 |
| `/about` | Ist / Bn | 原布局、ASCII speaker、点击本地播放原 WAV |
| `/terms` | Krt / Bn | 原文结构与导航锚点 |
| `/privacy` | Ort / Bn | 原文结构，保留可见网址，属性指向本地 |
| `/acceptable-use` | Nst / Bn | 原文结构 |
| `/church` | Hst / Bn | 原云层/头像/标题/正文/sticky CTA 与滚动算法 |
| `/subprocessors` | Vrt / Bn | 原文结构 |
| `/cookies` | srt / Bn | 实际跳转 `/privacy#cookies`；本地 302 |
| `/styles` | Lrt / Bn | 当前直接访问实际 `Cannot GET /styles` JSON 404；本地同结果 |
| `/polsia/talk` | Prt / Bn | 当前直接访问实际 `Cannot GET /polsia/talk` JSON 404；本地同结果 |

`Bn` 允许进入，但不能证明组件内部没有认证/token 约束；`YH` 对已认证用户另有 dashboard 跳转。`/styles`、`/polsia/talk` 的旧/当前源码均有组件声明，当前服务器真实 404 优先。没有凭源声明构建其不存在的界面或 microphone API。

## 额外实际匿名入口及变体

| 路由 | 路由组 / 组件 | 实测源行为与本地实现 |
|---|---|---|
| `/login` | DRe / fRe | 原 Google/email 视觉；点击清楚显示本地身份能力提示与工作区入口 |
| `/login?from=delayed_signup` | 同一组件的真实状态 | 真实延迟注册 DOM 变体 |
| `/connect` | DRe / ORe | 无 token 时真实“链接已过期”壳；不补造授权连接 |
| `/new` | wst / Qnt | 真实 initial/choice/idea/existing 状态，创建接本地 POST /api/companies |
| `/new/site` | wst / sst | 匿名真实跳 `/login`，本地 302 |
| `/payment/success` | wst / Q$ | 原结果壳；明确为本地样式示例，未发起交易 |
| `/subscription/success` | wst / Q$ | 同原结果壳；明确未接实际订阅/支付 |
| `/payment/cancelled` | wst / gNe | 原取消图标/布局；明确为本地样式示例 |

四个可用公告 ID 是 `79d144a7-1ec2-475c-b0bc-29c7b47437a5`、`646c22cc-83d2-4188-91cc-e60702e3391c`、`2a637515-bb09-4f02-b5d4-24d38a98d972`、`7e7f565e-ed38-4f88-bae9-54d382f4c625`。不猜未来或私有公告 ID。

## 明确排除的源范围

`$se` 和 Wrt 选择 `help.polsia.com` / help.* 的 Grt 路由：`/`、`/guides`、`/faq`、`/:slug`。主域 `polsia.com` 默认选 Yrt；rrt 对 *.polsia.com 禁用 development helpHost override。因此不能把 help 域路径当作主域尚未完成的公共页面。

admin 与 support 路由分别有 et / Or 身份检查及 audience 标记；即使 `/admin/login` 使用匿名入口，也属于管理身份范围。客户 `$u` 路由及组件内保护的 `/settings/vault`、`/settings/browser/:conversationId/:sessionId` 包含真实身份与私有对象约束，当前没有可捕获的匿名业务页面。`/auth/magic/:token`、`/erase-account/:token`、`/join/:uuid`、`/redeem/task-credits/:token` 需要真实 token/对象，不猜、不消费、不构建虚假的成功状态。

当前源码没有 canonical `/campaign` 或 `/demo` 路由。20 个本地已捕获 HTML 变体的内部 href 已定向扫描，没有发现额外匿名 canonical 业务页。外部社交、法律、support mailto、第三方店铺链接保留真实视觉而本地点击提示，不克隆第三方站、不发送邮件或付款。

## 验证状态与下一步

直接 handler 7/7 组、192 请求 PASS；20 HTML、36 原 CSS/字体/图片/WAV 字节与 SHA 一致；2 个真实 redirect、2 个真实 JSON 404、音频 Range206/416均 PASS。隐私段网址的可见文本回归通过。

公开路由/资源实施就绪，当前来源中没有尚未实施且有真实匿名页面证据的 canonical 入口。桌面/手机/交互截图相似度仍由主代理验收；不会仅凭 DOM/资源验证宣称 99.9% 视觉相似。私有 dashboard 视觉仍 `UNVERIFIED`。
