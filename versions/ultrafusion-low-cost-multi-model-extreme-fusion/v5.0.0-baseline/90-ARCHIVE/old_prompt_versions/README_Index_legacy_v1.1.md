# 📚 UltraFusion 仓库索引（Auto Index v1.1 — 中文为主 / 英文为辅）


本文件为整个 UltraFusion-SpecKit 的总索引入口（Master Index）。  
放在仓库根目录，可用于快速导航所有模块。

---

## 🔎 目录（Table of Contents）


### 00-INDEX（索引与导航 Index & Navigation）

路径：
`/00-INDEX/`


-
 
`README_Index.md`
（当前文件在根目录，但 00-INDEX 内也保留一份副本）
-
 
`Project_Master_Index_v1.0.md`
（总项目索引）
-
 
`Naming_Rules.md`
（命名规范，中英文）
-
 
`Changelog_All.md`
（版本变更总日志）

---

### 01-SPEC
_KIT（核心规范集 Core Specifications）
路径：`/01-SPEC_
KIT/`


-
 
`SPEC_KIT_v1.1.md`
（主规范）
-
 
`V15_FULL.md`
（完整可复制使用的 V15 全文规范）
-
 
`Prompt_Spec_v1.0.md`
（提示词行为规则）
-
 
`Fusion_Spec_v1.0.md`
（C 层融合行为规范）

---

### 02-RUNBOOK（运行手册 Execution Manuals）

路径：
`/02-RUNBOOK/`


-
 
`UltraFusion_Phase0_RUNBOOK_v1.0.md`
（手工运行指南）
-
 
`Browser_Auto_Runbook_v1.0.md`
（浏览器自动化测试指南）
-
 
`Phase2_Service_Deploy_v1.0.md`
（上线 Web 服务部署指南）

---

### 03-TESTS（专家测试 & 盲测 Expert Tests / Blind Evaluations）

路径：
`/03-TESTS/`


结构统一：

03-TESTS
└── Q1/
├── Q1_A_Raw.md
├── Q1_B_Raw.md
├── Q1_C_Fusion.md
├── Q1_D_Final.md
├── Q1_E_Final_Report.md（8–12 页完整版）
└── metadata.json

yaml
复制代码

每一个完整循环从
 
A
 
→
 
B
 
→
 
C
 
→
 
D
 
→
 
E。


---

### 04-KB（最终答案金标知识库 Ultra Answer Final）

路径：`/04-KB/`


-
 
存放最终稳定答案
 
`Ultra_Answer_Final`（单题一个文件）


---

### 05-TEMPLATES（统一模板库 Unified Templates）

路径：`/05-TEMPLATES/`


-
 
`A_Layer_Template_v1.0.md`

-
 
`B_Layer_Template_v1.0.md`

-
 
`C_Layer_Template_v1.0.md`

-
 
`D_Layer_Template_v2.0.md`

-
 
`E_Layer_Summary_Template_v1.0.md`


---

### 06-SYSTEM_UPGRADE（自举升级循环系统 Self-Bootstrapping Upgrade System）

路径：`/06-SYSTEM_UPGRADE/`


-
 
`Self-Bootstrapping_Upgrade_Loop_v1.0.md`

-
 
`Upgrade_System_Readme.md`


---

### 07-ARCHIVE（历史归档 / 旧稿 Archive & History）

路径：`/07-ARCHIVE/`


-
 
存放所有过时版本、早期实验稿等


---

## 📌 说明（Notes）


-
 
所有文件名均为
 
**中文＋英文**（中文为主、附英文解释）

-
 
所有目录结构均可稳定引用、可移植

-
 
每个模块都可独立复制出去当作模板使用


---

## ✔ 最佳实践（Best Practice）


建议你把这个
 
`README_Index.md`
 
放在：


-
 
**仓库根目录（推荐）**

-
 
`/00-INDEX/`
 
中保留一份副本


这样
 
GitHub
 
打开仓库时，用户第一眼就看到完整导航。


---
✅ 第三部分：你要怎么放置这个文件？
✔ 你应该把文件放在这里：
pgsql
复制代码
UltraFusion-SpecKit/
│── README.md（保持不动）
│── README_Index.md ← ← ← 放这里（首页）
│── 
00
-
INDEX
/
│      └── README_Index.md（副本）
│── 
01
-SPEC_KIT/
│── 
02
-RUNBOOK/
│── 
03
-TESTS/
│── 
04
-KB/
│── 
05
-TEMPLATES/
│── 
06
-SYSTEM_UPGRADE/
│── 
07
-ARCHIVE/
