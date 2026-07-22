# 01_PRECHECK

运行前检查：
- node -v
- npm -v
- git --version
- npx --version
- 浏览器是否可用
- Playwright 是否可安装或能否调用系统 Chrome/Edge
- 当前工作目录是否可写
- 是否能创建 screenshots 目录
- 是否能执行 npm run build

如果 Node 版本小于 20，标记 WARNING；如果目标模板要求 Node 24，则提示升级，不得假装通过。

预检输出：outputs/PRECHECK_REPORT.md

## 输出要求
- 所有结论必须中文可读。
- 关键证据必须落盘。
- 没有真实 URL、截图、build 和 QA，不得标记 PASS。
