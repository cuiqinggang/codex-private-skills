param([int]$Choice=-1)
$items=[ordered]@{
  '1'='检查项目';'2'='建立 Git 安全基线预览';'3'='开始单路线探索预览';'4'='开始多路线探索预览';'5'='查看工作树';'6'='初始化工作树环境';'7'='执行路线验收';'8'='路线比较';'9'='建立候选整合区预览';'10'='执行最终验收';'11'='查看主线合并建议';'12'='归档失败路线';'13'='清理已完成工作树预览';'14'='查看版本历史';'15'='建立恢复工作树预览';'16'='打开仪表盘';'17'='扫描现有技能包';'18'='查看技能包分级';'19'='查看 L3 重点技能';'20'='为某技能建立项目档案';'21'='生成某技能探索计划';'22'='启动 UltraFusion 安全探索预览';'23'='启动长流程代码安全探索预览';'24'='启动独立站技能安全探索预览';'0'='退出'
}
Write-Host '完整安全探索工作台 V1.0'
foreach($k in $items.Keys){Write-Host "[$k] $($items[$k])"}
if($Choice -lt 0){$raw=Read-Host '请选择';if(-not[int]::TryParse($raw,[ref]$Choice)){Write-Error '无效选择';exit 2}}
$key=[string]$Choice
if(-not $items.Contains($key)){Write-Error '无效选择';exit 2}
if($Choice -eq 0){Write-Host '已安全退出。';exit 0}
Write-Host "已选择：$($items[$key])"
Write-Host '高风险动作只提供预览。请使用同目录对应编号脚本并传入明确路径与确认参数。'
exit 0





