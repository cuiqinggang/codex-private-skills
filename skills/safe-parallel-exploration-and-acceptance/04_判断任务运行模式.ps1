param([Parameter(Mandatory=$true)][string]$ProjectPath,[Parameter(Mandatory=$true)][string]$TaskDescription,[string]$Risk='medium',[int]$FileCount=1,[switch]$StableVersion,[switch]$MultipleSolutions,[switch]$Parallel,[switch]$FormalDelivery)
& (Join-Path $PSScriptRoot 'scripts\classification\classify-task.ps1') -ProjectPath $ProjectPath -TaskDescription $TaskDescription -Risk $Risk -FileCount $FileCount -StableVersion:$StableVersion -MultipleSolutions:$MultipleSolutions -Parallel:$Parallel -FormalDelivery:$FormalDelivery







