# 失败复盘：Cursor 3.13.10 + Claude Code + DeepSeek V4 Pro

## 1. 旧中文化脚本不能直接套用

症状：Cursor 更新后顶栏恢复英文，旧版本脚本找不到签名。

原因：3.13.10 工作台压缩代码的 mnemonic 表达式发生变化，且更新覆盖 `resources\app`。

规则：版本严格门禁；先统计七项唯一匹配，再备份、替换、更新校验和。未知版本禁止扩大正则盲改。

## 2. 整桌面截图会掩盖真实状态

症状：其他窗口、视频和打印窗口覆盖 Cursor，无法判断命令面板是否打开。

规则：枚举 Cursor 的 `MainWindowHandle`，只截取该句柄对应窗口；每次仅执行一个动作并复查。

## 3. 快捷键误打开 Windows 打印窗口

症状：使用不可靠的窗口激活后发送快捷键，操作落到其他窗口。

规则：先按句柄 `SetForegroundWindow`，必要时点击 Cursor 内安全空白区域，再发送 F1；截图确认后才输入命令。

## 4. 未加载 Windows Forms 导致 SendKeys 失败

症状：`Unable to find type [System.Windows.Forms.SendKeys]`。

规则：调用前执行 `Add-Type -AssemblyName System.Windows.Forms`；失败后不能声称按键已成功。

## 5. 中文提示词没有进入 Claude Code 输入框

症状：脚本报告已粘贴，但截图显示输入框仍为空。

原因：焦点落在编辑器或聊天正文。

规则：按窗口矩形计算 Claude Code 输入框坐标，点击后粘贴；发送 Enter 前必须截图确认完整提示词可见。

## 6. Claude Code 页头看不出实际模型

症状：页面只显示 `Claude Code` 和 `Manual`，用户无法确认是不是 DeepSeek V4 Pro。

原因：扩展不显示自定义 Anthropic-compatible endpoint 模型名；`Manual` 是权限模式。

规则：生成安全路由证明并与回答并排显示；模型自报不是证据。第二轮必须让 Claude Code 调用 `Read` 读取证明。

## 7. 用户批准持久化，但执行安全策略不允许

症状：用户允许把 DeepSeek Key 写入 User 环境变量，但代理安全策略禁止持久写入云服务凭据。

规则：权限批准不能覆盖执行安全策略。使用 SecureString 输入和进程级变量；报告 `credential_persisted=False`，不得伪称已持久化。

## 8. 资源写入需要用户手动执行

症状：代理无法直接修改 Cursor 安装目录。

规则：先生成带备份、版本门禁和回滚信息的脚本；由用户在 PowerShell 手动运行；代理读取 JSON 输出并进行独立截图验收。

## 9. 模型验证不能只看配置

症状：环境变量看似正确，但无法证明实际调用成功。

规则：必须执行最小真实调用并保存退出码与非空固定返回。配置证据、真实调用和 UI 实际回答缺一不可。
