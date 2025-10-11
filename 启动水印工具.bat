@echo off
chcp 65001 >nul
echo ==========================================
echo    照片水印工具 v1.0
echo ==========================================
echo.
echo 正在启动应用程序...
echo.

cd /d "%~dp0"

if exist "dist\照片水印工具.exe" (
    start "" "dist\照片水印工具.exe"
    echo 应用程序已启动！
) else (
    echo 错误：找不到可执行文件！
    echo 请确保 dist\照片水印工具.exe 存在。
    pause
)
