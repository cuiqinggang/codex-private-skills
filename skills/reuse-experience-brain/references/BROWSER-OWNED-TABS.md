# EXP-BROWSER-001｜浏览器标签页所有权审计与原生批处理边界
版本V1；核查日期2026-10-30；分类CASE/ERROR/CANDIDATE_RULE；证据等级=实际原MCP操作日志、修正的独立验收及B2回归。

触发：既有浏览器MCP的跨页测试，被“全局所有标签页必须完全相等”的审计误报为丢失原页；或希望吸收批次执行功能而不替换正式浏览器。环境：OMP18.13.3、现有CDP9223+正式MCP8927、合成预约页面、原ACL。

LAST_GOOD：原页面URL均出现在操作事件中，已关闭唯一自有新标签页。FIRST_DELTA：额外出现一个来源未知、并非测试所有的ChatGPT页面；旧全局tab集合一致性断言将其误算为原页丢失。最小修复：保留原始FAIL日志，只修改验收检查——逐一核对原页面ID/URL与实际动作，确认测试自有唯一标签页确实关闭；未获所有权的新增页面不予关闭。B1纠正审计PASS，但原始ID第一轮未完整保留，因此要求下一轮保存前后ID。

现实回归：A1原始默认路径210.477秒但业务不合格；B1原检查为FAIL、修正后累计356.041秒；B2原MCP批处理14行完整成果，原页面保留及自有tab清理PASS，首次请求至独立验收132.022秒，模型工具错误4次已恢复。B2只证明合成UI及此合同，不与FAIL的A1计算同质量倍速。原AB四组推广门未通过；默认浏览器、正式FULL_POLICY和生产启动器保持不变，整体增强T_VALID、实际账单均NOT_MEASURED。

适用：原有受控浏览器共享环境下，按资源所有权审计、最小纠错、保留无关页面，采用成熟MCP批处理而非新写控制器。不适用：外部已登录站点、任意浏览器重启、全局新标签页归属判断、以一次B2测试宣称全面速度优势。

原证据：C:\Users\A\Documents\DSH-Workspace\browser-capability-absorb-20261030\COMPARISON-FINAL.json、B1-CORRECTED-AUDIT.json、FREEZE-R3.json、B2-FINAL.json、FINAL-ABSORPTION.json；原合同与冻结版本以同目录FREEZE.json及最新R3为准。
