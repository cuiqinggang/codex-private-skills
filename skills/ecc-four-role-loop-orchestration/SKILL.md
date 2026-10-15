---
name: ecc-four-role-loop-orchestration
description: ECC版本定位与兼容入口。用户提到ECC、ECC最新版、V3.1.1或3.11时，默认读取已发布的ECC V3.1.1；V2.1.0只供明确历史查询和旧任务复现。
---

# ECC 当前正式默认入口：V3.1.1

这是原技能名称的版本路由入口，不是把旧V2.1.0正文重命名为V3.1.1。

## ECC 默认版本锁定（2026-10-15）

- 用户指定当前默认正式版本：**ECC V3.1.1**；“ECC”“ECC最新版”“ECC 3.11”均指此版本。V2.1.0只作历史基线，禁止作为默认版本或读取失败时的替代品。
- 统一入口：`skills/artificial-single-page-extreme-time-engine/ECC_V3_1_1_NETWORK_AUTHORITY.md`。
- 正式源码：`cuiqinggang/ecc-v3.1.1`，tag `v3.1.1`，固定提交 `b9e651bc6c6751bff43db30b80d9cab983a7c412`。
- 发布：https://github.com/cuiqinggang/ecc-v3.1.1/releases/tag/v3.1.1
- 正文：https://github.com/cuiqinggang/ecc-v3.1.1/blob/b9e651bc6c6751bff43db30b80d9cab983a7c412/README.md
- README标题“V3.1”和发布包名“ecc-v3.1”属于该发布的原始命名，不能据此降级为V2.1.0。
- 已安装或云端目录若返回 `ecc-four-role-loop-orchestration V2.1.0`，必须标记历史副本并转读上述入口；不得把旧正文改个版本号冒充新版。新版不可读取时报告版本读取阻塞，不静默回退。
- 只在用户明确查询历史或旧任务锁定旧版本时读取V2.1.0；不删除旧冻结，不自动迁移正在运行的任务。后续升级须明确更新此默认指针。
- 本次核实发布、tag提交和README来源，不宣称本机部署、性能、长任务或恢复测试已通过。

## 按需读取

先读取权威索引，再读取固定提交的README及任务涉及的源码。运行、部署与验收按真实源码和目标合同执行；本入口不自动启动CLI、不改变代理或现有任务。

## 历史来源

V2.1.0（2026-07-23）的四角色十二层正文保留在已有历史技能/冻结中。当前云端技能目录可能仍缓存该正文；其“当前正式版本V2.1.0”声明只反映旧副本日期，不代表用户当前默认版本。读取历史正文必须注明历史版本。
