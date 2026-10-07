# 概率判断工具（可选）

状态：OPTIONAL_NOT_DEFAULT

当前主流程不读取、不启动本目录。

只有 ENGINE.md 中的概率工具门通过时才使用：
TOOL_GAIN = T_DIRECT - T_PROB > 0，且必须明显降低完整 T_VALID。

T_PROB 必须包含：
准备输入、启动/连接、网络、判断、解析、验证、失败/重试和卡顿风险。

可用成熟工具来源：
skills/hybrid-intelligence-probability-engine-v0-3-5/

历史集成文档：
../../archive/legacy-hipe/

这里保留调用辅助脚本，仅为按需使用；不是当前引擎依赖。
