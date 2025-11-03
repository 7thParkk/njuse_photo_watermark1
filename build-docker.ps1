# Docker 镜像构建和导出脚本 (PowerShell)

$IMAGE_NAME = "ai-travel-planner"
$IMAGE_TAG = "latest"
$OUTPUT_FILE = "ai-travel-planner.tar.gz"

# 检查 Docker 是否安装
Write-Host "检查 Docker 安装状态..." -ForegroundColor Cyan
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "检测到 Docker: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  错误：未找到 Docker" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Docker Desktop for Windows" -ForegroundColor Yellow
    Write-Host "下载地址: https://www.docker.com/products/docker-desktop/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "安装完成后：" -ForegroundColor Yellow
    Write-Host "1. 启动 Docker Desktop" -ForegroundColor White
    Write-Host "2. 等待 Docker 完全启动（系统托盘图标不再闪烁）" -ForegroundColor White
    Write-Host "3. 重新运行此脚本" -ForegroundColor White
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Host ""
Write-Host "🚀 开始构建 Docker 镜像..." -ForegroundColor Green

# 构建镜像
docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  构建失败！" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "请检查：" -ForegroundColor Yellow
    Write-Host "1. Docker Desktop 是否正在运行" -ForegroundColor White
    Write-Host "2. Dockerfile 是否存在" -ForegroundColor White
    Write-Host "3. 网络连接是否正常（需要下载依赖）" -ForegroundColor White
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit $LASTEXITCODE
}

Write-Host "✅ 镜像构建完成！" -ForegroundColor Green
Write-Host "📦 镜像信息：" -ForegroundColor Cyan
docker images | Select-String $IMAGE_NAME

Write-Host ""
Write-Host "💾 导出镜像文件..." -ForegroundColor Green

# 导出并压缩镜像
try {
    docker save "${IMAGE_NAME}:${IMAGE_TAG}" | Out-File -FilePath "ai-travel-planner.tar" -Encoding Binary
    Compress-Archive -Path "ai-travel-planner.tar" -DestinationPath $OUTPUT_FILE -Force
    Remove-Item "ai-travel-planner.tar" -Force
} catch {
    Write-Host "使用备用方法导出..." -ForegroundColor Yellow
    docker save "${IMAGE_NAME}:${IMAGE_TAG}" -o "ai-travel-planner.tar"
    $OUTPUT_FILE = "ai-travel-planner.tar"
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  导出失败！" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Read-Host "按 Enter 键退出"
    exit $LASTEXITCODE
}

$fileSize = (Get-Item $OUTPUT_FILE).Length / 1MB
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  镜像导出完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "📁 文件位置: $(Get-Location)\$OUTPUT_FILE" -ForegroundColor Cyan
Write-Host "📊 文件大小: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan

Write-Host ""
Write-Host "📝 使用说明：" -ForegroundColor Yellow
Write-Host "1. 将 $OUTPUT_FILE 文件分享给其他人"
Write-Host "2. 其他人可以运行以下命令导入："
if ($OUTPUT_FILE -eq "ai-travel-planner.tar.gz") {
    Write-Host "   gunzip -c $OUTPUT_FILE | docker load" -ForegroundColor White
} else {
    Write-Host "   docker load -i $OUTPUT_FILE" -ForegroundColor White
}
Write-Host "3. 然后运行容器："
Write-Host "   docker run -d -p 3000:80 --name $IMAGE_NAME ${IMAGE_NAME}:${IMAGE_TAG}" -ForegroundColor White

Write-Host ""
Read-Host "按 Enter 键退出"

