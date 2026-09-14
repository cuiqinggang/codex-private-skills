# P0 E1 结果确认路径纯分解实验

英文标识：RESULT_PATH_DECOMPOSITION

RUN_ID：P0-E1-RESULT-DECOMPOSITION-20260914T141601Z

## 1. 本轮目的

只把 P0-CONTROL-V1 当前 RESULT 路径拆成更细的真实时间段。方法论直接使用 mature-replication-four-column V4.0；没有重新设计方法，没有执行性能优化。

## 2. 上一正式基线

- T_CURRENT：32.55975 ms
- MIN：27.2659 ms
- P95：58.1779 ms
- REQUEST 中位：5.55075 ms
- QUEUE 中位：4.71925 ms
- EXECUTE 中位：3.4891 ms
- RESULT 中位：16.99775 ms
- T_PHY_WORKING_RANGE_V0.1：10–20 ms
- P0_99=NO

## 3. 单一假设

RESULT 约 17 ms 可能混合 ComfyUI 完成生命周期、history 可见、输出可见、客户端检测、HTTP /view、PNG 验证与证据写入。E1 只增加单调高精度时间戳验证该组成。

## 4. 为什么选择它

RESULT 是当前最大时间块，约占正式基线 52.20%，计划明确将 R1-A 结果确认分解作为第一实验。

## 5. 预计最大收益

本轮不优化。未来 RESULT 路径的理论收益上限不超过当前约 16.99775 ms。

## 6. 实际只修改了什么

只在独立实验 runner 副本中新增：execution_success、executing node=None、history 请求/响应/可见、一次性输出文件可见、/view 字节可见、客户端检测、PNG 验证、证据写入和计时结束后的 queue-idle 时间戳。真实 patch 为 runner.patch。

## 7. 明确没有修改什么

没有修改正式 SKILL.md、VERSION、Stage Ledger、V4.0 方法、P0 Contract、workflow、LoadImage、SaveImage、HTTP session、WebSocket 确认逻辑、history 请求次数、/view 路径、PNG 验证标准、ComfyUI、系统栈或运行参数。没有 sleep/polling 调整，没有性能优化。

## 8. 3 次预热

3/3 有效，串行执行；没有补跑或删除样本。原始数据见 warmup-runs.json。

## 9. 20 次正式测量

20/20 有效，串行执行；失败 0；Prompt ID 23/23 唯一，输出文件 23/23 唯一。原始数据见 measured-runs.json。

## 10. 总时间统计

E1 观测运行：

- Median/P50：36.74075 ms
- P95：49.9382 ms
- MIN：28.7726 ms
- MAX：69.7039 ms

相对 32.55975 ms 基线，中位总时间增加约 12.84%。E1 增加了观测工作，本轮数字不竞争、不替换正式 CURRENT。

## 11. REQUEST / QUEUE / EXECUTE / RESULT

- REQUEST 中位：5.25955 ms
- QUEUE 中位：6.4961 ms
- EXECUTE 中位：4.0695 ms
- RESULT 中位：19.6454 ms

RESULT 相对原 16.99775 ms 增加约 15.58%，作为观测扰动记录，不作性能结论。

## 12. RESULT 详细分解

20 次 measured 的中位值：

- SAVE_DONE → EXECUTION_SUCCESS_EVENT：0.67355 ms
- EXECUTION_SUCCESS_EVENT → HISTORY_VISIBLE：3.43885 ms
- EXECUTION_SUCCESS_EVENT → EXECUTING_NONE_EVENT：1.3741 ms
- EXECUTING_NONE_EVENT → HISTORY_REQUEST_START：0.42865 ms
- HISTORY_REQUEST_START → HISTORY_RESPONSE_BODY_DONE：0.94425 ms
- HISTORY_RESPONSE_BODY_DONE → HISTORY_VISIBLE：0.2049 ms
- HISTORY_VISIBLE → OUTPUT_VISIBLE：0.1955 ms
- OUTPUT_VISIBLE → CLIENT_DETECTED_READY：13.25845 ms
- HISTORY_VISIBLE → OUTPUT_API_BYTES_VISIBLE：13.38455 ms
- CLIENT_DETECTED_READY → RESULT_READY：1.3153 ms
- PNG 完整验证：0.5302 ms
- 证据 PNG 写入：0.7366 ms
- RESULT_READY 后 queue-idle 检查：0.96 ms，不计入 T_END_TO_END

TASK_DONE 精确 monotonic 时间：UNKNOWN。当前 ComfyUI 没有向客户端直接暴露 task_done 单调时间戳；HISTORY_VISIBLE 是本轮可可靠取得的第一个完成历史观察点。

固定 sleep：未发现。history polling interval：未发现。每轮 history 请求：1 次。WebSocket：每轮重新建立，但建立发生在 REQUEST_START 以前；关闭位于 RESULT 内。HTTP ClientSession：23 次运行共用一个 session。

## 13. 输出有效性

23/23 均满足：history success/completed、匹配 prompt、唯一新输出、有效 PNG、256×256、完整 zlib 解码、SHA-256 一致、每轮结束 queue idle。输出有效性 PASS。

## 14. 保留或回滚

保留 E1 证据和观测脚本供审计；不保留 E1 总时间为新 baseline，不修改 32.55975 ms CURRENT。不存在性能实现需要回滚。

## 15. 当前四项纵向状态

### 当前实测时间（CURRENT）

正式基线保持 32.55975 ms。E1 观察中位 36.74075 ms，仅用于 RESULT 分解。最显著观察是 OUTPUT_VISIBLE → CLIENT_DETECTED_READY 中位 13.25845 ms。

### 外部成熟前沿（EXTERNAL FRONTIER）

无新增证据。本轮没有执行外部研究。

### 第一性原理物理时间（FIRST-PRINCIPLES PHYSICAL TIME / T_PHY）

建议保持 T_PHY_WORKING_RANGE_V0.1=10–20 ms。E1 证明结果已在 history 后很快于文件系统可见，但 /view 到客户端检测仍占较大时间；尚未通过单变量实验证明其中可消除比例，因此证据不足以收窄区间。

### 迭代收敛（ITERATIVE CONVERGENCE）

E2 推荐单变量：保持 history、输出文件、PNG 完整解码、尺寸和 SHA-256 成功标准不变，仅比较当前 HTTP /view 读取与本机已确认 data/output 文件直接读取的结果取得路径。目的只验证 OUTPUT_VISIBLE → CLIENT_DETECTED_READY 的约 13.25845 ms 是否主要属于结果传输/检测路径。E2 本轮未执行，等待 ChatGPT 审核授权。

## 16. T_PHY 是否收窄

保持。证据不足以修改 10–20 ms 工作区间。

## 17. 新增经验

RESULT 中没有固定 sleep、没有 history 轮询、没有重复 history 请求。输出文件在 history 可见后的首次检查即存在；最大的已观测子段是输出文件可见到客户端检测完成。

## 18. 失败经验

没有 benchmark 失败。精确 task_done 时间无法从当前客户端事件可靠取得，保持 UNKNOWN，不以 execution_success 冒充 task_done。

## 19. 下一步候选

E2_RECOMMENDED_SINGLE_VARIABLE=LOCAL_OUTPUT_FILE_READ_VS_HTTP_VIEW

只提出候选，不执行。

## 20. Git 共同办公区

- 仓库：https://github.com/cuiqinggang/codex-private-skills
- 相对路径：workspaces/visual-art-engine-performance-ladder/stages/P0/P0-E1-RESULT-DECOMPOSITION-20260914T141601Z/
- EVIDENCE_COMMIT=57acf258dc422edb0f05e68f016c9ce27a3a6210
- SKILL_VERSION_CHANGED=NO
- PERFORMANCE_OPTIMIZATION_RUN=NO
- E2_EXECUTED=NO
