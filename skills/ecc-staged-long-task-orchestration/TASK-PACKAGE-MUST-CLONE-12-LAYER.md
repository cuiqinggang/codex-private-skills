# Task Package Must Clone 12 Layer

任何长任务命令包都必须克隆 Claude-style 12 Layer 原始结构。

## 固定格式

每一层都必须按这个格式写：

```text
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
```

## 不启用机制时的固定格式

如果某一层本任务不启用某个机制，也必须写：

```text
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

不能空着，不能省略。

## 一票否决

- 把 12 Layer 改成普通 12 步，FAIL。
- 使用“目标确认 / 现状读取 / 风险识别”等替代原始 12 层，FAIL。
- 只写英文层名，不写中文名，FAIL。
- 没有写层与层的连接关系，FAIL。
- Layer 5 没有写独立上下文、角色、权限、输出契约，FAIL。
- Execution Plane 自己宣布 final PASS，FAIL。
- Verification Plane 缺失，FAIL。
- Repair Loop 缺失，FAIL。
- Final Acceptance 缺失，FAIL。
- Codex 只返回文件夹路径，FAIL。
## 中文详细执行标准要求

任何 P3 FINAL-EXECUTABLE-TASK-PACKAGE 不仅要克隆 12 Layer 名称，还必须按 `CLAUDE-CODE-12-LAYER-DETAILED-CHINESE-EXECUTION-STANDARD.md` 写出每层中文详细操作标准。

每层必须包含文件要求、内容要求、禁止事项、时间门槛关联、多智能体 / 上下文隔离要求、Verification Plane 接受条件和失败返回。
