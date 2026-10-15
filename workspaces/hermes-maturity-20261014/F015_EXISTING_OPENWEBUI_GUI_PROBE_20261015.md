# F015｜已有 Chrome / Open WebUI GUI 合法附着探针
2026-10-15｜HERMES-ECO-20261014｜《三人行》V2｜V6桥C｜前置：F015_EXISTING_OPENWEBUI_GUI_GATE_FREEZE_20261015.md。
本节点是独立WebUI可见交互门的前置只读探针。以前本机http://127.0.0.1:3000/health返回HTTP200，Chrome进程运行；这两项证明网页服务/浏览器存在，绝不能视为网页登录或实际聊天PASS。
采用既有成熟Playwright/Chrome CDP**仅附着已存在会话**的方案：只读探测127.0.0.1:9222/json/version端点，未携带密钥、未读取Cookie、未启动第二浏览器、未改变Chrome命令行或代理。
实际结果：NO_APPROVED_CDP_ENDPOINT，Windows进程退出码0（已捕获连接失败作为结论），process runtime27.09s。当前没有已核实的可用Chrome CDP入口供控制现有打开标签页；不能用启动新浏览器/重启Chrome开启调试端口来绕过用户明示边界。
当前 F015_GUI_E2E=PENDING_LEGAL_GUI_ATTACHMENT：没有真实发送聊天消息、没有图片上传与模型选择可见交互、没有网页独立回执。不得通过CLI文本回答或服务健康200充当WebUI UI E2E验收。
无需让所有工作因F015阻断；F010正式CLI Repair8/8、F013原生技能发现171、F014跨Codex/Knowledge按需检索及官方KB Health PASS都独立继承。若后续有获准的现有UI附着工具/用户交互机制，再继续同一冻结合同，不重复启动新服务。
原F002综合五轮0/5，整站FINAL_VALID=NO。其它长稳/音视频/Session恢复未证实。F011安全静态仍单YAML模式告警，不会在这项UI工作中解决。
