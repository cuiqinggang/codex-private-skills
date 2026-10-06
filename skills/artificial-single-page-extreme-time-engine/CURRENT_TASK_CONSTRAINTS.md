# 《当前任务目标与正反约束 当前版》

状态：CURRENT  
任务：抖音不可下载链接一键完成 — 新方法 Reality 验证  
任务ID：DOUYIN-ONECLICK-METHOD-V1  
方法基线：《人工单页面极限短时间引擎 第8版》+《极限短时间执行大脑 第3版》+《新页面运行模板 第4版》  
HIPE集成：《HIPE v0.3.5 × 极限短时间引擎：集成冻结 第2版》

## 1. 用户真正要完成的功能

不是“重新研发一个下载器”。

唯一现实目标：

```text
复制抖音分享文本/链接
→ 双击桌面入口
→ 自动完成
→ 桌面得到可正常播放、同时含视频+音频的 MP4
```

实现手段不限，只要合法、现实可用且 T_VALID 最短：
- 调用成熟现成程序；
- 调用成熟 API；
- 复制/适配成熟开源能力；
- 组合已有组件；
- 必要时最小自研；
- browser fallback。

禁止为了“自己实现”而放弃更成熟、更快路线。

## 2. 本轮冻结样本

用户提供的真实分享文本：

```text
冰川蓝色防蓝光近视眼镜黑武士系列 #无框切边眼镜 #近视眼镜 #防蓝光眼镜 #无框眼镜 #黑武士系列 https://v.douyin.com/jRJYc4pme7Q/ 复制此链接，打开【抖音】，直接观看视频！
```

核心短链：

```text
https://v.douyin.com/jRJYc4pme7Q/
```

用户描述：约15秒眼镜广告视频。

## 3. VALID

正式结果必须同时满足：

1. 用户只需要先复制分享文本/链接，再双击一次桌面入口；
2. 双击后不需要人工再次粘贴、选择媒体、播放或手工修复；
3. 最终桌面生成新的 MP4；
4. 独立 ffprobe 证明：
   - video stream >=1；
   - audio stream >=1；
   - duration > 0；
5. 输出不是旧文件冒充新结果；
6. 正式 Reality exactly-once；
7. 失败不能删除已有有效正式结果；
8. FINAL_VALID 前所有必要步骤属于同一任务时间边界。

## 4. 两层时间

### 建设任务
从本任务正式 TASK_ACCEPTED 到第一个成熟功能 FINAL_VALID：

```text
T_BUILD_VALID
```

用于验证新版方法是否避免旧 R1-R10 的流程浪费。

### 生产子任务
成熟状态下：

```text
剪贴板已含分享文本
→ 双击桌面入口
→ 新 MP4 FINAL_VALID
```

记为：

```text
T_RUN_VALID
```

两者不得混称。

## 5. 权威工作区

方法权威：
```text
cuiqinggang/codex-private-skills
skills/artificial-single-page-extreme-time-engine/
```

本任务权威：
```text
workspaces/douyin-oneclick-method-v1/
```

本地目录只能作为执行落地/缓存。
不得把 C 盘目录当方法或任务冻结权威。

## 6. 旧 Greenfield 边界

R1-R10：
- 只作为“哪些方法会浪费时间”的反例；
- 不作为新任务代码基线；
- 不读取/复制其实现作为默认方案；
- 不继承 R9/R10 wait threshold、claim、临时前缀或局部优化链。

本任务不是 R11。

## 7. 新版虚拟成熟流程

```text
TASK
→ Reality Solvability Gate
→ Mature Solution Search
→ Recursive Forward Compile
→ CODE / JEV / GPT residual
→ DAG + 最大合法并行
→ 连续虚拟攻击
→ 一次整包 Freeze
→ Formal Reality
→ independent verifier
```

## 8. 当前成熟候选集（只作为搜索起点）

当前公开成熟生态已经存在：
- 单视频、短链解析、重试、browser fallback 的成熟 Douyin downloader；
- 统一 content-downloader，支持 Douyin 短链与 Playwright fallback；
- 自托管 Douyin/TikTok Download API，提供解析/下载 API。

因此当前默认可解性倾向：

```text
WORLD_SOLVED=YES
EXPECTED_CLASS=MATURE_DIRECT or MATURE_COMPOSABLE
```

但正式分类必须在 R0 读取现实环境和候选可用性后冻结，不能只凭文字宣告。

## 9. HIPE / JEV

```text
HIPE_ALWAYS_ON=YES
JEV_ALWAYS_CALL=NO
```

优先：
- CODE 解决确定性；
- JEV 解决有限语义 Choice；
- GPT 解决不可压缩 residual。

JEV 接入：
```text
ENDPOINT=https://openrouter.ai/api/alpha/decisions
MODEL=typesafe/jev-1.13
KEY_ENV=OPENROUTER_API_KEY
```

本机用户级环境变量已检测为存在；最小 Decisions API smoke test 已 PASS。
不得把密钥值写入仓库/日志/冻结。

## 10. Reality 预算

```text
DEFAULT_FORMAL_REALITY=1
METHOD_VALIDATION_TARGET=3..4
HARD_MAX=5
```

同一个具体功能如果首轮 FINAL_VALID，禁止为了凑轮数重复运行。
后续 2–4 个 Reality 应属于方法验证所需的不同样本/边界，而不是对同一样本做微调刷版本。

任何单一任务达到第5个 Reality 仍未收敛：
```text
MANDATORY_POSTMORTEM=YES
STOP
```

## 11. 当前节点

```text
DOUYIN-ONECLICK-METHOD-V1-R0
```

R0 只完成：
- 新任务冻结；
- Reality Solvability Gate；
- 成熟候选快速比较；
- 依赖图；
- CODE/JEV/GPT 路由；
- 整包虚拟成熟；
- Reality Freeze。

R0 不做正式下载 Reality。

R1 才是第一次正式 Reality。

## 12. 成功标准

新版方法成功的主要证据不是“最终也能下载”。

必须同时看到：
- 首轮前方案已明显成熟；
- 没有 R1→R10 式逐点补洞；
- 观测/安全/原子提交/验证从首版就存在；
- Reality 次数显著减少；
- 建设任务 T_BUILD_VALID 明显收缩；
- 生产 T_RUN_VALID 继续向物理/网络下限收敛。
