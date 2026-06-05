---
name: overseas-ai-region-setup
version: 0.4
description: 海外AI服务地区配置综合技能包 — IP检测+链路配置+浏览器环境+系统设置+Codex OAuth登录，可回滚可升级
trigger: 当用户需要配置海外AI服务的网络环境、通过OpenAI/Claude/Codex等风控检测、或执行Codex OAuth登录时加载此技能
---

# 海外AI服务地区配置综合技能包（可回滚）

## §0 核心原则

- **所有修改前必须快照当前状态**，存入回滚文件
- **最小改动优先**：先改必须项，通不过再逐步加码
- **可回滚**：任何配置都能一键恢复到修改前
- **用户语言偏好**：中文用户，系统语言不改英文（除非通不过再加）
- **综合工程**：这不是单一配置，是IP→链路→浏览器→系统→OAuth的完整链路

## §1 工程全景图

```
用户电脑
  │
  ├─ ① 代理层：Clash/跑跑云(出国) → 住宅IP(落地)
  │     目标：出口IP为美国住宅IP，ASN为美国ISP
  │
  ├─ ② 浏览器层：指纹浏览器(AdsPower等)
  │     目标：时区/语言/位置/IP一致，WebRTC不泄露
  │
  ├─ ③ 系统层：时区/区域设置
  │     目标：与IP所在地一致
  │
  ├─ ④ 账号层：Billing Address + OAuth
  │     目标：地址显示+美国真实地址，Codex OAuth授权
  │
  └─ ⑤ 验证层：Ping0/Whoer/browserleaks
        目标：风控值<20，匿名度100%，无泄露
```

## §2 IP纯净度检测

### 2.1 命令行快速检测

```bash
# 1. 查出口IP和ASN
curl -s ipinfo.io

# 2. 查IP类型/风控/proxy/hosting
curl -s "http://ip-api.com/json/{IP}?fields=status,isp,org,as,hosting,proxy,mobile"

# 3. 查ASN归属地（判断住宅vs机房）
curl -s "https://rdap.arin.net/registry/autnum/{ASN号}" | python3 -c "
import sys,json
d=json.load(sys.stdin)
print('ASN名称:', d.get('name','N/A'))
for e in d.get('entities',[])[:3]:
    vcard=e.get('vcardArray',[[],[]])
    if len(vcard)>1:
        for item in vcard[1]:
            if item[0]=='fn': print('实体:', item)
"
```

### 2.2 浏览器深度检测（需CDP）

- **Ping0.cc** → 风控值<20为极度纯净，15以下绿色，>30需警惕，>70必换
- **Whoer.net** → 匿名度100%，不显示"使用代理"
- **browserleaks.com/webrtc** → 检查WebRTC是否泄露真实IP
- **browserleaks.com/dns** → 检查DNS是否泄露

### 2.3 判定标准

| 检测项 | 通过 | 警告 | 不通过 |
|--------|------|------|--------|
| IP类型 | 家庭宽带/住宅 | 商业 | IDC机房/数据中心 |
| Ping0风控值 | <15 | 15-30 | >30 |
| Whoer匿名度 | 100% | 80-99% | <80% |
| 代理检测 | 否 | - | 是 |
| hosting字段 | false | - | true |
| ASN归属 | 美国ISP运营商 | - | 香港/离岸实体 |

### 2.4 已验证IP记录

| IP | ASN | ISP | 类型 | 风控 | 检测日期 | 结果 |
|----|-----|-----|------|------|----------|------|
| 142.249.37.52 | AS153371 BACK WAVES LIMITED | Back Waves Limited | ❌机房 | 未知 | 2026-05-01 | 不通过(香港注册实体) |
| 162.251.248.10 | AS10753 Level 3 Parent, LLC | Level 3 Communications | ✅住宅 | 低 | 2026-05-01 | 通过(美国本土ISP) |

## §3 链路配置（Clash链式代理）

### 3.1 架构

```
电脑 → 跑跑云(出国) → 住宅IP(落地美国) → OpenAI
        第一层代理          第二层代理
```

### 3.2 Clash配置方法

在Clash配置文件中添加链式代理节点：

```yaml
proxies:
  # 第一层：跑跑云节点（已有）
  - name: "跑跑云-美国"
    type: ss
    server: xxx
    port: xxx
    ...

  # 第二层：住宅IP（新增）
  - name: "住宅IP-California"
    type: socks5  # 或 http
    server: 162.251.248.10
    port: 12324
    username: <REDACTED_USERNAME>
    password: <REDACTED_PASSWORD>

  # 链式代理组合
  - name: "跑跑云→住宅IP"
    type: relay      # Clash的relay模式
    proxies:
      - 跑跑云-美国
      - 住宅IP-California
```

**注意：** 具体Clash配置格式取决于用户使用的Clash版本（Clash for Windows/Clash Verge/mihomo等）。relay模式在mihomo中可用，Clash for Windows可能需要用proxy-chain插件。

### 3.3 验证链路

配置完成后验证：
```bash
# 全局模式切换到链式代理节点后
curl -s ipinfo.io
# 应显示 162.251.248.10 和 Level 3 / eBlue Networks

curl -s "http://ip-api.com/json/?fields=isp,org,as,hosting,proxy"
# 应显示 hosting=false, proxy=false
```

## §4 浏览器环境配置（指纹浏览器）

### 4.1 推荐方案：AdsPower指纹浏览器

**创建新环境配置：**
```
名称: OpenAI-Codex-US
代理设置:
  类型: SOCKS5
  地址: 162.251.248.10
  端口: 12324
  账号: 14ae9af0bd9b5
  密码: 34baac8d16

指纹设置:
  语言: zh-CN (先不改，通不过再改en-US)
  时区: 基于IP自动 → America/Los_Angeles
  地理位置: 基于IP自动 → Lawndale, California
  WebRTC: 禁用UDP 或 替换为代理IP
  Canvas: 随机但固定
  WebGL: 随机但固定
  User-Agent: 默认(先不改)
  分辨率: 1920x1080
  字体: 默认英文集
```

### 4.2 替代方案：系统Chrome + 代理插件

如果不用指纹浏览器，也可以：
1. Chrome安装 SwitchyOmega 插件
2. 配置代理指向住宅IP
3. 安装 WebRTC Control 插件禁用WebRTC
4. 手动修改Chrome语言设置（如果需要）

**但注意：** 普通Chrome会泄露更多指纹，通过率低于指纹浏览器。

### 4.3 绝对不能出现的矛盾组合

- IP在美国 + 时区是Asia/Shanghai ❌
- IP在加州 + 地理位置在纽约 ❌
- WebRTC：**选Forward或Replace，不要选Disabled/DisableUDP**
  - Forward = 最自然，WebRTC显示住宅IP，像正常美国用户
  - Replace = 次选，用代理IP替换真实IP
  - Disabled/DisableUDP = 此地无银三百两！正常用户WebRTC是开着的，你关了反而可疑
  - Real = 绝对不能用，会泄露中国真实IP
- DNS用114.114.114.114 ❌
- Billing Address"不显示" ❌（比填错地址还差）

## §5 配置分层（从必改到可选）

### 第1层：必须改（不改必挂）

| # | 项目 | 目标 | 说明 |
|---|------|------|------|
| 1 | IP类型 | 独享静态住宅IP | 机房IP必被识别，ASN必须为美国ISP |
| 2 | 时区 | 与IP所在地一致 | Lawndale CA → America/Los_Angeles |
| 3 | WebRTC | 禁用或替换 | 防止泄露真实IP |
| 4 | DNS | 不泄露国内DNS | 指纹浏览器自动处理 |

### 第2层：建议改（大幅提升通过率）

| # | 项目 | 目标 | 说明 |
|---|------|------|------|
| 5 | Billing Address | 显示+填美国真实地址 | "不显示"=不信任，显示=可验证 |
| 6 | 地理位置 | 与IP城市一致 | 指纹浏览器中设置 |
| 7 | 浏览器语言 | en-US | 可先不改zh-CN，通不过再加 |

### 第3层：可选改（通不过时最后加码）

| # | 项目 | 目标 | 说明 |
|---|------|------|------|
| 8 | 系统区域 | 美国 | Windows设置→区域 |
| 9 | 系统语言 | 英文 | 最大改动，最后才考虑 |
| 10 | User-Agent | 英文OS | 指纹浏览器配置 |

## §6 OpenAI Codex OAuth 登录

### 6.1 登录方式

Hermes支持 `openai-codex` provider，通过OAuth认证：
```bash
hermes auth openai-codex
```

### 6.2 登录流程

1. **环境准备**：确保住宅IP链路已配置，指纹浏览器环境就绪
2. **执行授权**：`hermes auth openai-codex`
3. **浏览器弹窗**：会打开OpenAI登录页面
4. **完成登录**：用ChatGPT Plus账号登录
5. **授权确认**：点击"Continue"允许Codex访问
6. **返回Hermes**：授权完成，token缓存在本地

### 6.3 关键注意

- **必须用住宅IP环境**来打开OAuth弹窗，否则OpenAI可能拒绝
- Codex CLI也支持 `--device-auth` 模式（设备码登录），适合无浏览器环境：
  ```bash
  codex login --device-auth
  ```
- OAuth弹窗如果不工作，可尝试Device Code模式
- ChatGPT Plus订阅是前提，Codex走Plus订阅不走API Key

### 6.4 验证登录

```bash
hermes auth status
# 或
codex --check-login
```

## §7 回滚机制

### 7.1 快照文件

每次修改前，将当前状态写入快照目录：
```
~/.hermes/skills/productivity/overseas-ai-region-setup/snapshots/snapshot_YYYYMMDD_HHMMSS.json
```

快照内容模板：
```json
{
  "snapshot_id": "INITIAL_20260501_233000",
  "timestamp": "2026-05-01_23:30:00",
  "description": "修改前初始状态",
  "ip": "142.249.37.52",
  "ip_type": "datacenter",
  "ip_asn": "AS153371 BACK WAVES LIMITED",
  "timezone": "Asia/Shanghai",
  "browser_lang": "zh-CN",
  "system_region": "CN",
  "system_lang": "zh-CN",
  "webrtc": "default",
  "dns": "default",
  "billing_address_visible": false,
  "geolocation": "default",
  "user_agent": "default",
  "proxy_config": "跑跑云全局模式",
  "fingerprint_browser": "未使用",
  "notes": ""
}
```

### 7.2 回滚流程

1. 读取目标快照文件
2. 逐项对比当前值 vs 快照值
3. 对有差异的项，恢复为快照中的原始值
4. 输出回滚报告：哪些恢复了，哪些无法自动恢复

### 7.3 无法自动恢复的项

以下需要手动恢复：
- IP/代理切换（需在Clash中操作）
- OpenRouter Billing Address（需在OpenRouter网站操作）
- 指纹浏览器配置（需在AdsPower中操作）
- 系统语言（需Windows设置中操作）

## §8 IP被污染/失效的处理

### 8.1 判断IP是否需要换

- 之前能用，现在通不过 → **大概率IP被污染**
- Ping0风控值从低变高 → **被标记了**
- IP类型从"家庭宽带"变"IDC机房" → **数据库更新了**
- 指纹浏览器之前能过现在不行 → **IP可能被污染或风控升级**

### 8.2 换IP注意事项

- 新IP必须是**独享**的（不要共享）
- 换IP后**同步更新**指纹浏览器中的时区、语言、地理位置
- 新IP到手**先检测**纯净度再使用
- 不要用之前用过的IP（可能已被标记）

## §9 住宅IP服务商参考（2026年）

| 服务商 | 价格 | 付款方式 | 特点 |
|--------|------|----------|------|
| IPRoyal | $4.04/月 | 信用卡/PayPal | 静态住宅IP，<5个IP需KYC护照 |
| Cliproxy | $3.8/月 | 支持支付宝 | 中国用户友好 |
| kookeey | 多种套餐 | 支持支付宝 | 指纹浏览器生态集成 |
| Tello美国电话卡 | $5/月起 | 信用卡 | 真实移动IP，最纯净 |
| 用户当前住宅IP | - | - | 162.251.248.10:12324 (Level 3/California) |

## §10 陷阱与注意事项

- ip-api.com的hosting=false**不代表就是住宅IP**，很多小代理都报false
- ASN注册地在香港/离岸的，**基本是机房IP**，即使ip-api报hosting=false
- IP地理位置在美国 ≠ IP类型是住宅IP。**两个不同的维度**：地理看IP在哪，类型看ASN是谁发的
- Billing Address选"不显示"**比填错地址还差**，等于主动暴露可疑
- 频繁切换IP节点是**触发风控的头号原因**
- 指纹浏览器+住宅IP是黄金组合，缺一个都容易出问题
- WebRTC禁用 = 此地无银三百两，反而引起怀疑。应选Forward或Replace，让WebRTC显示住宅IP
- 系统语言先不改英文，**通不过再加**，避免影响日常使用
- 浏览器中文+IP美国 = 合理（美国华人用户），不算矛盾
- 时区中文+IP美国 = **矛盾**，必触发风控

## §11 完整操作步骤（基于社区成功经验）

> **昨日重现原则：以下步骤全部来自2026年社区实测成功经验，非理论推演。**
> 经验来源：AdsPower官方教程、William说(Youtube 1万+播放)、VPS大玩家、知乎专栏、X/Twitter社区实测

### 步骤1：准备住宅IP（最先做）

**为什么要先搞IP再装浏览器？** 因为指纹浏览器的时区、语言、地理位置都要跟IP走，IP不定下来，后面全白搭。

**操作：**
1. 购买独享静态住宅IP（参考§9服务商列表，或用你已有的）
2. 收到IP信息后，先检测纯净度：
   ```bash
   # 查IP和ASN
   curl -s ipinfo.io/{IP}
   # 查类型/风控
   curl -s "http://ip-api.com/json/{IP}?fields=isp,org,as,hosting,proxy"
   ```
3. 确认：ASN归属为美国ISP、hosting=false、proxy=false
4. 记录IP所在城市、州、时区（后面全要用）

**当前可用IP：** 162.251.248.10（加州Lawndale，时区America/Los_Angeles）

### 步骤2：安装AdsPower指纹浏览器

1. 下载安装：https://www.adspower.net/download
2. 注册登录（免费版有2个环境，够用）
3. 打开AdsPower客户端

### 步骤3：在AdsPower中新建浏览器环境

1. 点击左上角 **【新建浏览器】**
2. **基本设置：**
   - 名称：`OpenAI-Codex-US`（方便识别）
   - 分组：可自建"AI工具"分组

3. **代理设置：**
   - 代理类型：选 **自定义**
   - 💡 **快捷法：** 直接复制 `162.251.248.10:12324:14ae9af0bd9b5:34baac8d16` 粘贴到【代理主机】框，系统自动填充（出处：AdsPower官方帮助文档）
   - 点击 **【检查代理】** → 必须显示连接成功
   - 点击 **【确定】** 保存

4. **指纹设置（逐项详解，每项都有出处）：**

   **① 时区 → 基于IP自动（America/Los_Angeles）**
   - 是什么：浏览器告诉网站你所在的时区
   - 防什么：IP在加州但时区是Asia/Shanghai = 矛盾特征，直接被标记异常
   - 出处：腾讯云——"一致性，环境中的各项参数要对得上"；AdsPower官方——"同步设置纽约时区，显著提升稳定性"

   **② 语言 → 基于IP自动（先不改en-US）**
   - 是什么：浏览器告诉网站你用什么语言
   - 防什么：语言和IP严重矛盾会被标记，但中文+美国IP不算矛盾（美国华人多）
   - 出处：用户判断+AdsPower官方"基于IP自动"最安全

   **③ WebRTC → Forward（首选）或 Replace（次选）**
   - 是什么：浏览器通信协议，会暴露真实IP
   - 防什么：WebRTC可能绕过代理暴露中国真实IP
   - ⚠️ **绝对不要选Disabled/DisableUDP！** 正常用户WebRTC是开着的，你关了=此地无银三百两=反而可疑
   - Forward最自然=走STUN验证，像正常美国用户；Replace=用代理IP替换
   - 出处：AdsPower官方帮助文档——"Forward Mode uses Google's STUN servers to bypass detection"；BlackHatWorld——"Replace is usually the best option since it ensures your WebRTC IP matches your proxy"

   **④ Canvas → 随机（默认）**
   - 是什么：网站让你浏览器画隐藏图形，根据硬件差异生成"硬件身份证"
   - 防什么：多账号Canvas一样→平台判断同一台电脑→关联封号
   - 出处：AdsPower官方——"随机化设备指纹，彻底屏蔽真实硬件信息"；腾讯云——"真实用户的环境是有规律的，不是越随机越好"

   **⑤ WebGL → 随机（默认）**
   - 是什么：读显卡型号/驱动来识别你，和Canvas类似但是显卡信息
   - 防什么：同Canvas，多账号共享→关联
   - 出处：同Canvas

   **⑥ 地理位置 → 基于IP自动（Lawndale, CA）**
   - 是什么：浏览器告诉网站你的地理坐标
   - 防什么：IP在加州但位置在上海=矛盾
   - 出处：腾讯云一致性原则

   **⑦ User-Agent → 默认（基于IP自动）**
   - 是什么：浏览器告诉网站你用什么系统和浏览器版本
   - 防什么：中文系统UA包含zh-CN，可能和IP矛盾
   - 先不改，通不过再手动改英文Windows UA
   - 出处：腾讯云——"使用稳定的浏览器版本"

   **⑧ 分辨率 → 1920×1080**
   - 是什么：浏览器告诉网站你的屏幕多大
   - 防什么：异常分辨率容易被标记为模拟器
   - 1920×1080是全球最常见分辨率
   - 出处：腾讯云——"避免太特殊的参数"

   **⑨ 字体 → 默认英文集**
   - 是什么：浏览器告诉网站你安装了哪些字体
   - 防什么：暴露"宋体、微软雅黑"=明显中国电脑
   - 出处：知乎指纹浏览器文章——"字体列表是识别用户地区的重要维度"

5. **三大核心原则（出处：腾讯云开发者社区）：**
   - **一致性**：IP在哪，时区/位置/语言就跟到哪，不能矛盾
   - **唯一性**：每个环境指纹不同，不能关联
   - **稳定性**：不要频繁变来变去

6. 点击 **【确定】** 创建环境

### 步骤4：打开环境，验证指纹

1. 在【环境管理】中找到刚创建的环境，点击 **【打开】**
2. 浏览器打开后，逐个访问以下检测网站：

   **必检3项：**
   - **Ping0.cc** → 风控值应<30，IP类型应为"家庭宽带"
   - **Whoer.net** → 匿名度应100%，"代理服务器"应显示"否"
   - **browserleaks.com/webrtc** → 不应出现中国IP的ICE候选

   **如果3项全过 → 继续步骤5**
   **如果有1项不过 → 回到指纹设置排查**
   - Ping0风控值高 → IP可能被污染，需要换IP
   - Whoer检测到代理 → WebRTC没关好或DNS泄露
   - WebRTC泄露真实IP → 确认WebRTC设为"禁用UDP"

3. （可选）**ip-score.com** → 确认不在黑名单

### 步骤5：在AdsPower浏览器中访问OpenAI

1. 在AdsPower浏览器地址栏输入 `https://chat.openai.com`
2. 用ChatGPT Plus账号登录
3. **观察是否正常**：能登录、不跳验证、不报地区限制
4. 如果一切正常 → 继续步骤6

**如果被拦截/报地区限制：**
- 先检查Ping0/Whoer是否过关
- 如果IP和指纹都没问题，尝试把浏览器语言改为 `en-US`
- 再不行，把User-Agent改为英文Windows
- 最后手段：Windows系统区域改为美国

### 步骤6：配置OpenRouter Billing Address

1. 登录 OpenRouter → Settings → Billing
2. **Billing Address 选"显示"**，填美国真实地址：
   - 街道：真实美国街道地址（可以Google一个）
   - 城市：与IP城市一致（Lawndale）或附近城市（Los Angeles）
   - 州：California
   - 邮编：90260（Lawndale）或90001（LA）
   - 国家：United States
3. 保存

**为什么必须显示？** 选"不显示"= 平台无法验证你 = 更容易被风控。显示一个可验证的美国地址 = 信任度更高。

### 步骤7：执行Codex OAuth登录

1. 在WSL终端执行：
   ```bash
   hermes auth openai-codex
   ```
2. 会弹出浏览器窗口（或复制链接到AdsPower浏览器打开）
3. 在AdsPower浏览器中完成OpenAI登录和授权
4. 授权完成后回到终端确认

**如果浏览器弹窗不工作：**
```bash
# 使用Device Code模式
codex login --device-auth
```
会给你一个链接+设备码，在AdsPower浏览器中打开链接，输入设备码完成授权。

### 步骤8：验证

```bash
# 检查登录状态
hermes auth status
```

### 步骤9：如果通不过，逐步加码

按以下顺序逐一尝试，每次只改一项：

| 顺序 | 改什么 | 怎么改 | 恢复方法 |
|------|--------|--------|----------|
| 1 | 浏览器语言 | zh-CN → en-US | AdsPower指纹设置改回 |
| 2 | User-Agent | 默认 → 英文Windows UA | AdsPower指纹设置改回 |
| 3 | 地理位置 | 基于IP → 手动指定Lawndale | 改回"基于IP" |
| 4 | Windows系统区域 | CN → US | Windows设置→区域改回 |
| 5 | 系统语言 | 中文 → 英文 | Windows设置改回（最后手段） |

每改一项后重新测试步骤4的3个检测网站 + 步骤5的OpenAI访问。

### 失败后的回滚

说"回滚"，我会读取 `snapshots/snapshot_20260501_233000.json`，逐项恢复到修改前状态。

---

## §12 经验来源（昨日重现依据）

| 来源 | 关键经验 | 验证时间 |
|------|----------|----------|
| AdsPower官方教程 | 住宅IP+指纹浏览器+时区语言基于IP自动=防风控黄金组合 | 2026 |
| William说(Youtube 1万+播放) | 6个ChatGPT/Claude账号长期稳定：独享住宅IP+AdsPower+禁WebRTC | 2025-2026 |
| VPS大玩家 | Ping0风控值<20为安全，Stripe Radar代理检测机制详解 | 2025-2026 |
| 知乎AdsPower专栏 | "IP在美国+时区东八区+语言中文"矛盾特征直接被标记异常 | 2026 |
| X/Twitter @Monkey2060 | 先搞IP再装指纹浏览器，因为指纹配置要跟IP走 | 2026 |
| X/Twitter社区 | Billing Address不显示比填错还差，等于主动暴露可疑 | 2026 |
| 知乎Codex安装教程 | Device Code模式是OAuth弹窗不工作时的备选方案 | 2026 |
| AdsPower降智解决教程 | 住宅IP+禁WebRTC=解决降智核心方案 | 2026 |

---

## §13 升级日志

- v0.1 (2026-05-01): 初始版本，含配置分层、回滚机制、检测流程、IP服务商参考
- v0.2 (2026-05-01): 升级为综合技能包，新增：工程全景图、链路配置(Clash relay)、Codex OAuth登录流程、已验证IP记录、指纹浏览器替代方案、昨日重现保存库同步
- v0.4 (2026-05-01): 重大修正——WebRTC从"禁用UDP"改为Forward/Replace（用户发现"禁用=此地无银三百两"）；每项指纹设置增加详解（是什么/防什么/出处）；新增三大核心原则（一致性/唯一性/稳定性，出处：腾讯云）；新增Canvas/WebGL/字体/分辨率/UA逐项解释
