# GPT Request 12 Layer Command Pack Template

```text
TASK_ID:
TASK_NAME:

请按 Claude-style 12 Layer 原始结构生成完整可执行命令包。

硬规则：
1. 不能改成普通 12 步。
2. 不能改名、不能压缩、不能重解释。
3. 必须保留 12 个原始英文层名和中文名。
4. Layer 5 必须写独立上下文、角色、权限、输出契约。
5. Execution Plane 只能 claim，不能 self-accept。
6. Verification Plane 负责 acceptance / rejection。
7. Repair Loop 处理 rejected claims。
8. 没有 final acceptance，没有 final PASS。
9. Codex 不能只返回文件夹路径。

每层固定格式：

Layer X — 原始英文名
中文名：

本层目的：
本层输入：
本层动作：
本层产物：
本层验证：
失败返回：
证据路径：
本任务中的具体应用：

如果本任务不启用某机制，也必须写：

本任务不启用该机制，原因：
1.
2.
3.

替代保障：
1.
2.
3.

是否被 Verification Plane 接受：
YES / NO
```
