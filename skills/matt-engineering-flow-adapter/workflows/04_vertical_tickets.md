# 04 纵向闭环 Tickets

禁止按文件数量或技术层机械拆分。

每个 Ticket 必须从一个可观察输入贯穿到可验证输出，包含目标、影响文件、前置条件、实现步骤、测试、证据、风险、回滚和完成标准。

先建立依赖边，再按可独立验收顺序排列。Ticket 不自动创建 GitHub 或 GitLab Issue；上层明确指定 tracker 后才转换。

输出使用 templates/TICKET.md。
