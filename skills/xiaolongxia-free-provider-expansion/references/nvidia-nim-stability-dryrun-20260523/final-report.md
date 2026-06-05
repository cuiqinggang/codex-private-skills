# XIAOLONGXIA NVIDIA NIM Stability Dry-run Final Report

TASK_ID: `XIAOLONGXIA-NVIDIA-NIM-STABILITY-DRYRUN-20260523`

Final status:

`XIAOLONGXIA_NVIDIA_NIM_STABILITY_DRYRUN_PASS`

## 1. Key Handling

用户明确要求本轮不再强制轮换 key，继续把任务完成。因此本轮只在当前 PowerShell 进程中临时设置 `NVIDIA_API_KEY` 做 dry-run。

- 未写入长期全局环境变量。
- 未保存完整 key 到报告、技能包或输出文件。
- 测试后已移除当前进程环境变量。
- 仍建议正式生产接入前单独轮换一次 key，但这不阻断本轮 dry-run 结论。

## 2. G15 Marker Stability

Status: `G15_PASS_STABILITY_TESTS`

| Model | Marker pass | Marker avg latency |
| --- | ---: | ---: |
| `meta/llama-3.1-8b-instruct` | 3/3 | 667 ms |
| `nvidia/nemotron-3-super-120b-a12b` | 2/3 | 7533 ms |
| `meta/llama-3.1-70b-instruct` | 3/3 | 9872 ms |

结论：8B 和 70B marker 稳定；Nemotron 有 1 轮 marker 未按要求返回。

## 3. G16 Chinese QA

Status: `G16_PARTIAL_CHINESE_QA`

| Model | A/B count | Result |
| --- | ---: | --- |
| `meta/llama-3.1-8b-instruct` | 3/3 | 中文问答最好，速度最快 |
| `meta/llama-3.1-70b-instruct` | 3/3 | 中文可用，延迟更高 |
| `nvidia/nemotron-3-super-120b-a12b` | 0/3 | 输出英文推理/指令过程，不适合 |

## 4. G17 Xiaolongxia Style

Status: `G17_PARTIAL_XIAOLONGXIA_STYLE`

| Model | A/B count | Result |
| --- | ---: | --- |
| `meta/llama-3.1-8b-instruct` | 3/3 | 最适合小龙虾短回复，速度最低 |
| `meta/llama-3.1-70b-instruct` | 2/3 | 可做备用，但偶尔偏长或偏官方 |
| `nvidia/nemotron-3-super-120b-a12b` | 0/3 | 不建议继续作为群聊候选 |

## 5. G18 Final Ranking

| Model | Marker | Chinese QA | Xiaolongxia style | Combined avg latency | Tier |
| --- | --- | --- | --- | ---: | --- |
| `meta/llama-3.1-8b-instruct` | 3/3 | 3/3 A/B | 3/3 A/B | 738 ms | A+ |
| `meta/llama-3.1-70b-instruct` | 3/3 | 3/3 A/B | 2/3 A/B | 6631 ms | A+ |
| `nvidia/nemotron-3-super-120b-a12b` | 2/3 | 0/3 A/B | 0/3 A/B | 13263 ms | C |

推荐下一轮 OpenClaw dry-run 主候选：

`meta/llama-3.1-8b-instruct`

推荐备用：

`meta/llama-3.1-70b-instruct`

暂不建议：

`nvidia/nemotron-3-super-120b-a12b`

## 6. Boundary Verification

- 未改 Hermes / 爱马仕。
- 未改 Open WebUI。
- 未改旧 `3001` New API。
- 未覆盖当前 OpenRouter 生产配置。
- 未接真实群聊。
- 未把 NVIDIA 写入生产 OpenClaw 配置。
- `openclaw config validate` 通过。
- `C:\Users\A\.openclaw` 下未发现 NVIDIA provider/model 字符串。

## 7. Files And Skill Savepoint

Output root:

`C:\Users\A\Desktop\1\output\XIAOLONGXIA-NVIDIA-NIM-STABILITY-DRYRUN-20260523`

Updated skill:

`C:\Users\A\.codex\skills\xiaolongxia-free-provider-expansion`

H mirror:

`H:\CodexSkills\xiaolongxia-free-provider-expansion`

Hash result:

`HASH_MATCH_OK`, compared files: 27.

Security scan:

No full `nvapi-*`, `sk-or-v1-*`, or `sk-*` key pattern found in output, local skill, or H mirror.

## 8. Next Minimum Action

下一步只做 OpenClaw 候选路由 dry-run，不接真实群聊：

- NVIDIA provider 仍作为候选层。
- 主候选：`meta/llama-3.1-8b-instruct`
- 备用候选：`meta/llama-3.1-70b-instruct`
- 当前 OpenRouter 3011 生产池继续保持不动。
- fallback 仍先落在小龙虾应用层或消息适配层，不要假设 OpenClaw 内置 fallback 已经生产可用。
