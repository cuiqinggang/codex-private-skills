# Pi V1.3两份DMP精确执行回执

2026-11-11（北京时间）。用户要求只删conhost.exe.11068.dmp及conhost.exe.30308.dmp。

实读V1.3脚本与01-scratch.csv后发现，原清单只有一行，目标为整个CrashDumps目录，Unit=dir；配合-AllowDirDelete实际执行Remove-Item -Recurse，并没有把“两份文件”的文字证据转为文件白名单。未运行该目录删除命令。

改用两条Unit=file精确清单，原脚本不改：预演L1/L2=True、两条would-delete、blocked0。执行前重新核对脚本SHA、清单SHA及文件大小/mtime/inode/完整SHA；原conhost进程均已退出。随后使用V1.3 -Apply执行，不传-AllowDirDelete或-PurgeCaches，exit0，两条deleted，复验两目标均不存在，CrashDumps目录仍存在，其他原有内容未动。

| 文件 | 字节 | SHA256 |
|---|---:|---|
| conhost.exe.11068.dmp | 925553 | 8180df0963c781988d7bd0a21fd6313db0c9be1d69e5a946cdfac08acd2f732f |
| conhost.exe.30308.dmp | 800983 | 7aacfc096d0844af4f6a12e24df5f62f03c86fb3f1c8fbb12a2607f2f9b06875 |

合计1726536字节（约1.65MiB）。执行窗口C可用339702632448→339702894592，净增262144字节；存在其他写入且物理分配不同，不把逻辑量冒充净增。原V1.3 Get-DirBytes对文件目标计为0，GB输出也只有三位小数，因此原生“0GB”不能作未删除或实际字节证据；本次独立计量与存在性复查通过。

原目录清单已备份为K:/Video-Storage-Audit-20261110/v13-original-directory-manifest.csv；Pi包manifests/01-scratch.csv已改为两条精确文件、Status=DONE，重复运行会被状态门挡住。V1.3仍有通用门禁问题：缺Status未必拦截、Unit仅信清单而未验证实际类型、temp-owner未知可能放行。此次适用范围仅为独立验证后的两文件，不签收通用批删READY。

本机证据：v13-two-dmp-plan.json、v13-exact-two-dmp.csv、v13-two-dmp-preview/及v13-two-dmp-apply/原生回执、v13-two-dmp-result.json。Wan原资源停止与52条telemetry已重读，无新Freeze；未恢复服务或投GPU。旧MSIX、75%、完整GUI、8秒状态不变，FINAL_VALID=NO。
