# 同类故障决策树

```text
新建会话异常
│
├─ session/meta/index 没创建
│   └─ 查 create/path/permission/writer
│
└─ session/meta/index 已创建
    │
    ├─ 数据库 quick_check 失败
    │   └─ 数据层专项
    │
    └─ 数据库正常
        │
        ├─ 0-byte transcript 后端测试不支持
        │   └─ 查后端 empty contract
        │
        └─ 后端明确支持 empty transcript
            │
            ├─ ready=false 时就开始 hydrate
            │   └─ 前端 race 高概率
            │
            └─ ready=true 后才 hydrate
                └─ 继续查 UI error mapping / stale navigation
```

## 重装还是补丁？

```text
根因未知 + 安装疑似损坏
    -> 保护性官方重装/升级

根因已确认 + 最小补丁已验证 + 只剩部署
    -> 最小热补丁

官方更高稳定版已明确包含同等修复
    -> 官方升级优先于私有补丁
```
