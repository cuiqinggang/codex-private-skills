# 共同经验索引｜V1｜2026-10-27
先读取命中的卡片；下表仅导航。线上根：`skills/reuse-experience-brain/`。
所有业务状态都是注明日期的历史事实；使用前匹配当前环境。原始本机证据不可达时可使用本包历史摘录判断已知边界，不能认定服务当前健康或直接重放有副作用操作。

| 经验ID | 触发词 | 正文 |
|---|---|---|
| EXP-CODEX-001 | Codex、WebSocket、模型列表、stdio、MCP | [CODEX.md](CODEX.md) |
| EXP-STRIPE-001 | Stripe、第三第四行、原配色、标题叠色、hard-light | [STRIPE.md](STRIPE.md) |
| EXP-CALDAV-001 | Tymeslot、CalDAV、取消后缓存、UID、href | [CALDAV.md](CALDAV.md) |
| EXP-VEDA-001 | H3、VEDA、SM75、5帧、水平错块 | [VEDA.md](VEDA.md) |
| EXP-HARNESS-001 | LongHorizon、0.1.8、Windows、killpg | [HARNESS.md](HARNESS.md) |
| EXP-HTTP-001 | Tymeslot、302、登录重定向、健康探针 | [HTTP-REDIRECT.md](HTTP-REDIRECT.md) |
| EXP-DOCKER-001 | Docker、Starting Engine、WSL bootstrap、下次登录、旧PASS | [DOCKER-STARTUP.md](DOCKER-STARTUP.md) |
| EXP-H3-REPLAY-001 | H3、厨房、124帧、同种子、热态复现、图生视频 | [H3-REPLAY.md](H3-REPLAY.md) |
| EXP-VIDEO-AB-001 | 视频A/B、Canvas、FFmpeg、yuvj420p、颜色范围、JPEG优化 | [VIDEO-AB.md](VIDEO-AB.md) |
| EXP-PAYPAL-001 | PayPal中国个人卖家、AI服务、MCC、跨境收款授权 | [PAYPAL-ELIGIBILITY.md](PAYPAL-ELIGIBILITY.md) |
| EXP-GSB-001 | 谷深双擎、DSH V1.6、宿主加载五项、模型回执六项 | [GSB-V16.md](GSB-V16.md) |
| EXP-RENTAL-001 | 租赁、Louez、REA、AGPL、构建不等于业务交付 | [RENTAL-REUSE.md](RENTAL-REUSE.md) |
| EXP-FILESHARE-001 | 本机公网文件分享、Copyparty、免费隧道、本机免登录、访客只读、鼠标拖拽 | [FILE-SHARE.md](FILE-SHARE.md) |
| EXP-DELIVERY-001 | 验收太慢、7分钟、5小时、DSH、本地批量、重复验收、并发启停 | [DELIVERY-EFFICIENCY.md](DELIVERY-EFFICIENCY.md) |

| EXP-PI-001 | Pi、OMP、真实重启、单父执行、双子代理、MCP冷就绪 | [PI-REAL-BOOT.md](PI-REAL-BOOT.md) |
| EXP-BROWSER-001 | 浏览器原页保留、owned tab、全局tab误报、批处理、MCP | [BROWSER-OWNED-TABS.md](BROWSER-OWNED-TABS.md) |
| EXP-VIDEO-ART-001 | 十几年、H3、口型、台词不准、耳光触点、艺术验收 | [VIDEO-ARTISTIC-GATE.md](VIDEO-ARTISTIC-GATE.md) |

| EXP-N8N-001 | n8n、安全通告、2.45.7、镜像digest、工作流Hash、回归探针 | [N8N-SECURITY-20261031.md](N8N-SECURITY-20261031.md) |
| EXP-DEVSPACE-001 | DevSpace、D通道、3秒软期限、只读额外探针、UNKNOWN核账、MCP重连 | [DEVSPACE-D-20261031.md](DEVSPACE-D-20261031.md) |
| EXP-BROWSER-ATTACH-001 | Playwright、connectOverCDP、共享11页、初始化卡住、noDefaults | [BROWSER-ATTACH-20261031.md](BROWSER-ATTACH-20261031.md) |
| EXP-HERMES-BG-001 | Hermes后台cron、订单接续、order-test前缀、PYTHONPATH环境冲突 | [HERMES-BACKGROUND-20261031.md](HERMES-BACKGROUND-20261031.md) |

| EXP-GSB-PI-V2-001 | 谷深V2、Pi Google、DSH显式回退、元数据ACL、旧订单账本 | [GSB-PI-V2-20261101.md](GSB-PI-V2-20261101.md) |
| EXP-PI-LONGFLOW-001 | Pi长流程、RPC goal、会话恢复、MCP冷启动、8小时未验 | [PI-NATIVE-LONGFLOW-20261101.md](PI-NATIVE-LONGFLOW-20261101.md) |
| EXP-OPENMAUS-001 | OpenMausBot、0.1.136、Git checkpoint超时、平台化订单 | [OPENMAUSBOT-20261101.md](OPENMAUSBOT-20261101.md) |
| EXP-WIN-D-V13-001 | D隧道、V13、插件内部错误、临时URL变更、HTTP非MCP | [WINDOWS-D-V13-20261101.md](WINDOWS-D-V13-20261101.md) |

旧资料的继承范围与原日报校验：[INHERITANCE.md](INHERITANCE.md)、[INHERITANCE.json](INHERITANCE.json)。
新增只更新相关卡片及该行；重复事实按来源事件ID去重，保留旧版本与反例。当前没有证据支持的新问题必须明确无命中。

2026-10-31：新增4张脱敏卡，Docker、Pi、视频旧卡只追加当日边界。没有新的明确共享经验adopt/reject原任务回执，不记录虚假复用；完整记忆净T_VALID仍NOT_MEASURED。

2026-11-01：新增4张来自原项目回执的脱敏卡片，分别覆盖Pi＋Google强备V2、Pi原生长流程、OpenMausBot和Windows D隧道插件连通性；Docker与历史DSH卡只增加新的时间边界，旧事件不重复发布。强备V2原RESULT和本机复用日志存在EXP-PI/EXP-BROWSER/EXP-DELIVERY的实际采用，不证明记忆净业务T_VALID提速。正式BRAIN25及历史Freeze不变。

2026-11-02：新增Pi OMP真实升级/研究时限截断、抖音单链接公开回退、Stripe香港资质证据分级3张脱敏卡；Docker旧卡只新增20:08最新故障，不覆盖历史READY。Pi新旧版原对照旧18/18、新17/18与稍后研究2/2+2/2不能互相抹平，00:29实际公开入口已由原项目切换OMP18.15.0。无新独立完整记忆业务T_VALID改善对照，NOT_MEASURED；DSE/执行大脑/原任务Freeze未改。
