$ErrorActionPreference = 'Stop'
$Host.UI.RawUI.WindowTitle = 'D通道 - ngrok一次性本机配置'
$ngrokExecutable = 'C:/Users/A/AppData/Local/Microsoft/WindowsApps/ngrok.exe'
Write-Host 'D通道固定网址：一次性本机配置' -ForegroundColor Cyan
Write-Host '请在ngrok官网“您的身份验证令牌”页面复制现有Authtoken。'
Write-Host '仅粘贴到此本机窗口；不要发到聊天。输入内容不会显示。'
$ngrokToken = Read-Host '粘贴Authtoken后按回车' -MaskInput
if ([string]::IsNullOrWhiteSpace($ngrokToken)) { throw '未输入令牌，未修改配置。' }
try {
  & $ngrokExecutable config add-authtoken $ngrokToken
  if ($LASTEXITCODE -ne 0) { throw 'ngrok官方配置命令未成功。' }
} finally { $ngrokToken = $null }
& $ngrokExecutable config check
if ($LASTEXITCODE -ne 0) { throw 'ngrok配置检查未成功。' }
Write-Host '配置成功。请返回聊天回复：已配置' -ForegroundColor Green
Read-Host '按回车关闭此一次性窗口'
