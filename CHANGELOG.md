# 更新日志

所有重要的项目更改都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2025-11-19

### 新增
- ✨ 首次发布
- 📄 支持 JSON 文件查看和编辑
- 📝 支持 Proto 文件查看和编辑
- 🌳 双视图显示（结构树 + 源码编辑器）
- 🎨 语法高亮（JSON 和 Proto）
- 🔍 JSON 语法检查和错误定位
- 🎭 4套主题（GitHub/VS Code 亮暗色）
- ⌨️ 完整的快捷键支持
- 💾 配置持久化（主题和字体大小）
- 📦 Windows exe 打包支持
- 🔧 一键打包脚本（build.py）
- 🎯 图标自动生成
- 📚 完整的文档

### 功能特性

#### JSON 支持
- 树形视图显示 JSON 结构
- 支持对象、数组、字符串、数字、布尔、null
- 彩色类型标签
- 语法错误精确定位（行列号）
- 中文错误提示
- 容错保存（有错误也能保存）

#### Proto 支持
- 结构视图显示 Proto 定义
- 支持 Message、Enum、Service
- 解析字段、枚举值、RPC 方法
- 语法高亮
- 点击节点跳转到源码

#### 编辑功能
- 行号显示
- 撤销/重做（Ctrl+Z/Ctrl+Y）
- 复制/粘贴/剪切
- 全选（Ctrl+A）
- 实时语法高亮
- 自动保存配置

#### 视图功能
- 展开/收起所有节点
- 树节点与源码同步
- 字体缩放（Ctrl+/Ctrl-/Ctrl+0）
- 主题切换
- 滚动同步

#### 主题系统
- GitHub Light - 清爽明亮
- GitHub Dark - 护眼暗色
- VS Code Light - 经典亮色
- VS Code Dark - 专业暗色

### 技术特点
- ⚡ 零依赖 - 仅使用 Python 标准库
- 🚀 轻量级 - 源码约 600 行
- 📦 单文件 - exe 约 11 MB
- 🔧 易打包 - 一键生成 exe
- 🌍 跨平台 - Windows/macOS/Linux

### 工具脚本
- `build.py` - 一键打包脚本
- `create_icon.py` - 图标生成工具
- `diagnose.py` - 编码诊断工具
- `fix_encoding.py` - 编码修复工具
- `verify_exe.py` - exe 验证工具
- `test_encoding.py` - 编码测试脚本

### 文档
- `README.md` - 项目说明
- `BUILD_README.md` - 打包说明
- `SUMMARY.md` - 项目总结
- `QUICKSTART.md` - 快速开始
- `CHECKLIST.md` - 发布检查清单
- `CHANGELOG.md` - 更新日志（本文件）

### 修复
- 🐛 修复打包后 exe 运行时的 stdout 编码错误
- 🐛 修复 Windows 控制台中文显示问题
- 🐛 修复文件编码检测问题

### 已知问题
- Proto 语法检查功能较基础，仅做基本验证
- 大文件（>10MB）加载可能较慢
- 首次启动 exe 需要解压，稍慢

### 系统要求
- Windows 10/11（exe 版本）
- Python 3.7+（源码版本）
- Tkinter（通常已内置）

### 安装
```bash
# 源码运行
python p_viewer.py

# 或使用 exe
下载 P-Viewer.exe 直接运行
```

### 使用
```bash
# 打开程序
python p_viewer.py

# 打开文件
python p_viewer.py example.json
python p_viewer.py example.proto

# 或使用 exe
P-Viewer.exe
P-Viewer.exe example.json
```

---

## 未来计划

### [1.1.0] - 计划中
- [ ] 搜索功能（Ctrl+F）
- [ ] 替换功能（Ctrl+H）
- [ ] 书签功能
- [ ] 最近文件列表
- [ ] 拖拽打开文件
- [ ] 更多主题

### [1.2.0] - 计划中
- [ ] XML 格式支持
- [ ] YAML 格式支持
- [ ] TOML 格式支持
- [ ] 格式转换功能

### [2.0.0] - 远期计划
- [ ] 插件系统
- [ ] 自定义主题
- [ ] 多标签页
- [ ] 文件对比
- [ ] Git 集成

---

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

**P-Viewer** - 持续改进中 ✨
