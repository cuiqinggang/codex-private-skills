# 2026-10-16 19:55 恢复与最小修复验收

## 结论
原主路线已经恢复。用户19:48双击入口的真实记录为 API_PRIMARY / PASS，5,721.448ms；成功输出作品7694210317173856083，1038×576，28.733333秒，5311801字节。
19:50对原失败链接x2jZ6T5FqOQ及用户成功链接4rrBqCl4KtY分别只做解析，均PASS，约3322.881ms及2931.170ms。
同输入在未修改原主程序时由502/503转为成功，支持第三方解析端此前临时异常、随后恢复；没有证据支持“作者允许下载反而导致失败”。没有核验作者原生下载开关本身，不能编造该字段。

## 两条成功路径
- 之前：Seekin网页解析→C通道curl保存→ffprobe及完整FFmpeg解码，桌面文件已经保留。
- 本次：原API解析→原官方direct URL下载→原验收保存，未启动浏览器。
不能把云端Seekin成功解释成本机Seekin自动适配已通过；此前未通过候选保持历史，不激活。

## 已部署 v1.2.1
保留原API、session复用、选流和官方direct优先路线。
1. 仅幂等解析请求遇502/504时最多额外重试一次，间隔1秒；503或ENDPOINT_CIRCUIT_OPEN不连续重试，记录http_status/code/retry_after。健康调用无等待。
2. 成功和失败逐次保存history，最后结果原子更新last_run.json；不再只剩最后一次记录。
3. 旧备用显式继承本次分享链接，避免GPT参数和剪贴板输入不一致；从主入口调用旧备用时禁止启动浏览器，仅使用原SSR适配。备用exit0还必须核验输出文件及媒体元数据。
4. 桌面VBS等待子进程退出；失败使用Windows原生WScript.Shell.Popup提示10秒。文件使用UTF-16 BOM，正式入口与根目录入口一致。
5. 仅增加DOUYIN_OUTPUT_DIR用于隔离验收；普通双击仍保存用户桌面。没有改变FlClash、系统代理、权限、浏览器或已有业务。

生产备份：C:/AI/Douyin-Ultra-Direct/followup-backup-20261016-195502/。
生产run.py SHA256（Windows原始字节）：03c355eaa5dd0fc404497664e6d550370eb3f0f93d6a2b6bcc246c011554b802。
恢复包包含legacy_direct_save.py；仅已有旧备用安装存在时恢复它，不重建浏览器。restore.ps1已用Windows PowerShell5.1原生Parser检查：exit0；未执行整套恢复部署。

## 真实验收
19:55再次从原失败链接完整执行，主程序exit0 / API_PRIMARY / PASS。
输出至程序work/followup-acceptance-20261016，避免重复发布桌面文件。
原程序内部T_VALID_MS=4467.767；该数字不包含工具往返、后续全量解码、提示测试和文档保存，不是本次完整任务墙钟或物理极限。
720×1280；31.114739秒；2848345字节；H.264+AAC。
完整音视频FFmpeg解码exit0。
SHA256=d50c9c3a8b701068210c69a1a7116ecaf89d451fb212f08dcf78c46210e994e3，与之前桌面文件完全一致。
正常原始文件路径：C:/Users/A/Desktop/douyin_7669298890101094769_720p.mp4。
实际VBS失败提示分支使用隔离假失败命令测试，1秒自动关闭，cscript exit0，FAILURE_NOTIFICATION_BRANCH_PASS；没有额外视频下载。
七项确定性回归PASS：健康不等待、502一次重试恢复、连续502有界停止、503熔断不重试、历史不丢失、备用继承显式输入并核验文件、禁用旧备用浏览器启动。
验收记录：C:/AI/Douyin-Ultra-Direct/followup-acceptance-20261016.json；用户成功记录：user-success-20261016-194804.json。

用户常用播放器实际画面/音画同步未由本页面目视，保持PLAYER_PLAYBACK_NOT_VERIFIED。没有进行作者下载开关的受控A/B实验，不把故障恢复夸大为所有链接永久无故障。
