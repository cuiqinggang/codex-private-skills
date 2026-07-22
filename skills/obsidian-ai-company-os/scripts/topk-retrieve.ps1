param(
  [Parameter(Mandatory=$true)][string]$Query,
  [ValidateRange(1,20)][int]$TopK = 5,
${REDACTED_SECRET}
${REDACTED_SECRET}
  [string]$OutputPath = ''
)

$ErrorActionPreference = 'Stop'
foreach ($root in @($VaultRoot,$SkillsRoot)) {
  $resolved = (Resolve-Path -LiteralPath $root).Path
  if (-not $resolved.StartsWith('C:\',[StringComparison]::OrdinalIgnoreCase)) { throw "Active retrieval root must be on C drive: $resolved" }
}
$terms = @([regex]::Matches($Query.ToLowerInvariant(),'[\p{L}\p{N}_-]{2,}') | ForEach-Object Value | Select-Object -Unique)
if (-not $terms.Count) { throw 'Query has no searchable terms.' }
$skip = '\\(\.git|\.obsidian|node_modules|__pycache__|90-ARCHIVE|99_ARCHIVE|backups?|raw)\\'
$files = @(
  Get-ChildItem -LiteralPath $VaultRoot,$SkillsRoot -File -Recurse -Filter '*.md' -ErrorAction SilentlyContinue |
    Where-Object { $_.Length -le 524288 -and $_.FullName -notmatch $skip }
)
$hits = foreach ($file in $files) {
  $text = Get-Content -LiteralPath $file.FullName -Raw -ErrorAction SilentlyContinue
  if ($null -eq $text) { continue }
  $low = $text.ToLowerInvariant(); $name = $file.Name.ToLowerInvariant(); $score = 0
  foreach ($term in $terms) {
    if ($name.Contains($term)) { $score += 8 }
    $count = [regex]::Matches($low,[regex]::Escape($term)).Count
    $score += [Math]::Min($count,10)
  }
  if ($score -gt 0) {
    $excerpt = ($text -replace '\s+',' ').Trim()
    if ($excerpt.Length -gt 320) { $excerpt = $excerpt.Substring(0,320) }
    [pscustomobject]@{score=$score;path=$file.FullName;updated_at=$file.LastWriteTime.ToString('o');bytes=$file.Length;excerpt=$excerpt}
  }
}
$result = [pscustomobject]@{query=$Query;top_k=$TopK;roots=@($VaultRoot,$SkillsRoot);full_vault_read=$false;results=@($hits|Sort-Object score,updated_at -Descending|Select-Object -First $TopK)}
if ($OutputPath) { $result|ConvertTo-Json -Depth 6|Set-Content -LiteralPath $OutputPath -Encoding UTF8 }
$result|ConvertTo-Json -Depth 6
