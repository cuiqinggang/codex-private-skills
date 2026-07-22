---
name: agent-browser
description: Advanced browser automation via Playwright/CDP. Connect to existing Chrome sessions, precise element refs, PDF/video export, semantic locators.
homepage: https://github.com/vercel-labs/agent-browser
metadata: {"clawdbot":{"emoji":"🌐","requires":{"bins":["node","agent-browser"],"env":[""]},"primaryEnv":""}}
---

# Agent Browser

**Advanced browser automation for OpenClaw.**

## Installation

```bash
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps
```

## Quick Start

```bash
# Connect to existing Chrome (preserves login sessions!)
agent-browser connect --port 9222

# Or open new page
agent-browser open https://chat.openai.com

# Get interactive elements
agent-browser snapshot -i

# Interact using refs
agent-browser click @e1
agent-browser fill @e2 "your text"
agent-browser press Enter

# Close
agent-browser close
```

## Key Features

- **Chrome Bridge**: Connect to your existing Chrome (preserves cookies/login)
- **Element Refs**: Precise @e1, @e2 references from snapshots
- **Semantic Locators**: find role/button/text
- **Advanced Wait**: wait for element/text/URL/JS condition
- **PDF Export**: screenshot --full, pdf output.pdf
- **Video Recording**: record start/stop
- **Mouse Control**: mouse move/down/up/wheel

## Commands

### Navigation
- `open <url>` - Navigate to URL
- `back` / `forward` / `reload` - Browser navigation
- `close` - Close browser

### Snapshot
- `snapshot` - Full accessibility tree
- `snapshot -i` - Interactive elements only (recommended)
- `snapshot -c` - Compact output
- `snapshot -d 3` - Limit depth

### Interactions
- `click @e1` - Click element
- `fill @e2 "text"` - Fill input
- `type @e2 "text"` - Type without clearing
- `press Enter` / `press Control+a` - Keyboard
- `hover @e1` - Hover
- `select @e1 "value"` - Dropdown
- `upload @e1 file.pdf` - File upload
- `drag @e1 @e2` - Drag and drop

### Get Info
- `get text @e1` - Get element text
- `get html @e1` - Get innerHTML
- `get value @e1` - Get input value
- `get attr @e1 href` - Get attribute
- `get url` - Current URL
- `get count ".item"` - Count elements

### Wait
- `wait @e1` - Wait for element
- `wait 2000` - Wait milliseconds
- `wait --text "Success"` - Wait for text
- `wait --url "/dashboard"` - Wait for URL
- `wait --load networkidle` - Wait for network

### Screenshots & PDF
- `screenshot` - Screenshot to stdout
- `screenshot path.png` - Save to file
- `screenshot --full` - Full page
- `pdf output.pdf` - Save as PDF

### Video Recording
- `record start ./demo.webm` - Start recording
- `record stop` - Stop recording

## Chrome Remote Debugging

To connect to your existing Chrome (preserves login sessions):

1. Close all Chrome windows
2. Start Chrome with remote debugging:
   ```bash
   # Linux
   google-chrome --remote-debugging-port=9222
   
   # macOS
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   
   # Windows
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
   ```
3. Connect: `agent-browser connect --port 9222`

## Use Cases

- GPT Plus / Codex automation (with existing login)
- Form filling and submission
- Web scraping with dynamic content
- Testing web applications
- Automated workflows
- CAPTCHA handling (manual intervention + continue)
