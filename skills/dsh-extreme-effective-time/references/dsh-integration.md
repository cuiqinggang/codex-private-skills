# DSH 接入与真实边界
## 已有入口
- DSH Home：C:\AI\DeepSeek-Harness-Trial\dsh-home-mature-agent
- 原生技能根：该 Home 下 skills；用官方 filesystem provider 和 skill loader 按需发现/加载。
- 工作区：C:\AI\DeepSeek-Harness-Trial\workspace\deepseek-mature-agent
- 已验收隔离运行时：C:\AI\DeepSeek-Harness-Trial\dsh-0.2.1-rc.2-isolated\node_modules\@deepseek-ai\dsh\lib\bin.js
- 增强薄入口：C:\AI\DSH-Acceleration-20261024\launch.py / Run-DSH.cmd
- 实测依据：C:\AI\DSH-Acceleration-20261024\README.md、FINAL.json
上述为2026-10-24实测路径，使用前查当前存在性和实际入口；不得凭旧路径推断当前版本或上线状态。凭据只由原官方机制使用，不复制、不输出。

## 调用
用原生 skill 工具加载 dsh-extreme-effective-time，或官方直接用户调用 /dsh-extreme-effective-time。
增强 launch.py 为新任务默认加该原生技能调用；这是一条薄入口，不新增执行引擎。Web 工作区 AGENTS.md 提供调用路由；其他入口仅目录存在不证明其已自动加载。

模型候选：fast 使用经测 Flash/high，deep 保留 Pro/max，browser 仅按需加载原正式 MCP。模型选择不能替代业务成熟路径选择；不得自动绕过权限。只读默认；授权文件工作可用既有 workspace-write。原生 --session-id 须保持原工作目录和可兼容 preset。

## 实证范围（不是普遍性能承诺）
本轮原始数据任务：Pro/max 39.268秒；Flash/high 36.349秒；精确输出合同与精简 headless 配置32.753秒。仅单样本、子进程计时，有缓存/负载干扰；不包含全部调研/协调，不是完整项目T_VALID，不宣称十倍或稳定优势。
已通过：DSH原生skill加载并按严格合同审查、read→write→read实际产物、官方MCP browser_tabs只读、原生会话跨进程延续。
旧泛化审核首次输出夹带错误去重建议与虚构元数据，完整质量FAIL；明确合同优先和输出字段后复验通过。将此作为反例，禁止只凭工具调用和正面关键词判整篇合格。
仍未证明：复杂生产任务普遍收益、浏览器导航/点击与冲突写入、崩溃/重启自动恢复、GPT页面自动交接、24小时无人值守。

## 按需复用
- 浏览器唯一权威：C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\SKILL.md；动作前读取其当前合同。
- 组织/恢复基线：C:\AI\AI-Organization-V3-ExtremeTime-20261023\SKILL.md；新版本若存在，以当前用户指定的有效版本为准，不覆盖冻结历史。
- 现成专业技能与索引：DSH Home 的 skills 与成熟工作区 registry/skills-index；先定位再读，禁止全量注入。
- 在线技能主源：本技能由 Skills Git 工作区维护；Windows DSH 安装副本应与已提交版本一致。更新时只同步本技能，校验哈希，不碰凭据。

## 商用任务合同示例
目标：在现有预约应用完成并发修复。
冻结前：读取现有源码/最近验收，至多比较三种已有成熟实现，推演双客户端争抢同一时段、超时后未知提交、重启后状态；选最短可靠路径。
冻结后：实施所选修复，交付实际可操作应用与源码，用真实并发和数据读回验证；虚拟推演不能替代实测。历史已通过的无关功能不重测。
只有最终合同全部通过才计T_VALID；未通过则保留同一任务编号继续修复，不能因生成了报告就结案。

## 2026-10-24 系统增强后续实测
任务：DSH-PERFORMANCE-20261024-001。证据：C:\AI\DSH-Acceleration-20261024\PERFORMANCE-FINAL.json、SANDBOX-BOUNDARY.json、PERFORMANCE-RESUME.json。
- 正常权限新工作区：C:\Users\A\Documents\DSH-Workspace；原 C:\AI 目录修复已被官方脚本拒绝，不重复该修复、不改原目录权限。
- 官方受限沙盒已验证：本工作区写入通过，工作区外写入拒绝，只读写入拒绝；不是关闭沙盒取得成功。
- 真实代码修复任务，三候选均通过同一6项业务断言、独立复验和测试/输入完整性校验：Pro/max 57.359秒，Flash/high 31.720秒，Flash/low 27.788秒。为单次同题完整执行与复验计时，不包含本轮全部调研/环境诊断；不外推其他任务。
- 通用入口保留 Flash/high；确定性任务可显式 --mode deterministic（Flash/low），难题 --mode deep 保留 Pro/max，浏览器 --mode browser 按需接现有正式 MCP。
- 增强入口新任务默认以上新工作区和 workspace-write，保留官方批准；恢复必须显式传原 --cwd。同一已修复工程的原生跨进程恢复复验通过，13.272秒，无重复修改；不是崩溃/重启/24小时自动恢复认证。
- Python 在受限令牌中创建的私有 tempfile 子目录仍可能不可读写；仅换 TEMP 路径不能解决，生产任务遇此须如实标注。不可关闭沙盒、移除 deny 或绕过批准。测试数据如能在运行前合法准备，可保持业务断言与测试完整性进行隔离验证；不能修改生产测试以掩盖缺陷。
- 旧环境首次对比 Pro/max 210秒超时、外部6项测试通过但DSH自身未交付，因此完整交付FAIL；该失败证据保留。修正的是验证输入准备方式与工作区兼容性，不宣称Python私有临时目录机制已经修复。


