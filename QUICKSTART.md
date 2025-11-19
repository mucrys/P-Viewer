# P-Viewer 快速开始

## 5分钟上手指南

### 1. 运行源码（开发者）

```bash
# 克隆或下载项目
cd p-viewer

# 直接运行（需要 Python 3.7+）
python p_viewer.py

# 或打开示例文件
python p_viewer.py example.json
```

### 2. 打包为 exe（Windows）

```bash
# 一键打包
python build.py

# 输出文件在 dist 目录
# dist/P-Viewer.exe
```

### 3. 使用 exe

**方式 1: 双击启动**
- 双击 `P-Viewer.exe`
- 通过菜单打开文件

**方式 2: 拖拽打开**
- 将 JSON 或 Proto 文件拖到 `P-Viewer.exe` 图标上

**方式 3: 命令行**
```cmd
P-Viewer.exe example.json
P-Viewer.exe example.proto
```

## 界面说明

```
┌─────────────────────────────────────────────────────────┐
│ 文件  编辑  视图  工具  帮助                              │
├──────────────────┬──────────────────────────────────────┤
│ [展开] [收起]    │ [✓ 语法检查 (F5)]                    │
├──────────────────┼──────────────────────────────────────┤
│ 结构视图         │ 源码编辑器                            │
│                  │                                       │
│ Obj root {3}     │ 1  {                                  │
│   Str name       │ 2      "name": "P-Viewer",           │
│   Str version    │ 3      "version": "1.0.0",           │
│   Arr features   │ 4      "features": [...]             │
│                  │ 5  }                                  │
│                  │                                       │
└──────────────────┴──────────────────────────────────────┘
│ 文件: example.json (JSON) | 行: 2, 列: 15                │
└─────────────────────────────────────────────────────────┘
```

## 常用快捷键

| 功能 | 快捷键 |
|------|--------|
| 打开文件 | `Ctrl+O` |
| 保存文件 | `Ctrl+S` |
| 语法检查 | `F5` |
| 撤销 | `Ctrl+Z` |
| 重做 | `Ctrl+Y` |
| 复制 | `Ctrl+C` |
| 粘贴 | `Ctrl+V` |
| 全选 | `Ctrl+A` |
| 放大字体 | `Ctrl+` |
| 缩小字体 | `Ctrl-` |
| 重置字体 | `Ctrl+0` |

## 支持的文件格式

### JSON
- 树形视图显示结构
- 语法高亮
- 错误精确定位
- 实时编辑

### Proto
- 结构视图（Message/Enum/Service）
- 语法高亮
- 元素解析
- 实时编辑

## 主题切换

**菜单**: 视图 → 主题

- GitHub 亮色（默认）
- GitHub 暗色
- VS Code 亮色
- VS Code 暗色

## 问题排查

### 看到乱码？
```bash
# 运行诊断工具
python diagnose.py

# 修复编码
python fix_encoding.py
```

### exe 无法运行？
```bash
# 验证 exe
python verify_exe.py

# 重新打包
python build.py
```

### 杀毒软件拦截？
- 添加到白名单
- 或从源码运行

## 分发建议

### 单文件分发
只需分发 `P-Viewer.exe`

### 完整分发
打包整个 `dist` 目录为 ZIP：
```
P-Viewer-v1.0.0-windows.zip
├── P-Viewer.exe
├── examples/
│   ├── example.json
│   └── example.proto
├── README.md
└── 使用说明.txt
```

## 更多信息

- 完整文档: [README.md](README.md)
- 打包说明: [BUILD_README.md](BUILD_README.md)
- 项目总结: [SUMMARY.md](SUMMARY.md)

---

**P-Viewer** - 5分钟上手，轻松查看和编辑 JSON/Proto 文件 ✨
