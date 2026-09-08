# Mature upstream foundation

- PowerShell/PSScriptAnalyzer (MIT): official static checker with built-in and custom rules. Use when installed; absence must be explicit.
- pester/Pester (Apache-2.0): established PowerShell test and mock framework, compatible with Windows PowerShell 5.1 and supported PowerShell 7 releases.
- `System.Management.Automation.Language.Parser`: built into PowerShell and used as the dependency-free syntax gate.
- Microsoft PowerShell documentation: authoritative source for parsing, quoting, encoding, host-version, and native-command behavior.

This skill does not copy or install upstream packages. It orchestrates them and adds the user's machine profile, verified error catalog, and promotion loop.
