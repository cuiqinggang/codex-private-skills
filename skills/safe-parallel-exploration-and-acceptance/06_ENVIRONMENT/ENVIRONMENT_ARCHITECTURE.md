# Environment Architecture

Worktree 只隔离文件；Environment 负责运行时、依赖、本地私有配置、验证和测试。每棵工作树独立验证，不共享可写虚拟环境。

