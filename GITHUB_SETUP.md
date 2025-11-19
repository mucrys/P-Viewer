# GitHub 上传指南

## 步骤 1: 创建 GitHub Personal Access Token

1. 登录 GitHub: https://github.com
2. 点击右上角头像 → **Settings**
3. 左侧菜单最下方 → **Developer settings**
4. 左侧菜单 → **Personal access tokens** → **Tokens (classic)**
5. 点击 **Generate new token** → **Generate new token (classic)**
6. 填写信息：
   - **Note**: `P-Viewer Upload` (备注名称)
   - **Expiration**: 选择过期时间（建议 30 days 或 90 days）
   - **Select scopes**: 勾选 `repo` (完整的仓库访问权限)
7. 点击页面底部 **Generate token**
8. **重要**: 复制生成的 token（形如 `ghp_xxxxxxxxxxxx`）
   - ⚠️ 这个 token 只显示一次，请立即保存！

## 步骤 2: 在 GitHub 上创建新仓库

1. 访问: https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `P-Viewer`
   - **Description**: `程序员专用文件查看和编辑工具 - 支持 JSON 和 Proto 格式`
   - **Public** 或 **Private**: 选择公开或私有
   - ⚠️ **不要勾选** "Add a README file"
   - ⚠️ **不要勾选** "Add .gitignore"
   - ⚠️ **不要勾选** "Choose a license"
3. 点击 **Create repository**
4. 记下仓库 URL（形如 `https://github.com/你的用户名/P-Viewer.git`）

## 步骤 3: 配置本地仓库并推送

### 方式 A: 使用命令行（推荐）

在项目目录下运行以下命令：

```bash
# 1. 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/P-Viewer.git

# 2. 重命名分支为 main（GitHub 默认）
git branch -M main

# 3. 推送代码（会提示输入用户名和密码）
git push -u origin main
```

**输入凭据时：**
- Username: 你的 GitHub 用户名
- Password: 粘贴刚才复制的 Personal Access Token（不是你的 GitHub 密码！）

### 方式 B: 使用 Token 直接推送

```bash
# 1. 添加远程仓库（包含 token，替换 TOKEN 和 USERNAME）
git remote add origin https://TOKEN@github.com/USERNAME/P-Viewer.git

# 2. 重命名分支
git branch -M main

# 3. 推送
git push -u origin main
```

**示例**（替换实际值）：
```bash
git remote add origin https://ghp_xxxxxxxxxxxx@github.com/yourname/P-Viewer.git
git branch -M main
git push -u origin main
```

## 步骤 4: 验证上传

1. 访问你的仓库页面: `https://github.com/你的用户名/P-Viewer`
2. 检查文件是否都已上传
3. 检查 README.md 是否正确显示

## 步骤 5: 创建 Release（可选）

1. 在仓库页面，点击右侧 **Releases**
2. 点击 **Create a new release**
3. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `P-Viewer v1.0.0`
   - **Description**: 复制 CHANGELOG.md 中的内容
4. 上传 exe 文件：
   - 将 `dist/P-Viewer.exe` 拖到 "Attach binaries" 区域
   - 或打包为 ZIP 后上传
5. 点击 **Publish release**

## 常见问题

### Q: 推送时提示 "Authentication failed"
A: 
- 确认 token 是否正确复制（包含 `ghp_` 前缀）
- 确认 token 是否已过期
- 确认 token 权限包含 `repo`

### Q: 推送时提示 "remote: Repository not found"
A:
- 确认仓库名称拼写正确
- 确认仓库 URL 正确
- 确认你有该仓库的访问权限

### Q: 如何更新代码？
A:
```bash
# 1. 修改代码后
git add .
git commit -m "更新说明"
git push
```

### Q: 如何删除远程仓库配置？
A:
```bash
git remote remove origin
```

### Q: Token 泄露了怎么办？
A:
1. 立即到 GitHub Settings → Developer settings → Personal access tokens
2. 找到泄露的 token，点击 **Delete**
3. 重新生成新的 token

## 安全建议

1. ⚠️ **不要将 token 提交到代码中**
2. ⚠️ **不要在公开场合分享 token**
3. ⚠️ **定期更换 token**
4. ⚠️ **使用完毕后可以删除 token**

## 下一步

上传成功后，你可以：

1. 编辑仓库描述和标签
2. 添加 Topics（如 `json`, `proto`, `viewer`, `editor`, `python`, `tkinter`）
3. 创建 Release 并上传 exe 文件
4. 添加 GitHub Actions（自动化构建）
5. 邀请协作者

---

**准备好了吗？开始上传吧！** 🚀
