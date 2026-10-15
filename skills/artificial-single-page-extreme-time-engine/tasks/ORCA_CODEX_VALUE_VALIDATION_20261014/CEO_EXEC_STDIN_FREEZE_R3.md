# R3：官方非交互输入候选与有界实测合同

方法三人行V2 C002，桥V7 C优先/A暂停。延续用户授权；旧被拒GitHub运行时预检不重发。R2子进程已关闭且外部QA不通过；新副本重放，已验GOOD不动。

## 整体差分与成熟候选
1. 原worker-start TUI：固定源码write-terminal-agent-prompt将完整pastePayload一次写PTY再发CR；shared/terminal-bracketed-paste-text把LF转CR。R2 ready/turn_started与无产物并存，根因仍未证明。桌面PR不能冒充headless修复，不盲补Enter。
2. 官方Codex exec：本机0.160.0 help确认非交互、stdin、JSONL、last-message。固定rust-v0.160.0 exec/src/lib.rs blob0bfa07bd5587f6913b21d137874430a982824c15确认AutoReview配置会重新加载而不强制Never。显式approval_policy=on-request、approvals_reviewer=auto_review、workspace-write。选择这一局部替代。
3. Orca structured worker：权限/事件/完成全链证据尚缺，本轮不混入另一未验变量。

## 本次闭合范围
Orca官方隔离JSON导入、工作树和terminal create复用已验路径；模型仍gpt-6.1-sol ultra、priority为请求。仅新任务两目录CLI信任，真实home登录复用，不读取凭据、不修改全局配置。Orca终端内Python最小适配通过argv启动官方exe，stdin文件只送一次，stdout JSONL/stderr独立落盘；终端handle和cwd回执核验。不是自研调度器。

单模型、4GiB余量，启动前核对本任务已有模型/Node进程。任务限定T03、离线标准库测试，不调用外部业务API。模型最多360秒，超时或UNKNOWN不重发；只清理由当前官方server子孙关系确认的本次进程，保留所有证据。正常进程退出后官方terminal close；服务收尾仍用已验拥有关系清理。

验收需要exit0、DELIVERY、固定外部T03/compile三项全部通过且原BAD仍失败；之后独立回读源码差分、结果和进程。退出码/terminal就绪不是业务通过。局部脚本计时含组件准备至本地结果回读，另行归档时间不能遗漏；本次没有原生对照，不宣称效率增益。

## 冻结
analysis/business-exec-r3.py@f743b96dc079725337be2a820c7d22d3bc910189，blob de7bebc2dde11f55f978207323980ec4087ba74c，已逐字回读。
新目录business-exec-20261015-r3，存在则拒绝重跑。回滚为关闭本次拥有进程、保留隔离目录，未替换原软件。

本范围虚拟审查可进入一次有界Reality；整套Orca orchestration worker派发/heartbeat/completion/recovery未通过。本轮即使T03通过，也只认证Orca terminal→Codex exec→外部验收，不增加正式三任务、10轮、AB计数，不发布融合技能包。
