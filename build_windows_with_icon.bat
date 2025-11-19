@echo off
REM P-Viewer Windows 打包脚本（带图标）

echo ========================================
echo P-Viewer Windows 打包工具（带图标）
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo [1/5] 检查依赖...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [安装] 正在安装 PyInstaller...
    pip install pyinstaller
)

echo.
echo [2/5] 创建图标...
if not exist icon.ico (
    echo [提示] 正在生成图标文件...
    python create_icon.py
    if not exist icon.ico (
        echo [警告] 图标生成失败，将使用默认图标
        set ICON_PARAM=--icon=NONE
    ) else (
        set ICON_PARAM=--icon=icon.ico
    )
) else (
    echo [OK] 图标文件已存在
    set ICON_PARAM=--icon=icon.ico
)

echo.
echo [3/5] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist P-Viewer.spec del /q P-Viewer.spec

echo.
echo [4/5] 开始打包...
echo [提示] 这可能需要几分钟时间...
pyinstaller --name=P-Viewer ^
    --onefile ^
    --windowed ^
    --add-data "themes.py;." ^
    %ICON_PARAM% ^
    --clean ^
    --noupx ^
    p_viewer.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo [5/5] 整理输出文件...
if not exist dist\examples mkdir dist\examples
copy example.json dist\examples\ >nul 2>&1
copy example.proto dist\examples\ >nul 2>&1
copy README.md dist\ >nul 2>&1

REM 创建快速启动说明
echo 使用方法: > dist\使用说明.txt
echo. >> dist\使用说明.txt
echo 1. 双击 P-Viewer.exe 启动程序 >> dist\使用说明.txt
echo 2. 或拖拽 JSON/Proto 文件到 P-Viewer.exe 图标上打开 >> dist\使用说明.txt
echo 3. 或命令行运行: P-Viewer.exe 文件路径 >> dist\使用说明.txt
echo. >> dist\使用说明.txt
echo 示例文件在 examples 文件夹中 >> dist\使用说明.txt

echo.
echo ========================================
echo [完成] 打包成功！
echo ========================================
echo.
echo 输出目录: dist\
echo 可执行文件: dist\P-Viewer.exe
echo 文件大小: 
dir dist\P-Viewer.exe | find "P-Viewer.exe"
echo.
echo 示例文件: dist\examples\
echo   - example.json
echo   - example.proto
echo.
echo 使用方法:
echo   1. 双击 P-Viewer.exe 启动
echo   2. 拖拽文件到图标上打开
echo   3. 命令行: P-Viewer.exe example.json
echo.

pause
