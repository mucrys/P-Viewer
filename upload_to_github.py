#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GitHub 上传助手"""

import subprocess
import sys
import os
import getpass

def run_command(cmd, description="", show_output=True):
    """运行命令"""
    if description:
        print(f"\n{description}")
    
    try:
        if show_output:
            result = subprocess.run(cmd, check=True, shell=True, text=True)
        else:
            result = subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
        return True, result.stdout if not show_output else ""
    except subprocess.CalledProcessError as e:
        print(f"✗ 命令执行失败: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"错误信息: {e.stderr}")
        return False, ""

def main():
    """主函数"""
    print("=" * 70)
    print("P-Viewer GitHub 上传助手")
    print("=" * 70)
    
    # 检查 Git 状态
    print("\n[1] 检查 Git 状态")
    success, output = run_command("git status", show_output=False)
    if not success:
        print("✗ Git 未初始化或不在 Git 仓库中")
        return False
    
    if "nothing to commit" not in output and "working tree clean" not in output:
        print("⚠ 有未提交的更改")
        print(output)
        commit = input("\n是否提交这些更改？(y/n): ").strip().lower()
        if commit == 'y':
            message = input("提交信息: ").strip()
            if not message:
                message = "Update files"
            run_command(f'git add .', "添加所有文件")
            run_command(f'git commit -m "{message}"', "提交更改")
    else:
        print("✓ 工作区干净，已准备好推送")
    
    # 获取用户信息
    print("\n[2] 配置 GitHub 信息")
    print("\n请按照以下步骤操作：")
    print("1. 访问 https://github.com/settings/tokens")
    print("2. 点击 'Generate new token (classic)'")
    print("3. 勾选 'repo' 权限")
    print("4. 生成并复制 token")
    print("\n⚠️ Token 只显示一次，请妥善保存！")
    
    username = input("\n请输入你的 GitHub 用户名: ").strip()
    if not username:
        print("✗ 用户名不能为空")
        return False
    
    token = getpass.getpass("请输入你的 Personal Access Token (输入时不显示): ").strip()
    if not token:
        print("✗ Token 不能为空")
        return False
    
    repo_name = input("\n仓库名称 (默认: P-Viewer): ").strip()
    if not repo_name:
        repo_name = "P-Viewer"
    
    # 检查远程仓库
    print("\n[3] 配置远程仓库")
    success, output = run_command("git remote -v", show_output=False)
    
    if "origin" in output:
        print("⚠ 已存在 origin 远程仓库")
        print(output)
        remove = input("\n是否删除现有配置？(y/n): ").strip().lower()
        if remove == 'y':
            run_command("git remote remove origin", "删除现有远程仓库")
        else:
            print("保留现有配置")
    
    # 添加远程仓库
    remote_url = f"https://{token}@github.com/{username}/{repo_name}.git"
    success, _ = run_command(f'git remote add origin {remote_url}', "添加远程仓库", show_output=False)
    
    if not success:
        print("✗ 添加远程仓库失败")
        print("提示: 请确保在 GitHub 上已创建仓库")
        print(f"仓库地址: https://github.com/{username}/{repo_name}")
        return False
    
    print(f"✓ 已添加远程仓库: https://github.com/{username}/{repo_name}")
    
    # 重命名分支
    print("\n[4] 配置分支")
    run_command("git branch -M main", "重命名分支为 main")
    
    # 推送代码
    print("\n[5] 推送代码到 GitHub")
    print("正在推送，请稍候...")
    
    success, output = run_command("git push -u origin main", show_output=False)
    
    if success:
        print("\n" + "=" * 70)
        print("✓ 上传成功！")
        print("=" * 70)
        print(f"\n仓库地址: https://github.com/{username}/{repo_name}")
        print(f"访问查看: https://github.com/{username}/{repo_name}")
        
        print("\n下一步建议:")
        print("1. 访问仓库页面，检查文件是否完整")
        print("2. 编辑仓库描述")
        print("3. 添加 Topics 标签")
        print("4. 创建 Release 并上传 exe 文件")
        
        # 清理 token（安全考虑）
        print("\n[6] 清理敏感信息")
        clean = input("\n是否从 Git 配置中移除 token？(推荐 y): ").strip().lower()
        if clean == 'y' or clean == '':
            # 更新为不含 token 的 URL
            clean_url = f"https://github.com/{username}/{repo_name}.git"
            run_command(f"git remote set-url origin {clean_url}", "更新远程仓库 URL", show_output=False)
            print("✓ 已移除 token，后续推送需要重新输入凭据")
        
        print("\n" + "=" * 70)
        return True
    else:
        print("\n✗ 推送失败")
        print("\n可能的原因:")
        print("1. Token 权限不足（需要 'repo' 权限）")
        print("2. 仓库不存在（需要先在 GitHub 上创建）")
        print("3. Token 已过期")
        print("4. 网络连接问题")
        
        print("\n请检查并重试")
        print(f"仓库地址: https://github.com/{username}/{repo_name}")
        
        # 清理失败的配置
        run_command("git remote remove origin", show_output=False)
        return False

if __name__ == "__main__":
    try:
        print("\n⚠️ 注意事项:")
        print("1. 请确保已在 GitHub 上创建仓库")
        print("2. 请准备好 Personal Access Token")
        print("3. Token 需要有 'repo' 权限")
        
        proceed = input("\n准备好了吗？(y/n): ").strip().lower()
        if proceed != 'y':
            print("\n已取消")
            sys.exit(0)
        
        success = main()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
