#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试编码"""

import sys
import os

print("=" * 50)
print("编码测试")
print("=" * 50)

# 测试系统编码
print(f"系统默认编码: {sys.getdefaultencoding()}")
print(f"文件系统编码: {sys.getfilesystemencoding()}")
print(f"标准输出编码: {sys.stdout.encoding}")

# 测试中文字符串
test_str = "这是中文测试 - P-Viewer"
print(f"\n测试字符串: {test_str}")

# 测试文件读取
print("\n测试读取 example.json:")
try:
    with open('example.json', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"文件大小: {len(content)} 字符")
        print(f"前100个字符: {content[:100]}")
except Exception as e:
    print(f"错误: {e}")

# 测试 tkinter 中文
print("\n测试 Tkinter 中文支持:")
try:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 测试标题
    root.title("测试中文标题")
    
    # 测试标签
    label = tk.Label(root, text="这是中文标签")
    
    print("✓ Tkinter 中文支持正常")
    root.destroy()
except Exception as e:
    print(f"✗ Tkinter 中文支持异常: {e}")

print("\n" + "=" * 50)
print("测试完成")
print("=" * 50)
