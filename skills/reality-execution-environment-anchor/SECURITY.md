# 安全规则

## 远端零秘密
禁止把以下明文上传到仓库或任何远端安全镜像：
- 密码、API Key、Bearer、OAuth、Token
- Cookie 值、Authorization / Proxy-Authorization
- 代理用户名/密码
- 完整 storageState
- 原始 Trace/HAR/CDP 网络正文
- WebSocket 消息正文
- 可能包含凭据的完整浏览器命令行

远端只允许：
- presence（存在性）
- 类型/数量/长度
- SHA-256
- 已脱敏 URL/事件
- 文件大小、时间、结构摘要
- 不包含秘密的版本、状态与配置元数据

## 本机 raw
Browser R3 可为了精确 Reality 在本机 `raw/` 临时保存：
- trace.zip
- storage-state.json
- raw CDP JSONL
- DOMSnapshot
- HAR（若真实 harness 原本启用）
- 原始浏览器/网络宿主证据

这些原始文件不得由发布流程自动提交 Git。

## Reality 安全边界
采集期间禁止为了观测而修改：
代理、网络、Cookie、Profile、Service Worker、cache、route/mock、DOM 或网站状态。
