# F015｜Open WebUI 已打开浏览器：不新启浏览器的最小GUI接入Gate
继承 HERMES-ECO-F014-20261015；方法《三人行》V2；V6连接桥C先；F011业务CLI优先、UI专属才GUI。STATUS=VIRTUAL_MATURE_FROZEN。

历史成熟基线：Codex原技能 C:/Users/A/.codex/skills/hermes-mature-supertool-recovery-upgrade/SKILL.md V1.3.0 与 references/OPENWEBUI-MODEL-SELECTOR-REAL-UI-RECOVERY.md，2026-08历史有WebUI真实可视化交互/模型切换验收，但当前2026-10只确认本机3000/health200、Chrome进程存在，不能继承整个网页当前PASS。
真实目标：在已有的、用户正在使用的已登录Chrome/Open WebUI会话中发布一次合成最小聊天任务，确认页面可见消息/模型回执，不改变浏览器实例/登录态/代理/凭据。
成熟路线：先只读查已有Chrome CDP (127.0.0.1:9222/json/version) 是否由现有进程合法提供；若有且确认为同一当前用户已授权的Chrome，可用既存 Playwright connect_over_cdp 附着，不新启浏览器；无CDP则不用重启Chrome/开启第二实例/读取cookie/注入调试参数，记GUI_CONNECTION_PENDING。不能仅依据 health 200 判网页聊天通过。
在具备可控真实GUI且归属/权限清楚时，只执行一次小消息，用户原标签页不关闭、不清除历史；独立可见文本和后台真实模型回执一起核验。缺任一不把UI标PASS。不得用命令直打后端接口伪装网页操作。
本次只读发现若无合法GUI通道则自然结束，保留F010正式CLI业务PASS与F014技能发现PASS，不阻断无GUI依赖的其他能力门。
