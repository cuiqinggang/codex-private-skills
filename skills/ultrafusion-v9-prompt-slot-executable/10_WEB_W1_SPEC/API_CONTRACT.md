# API 合约

- `POST /runs` 新建运行
- `POST /runs/{id}/baseline` 录入基线
- `POST /runs/{id}/seal` 封存
- `POST /runs/{id}/stages/{stage}` 保存阶段输出
- `POST /runs/{id}/lock-final` 锁定终稿
- `POST /runs/{id}/open-comparison` 打开比较副本
- `POST /runs/{id}/value` 保存价值报告
- `GET /assets/{slot}` 只返回装载状态/哈希；提示词正文仅向受控执行服务只读提供

