# 2026-10-11 同类再次绕路事故：ComfyUI 修复合同被 image_gen 代替

## 真实事件与核实边界
用户明确要求：先升级现有图像技能包，然后按第28版极限短时间引擎，使用成熟方法修复“手指与饭勺融合、玻璃瓶缺失、画质不达标”，并展示**真实左右对比图**和实际生图证据。

实际在对应聊天中：
1. 调用了 ChatGPT `image_gen.text2im` 生成厨房图片，返回 `gen_id=f6fc87f8-42c4-4256-a6b7-8aa6efdd80b8`。
2. 再次调用 `image_gen.text2im` 绘制左右“原图/修正后”对比海报，返回 `gen_id=ed003cbe-8658-4d84-802a-f3a91da3f52f`。
3. 未见该轮通过 Windows ComfyUI 实际提交 `/prompt` 的对应 `prompt_id`、`/history`、冻结 workflow JSON、与生成文件一致的本地 SHA256，以及通过 Pillow 对真实两文件像素拼接的原始对比证据。
4. 本次对话另有较早 R1-R4 的真实 ComfyUI 生成历史；其存在**不代表**上述新生成的两张 image_gen 图片来自 ComfyUI，亦不能借用旧历史为新作品背书。
5. 未独立核算这两张 image_gen 图片的文件 SHA256 或原始二进制对应关系，字段记 `UNKNOWN`，不得凭 `gen_id` 虚构哈希。

## 事故裁决
- `BACKEND_REQUIRED=COMFYUI_LOCAL`
- `ACTUAL_BACKEND=CHATGPT_IMAGE_GEN`
- `ROUTE_VIOLATION=YES`
- `G-1=FAIL`；`G1=FAIL`；`G2=FAIL`；`G3_COMPARE_INVALID=YES`
- `COMFYUI_PROMPT_ID=NONE`；`QUALITY_AS_COMFYUI=NOT_VERIFIED`
- `FINAL_VALID=NO`；`VALID_TIME=UNKNOWN`
- 此两张图片只能作为事故记录，不可作为 Krea／Kontext 本机修复验收、性能基线或真实对比证据。

## 重复错误的原因和防复发要求
之前技能 `v1.2.1` 已有“工具选择前置门”文字，却仍未阻止同类行为。根因属于执行时未实际应用锁定的后端／来源条件，不能因为规则文本存在就报“防作弊已解决”。

修复分层：
- 规则层：技能入口升级 `v1.3.0`，引入 `IMAGE-SOURCE-ANTI-CHEAT-V3.md`，先判定生成后端和四种模式，再允许进入任务。
- 证据层：缺 ComfyUI 原生任务编号、history、工作流来源、输出文件和非生成式对比图即禁止认证为正式成果。
- 执行层：如果平台支持工具级 allowlist／denylist，再将已锁定的 ComfyUI 合同映射为真实工具路由约束；**当前 GitHub 文档不能证明该平台级机制已生效**。
- 回归层：下次必须以实际跨会话工具路由和可追溯证据验证，不得只用文字模拟 PASS。

本事故不修改此前 ComfyUI 历史工件，不自动重做图片，不把无证据结果覆写为成功。
