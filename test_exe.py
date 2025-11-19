#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试打包的 exe 文件"""

import os
import subprocess
import time

def test_exe():
    """测试 exe 文件"""
    exe_path = os.path.join('dist', 'P-Viewer.exe')
    
    if not os.path.exists(exe_path):
        print("✗ 找不到 P-Viewer.exe")
        print("  请先运行 build.py 进行打包")
        return False
    
    print("=" * 60)
    print("测试 P-Viewer.exe")
    print("=" * 60)
    
    # 检查文件大小
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n文件信息:")
    print(f"  路径: {exe_path}")
    print(f"  大小: {size_mb:.2f} MB")
    
    # 测试启动（带示例文件）
    example_json = os.path.join('dist', 'examples', 'example.json')
    
    if os.path.exists(example_json):
        print(f"\n测试启动:")
        print(f"  命令: {exe_path} {example_json}")
        print(f"  提示: 程序窗口将打开，请手动关闭以继续测试")
        
        try:
            # 启动程序（不等待）
            subprocess.Popen([exe_path, example_json])
            print(f"  ✓ 程序已启动")
            print(f"  请检查:")
            print(f"    1. 窗口是否正常显示")
            print(f"    2. 中文是否正常显示")
            print(f"    3. JSON 文件是否正确加载")
            print(f"    4. 树形视图是否显示")
            print(f"    5. 源码编辑器是否显示")
            
        except Exception as e:
            print(f"  ✗ 启动失败: {e}")
            return False
    else:
        print(f"\n⚠ 找不到示例文件: {example_json}")
    
    print("\n" + "=" * 60)
    print("测试说明:")
    print("  如果程序正常启动并显示，说明打包成功")
    print("  如果有问题，请检查:")
    print("    1. 是否缺少依赖文件")
    print("    2. 杀毒软件是否拦截")
    print("    3. 系统是否支持")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    test_exe()
