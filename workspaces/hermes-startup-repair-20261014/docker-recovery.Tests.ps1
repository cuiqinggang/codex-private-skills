$ErrorActionPreference = 'Stop'
$target = 'C:\Users\A\Hermes_Windows_Native_014\launcher\start-hermes-openwebui.ps1'
$tok = $null; $err = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($target,[ref]$tok,[ref]$err)
if ($err.Count) { throw 'PARSE_FAILURE' }
$fn = $ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq 'Ensure-Docker'},$true)[0]
Invoke-Expression $fn.Extent.Text
function Test-DockerReady { $false }
function Wait-Until { param($TimeoutSeconds,$IntervalSeconds,$Label,$Condition) $false }
function Invoke-DockerBounded { param($ArgumentLine,$TimeoutSeconds) $true }
function Write-Log { param($Message) }
$DockerDesktopExe = 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
$DockerTimeoutSeconds = 300

 Describe 'Docker readiness recovery' {
  Mock Write-Log {}; Mock Start-Process {}; Mock Test-Path { $true }
  Mock Invoke-DockerBounded { $true }; Mock Wait-Until { $true }
  It 'keeps a healthy engine running' {
   Mock Test-DockerReady { $true }; Ensure-Docker
   Assert-MockCalled Start-Process -Times 0 -Exactly
   Assert-MockCalled Invoke-DockerBounded -Times 0 -Exactly
  }
  It 'starts a stopped engine without restart' {
   Mock Test-DockerReady { $false }; Ensure-Docker
   Assert-MockCalled Start-Process -Times 1 -Exactly
   Assert-MockCalled Invoke-DockerBounded -Times 0 -Exactly
  }
  It 'recovers once after readiness timeout' {
   Mock Test-DockerReady { $false }; Mock Wait-Until { $Label -eq 'Docker API after official restart' }
   Ensure-Docker
   Assert-MockCalled Invoke-DockerBounded -Times 1 -Exactly -ParameterFilter { $ArgumentLine -eq 'desktop restart --timeout 60' -and $TimeoutSeconds -eq 65 }
  }
 }
