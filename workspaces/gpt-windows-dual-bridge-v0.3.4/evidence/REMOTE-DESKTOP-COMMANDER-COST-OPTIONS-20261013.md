# 《三人行》第2版候选评估｜Remote Desktop Commander 自建中转与云服务器｜2026-10-13

## 核心事实与范围
- Desktop Commander MCP 本地实现可开源使用；官方 Remote Desktop Commander hosted relay 的**服务端非开源**。购买 VPS 不意味着可直接部署官方收费 relay。
- 官方远程定价：Free $0/月含 10,000 次工具调用；Pro $20/月无月度次数上限。来源 https://desktopcommander.app/pricing/
- 用户已有可用的 OpenAI 官方 Secure MCP Tunnel + 本地 Desktop Commander MCP 0.2.52；2026-10-12 原始独立验收详见 skills/extreme-time-automation-bridge/evidence/OPENAI_TUNNEL_REAL_WINDOWS_REMOTE_PASS_20261012.md。
- 该链路真实 PASS：ChatGPT tools/list 26 工具、目录读取、写文件、读回、PowerShell 运行及退出码。尚未证明：重启登录自动恢复、长期稳定、全面权限审查。2026-10-13 当前 v0.3.4 也有 A 通道真实 Windows 工具调用 PASS。不能把这条渠道与 Remote Desktop Commander 托管额度混为一谈。
- 现有 GitHub Actions 备路 PASS 轻任务，但 2026-10-12 原生产工作流因下载 actions/upload-artifact ZIP 超时失败；不要把所有任务改走 GitHub。

## 三个成熟候选
A. 零新增 VPS：保留已验证的 OpenAI Secure MCP Tunnel + Windows 开源 Desktop Commander MCP；维护启动可靠性、密钥最小权限与审批规则。边际服务器租用费 $0，但可能受 ChatGPT/Platform 使用权限、政策和平台服务限制；不承诺绝对无额外费用或无配额。第一推荐。
B. 完全自有中转：Windows 出站连接 → 自控 HTTPS/OAuth MCP 网关/反向连接 → ChatGPT。建议优先 DigitalOcean Basic Droplet 1 GiB 1 vCPU 25 GiB SSD，2026-10-13 官方标价 $6/月：https://www.digitalocean.com/pricing/droplets。仅承载 relay，不在 1GB 机器上运行视频模型/复杂并行计算。开源组件可选 Desktop Commander stdio + 成熟的 Supergateway（stdio↔Streamable HTTP）或受维护的 MCP proxy，Cloudflare Tunnel/Access、OAuth；必须验证与 ChatGPT 实际适配及强认证。不可直接暴露无认证的 Shell API。需要管理服务器升级、监控、凭据、审计和可用性。
C. 原厂托管：Remote Desktop Commander Pro $20/月，不用自建中转，管理时间最少，月度工具调用无限，但依赖第三方服务及其政策。高工作量而不愿运维时可选。

## 价格备选/风险
- Hetzner EU CX23 2 vCPU/4GiB/40GB NVMe：2026-06-15 之后欧区标价 $6.49/月（税前，IPv4 另计 $0.60），即约 $7.09/月；资源/美元更高。官方价 https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/；IP 价 https://docs.hetzner.com/cloud/servers/primary-ips/overview/ 。官网此时部分机型显示 unavailable，库存需下单时核对；欧洲地点未必有最佳延迟。
- Oracle Always Free 不是正式稳定性首选：有闲置资源回收条件、容量与账户约束。 https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Cloudflare Tunnel 免费方案（https://developers.cloudflare.com/tunnel/）可以提供出站连通而无需自备 VPS，但**不自动提供完整 OAuth、安全授权、审计与 ChatGPT 客户端兼容性**；自定义域名可能额外付费。
- 价格均为公布值、可能因税、区域、IP、快照、域名、网络使用而变化；不可承诺全包固定成本。

## 方案收敛（非部署合同）
1. 当前最佳：**不购买 VPS，不复制官方 proprietary relay**；继续用现有实际 PASS 的开源 MCP + 官方 Secure MCP Tunnel。维持 FlClash、Windows 代理、浏览器、GitHub Runner 原状。
2. 完成最小增量验收：授权边界、Runtime Key 权限轮换与保管、单实例运行、Windows 重启后自动重连，真实 GPT→Windows 读/写/命令并回执；监控心跳与异常恢复；保留 GitHub B 为独立备用。
3. 若用户要求**彻底脱离第三方隧道配额/供应商**且实际测出限制，再隔离部署 DigitalOcean $6 VPS 自建授权中转；并与现有 A 做 10-30 个等负载任务端到端用时、成功率、恢复、维护成本对比。
4. 采购、订阅、迁移、代理/防火墙改动和取消现有桥需要单独授权；目前仅调研，不产生服务费用。
5. 无论选哪项，Windows 本机必须持续运行且联网；购买 VPS 不能自动修复本机掉线、断电、会话注销。
6. 如果后续变更多端 OAuth，需按当前 MCP 协议兼容性和实际 ChatGPT 账号权限实测；不得把『云主机在线』等同于『ChatGPT 可安全执行全部工具』。

## 冻结状态
DECISION=NO_PURCHASE_FIRST / PREFER_EXISTING_PROVEN_ROUTE
ALTERNATE_IF_NEEDED=DIGITALOCEAN_1GB_6USD
REALITY=EXISTING_ROUTE_PASS / NEW_VPS_NOT_DEPLOYED
EVIDENCE_DATE=2026-10-13
