#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证打包的 exe 文件"""

import os
import sys
import subprocess
import time

def verify_exe():
    """验证 exe 文件"""
    print("=" * 70)
    print("P-Viewer.exe 验证工具")
    print("=" * 70)
    
    exe_path = os.path.join('dist', 'P-Viewer.exe')
    
    # 检查文件是否存在
    print("\n[1] 检查文件")
    if not os.path.exists(exe_path):
        print(f"  ✗ 找不到: {exe_path}")
        print("  请先运行: python build.py")
        return False
    
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"  ✓ 文件存在: {exe_path}")
    print(f"  ✓ 文件大小: {size_mb:.2f} MB")
    
    # 检查示例文件
    print("\n[2] 检查示例文件")
    example_files = [
        os.path.join('dist', 'examples', 'example.json'),
        os.path.join('dist', 'examples', 'example.proto'),
        os.path.join('dist', 'README.md'),
        os.path.join('dist', '使用说明.txt')
    ]
    
    all_exist = True
    for f in example_files:
        if os.path.exists(f):
            print(f"  ✓ {f}")
        else:
            print(f"  ✗ {f}")
            all_exist = False
    
    if not all_exist:
        print("  ⚠ 部分文件缺失，但不影响程序运行")
    
    # 测试启动（无参数）
    print("\n[3] 测试启动（无参数）")
    print("  命令: P-Viewer.exe")
    print("  说明: 程序应该打开空白窗口")
    
    try:
        # 启动程序
        proc = subprocess.Popen(
            [exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd='dist'
        )
        
        # 等待一下看是否立即崩溃
        time.sleep(2)
        
        # 检查进程是否还在运行
        if proc.poll() is None:
            print("  ✓ 程序已启动（进程运行中）")
            print("  提示: 请手动检查窗口是否正常显示")
            print("        检查完毕后请关闭窗口")
            
            # 等待用户关闭
            print("\n  等待用户关闭窗口...")
            try:
                proc.wait(timeout=30)
                print("  ✓ 程序已正常关闭")
            except subprocess.TimeoutExpired:
                print("  ⚠ 程序仍在运行（超时30秒）")
                print("  提示: 请手动关闭窗口")
                proc.terminate()
                time.sleep(1)
                if proc.poll() is None:
                    proc.kill()
        else:
            # 进程已退出，检查返回码
            returncode = proc.returncode
            stdout, stderr = proc.communicate()
            
            if returncode == 0:
                print("  ⚠ 程序立即退出（返回码: 0）")
                print("  这可能是正常的，也可能表示有问题")
            else:
                print(f"  ✗ 程序异常退出（返回码: {returncode}）")
                if stderr:
                    print(f"  错误信息: {stderr.decode('utf-8', errors='ignore')}")
                return False
    
    except Exception as e:
        print(f"  ✗ 启动失败: {e}")
        return False
    
    # 测试启动（带 JSON 文件）
    print("\n[4] 测试启动（带 JSON 文件）")
    json_file = os.path.join('dist', 'examples', 'example.json')
    
    if os.path.exists(json_file):
        print(f"  命令: P-Viewer.exe examples\\example.json")
        print("  说明: 程序应该打开并显示 JSON 内容")
        
        try:
            proc = subprocess.Popen(
                [exe_path, 'examples\\example.json'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd='dist'
            )
            
            time.sleep(2)
            
            if proc.poll() is None:
                print("  ✓ 程序已启动")
                print("  提示: 请检查:")
                print("        1. JSON 文件是否正确加载")
                print("        2. 树形视图是否显示")
                print("        3. 源码编辑器是否显示")
                print("        4. 中文是否正常显示")
                
                print("\n  等待用户关闭窗口...")
                try:
                    proc.wait(timeout=30)
                    print("  ✓ 程序已正常关闭")
                except subprocess.TimeoutExpired:
                    print("  ⚠ 程序仍在运行（超时30秒）")
                    proc.terminate()
                    time.sleep(1)
                    if proc.poll() is None:
                        proc.kill()
            else:
                returncode = proc.returncode
                if returncode != 0:
                    stdout, stderr = proc.communicate()
                    print(f"  ✗ 程序异常退出（返回码: {returncode}）")
                    if stderr:
                        print(f"  错误信息: {stderr.decode('utf-8', errors='ignore')}")
                    return False
        
        except Exception as e:
            print(f"  ✗ 启动失败: {e}")
            return False
    else:
        print(f"  ⚠ 找不到示例文件: {json_file}")
    
    # 总结
    print("\n" + "=" * 70)
    print("验证完成")
    print("=" * 70)
    print("\n如果程序能正常启动并显示，说明打包成功！")
    print("\n可能的问题:")
    print("  1. 如果看到乱码 -> 检查系统字体")
    print("  2. 如果无法启动 -> 检查杀毒软件")
    print("  3. 如果功能异常 -> 查看错误信息")
    print("\n分发建议:")
    print("  1. 将 dist 目录打包为 ZIP")
    print("  2. 或只分发 P-Viewer.exe")
    print("  3. 建议包含示例文件和说明")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    try:
        verify_exe()
    except KeyboardInterrupt:
        print("\n\n用户中断")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        import traceback
        traceback.print_exc()
