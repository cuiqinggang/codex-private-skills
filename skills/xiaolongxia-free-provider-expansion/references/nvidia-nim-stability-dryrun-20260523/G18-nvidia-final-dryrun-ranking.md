# G18 NVIDIA Final Dry-run Ranking

| Model | Marker | Chinese A/B | Style A/B | Avg latency ms | Tier |
| --- | --- | --- | --- | ---: | --- |
| `meta/llama-3.1-8b-instruct` | 3/3 | 3/3 | 3/3 | 738 | A+ |
| `nvidia/nemotron-3-super-120b-a12b` | 2/3 | 0/3 | 0/3 | 13263 | C |
| `meta/llama-3.1-70b-instruct` | 3/3 | 3/3 | 2/3 | 6631 | A+ |

Recommended next OpenClaw dry-run primary: `meta/llama-3.1-8b-instruct`.
Recommended backups: `meta/llama-3.1-70b-instruct`.
Not recommended: `nvidia/nemotron-3-super-120b-a12b`.

Can enter OpenClaw candidate route dry-run: YES, if still not connected to real group chat.
Still not allowed: direct real group chat production use.
