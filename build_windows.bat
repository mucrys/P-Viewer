@echo off
REM P-Viewer Windows 打包脚本

echo ========================================
echo P-Viewer Windows 打包工具
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo [1/4] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
) else (
    echo [OK] PyInstaller 已安装
)

echo.
echo [2/4] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist P-Viewer.spec del /q P-Viewer.spec

echo.
echo [3/4] 开始打包...
pyinstaller --name=P-Viewer ^
    --onefile ^
    --windowed ^
    --add-data "themes.py;." ^
    --icon=NONE ^
    --clean ^
    p_viewer.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo [4/4] 复制示例文件...
if not exist dist\examples mkdir dist\examples
copy example.json dist\examples\ >nul
copy example.proto dist\examples\ >nul
copy README.md dist\ >nul

echo.
echo ========================================
echo [完成] 打包成功！
echo ========================================
echo.
echo 可执行文件位置: dist\P-Viewer.exe
echo 示例文件位置: dist\examples\
echo.
echo 使用方法:
echo   1. 双击 P-Viewer.exe 启动程序
echo   2. 或拖拽文件到 P-Viewer.exe 图标上打开
echo   3. 或命令行: P-Viewer.exe example.json
echo.

pause
