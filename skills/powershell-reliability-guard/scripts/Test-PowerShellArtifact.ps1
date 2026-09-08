[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$Path,

    [ValidateSet('WindowsPowerShell51', 'PowerShell7', 'Current')]
    [string]$Target = 'WindowsPowerShell51',

    [ValidateSet('Optional', 'Required', 'Skip')]
    [string]$Analyzer = 'Optional',

    [switch]$PassThru
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

$resolvedPath = (Resolve-Path -LiteralPath $Path).ProviderPath
$tokens = $null
$parseErrors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile(
    $resolvedPath,
    [ref]$tokens,
    [ref]$parseErrors
)

$issues = New-Object System.Collections.Generic.List[object]
foreach ($parseError in $parseErrors) {
    $issues.Add([pscustomobject]@{
        Gate = 'Parser'
        Severity = 'Error'
        Line = $parseError.Extent.StartLineNumber
        Rule = 'PowerShellParser'
        Message = $parseError.Message
    })
}

$content = [System.IO.File]::ReadAllText($resolvedPath)
$nonCodeTokenKinds = @('Comment', 'StringLiteral', 'StringExpandable', 'HereStringLiteral', 'HereStringExpandable')
$codeForCompatibility = (($tokens | Where-Object { $nonCodeTokenKinds -notcontains [string]$_.Kind }) |
    ForEach-Object { $_.Text }) -join ' '
if ($Target -eq 'WindowsPowerShell51') {
    $compatibilityPatterns = @(
        @{ Rule = 'PS7PipelineChain'; Pattern = '(?m)(?<![&|])(?:&&|\|\|)(?![&|])' },
        @{ Rule = 'PS7NullOperators'; Pattern = '(?m)(?:\?\?|\?\.)' },
        @{ Rule = 'PS7Ternary'; Pattern = '(?m)\?[^\r\n:]+:' },
        @{ Rule = 'PS7Parallel'; Pattern = '(?i)ForEach-Object\s+-Parallel\b' },
        @{ Rule = 'PS7NativePreference'; Pattern = '\$PSNativeCommandUseErrorActionPreference\b' }
    )
    foreach ($item in $compatibilityPatterns) {
        if ($codeForCompatibility -match $item.Pattern) {
            $issues.Add([pscustomobject]@{
                Gate = 'Compatibility'
                Severity = 'Error'
                Line = 0
                Rule = $item.Rule
                Message = 'PowerShell 7-only construct detected in a Windows PowerShell 5.1 target.'
            })
        }
    }
}

if ($content -match '(?m)`[ \t]+$') {
    $issues.Add([pscustomobject]@{
        Gate = 'Reliability'
        Severity = 'Warning'
        Line = 0
        Rule = 'FragileBacktickContinuation'
        Message = 'A continuation backtick is followed by whitespace. Prefer splatting or parentheses.'
    })
}

$analyzerState = 'Skipped'
if ($Analyzer -ne 'Skip') {
    $module = Get-Module -ListAvailable -Name PSScriptAnalyzer |
        Sort-Object Version -Descending |
        Select-Object -First 1
    if ($null -eq $module) {
        $analyzerState = 'Unavailable'
        if ($Analyzer -eq 'Required') {
            $issues.Add([pscustomobject]@{
                Gate = 'Analyzer'
                Severity = 'Error'
                Line = 0
                Rule = 'PSScriptAnalyzerRequired'
                Message = 'PSScriptAnalyzer is required but is not installed.'
            })
        }
    }
    else {
        Import-Module $module.Path -Force
        if ($Target -eq 'WindowsPowerShell51') {
            $settingsPath = Join-Path $PSScriptRoot 'PSScriptAnalyzerSettings.psd1'
            $analyzerResults = Invoke-ScriptAnalyzer -Path $resolvedPath -Settings $settingsPath
        }
        else {
            $analyzerResults = Invoke-ScriptAnalyzer -Path $resolvedPath -Severity @('Error', 'Warning')
        }
        foreach ($result in $analyzerResults) {
            $issues.Add([pscustomobject]@{
                Gate = 'Analyzer'
                Severity = [string]$result.Severity
                Line = $result.Line
                Rule = $result.RuleName
                Message = $result.Message
            })
        }
        $analyzerState = 'Ran'
    }
}

$errors = @($issues | Where-Object Severity -eq 'Error')
$summary = [pscustomobject]@{
    Status = if ($errors.Count -eq 0) { 'PASS' } else { 'FAIL' }
    Path = $resolvedPath
    Target = $Target
    HostVersion = $PSVersionTable.PSVersion.ToString()
    Analyzer = $analyzerState
    ErrorCount = $errors.Count
    WarningCount = @($issues | Where-Object Severity -eq 'Warning').Count
    Issues = @($issues)
}

if ($PassThru) {
    $summary
    return
}

$summary | ConvertTo-Json -Depth 6
if ($errors.Count -gt 0) { exit 1 }
exit 0
