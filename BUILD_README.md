# P-Viewer 打包说明

## Windows 打包

### 方法一：快速打包（无图标）

```cmd
build_windows.bat
```

这会创建一个基础的 exe 文件，无自定义图标。

### 方法二：完整打包（带图标）

```cmd
build_windows_with_icon.bat
```

这会：
1. 自动生成图标文件
2. 打包为带图标的 exe
3. 复制示例文件
4. 创建使用说明

**推荐使用此方法**

### 手动打包步骤

如果自动脚本失败，可以手动执行：

```cmd
# 1. 安装 PyInstaller
pip install pyinstaller

# 2. 可选：生成图标
pip install Pillow
python create_icon.py

# 3. 打包
pyinstaller --name=P-Viewer --onefile --windowed --add-data "themes.py;." --icon=icon.ico p_viewer.py

# 4. 输出文件在 dist 目录
```

## 打包选项说明

- `--name=P-Viewer` - 设置程序名称
- `--onefile` - 打包为单个 exe 文件
- `--windowed` - 无控制台窗口（GUI 程序）
- `--add-data "themes.py;."` - 包含主题配置文件
- `--icon=icon.ico` - 设置程序图标
- `--clean` - 清理临时文件
- `--noupx` - 不使用 UPX 压缩（提高兼容性）

## 输出文件

打包完成后，`dist` 目录包含：

```
dist/
├── P-Viewer.exe          # 主程序（约 10-15 MB）
├── examples/             # 示例文件
│   ├── example.json
│   └── example.proto
├── README.md             # 项目说明
└── 使用说明.txt          # 快速使用指南
```

## 使用打包后的程序

### 方式 1：直接启动
双击 `P-Viewer.exe`，然后通过菜单打开文件

### 方式 2：拖拽打开
将 JSON 或 Proto 文件拖拽到 `P-Viewer.exe` 图标上

### 方式 3：命令行
```cmd
P-Viewer.exe example.json
P-Viewer.exe example.proto
```

### 方式 4：右键菜单（可选）
可以将 P-Viewer 添加到文件右键菜单：

1. 创建注册表文件 `add_to_context_menu.reg`：
```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\*\shell\P-Viewer]
@="用 P-Viewer 打开"
"Icon"="C:\\Path\\To\\P-Viewer.exe"

[HKEY_CLASSES_ROOT\*\shell\P-Viewer\command]
@="\"C:\\Path\\To\\P-Viewer.exe\" \"%1\""
```

2. 修改路径为实际路径
3. 双击运行注册表文件

## 常见问题

### Q: 打包失败，提示找不到模块
A: 确保在项目目录下运行打包脚本，且 `themes.py` 文件存在

### Q: exe 文件太大
A: 这是正常的，PyInstaller 会打包 Python 解释器和所有依赖。可以尝试：
- 使用 `--onefile` 减少文件数量
- 使用虚拟环境减少依赖

### Q: 杀毒软件报警
A: PyInstaller 打包的程序可能被误报，可以：
- 添加到白名单
- 使用代码签名证书
- 从源码运行

### Q: 无法生成图标
A: 需要安装 Pillow 库：
```cmd
pip install Pillow
```

### Q: 程序启动慢
A: 首次启动会解压文件，后续会快很多。可以使用 `--onedir` 模式提速。

## 优化建议

### 减小文件大小
使用虚拟环境打包：
```cmd
python -m venv venv
venv\Scripts\activate
pip install pyinstaller
# 然后运行打包脚本
```

### 提高启动速度
使用目录模式（多文件）：
```cmd
pyinstaller --name=P-Viewer --onedir --windowed --add-data "themes.py;." --icon=icon.ico p_viewer.py
```

输出为 `dist\P-Viewer\` 目录，包含多个文件，但启动更快。

## 分发建议

### 单文件分发
- 优点：只需分发一个 exe 文件
- 缺点：首次启动慢，文件较大
- 适合：简单分发

### 目录分发
- 优点：启动快，可以更新单个文件
- 缺点：需要分发整个目录
- 适合：专业部署

### 压缩包分发
推荐打包为 ZIP：
```
P-Viewer-v1.0.0-windows.zip
├── P-Viewer.exe
├── examples/
├── README.md
└── 使用说明.txt
```

## 版本管理

每次发布新版本时：
1. 更新 `p_viewer.py` 中的版本号
2. 更新 `README.md` 中的版本号
3. 重新打包
4. 创建 Git tag：`git tag v1.0.0`

## 许可证

打包后的程序遵循 MIT License，可以自由分发。
