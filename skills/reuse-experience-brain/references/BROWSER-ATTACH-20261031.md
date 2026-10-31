# EXP-BROWSER-ATTACH-001｜共享Chrome连接成功但Playwright全页初始化卡住
版本：V1；核查：2026-10-31；分类：CASE/ERROR/SKILL_CANDIDATE；证据：原专用浏览器权威技能源核对与真实项目回执。

触发：DSH/SDK尝试connectOverCDP附着已有共享浏览器，MCP握手、WebSocket或单页CDP元数据明明返回快，却出现整体附着超时。环境：原持久Chrome/Profile和多页面并存；原任务AIORG-CROSSWEB-20261031-001。
LAST_GOOD：原Chrome/PID、既有身份与9223调试端口仍存在；Page.getFrameTree单页低于0.01秒。
FIRST_DELTA：官方SDK等待现有全部页面的waitForInitializedOrError，内部Promise.all形成全页耦合；不同目标的Page.enable、createIsolatedWorld等初始化可能不返回，导致connectOverCDP约7秒至30秒后失败。**不是已证明的外网断线**，更深触发页面/插件/版本未定。
候选修复：先回权威C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\SKILL.md、MATURE-OPERATIONS-CONTRACT、CDP-9223-SOURCE-RECOVERY，核对当前浏览器所有者与persistent启动/附着契约。noDefaults单次0.912秒附着曾成功，但后续临时页写入阶段再次超时，不能推广。
现实结果：primary限定公开只读PASS（150.663s），备端NOT_VALID，主端失效后接续NOT_TESTED；测试自有进程树停用，原浏览器、Profile及无关页面保留。
适用：同一Playwright共享CDP/多页环境、接入层首次差异诊断；不适用：断言特定网页永久坏、直接关所有tab、重启原共享浏览器、将Pi正式MCP某次单页PASS当作DSH备端PASS。
源：C:\Users\A\Documents\DSH-Workspace\aiorg-crossweb-20261031\SOURCE-INHERITANCE-REPORT.md、FINAL-STATUS.json、R5-STOP.json。