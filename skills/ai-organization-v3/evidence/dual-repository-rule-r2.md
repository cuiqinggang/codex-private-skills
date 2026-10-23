# V3 双仓并行强备规则 R2
正常节点：在线主仓与 C 盘并行提交同一 TASK_ID、NODE_ID、VERSION、成果摘要及哈希；各自独立读回校验，BOTH_VERIFIED 才是完整备份 PASS。
单边失败：成功副本可以供故障恢复，状态 DEGRADED_ONE_COPY；不得宣布备份通过。业务可在保留成功副本的前提下继续，但必须安排修复另一仓并重新校验；必要时限制不可逆动作。双边失败：不标记已提交版本，进入受控恢复。
主仓为 GitHub 在线仓，C 盘为独立强备。优先从主仓读取，主仓故障读取 C；恢复后根据版本和哈希对账，禁止直接以最后修改时间覆盖冲突。
真实独立验证：2026-10-23 测试节点 AIORG-V3-DUALREPO-TEST-20261023；在线 skills/ai-organization-v3/evidence/dual-repository-smoke-20261023.json 与本地 dual-repository-smoke-20261023.json 并行写入、双方读回内容一致。仅一个小测试文件，非完整工程全链路验证。
尚未验证：真实网络中断、在线写入权限拒绝、C盘故障及自动重试、跨换页任务业务最终结果、完整 T_VALID。不得宣布 V3 正式成熟。
