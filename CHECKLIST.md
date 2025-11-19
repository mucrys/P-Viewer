# P-Viewer 发布检查清单

## 打包前检查

- [ ] 所有文件编码为 UTF-8
  ```bash
  python fix_encoding.py
  ```

- [ ] 代码无语法错误
  ```bash
  python -m py_compile p_viewer.py
  python -m py_compile themes.py
  ```

- [ ] 源码可以正常运行
  ```bash
  python p_viewer.py example.json
  python p_viewer.py example.proto
  ```

- [ ] 版本号已更新
  - [ ] `p_viewer.py` 中的 `self.version`
  - [ ] `README.md` 中的版本号
  - [ ] `SUMMARY.md` 中的版本号

## 打包检查

- [ ] PyInstaller 已安装
  ```bash
  pip show pyinstaller
  ```

- [ ] 图标文件存在（可选）
  ```bash
  python create_icon.py
  ```

- [ ] 执行打包
  ```bash
  python build.py
  ```

- [ ] 打包成功
  - [ ] 无错误信息
  - [ ] `dist/P-Viewer.exe` 存在
  - [ ] 文件大小合理（~10-15 MB）

## 功能测试

- [ ] exe 可以启动（无参数）
  ```bash
  .\dist\P-Viewer.exe
  ```

- [ ] 打开 JSON 文件
  ```bash
  .\dist\P-Viewer.exe .\dist\examples\example.json
  ```
  - [ ] 树形视图正常显示
  - [ ] 源码编辑器正常显示
  - [ ] 语法高亮正常
  - [ ] 中文显示正常

- [ ] 打开 Proto 文件
  ```bash
  .\dist\P-Viewer.exe .\dist\examples\example.proto
  ```
  - [ ] 结构视图正常显示
  - [ ] 源码编辑器正常显示
  - [ ] 语法高亮正常
  - [ ] 中文显示正常

- [ ] 编辑功能
  - [ ] 可以编辑文本
  - [ ] 撤销/重做正常
  - [ ] 复制/粘贴正常
  - [ ] 保存功能正常

- [ ] 视图功能
  - [ ] 展开/收起节点正常
  - [ ] 点击节点跳转正常
  - [ ] 语法检查正常（F5）

- [ ] 主题切换
  - [ ] GitHub 亮色
  - [ ] GitHub 暗色
  - [ ] VS Code 亮色
  - [ ] VS Code 暗色

- [ ] 字体缩放
  - [ ] Ctrl+ 放大
  - [ ] Ctrl- 缩小
  - [ ] Ctrl+0 重置

## 文件检查

- [ ] 必需文件存在
  - [ ] `dist/P-Viewer.exe`
  - [ ] `dist/examples/example.json`
  - [ ] `dist/examples/example.proto`
  - [ ] `dist/README.md`
  - [ ] `dist/使用说明.txt`

- [ ] 文档完整
  - [ ] README.md
  - [ ] BUILD_README.md
  - [ ] SUMMARY.md
  - [ ] QUICKSTART.md
  - [ ] CHECKLIST.md（本文件）

## 兼容性测试

- [ ] Windows 10
- [ ] Windows 11
- [ ] 不同分辨率
  - [ ] 1920x1080
  - [ ] 1366x768
  - [ ] 2560x1440

- [ ] 不同 DPI 设置
  - [ ] 100%
  - [ ] 125%
  - [ ] 150%

## 安全检查

- [ ] 杀毒软件扫描
  - [ ] Windows Defender
  - [ ] 其他杀毒软件

- [ ] 数字签名（可选）
  - [ ] 代码签名证书
  - [ ] 签名验证

## 性能测试

- [ ] 启动时间 < 3秒
- [ ] 打开小文件 (< 100KB) < 1秒
- [ ] 打开中等文件 (100KB - 1MB) < 3秒
- [ ] 打开大文件 (1MB - 10MB) < 10秒
- [ ] 内存占用 < 150MB

## 分发准备

- [ ] 创建发布包
  ```
  P-Viewer-v1.0.0-windows-x64.zip
  ├── P-Viewer.exe
  ├── examples/
  │   ├── example.json
  │   └── example.proto
  ├── README.md
  └── 使用说明.txt
  ```

- [ ] 压缩包测试
  - [ ] 解压正常
  - [ ] 文件完整
  - [ ] 可以运行

- [ ] 发布说明
  - [ ] 版本号
  - [ ] 更新内容
  - [ ] 已知问题
  - [ ] 系统要求

## Git 提交

- [ ] 提交所有更改
  ```bash
  git add .
  git commit -m "Release v1.0.0"
  ```

- [ ] 创建标签
  ```bash
  git tag v1.0.0
  git push origin v1.0.0
  ```

## 发布

- [ ] 上传到 GitHub Releases
  - [ ] 发布说明
  - [ ] 附件（ZIP）
  - [ ] 截图

- [ ] 更新文档
  - [ ] 下载链接
  - [ ] 安装说明
  - [ ] 更新日志

## 后续支持

- [ ] 监控问题反馈
- [ ] 准备修复补丁
- [ ] 规划下一版本

---

## 快速验证命令

```bash
# 完整验证流程
python fix_encoding.py      # 修复编码
python build.py              # 打包
python verify_exe.py         # 验证
```

## 问题排查

如果遇到问题：

1. **编码问题**
   ```bash
   python diagnose.py
   python fix_encoding.py
   ```

2. **打包失败**
   - 检查 PyInstaller 版本
   - 清理 build/dist 目录
   - 查看错误日志

3. **运行异常**
   - 检查依赖文件
   - 查看错误信息
   - 尝试从源码运行

---

**检查完成后，即可发布！** ✨
