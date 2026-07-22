param([Parameter(Mandatory=$true)][string]$ProjectPath,[int]$Count=20)
git -C ([IO.Path]::GetFullPath($ProjectPath)) log --oneline --decorate --graph -n $Count







