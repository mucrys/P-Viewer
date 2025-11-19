# P-Viewer

程序员专用文件查看和编辑工具，轻量级，零依赖。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ 特性

### 支持格式
- 📄 **JSON** - 树形视图 + 语法高亮 + 错误定位
- 📝 **Proto** - 结构视图 + 语法高亮 + 元素解析

### 核心功能
- 🌳 **双视图显示** - 结构视图 + 源码视图，实时同步
- 🎨 **语法高亮** - JSON/Proto 语法着色
- ✏️ **源码编辑** - 行号、完整编辑功能
- 🔍 **语法检查** - JSON 错误精确定位
- 💾 **智能保存** - 容错保存
- 🎭 **主题切换** - 4套主题（GitHub/VS Code 亮暗色）

### 用户体验
- ⚡ **零依赖** - 仅使用 Python 标准库
- 🚀 **快速启动** - 单文件架构
- 💾 **配置持久化** - 自动保存主题和字体设置
- ⌨️ **快捷键** - 完整的快捷键支持

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Tkinter（Python GUI 库）
  - **Windows**: 自带，无需安装
  - **macOS**: 自带，无需安装
  - **Linux**: 需要安装 `python3-tk`

### 运行

```bash
# 直接运行
python p_viewer.py

# 打开指定文件
python p_viewer.py example.json
python p_viewer.py example.proto
```

## 📖 使用说明

### 文件操作
- **打开文件**: `Ctrl+O` 或 文件 → 打开
- **保存文件**: `Ctrl+S` 或 文件 → 保存
- **另存为**: 文件 → 另存为

### 编辑操作
- **撤销/重做**: `Ctrl+Z` / `Ctrl+Y`
- **复制/粘贴/剪切**: `Ctrl+C` / `Ctrl+V` / `Ctrl+X`
- **全选**: `Ctrl+A`

### 视图操作
- **语法检查**: `F5` 或点击工具栏按钮
- **展开/收起全部**: 点击结构视图工具栏按钮
- **双视图同步**: 点击结构节点自动跳转到源码

### 主题和字体
- **切换主题**: 视图 → 主题
- **字体缩放**: `Ctrl+` / `Ctrl-` / `Ctrl+0`（重置）

## 🎨 数据类型标签

### JSON
| 类型 | 标签 | 颜色 |
|------|------|------|
| 对象 | `Obj` | 🔵 蓝色 |
| 数组 | `Arr` | 🟢 绿色 |
| 字符串 | `Str` | 🟠 橙色 |
| 数字 | `Num` | 🟣 紫色 |
| 布尔 | `Bool` | 🔷 青色 |
| 空值 | `Null` | ⚪ 灰色 |

### Proto
| 类型 | 标签 | 说明 |
|------|------|------|
| Message | `Msg` | 消息定义 |
| Enum | `Enum` | 枚举定义 |
| Service | `Svc` | 服务定义 |
| Field | `Fld` | 字段 |
| RPC | `RPC` | RPC方法 |

## 🎭 主题

- **GitHub 亮色** - 清爽明亮
- **GitHub 暗色** - 护眼暗色
- **VS Code 亮色** - 经典亮色
- **VS Code 暗色** - 专业暗色

## ⚙️ 配置

配置文件自动保存到：`~/.p_viewer_config.json`

包含：
- 主题设置
- 字体大小

## 🔧 技术栈

- **语言**: Python 3.7+
- **GUI**: Tkinter（标准库）
- **依赖**: 零第三方依赖
- **架构**: 双文件（主程序 + 主题配置）
- **代码量**: ~600 行

## 📦 项目结构

```
p-viewer/
├── p_viewer.py          # 主程序
├── themes.py            # 主题配置
├── example.json         # JSON示例文件
├── example.proto        # Proto示例文件
└── README.md            # 项目说明
```

## 🎯 性能指标

- 启动时间: < 2秒
- 文件加载: < 2秒（1MB）
- 双视图同步: < 100ms
- 语法高亮渲染: < 500ms
- 内存占用: < 100MB

## 📄 许可证

MIT License

Copyright © 2025

---

**P-Viewer** - 让文件查看和编辑更简单 ✨
