#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断工具 - 检查编码问题"""

import sys
import os
import tkinter as tk
from tkinter import ttk

def diagnose():
    """运行诊断"""
    print("=" * 60)
    print("P-Viewer 编码诊断工具")
    print("=" * 60)
    
    # 1. 系统信息
    print("\n[1] 系统信息:")
    print(f"  操作系统: {sys.platform}")
    print(f"  Python 版本: {sys.version}")
    print(f"  默认编码: {sys.getdefaultencoding()}")
    print(f"  文件系统编码: {sys.getfilesystemencoding()}")
    print(f"  标准输出编码: {sys.stdout.encoding}")
    
    # 2. 文件检查
    print("\n[2] 文件检查:")
    files = ['p_viewer.py', 'themes.py', 'example.json', 'example.proto']
    for filename in files:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read(100)
                    print(f"  ✓ {filename} - UTF-8 读取成功")
            except UnicodeDecodeError:
                print(f"  ✗ {filename} - UTF-8 读取失败，可能不是 UTF-8 编码")
        else:
            print(f"  ? {filename} - 文件不存在")
    
    # 3. Tkinter 测试
    print("\n[3] Tkinter 中文测试:")
    try:
        root = tk.Tk()
        root.title("P-Viewer 诊断 - 中文测试")
        root.geometry("500x400")
        
        # 创建测试界面
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="中文显示测试", font=('Arial', 16, 'bold')).pack(pady=10)
        
        test_texts = [
            "1. 简体中文: 程序员专用文件查看工具",
            "2. 标点符号: ，。！？；：""''",
            "3. 数字混合: P-Viewer V1.0.0",
            "4. 特殊字符: ✓ ✗ → ← ↑ ↓",
            "5. JSON 关键字: 对象 数组 字符串 数字 布尔 空值",
            "6. Proto 关键字: 消息 枚举 服务 字段 方法"
        ]
        
        for text in test_texts:
            ttk.Label(frame, text=text, font=('Courier', 10)).pack(anchor=tk.W, pady=2)
        
        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        result_label = ttk.Label(frame, 
            text="如果上面的中文都能正常显示，说明编码没有问题。\n如果显示为乱码或方框，请检查系统字体设置。",
            font=('Arial', 9),
            foreground='blue')
        result_label.pack(pady=10)
        
        ttk.Button(frame, text="关闭", command=root.destroy).pack(pady=10)
        
        print("  ✓ Tkinter 窗口已打开，请检查中文显示")
        print("  提示: 如果看到乱码，可能是字体问题")
        
        root.mainloop()
        
    except Exception as e:
        print(f"  ✗ Tkinter 测试失败: {e}")
    
    # 4. 建议
    print("\n[4] 诊断建议:")
    print("  如果看到乱码，可能的原因:")
    print("  1. 编辑器编码设置不是 UTF-8")
    print("  2. Windows 控制台代码页不是 65001 (UTF-8)")
    print("  3. 系统缺少中文字体")
    print("  4. 文件保存时使用了错误的编码")
    
    print("\n  解决方法:")
    print("  1. VS Code: 右下角点击编码 -> 选择 'UTF-8'")
    print("  2. 控制台: 运行 'chcp 65001' 切换到 UTF-8")
    print("  3. 安装中文字体包")
    print("  4. 重新保存文件为 UTF-8 编码")
    
    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)

if __name__ == "__main__":
    diagnose()
