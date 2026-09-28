# 01包共同工作区交付清单

- 页面：极限短时间 v5.6自动化1
- 任务：ESTE-V55-USER-TEST-20260928-R1
- 包号：01（补交不增加包号）
- 状态：30，待Codex实际收件核验
- 原冻结摘要：d38aac4556a312956716fc860b255f1a27afab2afdb0f421607b78f998a1618a
- 原命令摘要：921a1be0bdee0cbf493297d7e699c3080607bcd8571e71f50568e0d9e4ef6c73
- 原完整ZIP（GPT侧留存）SHA256：655a899858f3ede1a4d0c870ac02755ff674df1186be6a64fa4b42019288da87
- 原嵌套候选ZIP SHA256：e40a1d94f6ff7a79377e6700289d1c325ef5a332821a78d433e156db56b74549
- 候选内核SHA256：698513c9a7b354935a43470ac2a0dba1d8c94ed1a331c82f49937e16f27c2a82
- 候选业务脚本SHA256：2449cb764adde94b441f4ccd03773e4d4c18726f22e0136745a594ff020a09a0

仓库原生交付文件：
1. TASK.md — 完整现实任务合同、收件门和返回合同。
2. execute_worker.py — 从冻结候选业务脚本中抽取的现实执行载荷；只含execute_data/execute，不含测试收件或restore角色。
3. 资料/现实应用输入.json — 原始输入；原包SHA256=dbdf870e53c86434facc3f3bdab1c99ced336b8dd39c31a5988b9d98a96eef8f。
4. 资料/冲突输入.json — 原始负例输入；原包SHA256=97f59321873745744a4dde67bb040dd2d7059d6e2966aeda8a6f015c79274cc5。

注意：原ZIP二进制本轮未上传；这里是同一01包的仓库原生展开传输修复，不是02包。Codex必须以实际回读和实际SHA256为准，不得把本清单声明当成文件核验。