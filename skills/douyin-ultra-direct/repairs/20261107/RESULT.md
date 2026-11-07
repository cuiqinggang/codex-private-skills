# 抖音极速直下 v1.3.0 修复验收

日期：2026-11-07，北京时间。

## 根因与修正

23:08:25、23:08:44、23:09:04的三条history均记录NO_URL_IN_CLIPBOARD；并非解析服务故障。原入口只读文本剪贴板，缺少网址也调用备用，再统一弹“解析服务暂不可用”。修复为输入缺失时一次粘贴框、取消静默退出、没有已验证分享链接不调用解析/备用。提取分享文案时跳过无关网址，校验官方抖音域名。有效剪贴板入口不增加交互，GPT明确链接用--url。

原run.py、run-hidden.vbs和旧冻结记录保留；新增run-v1.3.0.py、run-hidden-v1.3.0.vbs；桌面入口已指向新脚本，原桌面入口留存desktop-entry-pre-v1.3.0.vbs。没有修改Windows/代理/浏览器。

## 现实证据

输入：https://v.douyin.com/obhrXk09gEc/
作品：7704557750742715699。

- 原主路显式链接：23:13:01—23:13:17，PASS，程序15.829190秒，证明当前链接解析和下载可用。
- 新桌面入口：测试时暂存原文本剪贴板，写入无链接标记，实际启动桌面VBS，观察粘贴框并输入同链接；input_source=input_dialog，PASS。
- 新程序日志：23:16:04—23:17:17，72.830594秒，其中62.586884秒为输入/自动化等待。不得将此端到端样本剔除等待后声称提速。
- 文件：C:\Users\A\Desktop\douyin_7704557750742715699_20261107-231710.mp4。
- 20,562,883字节；1280×720；228.6秒；H.264视频/AAC音频；原生H.264，未重编码。
- 第一份完整音视频FFmpeg解码退出码0；修复后文件另作全量解码和SHA256对照，机器回执见本机acceptance-v1.3.0.json。
- 已在Windows Media Player实际打开并观察到本视频画面；听感及主观同步不能通过截图或文件解码推定，保持NOT_VERIFIED。
- 5项链接提取回归通过：完整分享、无关网址在前、纯文本、伪装域名、非抖音网址。
- 测试器首次窗口等待超时，后来沿同一个已启动的粘贴框完成；不将这次测试自动化故障归给下载器，也不隐去等待。

## 恢复

沿原技能恢复既有依赖和核心后，将本目录run-v1.3.0.py放入C:\AI\Douyin-Ultra-Direct。桌面“抖音极速直下.vbs”使用下面的ASCII文本；先保留当前入口。解释器必须是本机已安装的Python313，不安装新运行时。

```vbscript
Set sh = CreateObject("WScript.Shell")
cmd = Chr(34) & "C:\Users\A\AppData\Local\Programs\Python\Python313\pythonw.exe" & Chr(34) & " -X utf8 -B " & Chr(34) & "C:\AI\Douyin-Ultra-Direct\run-v1.3.0.py" & Chr(34) & " --interactive"
rc = sh.Run(cmd, 0, True)
```

回退仅恢复desktop-entry-pre-v1.3.0.vbs到桌面入口。不要回退当前新编号D连接，不启动浏览器，不修改网络设置。恢复后先做语法检查和输入回归，仅在用户要求下载时进行同链接现实下载。

CodeGraph：非Git本机应用目录，无.codegraph索引；按明确函数定向阅读和修改，未进行全库扫描。
Knowledge Brain：已读INDEX、ROUTING_MAP、skills-index及长期记忆入口；本机证据保存在原应用目录，公共恢复配方在本技能原目录的版本化修复区。
