# 《三人行》第2版｜MiniMax H3 三路成熟方案复核与商业化修正 R2
日期：2026-10-13；性质：V3隔离候选的增量研究与现状审计；非V2覆写、非通过认证、非新成片。
状态：RESEARCH_VERIFIED / REALITY_READINESS_ONLY / H3_RENDER_NOT_STARTED / FINAL_VALID=NO。

## 事实基线
- 正式V2 C链只有001–003合格；004真实三次失败（过度位移两次、近零一次），53张仍缺失，未生成56帧合规成片。旧B链004文件的单帧“审查通过”不等于正式C链第004帧通过。
- 实际连通Windows执行桥，读取 C:/AI/Polsia-Codex-20261011/outputs/codex-h3-v2-20261012/FINAL_TEST_RESULT.md，并对8188/8193/8194/18290本机端口执行只读探测，均未监听（本次检测时点）。不得把磁盘权重或旧日志当成可用H3服务。
- V2真实约束是56张独立源图/24fps/2.333s；商业新目标是15s原生音视频，与V2不可在“相同产品/价格/长度”意义上直接视为已实测提速。

## 成熟方案三选（基于MiniMax官方仓库、官方提示词Skill、官方品牌宣传Skill及Comfy资料）
A. 在线H3 Ref2VA 一次生成15秒（首选下一Reality）。用经过许可的场景/产品图片作为锚点，可用参考视频、参考音频；按官方h3-prompt-writing/reference六段提示词控制身份、场景、动作与音景。优点：原生时序、声音、可参考多素材、可选2K；风险：账户/额度、素材及商用权限、H3实际生成质量均未在本项目新任务验证。
B. 在线H3 FL2VA首尾帧15秒（单镜头备选）。必须已有独立合格的首帧、真实末帧；用官方base-en描述动作因果及落点。仅适用于需要单镜头轨迹和可控首尾画面的短片；不把现有C003冒充15秒末帧。若追求宣传片快节奏剪辑，可研究将连续几个合法短片经成熟视频剪辑工具拼接，但这属于另一完整生产合同，应独立Freeze，不能伪装本次同条件对照。
C. 本机 ComfyUI H3 多参考/首尾帧（特定场景备选）。用户有现存本地权重和历史工作流，但目前服务未监听。须明确资源、时间、故障率和本地商业许可证，禁止因为“无API费用”忽视显卡算力和人工修复成本，也禁止更改FlClash/浏览器。先评估再开机，不采用无限重试。

虚拟候选排序：A > B > C，为结构性方法选择，不是现实质量评分。V2全帧逐张模式保留于“明确要求逐张源图”的特殊合同，不再默认用于普通商业连续视频。

## 官方可复用现成技能与完整素材路径
- 官方H3模型、两模式、官方部署：https://github.com/MiniMax-AI/MiniMax-H3
- 官方通用提示词技能：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- 官方品牌宣传视频技能：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/brand-promo-video-generator
- 官方极简产品广告技能：https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/minimalist-product-ad-generator
- Comfy原生教程：https://docs.comfy.org/tutorials/video/minimax/minimax-h3
- 现成V3完整正式生图提示词：同目录PRODUCTION_PROMPT.md，不从零重写。
注意：官方brand-promo等Hub专用技能需要Hub内置hub_*能力，不能假设在普通Codex调用它们就能生视频；可合法复用其分镜、信息核验、节奏和验收思路。官方h3-prompt-writing是可直接复用的提示词技能。

## 商业审查：生产“流畅样片”与“商业有效短片”是两个目标
- 现有厨房果篮＋布料15秒单镜头可以做运动连续性与声画检验，但无真实品牌/卖点/真实产品认证，不可仅因为画质好就认定具备广告转化能力。
- 如果以原创生活美学广告进行下一轮商业创意：0–2秒强视觉钩子（织物纹理、晨光与有意图的手部动作）；2–5秒触摸建立触感；5–9秒拾起、展开说明工艺质感；9–12秒完成细节整理；12–15秒稳定产品英雄画面和视觉留白。所有动作连续、物体数、真实手部与声音必须可信；不编造品牌、材质性能或产品承诺。若原先的同题一致性技术比较是必须的，不能中途修改冻结分镜，应把这个更强创意作为下一自然节点。
- 参考广告成熟套路不等于直接照搬他人受版权保护的成片。保证素材授权、商业许可、音乐权利和水印要求。

## 经MiniMax官方站核对的现实价格（报价随平台与时点变化）
官方价目页面：https://platform.minimax.io/subscribe/token-plan?tab=api-enterprise
2026-10-13查询显示 H3 768P 0.08美元/秒，2K 0.13美元/秒。15秒基础输出账面成本分别1.20美元与1.95美元；前5张参考图免费，额外参考图0.04美元/张；视频参考、Context-IR、2K再生成等可能另计。尚未实际计费，没有权利把账面单价认定为已实际支付价格或出片总成本。
本地商业许可说明：https://support.comfy.org/articles/6065098425-minimax-commercial-licensing-who-needs-a-license-and-how-to-get-one；本地权重用于商业交付需要另确认许可；使用云端或第三方平台必须核对相应权益与条款。

## Reality结果与执行门禁
本次只做真实文件、现有服务、官方技能和价目的核实；无可直接使用的H3云端凭据已得到确认，未调用新H3生成任务，也没有15秒MP4。FINAL_VALID=NO，QUALITY=UNKNOWN，T_VALID=UNKNOWN。
新发现ChatGPT可选择连接OpenArt，并在该服务中选用MiniMax H3/H3 max；只有用户完成实际连接，且账号中有可用生成权限/额度后才能合法真实调用。该第三方报价、规格和商用权利独立核验，不等同官方API报价/授权。
下一Reality：以当前V3 PRODUCTION_PROMPT.md为冻结合同，先核对合法素材、连接/额度/计费条款，发起1次完整15秒视频生成并保存真task_id/时钟/账单/原片，逐段视觉、原生声音、同步与权限审查，按 GOOD/BAD/FIRST_DELTA 有限修复。不能用文档静态PASS或旧2.33秒片代替15秒成片。
