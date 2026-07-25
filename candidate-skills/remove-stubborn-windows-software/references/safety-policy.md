# 安全政策

## 证据类别

| 结果 | 判定 |
|---|---|
| `ABSENT` | 无目标 ARP/MSI 项、目标进程、目标服务/驱动、目标计划任务或目标安装根活跃证据 |
| `ACTIVE_PRODUCT` | 至少一个目标产品或可验证活跃组件仍存在 |
| `KNOWN_VENDOR_RESIDUE` | 产品入口已消失，但保留有有效厂商签名且被厂商/官方案例确认的残留 |
| `UNKNOWN_BLOCKER` | 来源、签名、归属或安全删除方法无法证明 |

`KNOWN_VENDOR_RESIDUE` 不能描述成“彻底删除”。如果用户的成功条件是零残留，它也是未通过。

后置 inventory 必须绑定卸载前 baseline 的 SHA-256，并沿用 baseline 中的精确安装根、进程路径、服务/驱动名、任务路径+名称及启动位置+名称。ARP 项消失不能清空这些观察目标。只有经过单独审核的 known-residue manifest 可把精确 evidence id 从 `UNKNOWN_BLOCKER` 提升为 `KNOWN_VENDOR_RESIDUE`；该 manifest 不授权删除。

## 允许自动执行

- 精确 MSI ProductCode 的 `msiexec.exe /x`。
- inventory 中存在、Authenticode 状态为 `Valid`、SHA-256 未变化的厂商卸载器。
- 发布者字符串与签名证书指纹同时匹配本轮人工批准的映射；计划把发布者、指纹和文件哈希一并绑定。
- 厂商卸载器原有、已记录的参数。

执行前重新验证机器、用户、计划有效期、计划哈希、文件哈希与签名。任何漂移即停止。

## 永不自动执行

- 对 `.sys`、DriverStore、注册表、Program Files 或 ProgramData 做通配/递归删除。
- `takeown`、宽泛 `icacls`、禁用系统保护、关闭杀毒防护或测试签名模式。
- 仅凭文件名、路径片段或网络帖子删除驱动、服务、任务或证书。
- 执行 inventory 中没有的卸载命令。
- 把 PowerShell、pwsh、cmd、wscript、cscript、mshta、rundll32 或 regsvr32 等系统 LOLBin 当成厂商卸载器，即使其系统签名有效。

人工批准映射使用：

```json
{"schemaVersion":1,"publishers":[{"publisher":"Exact Publisher","thumbprints":["UPPERCASE_CERT_THUMBPRINT"]}]}
```

注册表中的 `Publisher` 不是信任根；只有它与人工映射的 exact publisher、实际 Authenticode 证书 thumbprint、文件 SHA-256 同时匹配，且入口不是 LOLBin，才可进入计划。计划仍需用户对本轮 `planHash` 明确批准。
- 为“清干净”安装第三方清理器。

## 重启合同

输出：

```json
{
  "type": "rebootRequest",
  "reason": "vendor-uninstaller-requested",
  "resumeStep": "reinventory-and-verify",
  "evidencePath": "removal-result.json"
}
```

由调用方决定是否批准重启并用跨重启适配器 Arm。本技能不得自行重启。
