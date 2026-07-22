---
name: ppt-video-router-cn
description: 为静态 PPT、动态网页 PPT、PPT 转视频、HTML/CSS/JS 程序化视频、横竖屏短视频和真人视频包装选择最轻可行路线。用户询问“该用什么做 PPT/视频”“Frontend Slides、HyperFrames、Remotion 怎么选”“PPT 转视频”“程序化视频工厂”时使用。
---

# PPT 与视频中文路由

先判断输出和内容类型，再选择最轻可行路线；不因工具已安装就强行使用最重方案。

## 路由表

| 需求 | 默认路线 | 理由 |
|---|---|---|
| 纯静态 PPTX | 原生 PPTX/现有 PPT 流程 | 保留办公兼容性 |
| 动态网页 PPT | Frontend Slides | 单 HTML、16:9、浏览器交互 |
| 导航型演示/分支幻灯片 | HyperFrames `slideshow` | 演示模式和可导航结构 |
| PPT 转视频、图文讲解、产品介绍 | Frontend Slides + HyperFrames | 内容与渲染分层 |
| HTML/CSS/JS 程序化短视频 | HyperFrames | 确定性时间轴和本地 MP4 |
| 复杂 React 组件化批量视频 | Remotion，按需启用 | 仅在 React 生态确有收益时 |
| 真人连续表演、角色一致性 | 关键帧/图生视频/NLE 路线 | 不属于 HTML 渲染器能力 |
| 真人视频中的 UI、字幕、数据包装 | 原视频 + HyperFrames 合成 | 保留真人素材，只做包装 |

## 决策步骤

1. 明确最终产物：PPTX、HTML、PDF、MP4、横屏、竖屏或透明叠加层。
2. 判断内容：静态信息、离散幻灯片、程序化动画、真人连续镜头或混合素材。
3. 判断是否需要确定性逐帧渲染、批量变量、交互导航或 React 组件生态。
4. 选择最轻路线，并写出选择理由、输入要求、输出目录、验收和回滚。
5. 涉及中文演示内容时先调用 `humanize-ppt-cn`；涉及节奏时调用 `ast-attention-architect`。
6. 使用 HyperFrames 时只走本地 `init/lint/validate/snapshot/render`；默认禁用遥测，不使用 cloud/publish/auth/API Key。

## 输出契约

```text
推荐路线：
选择理由：
输入要求：
输出目录：
验证命令：
验收标准：
回滚方式：
不选其他路线的原因：
```

## 硬门禁

- 不把真人连续表演误当成 HyperFrames 生成任务。
- 不默认安装 Remotion；主路线确有能力缺口时再启用。
- 不用云端发布、上传或付费 API 代替本地闭环。
- 横竖屏分别排版，不允许简单裁切。

验收、失败复盘和使用记录规则见 `references/OPERATIONS.md`。

