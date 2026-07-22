# 海外数字产品独立站复刻技能包 v1

## 任务定义

这个技能包不是公司注册服务站，也不是 AI 图片工具站。它复刻的是视频里讲的这一类：

> 可以上架数字产品，线上收美金/外币，付款后自动发货的海外独立站。

核心闭环：

```text
数字产品准备 → 店铺/独立站上架 → Checkout 收款 → 付款成功 → 自动下载页/邮件交付 → 用户可重复下载 → 后台看订单
```

## 视频来源

- 本次上传视频文件：`/mnt/data/5a4c461a3c8f02da10a90e80e15cc3fa.mp4`
- 关键截图目录：`assets/video_keyframes/`
- 总览截图：`assets/video_keyframes/video_contact_sheet.jpg`

## 本包内容

```text
docs/00_视频图文索引.md
docs/01_正确业务定义.md
docs/02_成熟网站案例.md
docs/03_功能复刻蓝图.md
docs/04_页面与数据模型.md
docs/05_实施路线.md
docs/06_验收清单.md
commands/Codex_Hermes执行命令.md
SKILL.md
assets/video_keyframes/
assets/blueprints/
sources/reference_links.json
```

## 复刻优先级

第一阶段优先用 Lemon Squeezy / Payhip / Gumroad 跑通真实闭环，不要一开始就自建复杂后台。

最低可用版本必须满足：

1. 能上架 PDF / 模板 / 课程 / 素材包 / 软件授权等数字产品。
2. 有产品详情页，说明包含内容、价格、授权、退款和交付方式。
3. 能通过 Checkout 收美元/外币。
4. 付款成功后自动跳转下载页。
5. 自动发送邮件，邮件里有下载链接或访问说明。
6. 后台能看到订单和客户邮箱。
7. 用户无需人工客服即可拿到产品。

## 关键图纸

- `assets/blueprints/01_business_closed_loop.png`：业务闭环图
- `assets/blueprints/02_technical_architecture.png`：技术架构图
- `assets/blueprints/03_page_wireframe.png`：页面结构图

