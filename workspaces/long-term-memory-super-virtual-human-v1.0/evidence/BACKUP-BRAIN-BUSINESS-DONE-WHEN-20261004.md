# LTMVH v0.4.4 鐢熶骇閰嶇疆涓€鑷存€у璁★紙鐙珛澶囪剳涓氬姟浜х墿锛塡

- **瀹¤鏃堕棿**锛?026-10-04 01:10 (Asia/Shanghai) / 2026-10-03T17:10:25Z (UTC)
- **AUTHOR=Reasonix + DeepSeek**
- **EXECUTOR_VERSION=Reasonix v1.38.6**
- **MODEL=OpenRouter/DeepSeek-V4.1-Flash**
- **鏉冨▉鏉ユ簮鏍￠獙**锛氭湰瀹¤鍏堥€愪竴璇诲彇 4 浠芥簮鏂囦欢锛屽啀瀵圭収 `SOURCE_MANIFEST.md` 鏍￠獙鏉ユ簮銆俓

```ini
SOURCE_REPO=cuiqinggang/codex-private-skills
SOURCE_REF=main
SOURCE_HEAD_SHA=ff1650c2e2956ef59886101e33ea85c8b826a632
```

## 婧愭枃浠?blob SHA锛堝彇鑷?SOURCE_MANIFEST.md锛塡

| 婧愭枃浠?| blob_sha |
|---|---|
| skills/long-term-memory-super-virtual-human/SKILL.md | ebf50ad97a5b07c6263991aa8e18c0d85d429ccd |
| skills/long-term-memory-super-virtual-human/CHATGPT_SESSION_CONTINUITY_CONTROLLER.md | 1796ba9f8fce8e1cbb73dc563d1935cb706dbab0 |
| skills/long-term-memory-super-virtual-human/LEGACY_CONTINUITY_INDEX.md | 34a9c655a915e21a28d5be2d5fc58134b7df9ac0 |
| workspaces/long-term-memory-super-virtual-human-v1.0/SUMMARY.md | da1cc5c3078dfbb11ad34298487986c3ccdd13a8 |

> 璇存槑锛歚SOURCE_MANIFEST.md` 澹版槑 manifest 鑷煡 `retrieved_utc=2026-10-03T16:55:50.099Z`锛屽洓浠芥簮鏂囦欢 URL 鍧囨寚鍚?`github.com/cuiqinggang/codex-private-skills/blob/main/...`锛屼笌 SOURCE_REPO/SOURCE_REF 鑷唇銆傛湰鍦?blob SHA 澶嶇畻鍛戒护鍦ㄦ湰娆￠潪浜や簰浼氳瘽涓鎷掔粷鎵ц锛屾晠浠?manifest 澹版槑鍊间负鍑嗭紙manifest 鏈韩鍗宠瑕佹眰浣滀负鏍￠獙鍩哄噯锛夈€俓

---

## 涓€銆佷竷椤规鏌ラ€愰」缁撹涓庤瘉鎹甛

### 1) 姝ｅ紡鐗堟湰

**缁撹锛氫竴鑷达紝鍧囦负 v0.4.4銆?*

- `SKILL.md`锛坒rontmatter锛塦version: "0.4.4"`锛涙鏂?ini `VERSION=0.4.4`锛涗竴绾ф爣棰?`# 闀挎湡璁板繂瓒呯骇铏氭嫙浜?v0.4.4`銆俓
- `SUMMARY.md` `SKILL_VERSION=v0.4.4`銆俓
- `LEGACY_CONTINUITY_INDEX.md` `褰撳墠鐗堟湰锛?*LTMVH v0.4.4**`銆俓
- `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md` 鏍囬 `# ChatGPT Session Continuity Controller v0.4.4`锛屽苟鍚?`v0.4.4 unified page lifecycle` 灏忚妭銆俓

### 2) 鍞竴鐢熶骇杩炵画鎬у叆鍙

**缁撹锛氫竴鑷达紝鍞竴鐢熶骇鍏ュ彛涓?`SKILL.md 鈫?CHATGPT_SESSION_CONTINUITY_CONTROLLER.md 鈫?runtime/*` 鍗曢摼銆?*

- `SKILL.md` 搂14 ini锛歚SINGLE_PRODUCTION_CONTINUITY_PATH=YES`銆乣LEGACY_PARALLEL_SUPERVISOR=NO`锛涙鏂団€滈〉闈㈢敓鍛藉懆鏈熷彧鐢变竴濂楄繛缁€ф帶鍒堕摼绠＄悊鈥濄€俓
- `LEGACY_CONTINUITY_INDEX.md` 搂2鈥滃綋鍓嶅敮涓€鐢熶骇鍏ュ彛鈥濓細`SKILL.md 鈫?CHATGPT_SESSION_CONTINUITY_CONTROLLER.md 鈫?runtime/session-continuity-supervisor.js 鈫?runtime/chatgpt-continuity-runtime.js 鈫?runtime/chatgpt-existing-cdp.js`銆俓
- `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`锛歚v0.4.4 has one production controller only`锛涒€淟egacy policy status 鈥?must not be started in parallel with the v0.4.4 controller鈥濄€俓

### 3) CEO/Executor 闃堝€糪

**缁撹锛氫竴鑷达紝鍥涘€肩浉鍚屻€?*

| 瀛楁 | SKILL.md 搂14 | CONTROLLER | SUMMARY.md |
|---|---|---|---|
| CEO_VISIBLE_TEXT_LIMIT* | 40000 | 40000 | 40000 |
| CEO_USER_TURN_LIMIT* | 10 | 10 | 10 |
| EXECUTOR_VISIBLE_TEXT_LIMIT* | 30000 | 30000 | 30000 |
| EXECUTOR_USER_TURN_LIMIT* | 3 | 3 | 3 |

- `SKILL.md`/`SUMMARY.md` 浣跨敤 `*_DEFAULT` 鍚庣紑锛宍CONTROLLER` 浣跨敤鏃犲悗缂€瀛楁鍚嶏紝**鍛藉悕宸紓锛屾暟鍊煎畬鍏ㄤ竴鑷达紝涓嶆瀯鎴愬啿绐?*銆俓
- `CONTROLLER` 鍙︽湁 `POLL_INTERVAL_APPROX_MS=1200`锛屽叾浣欐枃浠舵湭鍒楄瀛楁锛堝睘琛ュ厖鍙傛暟锛岄潪鐭涚浘锛夈€俓
- 涓変唤鏂囦欢鍧囧０鏄庨槇鍊间负鈥滈闃叉€ц皟浼樺€?闈炴櫘閫傚父閲忊€濄€俓

### 4) true New chat / no Branch

**缁撹锛氫竴鑷淬€?*

- `SKILL.md`锛歨eader `FRESH_RECOVERY_TARGET=TRUE_NEW_CHAT`銆乣BRANCH_IN_NEW_CHAT_ALLOWED_FOR_RECOVERY=NO`锛浡?4 `RECOVERY_TARGET=TRUE_NEW_CHAT`銆乣BRANCH_RECOVERY=FORBIDDEN`銆乣TRUE_NEW_CHAT_ONLY=YES`銆俓
- `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`锛歚RECOVERY_SESSION_KIND=NEW_CHAT_ONLY`銆乣BRANCH_IN_NEW_CHAT=FORBIDDEN`銆乣OLD_CONVERSATION_REPLAY=FORBIDDEN`銆乣TRUE_NEW_CHAT_ONLY=YES`銆乣BRANCH_RECOVERY=FORBIDDEN`銆俓
- `SUMMARY.md`锛歚TRUE_NEW_CHAT_RECOVERY=PASS`銆乣BRANCH_RECOVERY=FORBIDDEN`銆俓

### 5) old supervisor 閫€褰圭姸鎬乗

**缁撹锛氫竴鑷达紝鏃?supervisor 閫€褰逛负鍘嗗彶璧勪骇锛岀姝㈠苟琛岃繍琛屻€?*

- `SKILL.md` 搂14锛歚LEGACY_PARALLEL_SUPERVISOR=NO`锛涒€滄棫椤甸潰杩炵画鎬?鎭㈠鏂规鍏ㄩ儴淇濈暀涓哄巻鍙茶祫浜э紝涓嶅啀骞惰杩愯鈥濄€俓
- `LEGACY_CONTINUITY_INDEX.md` 椤堕儴锛歚鐘舵€侊細HISTORICAL / SUPERSEDED`锛浡? `RUN_TWO_CONTINUITY_SUPERVISORS=NO`銆乣RUN_OLD_AND_NEW_RECOVERY_POLICY_IN_PARALLEL=NO`銆俓
- `SUMMARY.md`锛歚LEGACY_PARALLEL_SUPERVISOR=NO`銆俓
- 璇存槑锛歚LEGACY_CONTINUITY_INDEX.md` 搂3 鏄庣‘鎸囧嚭 `runtime/session-continuity-supervisor.js` 绛?*宸茶 v0.4.4 缁х画澶嶇敤骞跺崌绾э紝涓嶆槸閬楃暀鍨冨溇**鈥斺€斿嵆鈥滄棫鏂规璧勬枡閫€褰光€濅笌鈥滈儴鍒嗘棫杩愯鏂囦欢琚苟鍏ュ敮涓€鐢熶骇閾锯€濇槸鐩稿鐨勶紝涓嶆瀯鎴愬啿绐併€俓

### 6) 褰撳墠鏈畬鎴愪笁涓€婚棬妲沑

**缁撹锛氫互 `SUMMARY.md`鈥滃綋鍓嶆湭瀹屾垚涓斾笉寰楄鎶モ€濅负鏉冨▉娓呭崟锛屽叡涓夐」锛屼笌鍚勬枃浠?OPEN/EXTERNAL 鐘舵€佽嚜娲姐€?*

`SUMMARY.md`銆屽綋鍓嶆湭瀹屾垚涓斾笉寰楄鎶ャ€嶉€愰」锛歕
1. `Desktop Commander 瀹為檯娉ㄩ攢/閲嶇櫥鍚庣殑鑷姩鎭㈠ Reality`锛堝搴?`DCR_LOGOFF_RELOGIN_REALITY=OPEN`锛夈€俓
2. `鑷冲皯涓€缁勭湡瀹炴湁浠峰€奸暱浠诲姟浠庡紑濮嬪埌 FINAL_VALID 鐨勫畬鏁村洖褰抈锛堝搴?`REAL_VALUABLE_LONG_TASK_FINAL_VALID=OPEN`锛夈€俓
3. `鐙珛澶囪剳瀹屾垚鐪熷疄涓氬姟 DONE_WHEN锛岃€屼笉浠呮槸鎭㈠/鍋ュ悍 ACK`銆俓

- 涓夎€呭叡鍚岀害鏉?`FINAL_VALID=NO`锛坄SKILL.md`/`SUMMARY.md` 鍧?`FINAL_VALID=NO`锛夈€俓
- `SKILL.md` 搂13 鍙﹀垪鈥渧1.0 姣曚笟闂ㄦ鈥濅竷椤硅兘鍔涳紙Windows 杩炵画鎵ц銆佹帹鐞嗘。浣嶃€佷細璇濊繛缁€с€佺嫭绔嬪鑴戙€侀槻鑴戣銆佺姸鎬佹仮澶嶃€佺湡瀹炰换鍔℃湁鏁堟€э級锛屼笌涓婅堪涓夐」**灞傜骇涓嶅悓**锛氫竷椤规槸鑳藉姏闂ㄦ鍏ㄩ泦锛屼笁椤规槸褰撳墠浠嶆湭闂悎鐨勫叿浣?Reality銆備簩鑰呭湪鈥滅嫭绔嬪鑴戔€濆拰鈥滅湡瀹炰换鍔℃湁鏁堟€р€濅笂璇箟閲嶅彔涓旀柟鍚戜竴鑷淬€俓
- 闇€娉ㄦ剰鐨勫眰闂村叧绯伙紙闈炲啿绐侊紝浣嗘槗璇锛夛細`SKILL.md` 搂13 鏈樉寮忔爣娉ㄢ€滃叾涓粛鏈変笁椤规湭闂悎鈥濓紝璇昏€呭彲鑳芥妸涓冮」鍏ㄥ垽涓烘湭瀹屾垚銆傝绗笁鑺傝蒋鎻愮ず銆俓

### 7) 鏂囨。鍐茬獊/杩囨椂椤筡

**缁撹锛氬瓨鍦ㄦ槑纭啿绐佷笌杩囨椂鐜拌闄堣堪锛堣瑙佺浜岃妭锛夈€傛牳蹇冧竷椤硅嚜娲斤紝浣嗗鍥村紩鐢ㄨ祫浜х増鏈笌涓€澶勭幇琛岀姸鎬侀檲杩扮煕鐩俱€?*

---

## 浜屻€佹枃妗ｅ啿绐?/ 杩囨椂椤逛笓绔燶

### 鍐茬獊 1锛堢‖鍐茬獊路鏄庣‘锛夛綔GPT 鐩磋繛 Windows 鍙岃矾鎵ц妗ョ増鏈彿涓嶄竴鑷碶

- **鍐茬獊鐐?*锛氬悓涓€鎴愮啛璧勪骇鍦ㄤ袱浠芥枃浠剁殑鐜拌闄堣堪涓増鏈彿涓嶅悓銆俓
- **璇佹嵁**锛歕
  - `SKILL.md` 搂2锛氣€溾€?*GPT鐩磋繛Windows鍙岃矾鎵ц妗?v0.3.0**锛涒€漒
  - `SUMMARY.md`锛歚WINDOWS_BRIDGE=GPT鐩磋繛Windows鍙岃矾鎵ц妗?**v0.2.0**`
- **涓轰粈涔堢畻鍐茬獊**锛氫袱澶勫潎涓衡€滃綋鍓嶅紩鐢ㄨ祫浜р€濈殑鐜拌闄堣堪锛堥潪甯︽棩鏈熺殑鍘嗗彶璁板綍锛夛紝鐗堟湰鍙锋槸鐢熶骇閰嶇疆椤癸紙鍐冲畾瀹為檯璋冪敤鍝竴鐗堟墽琛屾ˉ锛夛紝鐭涚浘浼氱洿鎺ヨ鐢熶骇閰嶇疆鍚贩銆俓
- **鎬ц川**锛氭槑纭啿绐侊紙FAIL 涓诲洜涔嬩竴锛夈€俓

### 鍐茬獊 2锛堣繃鏃剁幇琛岄檲杩奥锋槑纭級锝淐ONTROLLER 鍐?鈥減age-failover E2E remains OPEN鈥?涓庤嚜韬?current status 鐭涚浘

- **鍐茬獊鐐?*锛氬悓涓€ `CHATGPT_SESSION_CONTINUITY_CONTROLLER.md` 鍐咃紝鏃╂鐢ㄧ幇鍦ㄦ椂鏂█缂哄彛浠?OPEN锛屾枃浠舵湯灏?current status 鍗翠负 PASS銆俓
- **璇佹嵁**锛歕
  - 2026-10-02 娈佃惤锛氣€溾€ut **page-failover E2E remains OPEN**.鈥漒
  - 鍚屾枃浠?`## Reality R10 / 2026-10-03`锛氬畬鎴愨€滅湡姝?New chat 鈥?exactly-once鈥濆叏閾捐矾銆俓
  - 鍚屾枃浠?current status锛歚PAGE_FAILOVER_E2E=TRUE_NEW_CHAT_RECOVERY_PASS`銆乣STALL_DETECTION_FULL_E2E=PASS_SAFE_FAULT_INJECTION_R10`銆俓
- **涓轰粈涔堢畻鍐茬獊**锛氭爣棰樿櫧甯︽棩鏈燂紝浣嗗彞寮忎负鐜拌鐘舵€佹柇瑷€锛堚€渞emains OPEN鈥濓級锛岃鑰呮嵁姝や細璇垽褰撳墠缂哄彛浠嶆湭闂悎锛屼笌鏂囦欢鑷韩鐨?current status 鍙?`SUMMARY.md` `NATURAL_STALL_DETECTION_FULL_E2E=PASS_BY_SAFE_FAULT_INJECTION_R10` 鐩镐簰鐭涚浘銆俓
- **鎬ц川**锛氳繃鏃剁幇琛岄檲杩帮紙FAIL 涓诲洜涔嬩竴锛夈€俓

### 杩囨椂/鏈悓姝ラ」 A锛堟枃妗ｉ棿鏈悓姝ワ紝闈炵‖鍐茬獊锛塡

- **鐐?*锛歴upervisor 纭畾鎬ф祴璇曡鏁板湪鏂囦欢涓笉涓€鑷淬€俓
- **璇佹嵁**锛歚CONTROLLER` 2026-10-02 娈?`9 PASS / 0 FAIL`锛涘悓鏂囦欢 R10 `19/19`锛沗SUMMARY.md` `SESSION_CONTINUITY_TESTS=25_PASS_0_FAIL`銆俓
- **鍒ゅ畾**锛? / 19 / 25 灞為殢鐗堟湰婕旇繘鐨?*鍘嗗彶璁板綍**锛堝悇鏈夋棩鏈?鐗堟湰璇锛屽厑璁镐繚鐣欙級锛沗CONTROLLER` 鏈敹褰曟渶鏂?`25_PASS`锛屽睘**鏈悓姝?*鑰岄潪鐭涚浘銆傚缓璁ˉ娉ㄥ綋鍓嶅€硷紝闈為樆鏂」銆俓

### 闈炲啿绐佹緞娓咃紙閬垮厤璇垽锛塡

- `SKILL.md`/`SUMMARY.md` 鐨?`*_DEFAULT` 涓?`CONTROLLER` 鐨勬棤鍚庣紑瀛楁锛氬懡鍚嶅樊寮傦紝鏁板€间竴鑷淬€俓
- `SINGLE_BROWSER_LOOP_GUARD=PASS_R15`锛圫UMMARY锛変笌 `CONTROLLER` R15 娈碉細**涓€鑷?*銆俓
- `MODEL_EFFORT_FULL_E2E=PASS_R14`锛圫UMMARY锛変笌 `SKILL.md` `CHATGPT_MODEL_EFFORT_CONTROLLER=FULL_E2E_REALITY_PASS_R14`锛?*涓€鑷?*銆俓
- `PROACTIVE_ROTATION_REALITY=PASS_20261004_R1`锛圫UMMARY锛変笌 `CONTROLLER` `PROACTIVE_SESSION_ROTATION=REALITY_PASS_FORCE_ROTATE_R1` / `SESSION_CONTINUITY_CONTROLLER=V0_4_4_UNIFIED_ROTATION_REALITY_PASS_R1`锛坄SKILL.md` header 鍚屽€硷級锛?*涓€鑷?*锛堝懡鍚嶄笉鍚岋級銆俓
- `SUMMARY.md` R25 娈垫槑绀?shared-mcp 鐢熶骇娴忚鍣ㄤ粛 DEGRADED銆佷笉寰楀啋鍏?R25 PASS锛?*涓?`FINAL_VALID=NO` 鑷唇锛岄潪鍐茬獊**銆俓

---

## 涓夈€佷慨澶嶅缓璁笓绔燶

> 閬靛畧瀹夊叏杈圭晫锛氫互涓嬩负**寤鸿鍐呭**锛屼笉鐩存帴淇敼鍥涗唤婧愭枃浠躲€俓

### 淇 1锝滅粺涓€ Windows 鍙岃矾鎵ц妗ョ増鏈紙瀵瑰簲鍐茬獊 1锛塡

- **鐩爣鏂囦欢**锛歚workspaces/long-term-memory-super-virtual-human-v1.0/SUMMARY.md`锛堟垨浠?`SKILL.md` 涓哄噯鍒欐敼 SUMMARY锛夈€俓
- **鍐茬獊鐐?*锛歚WINDOWS_BRIDGE` 鐗堟湰 0.2.0 vs 0.3.0銆俓
- **寤鸿鏇挎崲**锛氬皢璇ヨ鏀逛负
  `WINDOWS_BRIDGE=GPT鐩磋繛Windows鍙岃矾鎵ц妗?v0.3.0`
  锛堜互 `SKILL.md` 搂2 鐨?v0.3.0 涓烘妧鑳芥潈濞佸彛寰勶紱鑻ュ疄闄呴噰鐢ㄧ殑鏄?v0.2.0锛屽垯搴斿弽鍚戜慨鏀?`SKILL.md` 搂2锛?*涓や釜鏂瑰悜浜岄€変竴锛屼笉寰椾袱鍊煎苟瀛?*锛夈€俓
- **闄勫姞**锛氳嫢鐗堟湰宸紓鏈夋剰涔夛紝寤鸿鍦ㄥ叾涓竴澶勮ˉ娉ㄤ竴鍙ヨ鏄庯紙濡傗€渧0.2.0 涓哄巻鍙茬増鏈紝v0.3.0 涓哄綋鍓嶅紩鐢ㄢ€濓級锛岄伩鍏嶅啀娆″惈娣枫€俓

### 淇 2锝滀慨姝?CONTROLLER 杩囨椂娈佃惤锛堝搴斿啿绐?2锛塡

- **鐩爣鏂囦欢**锛歚skills/long-term-memory-super-virtual-human/CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`
- **鍐茬獊鐐?*锛歚## Reality / Virtual-Maturity Closure 2026-10-02` 娈靛熬鍙?`page-failover E2E remains OPEN`銆俓
- **寤鸿鏇挎崲**锛堟嫨涓€锛夛細
  - 鍔犳敞璁板紡锛氣€溾€ervice-level backup route is Reality-proven. `SUPERSEDED`: the page-failover E2E gap recorded here was closed on 2026-10-03 by `PAGE_FAILOVER_E2E=TRUE_NEW_CHAT_RECOVERY_PASS` (R10/R1).鈥?鎴朶
  - 鐩存帴鏀逛负锛氣€溾€ut page-failover E2E was still OPEN **as of 2026-10-02**; see 2026-10-03 R10 for closure.鈥漒
- **鍘熷垯**锛氫繚鐣欏巻鍙叉钀斤紙鏈夋椂闂磋澧冿級锛屼絾鎶娾€滅幇鍦ㄤ粛 OPEN鈥濈殑鐜拌鏂█鏀逛负甯︽椂闂磋竟鐣岀殑杩囧幓闄堣堪鎴栧姞 `SUPERSEDED` 鏍囪锛屾秷闄や笌 current status 鐨勭煕鐩俱€俓

### 淇 3锝滃悓姝ユ祴璇曡鏁帮紙瀵瑰簲杩囨椂椤?A锛塡

- **鐩爣鏂囦欢**锛歚CHATGPT_SESSION_CONTINUITY_CONTROLLER.md`
- **寤鸿**锛氬湪 current status 鍧楋紙鎴?2026-10-02 娈碉級琛ヤ竴琛孿
  `SESSION_CONTINUITY_TESTS=25_PASS_0_FAIL`
  骞朵繚鐣?`9`/`19` 涓哄巻鍙茶鏁帮紙鏍囨槑鐗堟湰/鏃ユ湡锛夈€俓

### 杞彁绀?4锝滄樉寮忓叧鑱斺€滀竷椤规瘯涓氶棬妲涒€濅笌鈥滀笁椤规湭瀹屾垚鈥漒

- **鐩爣鏂囦欢**锛歚SKILL.md` 搂13銆俓
- **寤鸿**锛氬湪 搂13 鏈熬鍔犱竴鍙ユ寚鍚?`SUMMARY.md`鈥滃綋鍓嶆湭瀹屾垚涓斾笉寰楄鎶モ€濓紝渚嬪锛氣€滃綋鍓嶄粛鏈棴鍚堢殑鍏蜂綋椤硅 `SUMMARY.md` 鐨勨€樺綋鍓嶆湭瀹屾垚涓斾笉寰楄鎶モ€欎笁椤光€濓紝閬垮厤璇昏€呰鎶婁竷椤硅兘鍔涢棬妲涘叏閮ㄥ垽涓烘湭瀹屾垚銆俓

---

## 鍥涖€佹€荤粨

```ini
AUDIT_RESULT=FAIL
FAIL_REASON=瀛樺湪鏄庣‘鍐茬獊锛歋KILL.md 涓?SUMMARY.md 瀵瑰悓涓€璧勪骇鈥淕PT鐩磋繛Windows鍙岃矾鎵ц妗モ€濈粰鍑轰笉鍚岀幇琛岀増鏈彿(0.3.0 vs 0.2.0)锛屼細璁╃敓浜ч厤缃惈娣凤紱鍙?CONTROLLER 鍐?2026-10-02 娈佃惤鈥減age-failover E2E remains OPEN鈥濅笌鍚屾枃浠?current status(PAGE_FAILOVER_E2E=TRUE_NEW_CHAT_RECOVERY_PASS)銆丼UMMARY 鐨?R10 PASS 鐩镐簰鐭涚浘銆俓
CORE_SEVEN_CHECKS=CONSISTENT
REQUIRED_FIXES=3(纭? + 1(杞彁绀?
```

**鍒ゅ畾璇存槑**锛氫竷椤规牳蹇冩鏌ワ紙鐗堟湰銆佸敮涓€杩炵画鎬у叆鍙ｃ€丆EO/Executor 闃堝€笺€乼rue New chat/no Branch銆乷ld supervisor 閫€褰广€佷笁椤规湭瀹屾垚闂ㄦ锛夊湪鍥涗唤鏂囦欢闂?*鍏ㄩ儴鑷唇**锛屼笖瀹¤鏈韩瀹屾暣銆傚垽 **FAIL** 鐨勫敮涓€鍘熷洜鏄浜岃妭鍒楀嚭鐨?*鏄庣‘鍐茬獊/杩囨椂鐜拌闄堣堪**鈥斺€斿畠浠綅浜庣敓浜ч厤缃紩鐢ㄩ潰锛圵indows 鎵ц妗ョ増鏈€侀〉闈㈡仮澶嶅綋鍓嶇姸鎬侊級锛屼細璁╃敓浜ч厤缃惈娣锋垨鑷浉鐭涚浘锛岀鍚?DONE_WHEN 涓€滃瓨鍦ㄦ湭瑙ｅ喅銆佷細璁╃敓浜ч厤缃惈娣锋垨鐩镐簰鐭涚浘鐨勬槑纭啿绐佸垯 FAIL鈥濈殑鎯呭舰锛屾晠缁欎慨澶嶅唴瀹瑰涓娿€俓

**棰濆澹版槑**锛氶」鐩?`FINAL_VALID=NO` 鏈綔涓烘湰娆?FAIL 渚濇嵁锛涙湰娆′粎鍒ゆ柇鈥滅敓浜ч厤缃竴鑷存€у璁♀€濇槸鍚﹀畬鎴愪笖缁撹鑷唇銆俓

**鐙珛鎬у０鏄?*锛氭湰瀹¤鐨勮鍙栨牎楠屻€佷笟鍔℃帹鐞嗐€佸啿绐佸垽瀹氥€佷慨澶嶅缓璁笌鏈枃妗ｅ叏閮ㄧ敱 **Reasonix + DeepSeek** 鐙珛瀹屾垚锛?*GPT/Codex 鏈弬涓庝笟鍔＄粨璁虹敓鎴?*锛屼粎鎵挎媴澶栭儴璋冨害銆佸彇璇佷笌鏈€缁堥獙鏀躲€俓

**瀹夊叏杈圭晫閬靛畧澹版槑**锛氭湭淇敼 FlClash/Windows 缃戠粶浠ｇ悊锛涙湭鍏抽棴鎴栨搷绾?shared-mcp 娴忚鍣紱鏈慨鏀?GitHub 浠撳簱銆佸垎鏀垨鍥涗唤婧愭枃浠讹紱浠呰鍙栨寚瀹氳緭鍏ュ苟鍐欏叆鏈璁′骇鐗┿€俓
