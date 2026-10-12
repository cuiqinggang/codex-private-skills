# Polsia 公开资产接续恢复

此包恢复本轮公开页面使用的 36 个原始资产。恢复脚本和独立 manifest 必须保存在同一目录；不要单独修改 manifest 或重新计算 pin 来接受上游变更。

## 接续顺序

在新的项目目录执行以下命令。这里只说明未来接续步骤，本轮未执行 clone 或资产下载。

```powershell
git clone https://github.com/AI-Builder-Club/open-polsia.git open-polsia
Set-Location open-polsia
git checkout --detach c62ba0be3368815dc9011848d96875ef228f1607
```

先将本交付包的文本 source overlay 按原相对路径复制到这个新 clone，包含 `src/services/public-page.ts`、20 个页面 HTML 与 `local.css`、`local.js`、`states.json`。其他业务源文件与依赖按交付包主说明恢复；此资产脚本不复制源文件、不启动数据库或站点。

保持当前工作目录为新 clone 根目录，使用 Node.js 24 调用接续包中的脚本。下列路径由接手者替换为交付包实际位置：

```powershell
node <交付包绝对路径>/source-snapshot-restore-assets.mjs
node <交付包绝对路径>/source-snapshot-restore-assets.mjs --apply
node <交付包绝对路径>/source-snapshot-restore-assets.mjs --verify-only
```

第一条只读输出缺失清单；第二条核对 Git HEAD、handler 和 23 个文本文件的 SHA，下载缺失资产；第三条只读核对全部 36 资产与 23 文本。恢复成功输出 `PASS_RESTORED_ALL_PINNED_ASSETS`；只读完整核对成功输出 `PASS_ALL_ASSETS_AND_TEXT`。

## 支持边界

- 仅写入新 clone 下固定的 `public/polsia` 平面 allowlist；目录必须已经由文本 overlay 建立。
- 现有 SHA 与大小精确匹配的资产直接复用。现有不匹配资产返回 `BLOCKED_EXISTING_ASSET_MISMATCH`。不提供覆盖功能，`--replace` 直接拒绝；请另建干净 source 目录，不删除或修改旧目录。
- 候选文件先全部下载到同目录 `wx` 临时文件，逐项验证来源、字节数、SHA 并 flush；全部候选通过后才安装。
- 安装缺失目标使用 `link(temporary, target)` 的原子 no-clobber 语义，再移除临时名字。并发创建目标会使安装失败，不使用会覆盖现有文件的普通 rename。
- 应用阶段使用 `wx` 互斥锁；不自动删除既存锁。拒绝重解析目录、符号链接和目标硬链接。失败只清理仍匹配本次身份和内容的自有新文件；发生目录或文件身份变化时保留现场并报错。
- 仅访问 manifest 中固定公开 HTTPS 资源，拒绝重定向；最大单文件 25 MiB。上游字节发生变化时停止，不放宽 SHA 或改抓其他来源。
- 不读取账户或凭据，不改变系统、PATH、代理、网络设置或服务，不启动模型任务，不执行外部 Git 写入，不传输数据库与已有业务产物。

## 38 / 36 / 20 的对应关系

原采集 manifest 有 38 项；其中原首页 HTML 和生产 JavaScript bundle 仅用于查证，克隆服务使用重建页面和本地交互脚本，因此这两项不进入资产恢复。

36 个原始使用资产 = 35 个图片、字体、音频 + 原站 CSS。页面部分另有 20 个 HTML，另有 3 个本地适配文本 `local.css`、`local.js`、`states.json`。服务实际映射共 59 个公开文件：36 + 20 + 3。

独立 manifest 的每个资产包含精确相对目标、原 URL、SHA-256、字节数和实际服务路径；23 个文本 overlay 也包含精确 SHA 和字节数。导出器通过真实 handler 映射与已下载原字节指纹关联来源，不按扩展名或文件名猜测。

本地导出器 `export-restorable-public-assets.mjs` 只用于维护当前工作区 manifest，包含本机路径，不是接手者恢复命令。接手者使用已固定 pin 的恢复脚本与独立 manifest。
