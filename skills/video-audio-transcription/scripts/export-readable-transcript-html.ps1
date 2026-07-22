param(
  [Parameter(Mandatory=$true)]
  [string]$TranscriptPath,

  [string]$OutputPath = "",
  [string]$Title = "Video Transcript",
  [string]$Subtitle = "large-v3 transcript, readable and copy-ready"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $TranscriptPath)) {
  throw "Transcript not found: $TranscriptPath"
}

if (-not $OutputPath) {
  $dir = Split-Path -Parent $TranscriptPath
  $OutputPath = Join-Path $dir "readable-transcript.html"
}

$text = Get-Content -LiteralPath $TranscriptPath -Raw -Encoding UTF8
$encodedText = [System.Net.WebUtility]::HtmlEncode($text.Trim())
$encodedTitle = [System.Net.WebUtility]::HtmlEncode($Title)
$encodedSubtitle = [System.Net.WebUtility]::HtmlEncode($Subtitle)

$html = @"
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>$encodedTitle</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #202124;
      --muted: #5f6368;
      --line: #d9dde3;
      --bg: #ffffff;
      --button: #1f2937;
      --buttonText: #ffffff;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: system-ui, -apple-system, "Segoe UI", "Microsoft YaHei UI", "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif;
      font-size: 19px;
      font-weight: 500;
      line-height: 1.9;
      letter-spacing: 0;
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }

    main {
      max-width: 900px;
      margin: 0 auto;
      padding: 34px 26px 72px;
    }

    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 18px;
      margin-bottom: 26px;
      border-bottom: 1px solid var(--line);
    }

    h1 {
      margin: 0;
      font-size: 28px;
      font-weight: 650;
      line-height: 1.3;
    }

    .meta {
      margin-top: 8px;
      color: var(--muted);
      font-size: 14px;
      font-weight: 450;
      line-height: 1.5;
    }

    button {
      flex: 0 0 auto;
      border: 0;
      border-radius: 6px;
      padding: 10px 15px;
      background: var(--button);
      color: var(--buttonText);
      font: inherit;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
    }

    button:active {
      transform: translateY(1px);
    }

    #transcript {
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      font-weight: 500;
    }

    @media (max-width: 640px) {
      body {
        font-size: 18px;
      }

      main {
        padding: 24px 18px 56px;
      }

      header {
        align-items: flex-start;
        flex-direction: column;
      }

      h1 {
        font-size: 24px;
      }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>$encodedTitle</h1>
        <div class="meta">$encodedSubtitle</div>
      </div>
      <button type="button" id="copyBtn">&#22797;&#21046;&#20840;&#25991;</button>
    </header>

    <article id="transcript">$encodedText</article>
  </main>

  <script>
    const button = document.getElementById("copyBtn");
    const transcript = document.getElementById("transcript");

    button.addEventListener("click", async () => {
      const text = transcript.innerText.trim();
      try {
        await navigator.clipboard.writeText(text);
        button.textContent = "\u5df2\u590d\u5236";
        window.setTimeout(() => {
          button.textContent = "\u590d\u5236\u5168\u6587";
        }, 1400);
      } catch {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(transcript);
        selection.removeAllRanges();
        selection.addRange(range);
        button.textContent = "\u5df2\u9009\u4e2d";
      }
    });
  </script>
</body>
</html>
"@

Set-Content -LiteralPath $OutputPath -Value $html -Encoding UTF8
Write-Host "READABLE_TRANSCRIPT_HTML_DONE"
Write-Host "Output: $OutputPath"
