# 公开页面设计验收

范围：用户指定的 polsia.com 可观测公开页面，20个HTML变体。桌面1440×900、手机390×844、平板768×1024。源与本地同时组成比较图，补充5张可读局部比较。有效清单 visual-qa/validated-comparisons.json，35组均由非作者独立查看；原先加载瞬态/同名覆盖风险图永久排除出有效比较，失败原件保留。

五项逐一复核：原字体和字号层级、间距与布局、断点可用性、颜色/状态/表面、原图片像素来源与裁切。办公照片、白黑logo、云层、人像、商品、4公告原图与10字体等原资源SHA核验；没有用占位或绘图替换。语言菜单、表单、实际创建与持久恢复、原音频播放及暂停已真实浏览器测试；输入错误、disabled、back、hover与mobile overflow均已覆盖。

关闭的问题：privacy可见URL换行、语言搜索hidden被display:flex覆盖、menu选择状态与刷新持久化、恢复性CLI重连误判。截图中的source/logo和local/公告加载瞬态通过双边完整载入重采闭环。取消样式页文案两行和footer一行与参考卡片高度对齐。无未处理P0/P1/P2产品发现。

用户允许文字不同：部分原站实时翻译与固定本地文字不同，不将允许的字形/换行差异报告为全字一致。动画终端文案与脉冲相位有差异。没有实测全站99.9%相似度，设计验收只针对本次公开范围。交易壳明确未发起交易；私有控制台视觉未纳入，不用这份报告宣称全部能力对等。

独立证据 pcl04/validated-visual-audit-latest.json、VALIDATED_VISUAL_REVIEW.md、public-browser-receipt-readback.json。

Final verdict: passed
