@echo off
timeout /t 20 /nobreak >nul
set NODE_PATH=C:\AI\Playwright-Native-AI-Browser\node_modules
start "ChatGPT Continuity Attach-Only" /min "C:\Program Files\nodejs\node.exe" "C:\AI\ltmvh-v03-test\skills\long-term-memory-super-virtual-human\runtime\chatgpt-continuity-runtime.js" --profile "C:\AI\Playwright-Native-AI-Browser\profile\shared-mcp" --lease-root "C:\AI\Playwright-Native-AI-Browser\ltmvh-chatgpt-lease" --cdp-endpoint "http://127.0.0.1:9223" --never-launch true --no-auto-new-page true
exit /b 0