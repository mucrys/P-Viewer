#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复文件编码 - 确保所有文件都是 UTF-8"""

import os
import sys

def fix_file_encoding(filename):
    """修复单个文件的编码"""
    if not os.path.exists(filename):
        print(f"  跳过: {filename} (文件不存在)")
        return False
    
    try:
        # 尝试多种编码读取
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig', 'latin-1']
        content = None
        original_encoding = None
        
        for enc in encodings:
            try:
                with open(filename, 'r', encoding=enc) as f:
                    content = f.read()
                    original_encoding = enc
                    break
            except (UnicodeDecodeError, LookupError):
                continue
        
        if content is None:
            print(f"  失败: {filename} (无法识别编码)")
            return False
        
        # 以 UTF-8 重新写入
        with open(filename, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        
        if original_encoding == 'utf-8':
            print(f"  ✓ {filename} (已是 UTF-8)")
        else:
            print(f"  ✓ {filename} (从 {original_encoding} 转换为 UTF-8)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ {filename} (错误: {e})")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("P-Viewer 编码修复工具")
    print("=" * 60)
    print("\n正在修复文件编码为 UTF-8...\n")
    
    # 需要修复的文件列表
    files = [
        'p_viewer.py',
        'themes.py',
        'example.json',
        'example.proto',
        'README.md',
        'BUILD_README.md',
        'build_windows.bat',
        'build_windows_with_icon.bat',
        'create_icon.py',
        'test_encoding.py',
        'diagnose.py'
    ]
    
    success_count = 0
    for filename in files:
        if fix_file_encoding(filename):
            success_count += 1
    
    print(f"\n完成: {success_count}/{len(files)} 个文件处理成功")
    print("\n" + "=" * 60)
    print("建议:")
    print("1. 在 VS Code 中，右下角点击编码，选择 'UTF-8'")
    print("2. 设置 VS Code 默认编码: 文件 -> 首选项 -> 设置")
    print("   搜索 'files.encoding'，设置为 'utf8'")
    print("3. 如果仍有问题，尝试关闭并重新打开文件")
    print("=" * 60)

if __name__ == "__main__":
    main()
