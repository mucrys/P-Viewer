# P-Viewer 项目总结

## 项目信息

- **项目名称**: P-Viewer
- **版本**: V1.0.0
- **描述**: 程序员专用文件查看和编辑工具
- **支持格式**: JSON, Proto
- **许可证**: MIT License

## 文件结构

```
p-viewer/
├── p_viewer.py                    # 主程序 (~600行)
├── themes.py                      # 主题配置
├── example.json                   # JSON示例文件
├── example.proto                  # Proto示例文件
├── README.md                      # 项目说明
├── BUILD_README.md                # 打包说明
├── SUMMARY.md                     # 项目总结（本文件）
│
├── build.py                       # Python打包脚本（推荐）
├── build_windows.bat              # Windows批处理打包脚本
├── build_windows_with_icon.bat    # 带图标的批处理打包脚本
├── create_icon.py                 # 图标生成脚本
├── icon.ico                       # 程序图标
├── icon.png                       # 图标PNG版本
│
├── test_encoding.py               # 编码测试脚本
├── diagnose.py                    # 诊断工具
├── fix_encoding.py                # 编码修复工具
├── test_exe.py                    # exe测试脚本
│
├── .gitignore                     # Git忽略配置
├── .vscode/                       # VS Code配置
│   └── settings.json              # 编辑器设置
│
└── dist/                          # 打包输出目录
    ├── P-Viewer.exe               # 可执行文件 (~11MB)
    ├── examples/                  # 示例文件
    │   ├── example.json
    │   └── example.proto
    ├── README.md
    └── 使用说明.txt
```

## 核心功能

### 1. 双格式支持
- **JSON**: 树形视图 + 语法高亮 + 错误定位
- **Proto**: 结构视图 + 语法高亮 + 元素解析

### 2. 双视图显示
- **左侧**: 结构树视图（可展开/收起）
- **右侧**: 源码编辑器（带行号、语法高亮）
- **同步**: 点击树节点自动跳转到源码位置

### 3. 编辑功能
- 完整的文本编辑功能（撤销/重做/复制/粘贴）
- 实时语法高亮
- 行号显示
- 语法检查（JSON）

### 4. 主题系统
- GitHub 亮色/暗色
- VS Code 亮色/暗色
- 字体缩放（Ctrl+/Ctrl-/Ctrl+0）

### 5. 配置持久化
- 自动保存主题设置
- 自动保存字体大小
- 配置文件：`~/.p_viewer_config.json`

## 技术特点

### 零依赖
- 仅使用 Python 标准库
- 无需安装第三方包即可运行源码
- 打包后为单个 exe 文件

### 跨平台
- Windows: 完全支持
- macOS: 支持（需要 Python + Tkinter）
- Linux: 支持（需要 Python + python3-tk）

### 轻量级
- 源码: ~600 行
- exe 文件: ~11 MB
- 启动速度: < 2秒
- 内存占用: < 100MB

## 使用方法

### 运行源码
```bash
# 直接运行
python p_viewer.py

# 打开指定文件
python p_viewer.py example.json
python p_viewer.py example.proto
```

### 使用 exe
```cmd
# 方式1: 双击启动
P-Viewer.exe

# 方式2: 拖拽文件到图标
# 将文件拖到 P-Viewer.exe 图标上

# 方式3: 命令行
P-Viewer.exe example.json
```

## 打包说明

### 快速打包
```bash
python build.py
```

这会自动：
1. 检查并安装 PyInstaller
2. 清理旧文件
3. 生成图标（如果有 Pillow）
4. 打包为 exe
5. 复制示例文件
6. 创建使用说明

### 输出文件
- `dist/P-Viewer.exe` - 主程序
- `dist/examples/` - 示例文件
- `dist/README.md` - 说明文档
- `dist/使用说明.txt` - 快速指南

## 编码问题解决

### 如果看到乱码

1. **运行诊断工具**
```bash
python diagnose.py
```

2. **修复文件编码**
```bash
python fix_encoding.py
```

3. **VS Code 设置**
- 右下角点击编码 -> 选择 "UTF-8"
- 设置 -> 搜索 "files.encoding" -> 设置为 "utf8"

4. **已配置**
- 项目已包含 `.vscode/settings.json`
- 自动设置 UTF-8 编码

## 快捷键

### 文件操作
- `Ctrl+O` - 打开文件
- `Ctrl+S` - 保存文件

### 编辑操作
- `Ctrl+Z` - 撤销
- `Ctrl+Y` - 重做
- `Ctrl+X` - 剪切
- `Ctrl+C` - 复制
- `Ctrl+V` - 粘贴
- `Ctrl+A` - 全选

### 视图操作
- `F5` - 语法检查
- `Ctrl+` - 放大字体
- `Ctrl-` - 缩小字体
- `Ctrl+0` - 重置字体

## 数据类型标签

### JSON
- `Obj` - 对象（蓝色）
- `Arr` - 数组（绿色）
- `Str` - 字符串（橙色）
- `Num` - 数字（紫色）
- `Bool` - 布尔（青色）
- `Null` - 空值（灰色）

### Proto
- `Msg` - 消息定义
- `Enum` - 枚举定义
- `Svc` - 服务定义
- `Fld` - 字段
- `RPC` - RPC方法

## 常见问题

### Q: 打包后的 exe 文件太大？
A: 这是正常的，PyInstaller 会打包 Python 解释器。可以使用虚拟环境减小体积。

### Q: 杀毒软件报警？
A: PyInstaller 打包的程序可能被误报，添加到白名单即可。

### Q: 程序启动慢？
A: 首次启动会解压文件，后续会快很多。

### Q: 中文显示乱码？
A: 运行 `python fix_encoding.py` 修复编码，或检查 VS Code 编码设置。

### Q: 无法生成图标？
A: 需要安装 Pillow: `pip install Pillow`

### Q: exe 运行报错 "AttributeError: 'NoneType' object has no attribute 'encoding'"？
A: 这个问题已修复。在打包后的 exe 中，sys.stdout 可能是 None。重新运行 `python build.py` 打包即可。

### Q: 如何验证 exe 是否正常？
A: 运行 `python verify_exe.py` 进行完整验证测试。

## 开发建议

### 添加新功能
1. 修改 `p_viewer.py`
2. 测试功能
3. 更新版本号
4. 重新打包

### 添加新主题
1. 编辑 `themes.py`
2. 添加新主题配置
3. 在菜单中添加选项

### 支持新格式
1. 在 `detect_file_type()` 中添加检测
2. 实现 `load_xxx_file()` 方法
3. 实现 `refresh_xxx_tree()` 方法
4. 实现 `apply_xxx_highlight()` 方法

## 分发建议

### 单文件分发
- 只需分发 `P-Viewer.exe`
- 适合简单场景

### 完整分发
- 打包 `dist/` 目录为 ZIP
- 包含示例文件和说明
- 适合正式发布

### 建议文件名
```
P-Viewer-v1.0.0-windows-x64.zip
```

## 许可证

MIT License - 可以自由使用、修改和分发

## 作者

Copyright © 2025

---

**P-Viewer** - 让文件查看和编辑更简单 ✨
