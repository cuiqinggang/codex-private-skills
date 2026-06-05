# G15 Stability Marker Tests

| Model | Round | HTTP | Success | Marker | Latency ms | Error |
| --- | --- | ---: | --- | --- | ---: | --- |
| `meta/llama-3.1-8b-instruct` | ROUND1 | 200 | true | true | 1234 | `none` |
| `meta/llama-3.1-8b-instruct` | ROUND2 | 200 | true | true | 404 | `none` |
| `meta/llama-3.1-8b-instruct` | ROUND3 | 200 | true | true | 364 | `none` |
| `nvidia/nemotron-3-super-120b-a12b` | ROUND1 | 200 | true | true | 6757 | `none` |
| `nvidia/nemotron-3-super-120b-a12b` | ROUND2 | 200 | true | false | 3678 | `none` |
| `nvidia/nemotron-3-super-120b-a12b` | ROUND3 | 200 | true | true | 12163 | `none` |
| `meta/llama-3.1-70b-instruct` | ROUND1 | 200 | true | true | 946 | `none` |
| `meta/llama-3.1-70b-instruct` | ROUND2 | 200 | true | true | 27718 | `none` |
| `meta/llama-3.1-70b-instruct` | ROUND3 | 200 | true | true | 953 | `none` |

Status: `G15_PASS_STABILITY_TESTS`
