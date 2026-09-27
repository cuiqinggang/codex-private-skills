# v5.2.1 修复经验沉淀：R1-R4

## 总原则

1. 单点故障只做单点修复：ISOLATED_FAILURE_REQUIRES_ISOLATED_FIX。
2. 只有出现系统性/架构性证据，才允许扩大修改面。
3. 未实际执行的检查只能记 NOT_RUN，不能推断 PASS。
4. 真实使用测试失败必须区分 PRODUCT / TEST_HARNESS / EXTERNAL。
5. 测试设施失败不能自动推导产品失败。
6. 已经通过且与当前故障无关的冻结资产必须保持 blob 不变。
7. 用户可见控制面保持最小；机器审计细节放 Freeze Manifest / Contract。

## R1：Markdown 传输等价假阴性

现象：时间锚中的 T-star 在 Markdown 传输后增加单层转义，Validator 误判缺少数字时间锚。

根因：Validator 对展示层字节形式过度严格。

正确修复：
- 时间锚及数字仍是硬门。
- 仅允许 T-star 原形与单层 Markdown 转义语义等价。
- 双层异常转义、token 改名仍拒绝。
- 不做广泛 Markdown 去转义。

经验：验证器应检查业务语义和关键结构，不应把无害的传输层表现差异当产品故障。

## R2：临时辅助脚本 KeyError

现象：Codex 在真实使用测试中临时编写参数提取脚本，脚本自身 KeyError，冻结 Renderer 尚未运行。

归因：
- FAIL_SOURCE=TEST_HARNESS
- PRODUCT_DEFECT_ESTABLISHED=NO

正确修复：
- 真实使用测试阶段禁止临时编写辅助脚本。
- 需要自动化的验证器/工具必须在虚拟阶段预先实现、回归并 Freeze。
- 测试设施故障修复后必须从测试入口重新运行，不从故障点继续算 PASS。

经验：不要把测试器本身变成新的未测试产品。

## R3：LF→CRLF 物化差异

现象：Windows worktree 将 Git 中 LF 物化成 CRLF；git diff 因归一化为空，但原始工作区 bytes 与 Freeze blob 不同。

归因：
- FAIL_SOURCE=TEST_HARNESS
- PRODUCT_DEFECT_ESTABLISHED=NO

正确修复：
- Freeze 字节身份权威源 = GIT_OBJECT_BYTES。
- 精确字节执行从 Git 对象数据库无损物化。
- Worktree 原始 bytes 不作为跨平台 Freeze 身份证据。
- 不修改 core.autocrlf、系统 Git 设置或产品文件来迎合验收。

经验：冻结身份必须锚定不可变对象，不锚定可能被平台转换的工作区表示。

## R4：最小修复验证

R4 只修改物化/校验规则，不修改 Runtime、Renderer、低层测试、时间规则、Markdown 等价规则、简洁派发和产品逻辑。

实际结果：
- RESULT=PASS
- FAIL_SOURCE=NONE
- PRODUCT_DEFECT_ESTABLISHED=NO
- Freeze/Manifest 原始字节核验通过
- Runtime/Test 相对 R3 保持不变
- 精确冻结字节低层回归 10/10 PASS，退出码 0
- 冻结 Validator 校验接收原文 PASS
- Freeze→实、Locator、时间锚、简洁派发均 PASS

## 长期固定规则

故障处理顺序固定为：

观察真实失败 → 分类 PRODUCT/TEST_HARNESS/EXTERNAL → 找最小根因 → 仅修改根因对应层 → 保持无关已通过资产不变 → 低层回归 → 新 Freeze → 重新真实使用测试。

禁止“看到一个故障就顺手重构整个系统”。
