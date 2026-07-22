param([Parameter(Mandatory=$true)][string]$WorktreePath,[string]$Disposition='auto',[string[]]$SelectedFiles=@(),[string[]]$RejectedFiles=@())
& (Join-Path $PSScriptRoot 'scripts\acceptance\evaluate-route.ps1') -WorktreePath $WorktreePath -Disposition $Disposition -SelectedFiles $SelectedFiles -RejectedFiles $RejectedFiles







