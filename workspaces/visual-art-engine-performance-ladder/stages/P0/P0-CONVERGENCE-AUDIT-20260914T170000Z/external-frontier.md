# External Frontier Recheck

- Rechecked 2026-09-14.
- Official ComfyUI WebSocket example waits for xecuting with node None, then reads /history/{prompt_id} and fetches output through /view: https://github.com/Comfy-Org/ComfyUI/blob/master/script_examples/websockets_api_example.py
- Official message documentation defines xecution_success as all nodes executed successfully and xecuting node=None as completion; E6 proves history may still be unavailable at the earlier client boundary: https://docs.comfy.org/development/comfyui-server/comms_messages
- Official routes document /prompt, /ws, /history/{prompt_id}, /view, and /queue: https://docs.comfy.org/development/comfyui-server/comms_routes
- Upstream /view returns a server-side FileResponse; no directly comparable P0-CONTROL-V1 latency benchmark was found: https://github.com/Comfy-Org/ComfyUI/blob/master/server.py
- Conclusion: mature path matches current implementation; no exact comparable external time constrains CURRENT further.
