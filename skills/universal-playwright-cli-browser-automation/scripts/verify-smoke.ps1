$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path ".\evidence" | Out-Null

playwright-cli --help | Out-Null
playwright-cli open https://demo.playwright.dev/todomvc/ --headed
playwright-cli type "UNIVERSAL_PLAYWRIGHT_CLI_VERIFY_OK"
playwright-cli press Enter
playwright-cli snapshot --filename=.\evidence\verify-snapshot.yml
playwright-cli screenshot --filename=.\evidence\verify-screenshot.png
playwright-cli close

Write-Host "UNIVERSAL_PLAYWRIGHT_CLI_VERIFY_PASS"
