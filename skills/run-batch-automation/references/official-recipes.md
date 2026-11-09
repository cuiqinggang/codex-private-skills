> V1.3补充：本页保留原分类和来源；最新范围、版本及导入条件以 R87-Catalog-Coverage.json 和 catalog-sources.json 为准，未配置项不代表本机可运行。

# 官方成熟批处理接口

以下均为官方资料核查，当前目标机安装与业务调用未验；首次具体任务核对原版本接口与依赖，不因此重复安装全部工具。占位符是调用模板，不是已经运行的命令。

## duckdb-multiple-files

**多CSV/Parquet/JSON整批读取与查询 — DuckDB**

冻结多文件清单、字段/类型/金额语义；不要依赖推断保留前导零。
原生文件列表或glob输入；需要按列名合并时显式确认union_by_name。

```json
{
  "sql_shape": "SELECT * FROM read_csv(['<IN1.csv>','<IN2.csv>']);"
}
```

验收：核对文件与行数、列类型、重复项及精确汇总；金额优先既有整数分/精确节点。
边界：不同schema和自动类型推断须按合同处理；不是无限精度金额计算器。

官方来源：https://duckdb.org/docs/stable/data/multiple_files/overview；https://duckdb.org/docs/stable/data/csv/overview

## imagemagick-images

**图片批量缩放裁切与格式转换 — ImageMagick 7**

明确图片清单、尺寸/颜色/透明度合同和独立输出目录。
调用原生mogrify一次处理多图。

```json
{
  "argv": [
    "magick",
    "mogrify",
    "-path",
    "<EXISTING_OUT_DIR>",
    "-resize",
    "<GEOMETRY>",
    "<FILE1>",
    "<FILE2>"
  ]
}
```

验收：逐文件解码、尺寸/格式/透明度及输入输出对应；按视觉要求检查。
边界：mogrify默认可能改写原图，必须指定隔离输出并预查同名冲突。

官方来源：https://imagemagick.org/mogrify/；https://imagemagick.org/command-line-options/

## ffmpeg-media

**音视频清单拼接及既定转码配方 — FFmpeg / ffprobe**

先明确是拼接一个成片还是逐文件转换；检查流/编码/时间戳与交付格式。
兼容流使用concat清单；独立多文件转换调用原工具批次循环。

```json
{
  "argv": [
    "ffmpeg",
    "-n",
    "-f",
    "concat",
    "-safe",
    "1",
    "-i",
    "<RELATIVE_SAFE_LIST>",
    "-c",
    "copy",
    "<OUT>"
  ]
}
```

验收：逐输出检查时长、流、完整解码和声音；交付要求播放时在用户播放器实际播放。
边界：stream copy不做重编码，拼接要求兼容；不是将任意多个输入直接通配后自动转码。

官方来源：https://ffmpeg.org/ffmpeg-formats.html#concat-1；https://ffmpeg.org/ffmpeg.html；https://ffmpeg.org/ffprobe.html

## libreoffice-convert

**Office文件原生批量转换 — LibreOffice**

支持的文件格式、正确过滤器、字体及输出命名映射；独立工作目录。
headless convert-to接受多个输入，outdir指向新目录。

```json
{
  "argv": [
    "<SOFFICE>",
    "--headless",
    "--convert-to",
    "<FORMAT>",
    "--outdir",
    "<OUT_DIR>",
    "<FILE1>",
    "<FILE2>"
  ]
}
```

验收：核对输出数量并打开检查正文/表格/页数；外部重算与缓存读回分别登记。
边界：同名输出和共享profile先处理；不把退出0当排版保真或公式已重算。

官方来源：https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html

## pandoc-documents

**多份Markdown等资料合成为文档 — Pandoc**

明确输入顺序、文档结构和原模板。
原生多输入合成为一个输出；独立文件转换按原工具逐文件调用。

```json
{
  "argv": [
    "pandoc",
    "-s",
    "<FILE1.md>",
    "<FILE2.md>",
    "-o",
    "<OUT.docx>"
  ]
}
```

验收：检查章节、引用、表格及目标应用打开效果。
边界：多输入会拼为一本，不能误当各自独立输出；复杂版式可能丢失。

官方来源：https://pandoc.org/MANUAL.html

## qpdf-pages

**PDF合并拆分旋转与页面清单 — qpdf**

明确页面范围、顺序及独立输出；只做原合同的结构操作。
原生pages/split-pages，长参数可用官方参数文件。

```json
{
  "merge_argv": [
    "qpdf",
    "--empty",
    "--pages",
    "<IN1.pdf>",
    "<IN2.pdf>",
    "--",
    "<OUT.pdf>"
  ],
  "split_argv": [
    "qpdf",
    "--split-pages",
    "<IN.pdf>",
    "<OUT_PATTERN>"
  ]
}
```

验收：qpdf --check后核对页数、页序和实际关键页面；警告退出码单列。
边界：结构检查不能证明内容/视觉完全正确；不包含OCR或扫描件文字识别。

官方来源：https://qpdf.readthedocs.io/en/stable/cli.html

## powershell-command-batch

**Windows已有命令清单原生批次执行 — PowerShell**

每项已有经确认的原命令、明确输入/输出映射；不把输入内容当脚本。
优先原生批接口，否则ForEach-Object调用已审核命令；并发参数按资源限定。

```json
{
  "native_interface": "ForEach-Object -Process <approved-existing-operation>",
  "optional_parallel_interface": "ForEach-Object -Parallel <approved-operation> -ThrottleLimit <N>"
}
```

验收：逐项检查退出状态和产物，任何缺项保留未完成。
边界：runspace不是独立机器；外部进程用显式WorkingDirectory，勿共享相对输出。

官方来源：https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/foreach-object?view=powershell-7.5

## gnu-parallel-resume

**已有命令批次的日志与差量恢复 — GNU Parallel**

原执行端确缺少日志恢复；命令、输入顺序、joblog冻结，外部副作用先对账。
调用joblog和resume-failed恢复未完成/失败项。

```json
{
  "documented_flags": [
    "--joblog",
    "--resume-failed"
  ],
  "source_of_commands": "existing reviewed command; no generated shell from untrusted inputs"
}
```

验收：日志和实际输出独立核对，不能凭日志跳过业务验收。
边界：恢复依赖不变的命令/输入/日志；Windows额外运行环境未核，不作默认入口。

官方来源：https://www.gnu.org/software/parallel/parallel_tutorial.html；https://www.gnu.org/software/parallel/man.html
