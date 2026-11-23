# V15 注入验收门报告

**验收门规则**:
- A/B/C/D 每层 prompt 必须包含 V15
- 必须记录 V15_SHA256
- 必须记录 PROMPT_ASSEMBLY_STATUS
- 任一层缺失 V15 → UF_PROMPT_ASSEMBLY_FAIL
- 失败层的输出不得进入下一层

**状态**: ✅ 全部规范已创建
