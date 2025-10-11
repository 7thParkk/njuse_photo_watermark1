## 目标概述
实现一个命令行工具：批量读取指定路径下图片的 EXIF 拍摄日期（取年月日）作为文本水印，按用户指定的字体大小、颜色、位置绘制到图片上，输出到“原目录名_watermark”子目录。

## 使用场景与假设
- 输入路径既可以是文件也可以是目录。若为目录，默认处理该目录下的所有图片文件（可选：支持递归）。
- 拍摄时间从 EXIF 中读取优先字段：`DateTimeOriginal` → `CreateDate` → `DateTime`。无 EXIF 或无时间时可选择跳过或使用文件创建时间（可配置）。
- 输出目录命名：`{原目录名}_watermark`，位于原目录下；文件名沿用原名（可选添加后缀 `_wm`）。
- 仅为位图格式添加水印：JPEG/JPG、PNG、WEBP、TIFF（以 Pillow 支持为准）。

## 命令行交互设计
### 基本用法
- 处理目录：
```bash
photo-wm "C:\\path\\to\\images"
```
- 处理单文件：
```bash
photo-wm "C:\\path\\to\\images\\IMG_0001.jpg"
```

### 主要参数
- `--font-size, -s`：字体大小，默认 32。
- `--color, -c`：颜色（十六进制或常见名称），默认 `#FFFFFF`。
- `--position, -p`：位置，枚举：`top-left|top-right|center|bottom-left|bottom-right`，默认 `bottom-right`。
- `--margin, -m`：边距像素，默认 16（水平和垂直统一；可扩展为 `--margin-x --margin-y`）。
- `--date-format, -f`：日期格式，默认 `YYYY-MM-DD`（支持 `YYYY/MM/DD`、`YYYY.MM.DD` 等）。
- `--font-path`：字体文件路径（Windows 推荐 `C:\\Windows\\Fonts\\msyh.ttc`；找不到则回退到默认字体）。
- `--recursive, -r`：递归处理子目录，默认 false。
- `--fallback-filetime`：EXIF 缺失时使用文件创建时间，默认 true。
- `--suffix`：输出文件名后缀，默认空（可配置 `_wm`）。
- `--overwrite`：若输出已存在是否覆盖，默认 false（否则跳过或自动加序号）。
- `--ext`：输出格式，默认与原图一致（可指定 `jpg|png|webp`）。
- `--quality`：输出质量（JPG/WEBP 有效），默认 90。
- `--dry-run`：仅预览将要处理的文件与参数，不写文件。
- `--verbose, -v`：输出详细日志。

### 示例
- 蓝色小水印居中、大字体、递归处理：
```bash
photo-wm "D:\\Album\\Trip2023" -r -s 42 -c "#3A7BFF" -p center -m 24
```
- 指定中文字体与日期格式，EXIF 缺失使用文件时间：
```bash
photo-wm "D:\\Photos" --font-path "C:\\Windows\\Fonts\\msyh.ttc" -f "YYYY年MM月DD日" --fallback-filetime
```

## 核心流程
1. 解析参数与校验（路径存在、字体文件存在/可回退、颜色格式、位置枚举）。
2. 收集待处理文件列表：
   - 若是文件：仅该文件。
   - 若是目录：列出符合扩展名的图片；若 `--recursive`，深度优先遍历。
3. 为每个文件：
   - 读取 EXIF：
     - 优先字段：`DateTimeOriginal`、`CreateDate`、`DateTime`（不同库命名略有差异）。
     - 解析为 `datetime`；若失败且 `--fallback-filetime`，读取文件创建/修改时间。
     - 格式化为用户指定 `date-format`。
   - 打开图像，计算文本尺寸与放置坐标：
     - 基于 `font-size` 与字体度量获取文本宽高。
     - 根据 `position` 与 `margin` 计算左上角坐标。
   - 绘制水印：
     - 先可选绘制半透明阴影/描边增强可读性（可后续扩展 `--shadow --stroke`）。
     - 使用 RGBA 颜色，支持透明度（可后续扩展 `--alpha`）。
   - 输出路径：
     - 输出目录 `原目录名_watermark`；若输入为文件，输出到该文件所在目录的 `所在目录名_watermark`。
     - 文件名加后缀（若提供），扩展名根据 `--ext` 或原格式。
     - 存在冲突：
       - `--overwrite`: 覆盖。
       - 否则：`name (1).jpg` 递增命名。
   - 保存时保留基本 EXIF（若格式支持；如需要保留完整 EXIF，可使用 piexif 回写）。
4. 统计处理结果与错误，输出汇总。

## 位置与文本布局规则
- 位置枚举映射：
  - `top-left`: `(margin, margin)`
  - `top-right`: `(image_width - text_width - margin, margin)`
  - `center`: `((image_width - text_width)/2, (image_height - text_height)/2)`
  - `bottom-left`: `(margin, image_height - text_height - margin)`
  - `bottom-right`: `(image_width - text_width - margin, image_height - text_height - margin)`
- 文本测量：使用字体度量获得 `text_width, text_height`，考虑行高与基线。避免越界，必要时做最小缩放或截断（可选：`--fit` 自动缩小防溢出）。

## 依赖与技术选型
- 语言：Python 3.10+（跨平台、图片生态成熟）。
- 图像处理：Pillow（`PIL`）。
- EXIF 读取：
  - 简单读取：Pillow 自带 `Image._getexif()`（有限制）。
  - 稳健读取/写回：`piexif` 或 `exifread`。建议：读取用 `exifread`（识别广），保留 EXIF 用 `piexif`（可选）。
- CLI：`argparse` 或 `typer`（推荐 `typer` 提升可用性与自动帮助）。
- 日志：`logging`。

## 错误处理与鲁棒性
- 路径不存在、无权限：友好报错并退出。
- 非图片或损坏文件：跳过并记录警告。
- EXIF 缺失或字段不可解析：
  - 若 `--fallback-filetime`：改用文件时间。
  - 否则：跳过该文件并记录。
- 字体不可用：回退到默认字体（并提示）。
- 颜色解析失败：提示并退出。
- 写入失败（只读目录、被占用）：提示并跳过该文件。

## 性能与并发（可选）
- 对大量文件可引入多进程/多线程（I/O 密集），通过 `concurrent.futures`。
- 控制并发度，避免高内存占用与文件句柄耗尽。
- 进度条（可选）：`tqdm`。

## 日志与输出
- 默认打印概览：处理数、成功数、跳过数（无 EXIF/失败）、输出目录。
- `--verbose` 打印每个文件的来源时间、绘制参数与输出路径。
- `--dry-run` 预演将要写入的文件名和水印文本。

## 日期解析与格式化
- EXIF 字段常见格式：`YYYY:MM:DD HH:MM:SS`。
- 解析后仅取年月日。`--date-format` 映射：
  - 支持模板：`YYYY`、`MM`、`DD`。
  - 示例：`YYYY-MM-DD`、`YYYY/MM/DD`、`YYYY年MM月DD日`。
- 时区：通常本地时区即可；若用户需要，可后续扩展 `--tz`。

## 目录与文件命名策略
- 输入为目录：输出目录为 `输入目录/_dirname_watermark`，其中 `_dirname` 为该目录名。
- 输入为文件：输出目录为 `文件所在目录/所在目录名_watermark`。
- 文件名冲突：优先 `--suffix`；无后缀则自动增加序号。

## 关键实现模块划分
- `cli.py`：参数解析、入口。
- `scanner.py`：目录/文件收集与过滤。
- `exif_reader.py`：读取与规范化时间字段。
- `watermark.py`：文本测量、位置计算、绘制。
- `io_utils.py`：输出目录/文件名生成、冲突处理、EXIF 保留（可选）。
- `main.py`：任务编排、错误捕获与日志。

## 测试要点
- 各格式图片：JPG/PNG/WEBP/TIFF。
- 有/无 EXIF，异常 EXIF（空、乱序、无 `:`）。
- 不同位置与边距的布局正确性。
- 不同颜色/透明度/字体大小的可读性（未来加 `--alpha`）。
- 递归与非递归行为一致。
- 冲突命名与覆盖策略有效。
- Windows 中文路径、空格路径、权限不足情况。
- 大量文件下的稳定性与资源回收。

## 未来扩展（可选）
- 批量自定义水印文本模板：`--template "{YYYY}-{MM}-{DD} | {camera_model}"`
- 轮廓描边/阴影：`--stroke 2 --stroke-color "#000" --shadow 2,2,0.3`
- 旋转与 EXIF 方向自动矫正
- 多语言本地化
- GUI 简易版


