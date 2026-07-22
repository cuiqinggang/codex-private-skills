# 数据流

原始问题是 A_Initial 与 A 层共同输入；A 输出仅流向 B，B 输出仅流向 C，C_Fusion 流向 D。封存的 A_Initial 只在 D_Final 锁定后以比较副本流向 VALUE。核心提示词只读流入对应节点，运行产物永不回写核心文件。

