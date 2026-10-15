# Hermes F007 当前版真实图片视觉最小门｜Reality前冻结
TASK_ID=HERMES-ECO-20261014 | METHOD=《三人行》V2项目级使用 | Bridge=V6 C>A>B | Hermes专项v2.0
NODE=F007-VISION | PHASE=VIRTUAL_MATURE_FROZEN | CURRENT_SYSTEM_FINAL_VALID=NO | F002_5_ROUNDS=0/5

## 不重做成功节点
F006记录：当前CLI marker模型调用退出0，独立文件读取隐藏校验值退出0，任务级checkpoint/handoff/resume/closeout当前真实通过。官方Runs API HTTP400只有离线补丁，不因为CLI成功就冒充Runs API已通。此次只验证另一个独立未闭合能力：原生图片视觉。

## 成熟方案
不安装或部署新的视觉堆栈。使用当前已存在的正式Hermes CLI和 vision_analyze 原生视觉工具（已部署Qwen3-VL视觉链）；保留默认模型、提供商、代理、浏览器。原素材必须是现存的合成图片，不生成新图片：
C:/Users/A/.hermes/skills/hermes-mature-supertool/evidence/HERMES-ECO-20261014/F002/R01/visual.png
它由已有F002 prepare.py生成，SHA256应为5a845dacd5b306942b0c7c48ca38c64fd1edc6ea2c32c8411e800a57626dabc9。

## Reality
仅通过已继承且已真实通过的正式CLI wrapper提交一次指令：必须实际调用vision_analyze分析指定图片；不得通过读取prepare.py或脚本推断图形，不得访问其它目录/用户资料，不得修改任何文件；直接返回从左到右的三个颜色和形状列表。最多一次自然调用，不并行不重试。记录退出码、输出、runtime。

## 外部确定性验收
现有prepare.py构图：从左到右蓝色矩形、红色圆形、绿色三角形。精确期待JSON：
[{"color":"blue","shape":"rectangle"},{"color":"red","shape":"circle"},{"color":"green","shape":"triangle"}]
成功出错要区分能否证明真实工具调用：只看CLI正确输出不能证明内部vision_analyze具体工具发生；如没有系统侧工具回执，最多 IMAGE_CONTENT_PASS_TOOL_ID_UNVERIFIED，不能升级到视觉原生工具完整PASS。若模型声称没使用工具，标Blocked；失败/超时停。

## 非目标
没有验证视频、音频、OpenWebUI网页上传、Hermes API图片输入，亦未做模型路由稳定性与完整T_VALID。不可更改FlClash、代理、密钥、容器、浏览器、其它业务状态。
