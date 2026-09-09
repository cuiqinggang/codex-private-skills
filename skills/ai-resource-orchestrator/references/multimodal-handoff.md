# 已实测媒体交接范围（2026-09-09）
入口：现有 playwright-native-ai-browser 正式技能；先读其合同。ARO 只选择资源，不另建浏览器、控制器或传输服务。

## 本机本轮通过的业务
- PNG 原图：随机短码、位置/形状及表格数值盲测；现有网页 GPT 处理并回传 1280×960 PNG，控制端独立解码、核对尺寸及像素对应。
- 原 MP4：9秒合成视频、3段视觉事件与2段音轨；接收方工具分析原文件，正确给出随机码、视觉顺序、实际边界3.2/6.2秒、音调440/880Hz及时间。
- 按接收方实际分析截取第二段：实际取回3秒MP4，全部视频帧和音频采样独立核验。
- query → send → wait_extract 必须原样复用正式 scripts/chatgpt-business-entry.js；恢复先 query 原 marker，ALREADY_RECEIVED_NO_RESEND 不算新提交。

## 附件与成果动作
附件上传与下载使用现成浏览器工具，提交/查询/取回答案仍由原正式业务入口负责。每次以实时页面检查实际控件及上传完成状态，不按旧坐标硬点。
文件名或本地路径不是附件送达证据。下载链接须在代码块外；本机PNG文件卡先打开预览，再点击预览内“下载”。打开预览无 download 事件不是文件生成失败。
保存实际文件后独立解码，检查预定通过标准。以本任务 manifest 记录原件、派生、成果、大小、哈希、来源、有效句柄，以及 INPUT_RECEIVED / CONTENT_UNDERSTOOD / TOOL_EXECUTED / OUTPUT_RETURNED / OUTPUT_VERIFIED。
只有两端原始字节实际可取并核对才称 BYTE_IDENTITY=VERIFIED。传输、分析、业务加工和逐字节保真分别判定。

本轮另外取回接收会话中的原 PNG（5823字节）和 MP4（24220字节），控制端与源逐字节比较及 SHA-256 一致；BYTE_IDENTITY=VERIFIED 仅覆盖这两个原件。

## 限制
以上仅对所测 PNG 和9秒MP4及本次网页入口成立。它不是艺术制图、长视频、所有格式或永久可用声明。VIDEO_DERIVED 本轮未调用，不以本地生成帧冒充接收方派生资料验收。
网页可见选择状态不证明请求模型/力度；本轮相应字段 UNKNOWN。Reasonix 文本入口不因菜单有vision名字就获批多模态能力，其附件能力必须单测；原生 write_file 受权限策略拒绝仍为 BLOCKED，不能用网页或Codex成果代替。
验收与失败复盘：[最近使用记录](../USAGE-LOG.md)。
