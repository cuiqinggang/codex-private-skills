# P0-CONTROL-V2-CANDIDATE

状态：`CANDIDATE / NOT_FROZEN`

最高层任务、workload、计时起点与正确性门禁继承 P0-CONTROL-V1。唯一变化是结果取得：在 matching prompt history 已确认成功且返回唯一 SaveImage 输出后，不再经 localhost HTTP `/view` 回读；客户端用 history 的 `type=output`、`subfolder`、basename `filename` 在已知 ComfyUI output root 内解析路径，解析结果必须仍位于该 root，然后读取同一文件。

每次必须完整验证 PNG CRC、完整 zlib、256×256、SHA-256 和 prompt/output 唯一归属。不得轮询、跳过 history、减少 workload 或伪造完成。

合同候选等价性：每个 B measured run 在正式计时结束后，再对同一 prompt 输出执行 HTTP `/view` 双取证，HTTP 与本地字节 SHA-256 必须一致；该双取证不进入性能计时。
