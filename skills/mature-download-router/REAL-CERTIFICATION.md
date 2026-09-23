# v0.1.2 Reality Certification

原则：这个技能只负责“把下载任务交给成熟下载工具”。不再为路由规则设计多阶段认证。

唯一现实认证目标：

```text
把一个最小真实下载任务交给成熟下载器
-> 文件成功落地
-> 文件大小 > 0
-> 记录 T_VALID
```

固定最小测试：

```text
TOOL=aria2c
URL=https://raw.githubusercontent.com/aria2/aria2/release-1.37.0/README.rst
DEST=C:\AI\Mature-Download-Router-Real-Test\minimal\README.rst
NETWORK_CONTEXT=http://127.0.0.1:7890
```

只使用当前已存在的网络出口，不修改任何持久代理设置。

PASS：

```text
aria2c command succeeds
OUTPUT_EXISTS=YES
OUTPUT_SIZE>0
T_VALID_MS recorded
```

PASS 后：

```text
REAL_CERTIFIED=YES
```

以后遇到 Hugging Face / GitHub / Browser 等来源，直接按 SKILL.md 的成熟工具映射调用；不再为本技能额外制造测试工程。具体成熟工具若在未来真实任务中失败，再记录该现实差异。
