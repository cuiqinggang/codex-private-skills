# B33 无业务真实交接测试合同
TASK_ID=B33_REAL_HANDOFF_SMOKE_20261009
CONTRACT_VERSION=1
ROUTE=B
METHOD=B33/B29/B23
FINAL_GOAL=新ChatGPT聊天收到本测试任务的短状态码，从GitHub读取真实CURRENT/F001，确认和为42，然后仅回复ACK-B33-SMOKE-42，不创建更多聊天。
DONE_WHEN=仅当本测试聊天能够按冻结事实回复ACK-B33-SMOKE-42时完成。不是实际业务发送。
INPUT=8+13+21
EXPECTED=42
PROHIBITIONS=不发送业务消息、不再次交接其他聊天、不操作网络代理、不下载/复制私密数据、结果未知不重试发送。
