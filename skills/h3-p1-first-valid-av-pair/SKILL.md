---
name: h3-p1-first-valid-av-pair
description: H3-P1：首个有效图声对 v1.0.0。继承 H3 视频项目的中间任务；不是新总引擎。本版登记任务、保留原资产引用并提供已测试的只读资料回收胶囊；图声生成尚未虚拟成熟或现实认证。
metadata:
  version: "1.0.0"
  display_name: "H3-P1：首个有效图声对"
  english_name: "H3-P1 First Valid Audio-Visual Pair"
  parent: "h3-high-fidelity-local-video-recreation"
  method_dependency: "first-principles-physical-limit-convergence@5.0.2"
  project_status: "VIRTUAL_IN_PROGRESS"
---

# H3-P1：首个有效图声对 v1.0.0

## 定位和唯一目标
这是旧 H3 视频工作的连续中间阶段，不重做 P0，不另建通用引擎，不提前铺开 P2-P7。总方向保留原创视频、优秀视频复刻与改造；P1 只验证能作为后续输入的首个有效图声对。P1 完成不自动证明长视频、复杂动作、角色一致性或完整制作链已经通过。

唯一核心：`T* = min(T_VALID)`。质量、语义匹配、正确性、安全、成本和资源只进入 VALID 或硬约束。在同一目标、同一 VALID、同一启动状态下，T_VALID 越短越好。名称、版本或小程序通过均不等于 P1 成熟。

## P1 当前任务合同
从已冻结的文字任务出发，本次产生有效图像、语义匹配的有效声音及有效时间关系，并交付可定位、可复核的产物和证据。不得拿预先备好的目标图片冒充从零生成；声音是否必须本次生成及允许的来源须明确冻结，暂按本次生成方向设计。固定帧显示及声音事件的关系不自动等于口型或连续动作同步。

尺寸、声音长度、测试事件、语义验证方法、具体工作流、节点及模型身份、冷热启动口径、重试/超时策略和数值时间锚尚未完整冻结，因此 `P1_SPEC_COMPLETE=NO`，`P1_VIRTUAL_COMPLETE=NO`，`P1_GENERATION_DISPATCH_ALLOWED=NO`。

`T_VALID` 起于冻结任务入口接收，止于图像、声音、关系、交付与必要验证首次全部成立；包括在线准备、实际生成、失败尝试、验证和交付。一次性研发费用单独记录；为本次输入做的预生成不能藏到计时外。旧 P0 时间、资料回收时间或状态机证书时间均不是 P1 时间。

## 原资产继承，不覆盖
共同仓库：`cuiqinggang/codex-private-skills`。

- P0 固定提交：`8290afc2953319b0eb6bc0dd74c5cedc0c1ffac1`；分支 `codex/h3-p0-mature-convergence-v2`；目录 `docs/h3-p0/20260917-mature-convergence-v2/`。
- P0 冻结 JSON：`H3-P0-FINAL-99-FREEZE-v1.json`，blob `65e708380189a113970d976f65d97052bc56d972`。历史 32×32、5 帧、1 步基准与 P1 不同；历史 20/20 有效交付不迁移为 P1 认证。
- 已回读的旧执行器：`docs/h3-p0/20260916-first-principles-v1/H3-P0-runner.py`，blob `22fc7bdca8326321d69ee039ac604ac275b7ddfe`。只是历史来源，不直接执行；它缺少 P1 图声语义验证，且旧控制操作不得自动继承。
- 方法 v5.0.2：分支 `codex/first-principles-physical-limit-convergence-v5.0.2-virtual-freeze`，文件 `skills/first-principles-physical-limit-convergence/SKILL.md`，本次读取 blob `1792d14a2fb45b60cb93876f6d615c110990937d`。
- 本机高保真父技能、质检 SOP、失败记录、电影工厂 SOP、母工作流和模型位置见 `ASSET-RECOVERY.py` 的九项白名单。历史路径可定位不代表本机今天仍存在；模型元数据不代表模型内容已校验。

本轮新增文件在独立分支，不改父技能，不改 P0 冻结，不改代理、模型、驱动、系统设置或常驻服务。不将未同步的本机材料假称已经在共同仓库。

## 虚内部的当前动作：只读资产回收
为了让 GPT 读取旧技能和真实工作流，而非凭记忆重写，当前只冻结 `H3P1-v1.0.0-ASSET-RECOVERY-R1` 这个资料回收子任务。

`ASSET-RECOVERY.py` 只读五个明确文本/JSON 文件；对三个已知模型和已有 Python 只读文件元数据，不读大模型内容。每个文本最多 2 MiB。不递归搜索、不启动或停止进程、不联网、不调用 /prompt、不生成媒体、不读取环境变量或凭据文件。

缺失、权限拒绝、内容变化、哈希差异、编码错误等逐项记录；疑似密钥内容不复制。仅在 `C:\AI\H3-P1-Acceptance\v1.0.0\` 下新建唯一输出目录，保存快照和计时收据，不覆盖旧输出。输出材料仍需按最小必要范围处理；疑似敏感项禁止自动上传。

`inventory_capture=PASS` 只表示本轮盘点结果成功落盘并回读，不表示每个资产都存在，更不表示 P1 生成通过。任何资产差异只带证据返回 GPT，不现场修复、重新下载或改母工作流。

GPT 已对精确源码执行 20 项 CPU 隔离测试，包括新 namespace 物化、权限/缺失/哈希/编码/大小/敏感内容、禁止模型内容读取、禁止覆盖、验证器状态攻击、写入失败和目标平台限制。测试报告见 `GPT-SELFTEST-RESULT.json`；不是 Windows 目标实测或 H3 GPU 实测。

## 给 Codex 的唯一当前动作
只执行 `RECOVERY-FREEZE.json` 指定的只读回收胶囊。先按完整远程定位核对源 blob 和 SHA-256；读取源码全文，在同一 Python namespace 编译/执行并调用 `run_reality()` 一次。优先使用已知已有解释器 `C:\AI\MiniMax-H3\.venv\Scripts\python.exe`；缺失即停止，不扫描、不安装、不换环境。物化源码仅允许在上述独立输出根目录内。

回传 `ASSET-SNAPSHOT.json`、`RECOVERY-RECEIPT.json` 的可访问文件或全文，以及快照 SHA-256、起止时间、资料回收耗时和资产差异。零差异时也停止回 GPT；本轮不继续生成。若需要同步共同仓库，只新增本任务证据文件，不覆盖原证据，禁止上传密钥或无关内容。

定位：`【H3-P1首个有效图声对｜v1.0.0原资产只读回收｜01｜实】`。

## 收到回收证据后，仍在 P1 的虚内部完成
优先从已恢复的 H3 原生联合图声工作流复用；与已有成熟图片+声音组合方案在同一合同下比较。不能只凭独立生成可并行就选择拆分，也不能把 JEV 或其它未完成项目设为先决条件。成熟检索和实际实现验证均完成后，冻结唯一方案、独立语义验收、失败分支与有依据的 P1 最短时间锚，再发布 P1 生成 Reality Capsule。

`虚 -> 实 -> 完成`；现实失败只能 `Reality Delta -> STOP -> 回虚 -> 新冻结`。本版的资料回收胶囊有独立有限作用域，其完成不能晋升整个 P1 的虚拟成熟状态。

## 当前结果
- 版本：1.0.0，已建立；属于项目登记/分析与资料回收实现版本。
- P0：保留历史冻结，本轮没有重跑。
- 资料回收程序：GPT 隔离测试通过；Windows 目标回收待执行。
- P1 图声方案：虚拟成熟进行中；生成实现、语义验收、P1 时间锚待完成。
- P1 现实生成次数：0；P1 虚拟/现实 T_VALID 均未取得，必须保持 null 而非 0。
