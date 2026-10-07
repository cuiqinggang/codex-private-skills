# 抖音极速直下 v1.1 — 快速恢复合同

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
