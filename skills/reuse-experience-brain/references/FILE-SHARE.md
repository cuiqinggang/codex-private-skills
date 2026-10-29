# EXP-FILESHARE-001｜本机免登录管理与公网只读隔离、真实拖拽验收
版本V1；核查2026-10-29；类别CASE/ERROR/CANDIDATE_RULE；原任务AIORG-FILESHARE-20261029-001与AIORG-FILESHARE-DRAG-20261029-002。
触发：本机文件夹直接分享给外网、拖入文件后公网可下载、文件服务器本机免登录而访客不得上传、HTTP检查通过但用户实际拖拽失败。
环境：Windows10、C:\AI\Public-Server、官方Copyparty v1.20.26、已有cloudflared免费隧道、既有Windows任务计划；Copyparty官方单一源站。当前公网随机域名每次隧道重启可能改变，不在卡片保存历史地址供下次使用。
LAST_GOOD：本地及公网HTTP接口各27/27，验证匿名仅只读、本机上传字节、下载Range 206、ZIP及中文名、私有卷与凭据不可读、受保护分享、异常来源头与跨站本地写入拒绝。
FIRST_DELTA：原HTTP 27项从未操作Windows鼠标拖拽，用户真实拖入网页未见文件；同时免登录owner和公网访客若走同一IPv4回环来源可能混淆身份。
最小成熟修正：不自研网盘，采用Copyparty现成IP账户映射与权限、IPv4 127.0.0.1只给本机owner，IPv6 ::1仅作为cloudflared访客源站；桌面增加Windows原生文件夹目录联接，本机Ctrl+鼠标拖入该目录即由既有shared卷提供公网读取。
回归：2026-10-29 18:43+08和18:46+08本机与公网27/27 API PASS；20:09+08实际Windows原生鼠标Ctrl+拖放合成文件，源保留、文件字节一致、目录联接指向真实shared、外网下载SHA一致，公网仍匿名只读。网页浏览器鼠标拖拽因控制超时NOT_VERIFIED，不能将原生目录拖拽/HTTP API认证扩大为浏览器拖拽PASS。
边界：本机配置与公网访客行为实测仅限该环境；真实Windows重启自动恢复、异网手机交互、大文件及全部媒体类型、实际密码链接到期、生产长期安全与完整T_VALID均未认证。用户私有数据不得放入公开shared；原生目录联接不是OS安全沙箱。新订阅=0，不等于总运行成本0。
实际复用：原文件分享FINAL回执的experience字段记EXP-DELIVERY-001/V1 adopted（继承已通过节点、同实例单控制者、不因应用故障误切Windows通道）。这是受限项目行动采用，不是记忆改善完整T_VALID的同合同对照。
原始证据（C盘原位）：C:\AI\Public-Server\file-share-final-acceptance.json、file-share-drag-acceptance.json、share-upgrade.json、status.json；专业入口skills/ai-automation-organization-v5/references/file-share-v2.md及同目录验收JSON。状态以最新原回执而不是本卡历史快照为准。