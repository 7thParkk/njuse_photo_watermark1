@echo off
REM Docker 镜像构建和导出脚本 (Windows)

set IMAGE_NAME=ai-travel-planner
set IMAGE_TAG=latest
set OUTPUT_FILE=ai-travel-planner.tar.gz

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo  错误：未找到 Docker
    echo ========================================
    echo.
    echo 请先安装 Docker Desktop for Windows
    echo 下载地址: https://www.docker.com/products/docker-desktop/
    echo.
    echo 安装完成后：
    echo 1. 启动 Docker Desktop
    echo 2. 等待 Docker 完全启动（系统托盘图标不再闪烁）
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo 检测到 Docker 版本:
docker --version
echo.

echo Building Docker image...

docker build -t %IMAGE_NAME%:%IMAGE_TAG% .

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo  构建失败！
    echo ========================================
    echo.
    echo 请检查：
    echo 1. Docker Desktop 是否正在运行
    echo 2. Dockerfile 是否存在
    echo 3. 网络连接是否正常（需要下载依赖）
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo Image built successfully!
echo.
echo Image information:
docker images | findstr %IMAGE_NAME%

echo.
echo Exporting image...

REM 检查 gzip 是否可用（Windows 10+ 通常自带）
where gzip >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    docker save %IMAGE_NAME%:%IMAGE_TAG% | gzip > %OUTPUT_FILE%
) else (
    echo 警告: 未找到 gzip，将导出未压缩的 tar 文件...
    docker save %IMAGE_NAME%:%IMAGE_TAG% -o ai-travel-planner.tar
    set OUTPUT_FILE=ai-travel-planner.tar
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ========================================
    echo  导出失败！
    echo ========================================
    echo.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================
echo  镜像导出完成！
echo ========================================
echo File location: %CD%\%OUTPUT_FILE%
echo.
echo Usage instructions:
echo 1. Share the %OUTPUT_FILE% file with others
echo 2. Others can import it using:
if "%OUTPUT_FILE%"=="ai-travel-planner.tar.gz" (
    echo    gunzip -c %OUTPUT_FILE% ^| docker load
) else (
    echo    docker load -i %OUTPUT_FILE%
)
echo 3. Then run the container:
echo    docker run -d -p 3000:80 --name %IMAGE_NAME% %IMAGE_NAME%:%IMAGE_TAG%

pause

