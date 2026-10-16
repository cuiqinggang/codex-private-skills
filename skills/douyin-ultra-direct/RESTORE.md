# 抖音极速直下 v1.2.1 — 快速恢复合同

## 权威来源

REPO=cuiqinggang/codex-private-skills
PATH=skills/douyin-ultra-direct/

恢复时必须先读取：
1. SKILL.md
2. RESTORE.md
3. R2_REALITY_FREEZE.md
4. run.py
5. run-hidden.vbs
6. restore.ps1

禁止先从零搜索新下载器。

## 恢复目标

恢复后用户操作必须仍为：

复制抖音分享文本/短链
→ 双击桌面“抖音极速直下”
→ 自动在桌面生成有效 MP4

并保留 GPT 入口：
复制链接 → 对 GPT 说“下载抖音”。

## 最短恢复

若技能包文件已在同一目录：

powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\restore.ps1

restore.ps1 只做确定性恢复，不执行正式视频下载 Reality。

## restore.ps1 应完成

- 创建 C:\AI\Douyin-Ultra-Direct
- 部署 run.py
- 部署 run-hidden.vbs
- 部署 SKILL.md / RESTORE.md
- 创建/覆盖桌面 C:\Users\A\Desktop\抖音极速直下.vbs
- Python py_compile
- 检查 curl.exe
- 检查 ffprobe.exe
- 不创建或写入任何密钥
- 不修改网络代理

## 依赖

必须存在：
- Windows
- Python 3
- curl.exe
- ffprobe.exe

session.cookies：
- 可以不存在；
- 首次运行由程序自动登录并生成；
- 不进入仓库。

旧成熟 fallback：
C:\AI\Douyin-Direct-Save-Windows\Douyin-Direct-Save.cmd

若不存在：
- 不阻止主路恢复；
- 只代表 fallback 暂不可用；
- 不得为了 fallback 阻塞主路。

## 静态门禁

恢复完成后只做：
- run.py py_compile；
- 桌面入口存在；
- run-hidden.vbs 与桌面入口内容一致；
- curl/ffprobe 可发现。

默认不自动下载测试视频。

## Reality

只有在以下情况做：
- 用户明确要求重新认证；
- 外部 API/CDN 已发生变化；
- 静态恢复成功但真实下载出现失败。

Reality 仍遵守：
连续虚拟成熟 → Freeze → 1次 Reality。


## 2026-10-16恢复补充

必须同时取得新版run.py、run-hidden.vbs、legacy_direct_save.py、SKILL.md、RESTORE.md和restore.ps1。新版restore.ps1将VBS写为UTF-16 BOM，避免中文失败提示在Windows Script Host中损坏；仅已有C:/AI/Douyin-Direct-Save-Windows/src/direct_save.py存在时，先备份再恢复安全备用入口，不新建下载器或浏览器。

正常下载仍走原API和官方direct；备用SSR失败时不启动第二浏览器。history保存逐次结果，last_run.json只代表最近一次。503/ENDPOINT_CIRCUIT_OPEN记录服务冷却时间并有界失败，不无限等待或反复请求。恢复后的性能数字不能套用历史最快样本；当前复验证据见repairs/20261016/FOLLOWUP_1955.md。新版restore.ps1本轮仅完成PS5.1语法验收，未重新部署恢复整套环境。
