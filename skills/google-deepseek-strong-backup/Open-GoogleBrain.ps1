$root = Split-Path -Parent $PSCommandPath
Start-Process 'https://gemini.google.com/app'
Start-Process notepad.exe -ArgumentList ('"{0}"' -f (Join-Path $root 'GOOGLE_BRAIN_PROMPT.md'))
