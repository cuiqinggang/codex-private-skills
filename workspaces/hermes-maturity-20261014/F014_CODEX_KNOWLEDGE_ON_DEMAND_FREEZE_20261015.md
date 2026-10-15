# F014｜Hermes 跨Codex技能/Knowledge Brain按需检索能力验证
任务 HERMES-ECO-20261014，继承 F013 已经实际PASS的 Hermes 原生技能发现171项，方法《三人行》V2+执行桥V6 C优先+原母技能v2.0，STATE=VIRTUAL_MATURE_FROZEN。
原则：用户想让约400个技能及知识资产可使用；现实盘点Codex218份SKILL.md，Hermes旧161份SKILL.md（当前索引171条）和KB632文件，不能简单相加或宣称均自动可执行。
成熟路径：Hermes `skill_view` 对自有技能按需读取；跨Codex/Knowledge不靠复制数百文件，使用现有 Hermes原生 `read_file` / `search_files` 与已有Knowledge Brain INDEX.md→ROUTING_MAP.md→索引→定点Top-K SKILL.md。Codex源码保持唯一，严格只读，不触碰任务非必需系统。
第一次Reality极小验证：新Hermes正式CLI单次只读任务，让其真实读取 C:/Users/A/.codex/skills/verification-before-completion/SKILL.md 与 C:/Users/A/.codex/knowledge-brain/ROUTING_MAP.md，输出技能标题/最低验收原则以及Knowledge对reusable skills的第一目标索引和第二目标目录；必须基于真实tool result，不可凭提示词猜测。未来业务凭此方案取得所需片段并应用，避免加载全量632文件。
KEEP条件：原生工具实际返回跨根文件并且内容准确、只读、无凭据泄露；ABANDONED：文件权限/工具路径拒绝，停在首次差分，改走已授权直接Windows文件读取+Hermes任务隔离输入，不绕过用户授权。
后续将验证成功的顺序沉淀到当前 Hermes母技能短入口指针及独立references中，不改变已有上位方法v2，也不将 external_dirs 全量指向可写Codex目录——官方文档明确外部目录一旦可写，就能被agent的skill_manage修改，需先解决共享资产安全/同名冲突才能开放批量索引。
完成这项只认证跨根只读知识复用，不代替脚本执行权限或整站5轮/长稳认证，FINAL_VALID仍NO。
