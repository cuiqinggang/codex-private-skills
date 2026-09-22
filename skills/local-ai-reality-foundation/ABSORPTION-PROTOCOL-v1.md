# Foundation 任务后吸收合同 v1

每个任务在现实结果结束后都必须运行一次逻辑检查，但不必每次都升级 Foundation。

## 输入
- 新 Reality facts
- 新 T_VALID / timing
- 新失败根因
- 新环境边界
- 新成熟本地资产

## 唯一吸收判据

```text
未来是否能：
A. 缩短达到 VALID 的时间
或
B. 避免重复 Reality 采集/重复失败
或
C. 让 Exact Twin 保持完成当前任务所需的必要真实性
```

A/B/C 全 NO：
```text
ABSORB=NO
```

至少一个 YES：
```text
ABSORB=YES
```

## 禁止吸收
- 与未来任务无关的日志噪声；
- 可以从已有资产确定性再生的数据；
- 只为了“更完整”而存在的数据；
- 无来源的推断；
- Shadow 假设冒充 Reality。

## 新版本要求
- 完整当前 snapshot；
- 本版 delta；
- evidence pointer；
- previous_version；
- version bump reason；
- 历史版本不覆盖。
