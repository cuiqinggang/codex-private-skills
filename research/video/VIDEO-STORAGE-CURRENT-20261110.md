# 视频空间整理 CURRENT — 2026-11-10

任务：VIDEO-STORAGE-20261110；接续BLUE8 Wan8秒；状态：DELETION_POLICY_ACTIVE / BROAD_MIGRATION_CANCELLED / FINAL_VALID=NO。

## 已完成
- 已回读高品质视频主包与Wan V1.4，新增[试运行及空间治理V1.5](../../skills/video-extreme-time-engine/references/BLUE8-WAN-TRIAL-STORAGE-V1_5-20261110.md)，主包已指向新记录。
- 视频定向盘点30个目录（其中空目录也列入），逻辑总大小413834681416字节（约385.4GiB）。大文件存在约34GB已识别硬链接重复，不能把逻辑路径大小当物理占用；没有完成C盘所有其他业务目录全盘审计。
- 最大目录：MiniMax-H3 194558912519字节；Star7-Manual70095455713；S2V当日目录66195196373；Aaki42906874268；MuseTalk16658826801。技能/文字不是大头，禁止通过删除经验凑比例。
- 已删除9条精确废弃下载路径：旧S2V镜像.part、Wan两条.download及三条.incomplete、H3 BITS三个.tmp。含同一inode的多个路径，去重后约66037825897字节；磁盘初值93885284352可用字节，清理后约159812374528字节，净增约61.4GiB，受同时其他任务写入影响。
- BITS临时文件完整SHA与正式模型不同，不标为重复；抽查中尾数据零填充，无当前BITS任务引用。保留下载头、大小、mtime、inode、双SHA、删除清单。正式模型保留。
- 新Wan主模型已官方SHA验证；81f预处理原生14:09:548完成。本页查看第0/40/80帧JPEG，低头/合手骨架和含嘴面部裁剪抽查通过；非逐帧全验，未生成合格8秒。

## 正在运行的精确迁移
本机证据根：K:/Video-Storage-Audit-20261110。
计划action-plan.json，sha256=7ebbc8375438c379ce241253af77c55e558021be4a002f9a61211478b7684c26。
现有execute-plan.py将7个模型目录、212个文件、235664430879唯一字节迁至K:/Video-Assets-20261110镜像路径；K是USB盘，完整复制/哈希复核耗时不能当故障。
仅在源身份/大小/mtime未变、目标完整SHA与复制源流SHA相等、全树文件集合一致后，逐文件移除C原件，再删除空目录并建立原路径junction；跨树hardlink按原inode在K保留共享。逐文件事件写actions.jsonl，全树回执写migration-receipt.json。现未将迁移计划字节计入实际释放。
原活跃Wan新权重、H3 .venv、原素材、技能、工作流、小体积错误证据保留。Aaki UMT5模型目录迁移后依原路径junction继续访问，必须复验。75%是目标，不能将迁移冒充永久删除，也不能为比例删除唯一有效资产。

## 接续与验收
- D20261110-02 open_workspace本页实际超时；A Remote Desktop Commander已读写执行成功，DESKTOP-4A1EGTM，device f6990966-5870-484b-bf79-409bc6fb963e。不中断其他ECC/Pi业务，不改代理。
- 迁移创建时wrapper32972、child33572；恢复必须重新核cmdline/创建时间与I/O，不能凭旧PID。运行中不启动第二迁移/GPU。目标已存在时禁止盲重跑原executor；按plan/actions/hash精确接续。
- LOOP-CONTRACT.json、STATE.json、RUN-LOG.jsonl负责跨轮接续；先读实际状态，正常I/O推进时等待。完成后逐一复核212原路径、7junction目标、共享.pth和UMT5及实际GUI入口，再报实际物理净释放和比例。路径计数不等于实际分配字节。
- Browser本页初始化超时；尚未完成迁移后GUI验收，不报PASS。不要用云端桌面冒充用户本机。
- 迁移完成后读取原Wan CURRENT、queue/history/intent，按原submit_stage.py接续81帧；没有intent才允许唯一新提交，RAM准入<80、原守护不放宽。短段质量合格再193控制裁192、608×83224fps8秒保留原声，并在本机播放器验收。
- 全部失败、安装、下载、清理/迁移、恢复和验收计入完整时间，未测T_VALID保持UNKNOWN。

## 恢复注意
长文件名须使用Windows长路径前缀。目录枚举缓存/硬链接目录项可能显示旧长度或零长度，需open句柄后的os.fstat复核，不能据目录缓存认定文件损坏或复制没有进度。已完成清理的bits-clean-result.json与longpath-transfer-result.json不可重做。7个迁移目录不含新Wan模型或共享Python环境；副本校验未成功前C原件不删除。此记录与计划归档不代表迁移、空间比例、GUI或作品验收完成。

## 可复用候选与原件
精确适配脚本已保存：[计划生成](storage-20261110/build-plan.py)、[守卫执行](storage-20261110/execute-plan.py)。它们是本次固定路径、固定计划合同的运行/恢复原件，不是通用磁盘清理器；状态CANDIDATE_RUNNING，未完成迁移后GUI及独立复验，不登记READY。禁止把脚本改成宽泛目录删除或在另一台电脑原样调用。当前已核现有worker命令、创建时间和连续I/O（一次3秒增加218103808字节）；状态WAITING仅表示本轮等待现有迁移推进，不表示任务关闭。

## 用户纠正后现行规则（覆盖上述运行中迁移安排）
用户明确：未证明有帮助且已弃用的模型应直接删除，不能搬K继续占空间。已核worker身份并停止原execute-plan.py（PID33572，stopped=true），保存MIGRATION-CANCELLED-BY-USER.json；禁止恢复旧7目录批量迁移，也不能把已删除模型按旧计划恢复。
已完成3个目录junction，其余保留C源。旧复制产生的17976786944字节未完成K副本已删除，完整Star7源仍在C。
新增永久删除：S2V BF1632591643778字节、FP816394832474字节、该弃用路线音频编码器630997322字节；W4A8候选12540858008字节及1533字节下载sidecar（本机同规格更慢、未晋级）；被INT4 ConvRot替代的NVFP4编码器15687142551字节。分别保留真实失败/比较证据，不能说这些文件均为字节损坏；依据是本机路线弃用且对当前任务无帮助。当前Wan配套与已验证INT4基线保留。
本轮另清掉2份已证截断旧权重，共3282042880字节：按Safetensors头中data_offsets得应有完整长度，均大于实长；无下载进程，且不属于迁移计划。extra-clean-result.json有回执。
退役删除前后C新增可用49617481728字节、K新增46204792832字节（含取消复制副本）；不把先迁移后删除在两个盘重复算成同一份原资产收益。C当前可用约288.4GiB，最终实测以STATE为准。删除精确计划/指纹/身份/原因在delete-retired-models-plan.json与result.json。
已迁移3树原54路径中，退役3项是预期删除，剩余51项继续检查。实际GUI：Chrome访问8198得到HTTP403；本机直连root/queue/object_info=200，说明服务后台可达，不是GUI验收通过。未改代理，不绕过403，不伪报保留工具全部可用。剩余有效性审计、GUI与8秒仍未完成；75%目标不报通过。当前规则已写入接续任务，防止旧自动流程重新搬运弃用资产。
