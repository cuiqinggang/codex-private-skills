# G08 NVIDIA NIM Marker Tests

Status: `G08_PASS_NVIDIA_MARKER_CANDIDATE_FOUND`

## Scope

- Base URL: `https://integrate.api.nvidia.com/v1`
- Endpoint: `/chat/completions`
- Parameters: `temperature=0`, `max_tokens=120`, `stream=false`
- One request per model with 3 second spacing.
- API key was used only in process memory and was not written to outputs.

## Results

| Model | Visible in /models | HTTP | Success | Marker | Latency ms | Error | Candidate | A class suggestion | Preview |
| --- | --- | ---: | --- | --- | ---: | --- | --- | --- | --- |
| `meta/llama-3.1-8b-instruct` | true | 200 | true | true | 1652 | `none` | true | true | NVIDIA_LLAMA31_8B_OK |
| `moonshotai/kimi-k2.5` | false | 404 | false | false | 499 | `WebException` | false | false |  |
| `minimaxai/minimax-m2.5` | false | 410 | false | false | 467 | `WebException` | false | false |  |
| `z-ai/glm5` | false | 410 | false | false | 417 | `WebException` | false | false |  |
| `nvidia/nemotron-3-super-120b-a12b` | true | 200 | true | true | 3195 | `none` | true | true | NVIDIA_NEMOTRON_SUPER_OK |
| `meta/llama-3.1-70b-instruct` | true | 200 | true | true | 10272 | `none` | true | true | NVIDIA_LLAMA31_70B_OK |

## Success Criteria

- HTTP 200 model count: 3
- Marker pass count: 3
- Baseline `meta/llama-3.1-8b-instruct` marker pass: true
- JSON output is valid and readable.
- Report contains no API key.
