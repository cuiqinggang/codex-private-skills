# GPT Final Acceptance Review Template

```text
TASK_ID:
TASK_NAME:

你正在做 GPT 最终验收。

请检查：
1. 是否完整保留 12 层英文名。
2. 是否完整保留 12 层中文名。
3. 是否明确禁止普通 12 步替换。
4. 是否明确不能改名、不能压缩、不能重解释。
5. Layer 5 是否有独立上下文、角色、权限、输出契约。
6. Execution Plane 是否只能 claim，不能 self-accept。
7. Verification Plane 是否负责 acceptance / rejection。
8. Repair Loop 是否处理 rejected claims。
9. 是否没有 final acceptance 就没有 final PASS。
10. Codex 是否没有只返回文件夹路径。
11. 是否有 final-acceptance.md。
12. 是否有 final-acceptance.json。

输出：

Final Result: PASS / PARTIAL / FAIL

Acceptance:
- 12 layer names preserved:
- Chinese names preserved:
- ordinary 12-step replacement blocked:
- Layer 5 context isolation valid:
- Execution Plane claim-only:
- Verification Plane independent:
- Repair Loop closed:
- Final Acceptance authoritative:
- Codex evidence return sufficient:

Rejected claims:

Required repair:

Final status code:
ECC_STAGED_LONG_TASK_12_LAYER_COMPACT_CORE_FLOW_PATCH_PASS
```
