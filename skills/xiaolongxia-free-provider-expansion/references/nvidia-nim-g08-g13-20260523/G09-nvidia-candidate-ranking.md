# G09 NVIDIA Candidate Ranking

## A Class - Immediate Candidate Pool

- `meta/llama-3.1-8b-instruct`: marker passed, HTTP 200, latency 1652 ms.
- `nvidia/nemotron-3-super-120b-a12b`: marker passed, HTTP 200, latency 3195 ms.
- `meta/llama-3.1-70b-instruct`: marker passed, HTTP 200, latency 10272 ms.

## B Class - Continue Observing

- None in this run.

## C Class - Not Recommended Now

- `moonshotai/kimi-k2.5`: HTTP 404, error=WebException. 404 page not found 
- `minimaxai/minimax-m2.5`: HTTP 410, error=WebException. {"type":"about:blank","title":"Gone","status":410,"detail":"The model 'minimaxai/minimax-m2.5' has reached its end of life on 2026-05-12T00:00:00Z and is no longer available."} 
- `z-ai/glm5`: HTTP 410, error=WebException. {"type":"about:blank","title":"Gone","status":410,"detail":"The model 'z-ai/glm5' has reached its end of life on 2026-05-18T00:00:00Z and is no longer available."} 

## Recommended Route

- Primary candidate: `meta/llama-3.1-8b-instruct`.
- Fallback candidate: `nvidia/nemotron-3-super-120b-a12b`, `meta/llama-3.1-70b-instruct`.
- Next stability test models: all A class models, with Chinese Q&A and Xiaolongxia-style short reply prompts.
- OpenClaw candidate provider: YES, generate candidate-only config using A class models.

## Notes

- `meta/llama-3.1-8b-instruct` is fastest and suitable as the first NVIDIA dry-run primary candidate.
- `nvidia/nemotron-3-super-120b-a12b` is a high-quality candidate but must pass Chinese and group-chat style tests before formal use.
- `meta/llama-3.1-70b-instruct` passed but is slower than the 8B model; keep as fallback candidate.
- Kimi, Minimax, and GLM5 are not currently suitable through this NVIDIA endpoint/id set.
