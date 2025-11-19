#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P-Viewer 打包脚本"""

import os
import sys
import shutil
import subprocess

def print_step(step, total, message):
    """打印步骤信息"""
    print(f"\n[{step}/{total}] {message}")
    print("=" * 60)

def run_command(cmd, description):
    """运行命令"""
    print(f"执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if e.stdout:
            print(f"输出: {e.stdout}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"异常: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("P-Viewer Windows 打包工具")
    print("=" * 60)
    
    # 步骤 1: 检查 PyInstaller
    print_step(1, 5, "检查 PyInstaller")
    try:
        import PyInstaller
        print(f"✓ PyInstaller 已安装 (版本: {PyInstaller.__version__})")
    except ImportError:
        print("PyInstaller 未安装，正在安装...")
        if not run_command([sys.executable, "-m", "pip", "install", "pyinstaller"], "安装 PyInstaller"):
            print("✗ 安装失败")
            return False
        print("✓ PyInstaller 安装成功")
    
    # 步骤 2: 清理旧文件
    print_step(2, 5, "清理旧文件")
    dirs_to_clean = ['build', 'dist']
    files_to_clean = ['P-Viewer.spec']
    
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"✓ 已删除目录: {d}")
    
    for f in files_to_clean:
        if os.path.exists(f):
            os.remove(f)
            print(f"✓ 已删除文件: {f}")
    
    # 步骤 3: 生成图标（可选）
    print_step(3, 5, "生成图标")
    icon_param = "--icon=NONE"
    if not os.path.exists('icon.ico'):
        print("尝试生成图标...")
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            size = 256
            img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            margin = 20
            draw.ellipse([margin, margin, size-margin, size-margin], 
                        fill='#0078d4', outline='#005a9e', width=4)
            
            try:
                font = ImageFont.truetype("arial.ttf", 140)
            except:
                font = ImageFont.load_default()
            
            text = "P"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (size - text_width) // 2
            y = (size - text_height) // 2 - 10
            
            draw.text((x, y), text, fill='white', font=font)
            
            sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
            icons = [img.resize(s, Image.Resampling.LANCZOS) for s in sizes]
            icons[0].save('icon.ico', format='ICO', sizes=[(s[0], s[1]) for s in sizes])
            
            print("✓ 图标生成成功: icon.ico")
            icon_param = "--icon=icon.ico"
        except ImportError:
            print("⚠ Pillow 未安装，跳过图标生成")
            print("  提示: pip install Pillow")
        except Exception as e:
            print(f"⚠ 图标生成失败: {e}")
    else:
        print("✓ 使用现有图标: icon.ico")
        icon_param = "--icon=icon.ico"
    
    # 步骤 4: 打包
    print_step(4, 5, "开始打包")
    print("这可能需要几分钟时间，请耐心等待...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=P-Viewer",
        "--onefile",
        "--windowed",
        "--add-data", f"themes.py{os.pathsep}.",
        icon_param,
        "--clean",
        "--noupx",
        "p_viewer.py"
    ]
    
    if not run_command(cmd, "打包程序"):
        print("✗ 打包失败")
        return False
    
    print("✓ 打包成功")
    
    # 步骤 5: 整理输出
    print_step(5, 5, "整理输出文件")
    
    # 创建示例目录
    examples_dir = os.path.join('dist', 'examples')
    if not os.path.exists(examples_dir):
        os.makedirs(examples_dir)
        print(f"✓ 创建目录: {examples_dir}")
    
    # 复制文件
    files_to_copy = [
        ('example.json', examples_dir),
        ('example.proto', examples_dir),
        ('README.md', 'dist')
    ]
    
    for src, dst_dir in files_to_copy:
        if os.path.exists(src):
            dst = os.path.join(dst_dir, os.path.basename(src))
            shutil.copy2(src, dst)
            print(f"✓ 复制: {src} -> {dst}")
    
    # 创建使用说明
    usage_file = os.path.join('dist', '使用说明.txt')
    with open(usage_file, 'w', encoding='utf-8') as f:
        f.write("P-Viewer 使用说明\n")
        f.write("=" * 50 + "\n\n")
        f.write("使用方法:\n")
        f.write("1. 双击 P-Viewer.exe 启动程序\n")
        f.write("2. 拖拽 JSON/Proto 文件到 P-Viewer.exe 图标上打开\n")
        f.write("3. 命令行运行: P-Viewer.exe 文件路径\n\n")
        f.write("示例文件:\n")
        f.write("- examples/example.json\n")
        f.write("- examples/example.proto\n\n")
        f.write("支持格式:\n")
        f.write("- JSON 文件 (.json)\n")
        f.write("- Proto 文件 (.proto)\n\n")
        f.write("更多信息请查看 README.md\n")
    print(f"✓ 创建: {usage_file}")
    
    # 显示结果
    print("\n" + "=" * 60)
    print("打包完成！")
    print("=" * 60)
    
    exe_path = os.path.join('dist', 'P-Viewer.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\n可执行文件: {exe_path}")
        print(f"文件大小: {size_mb:.2f} MB")
    
    print(f"\n输出目录: dist/")
    print("  ├── P-Viewer.exe")
    print("  ├── examples/")
    print("  │   ├── example.json")
    print("  │   └── example.proto")
    print("  ├── README.md")
    print("  └── 使用说明.txt")
    
    print("\n使用方法:")
    print("  1. 双击 P-Viewer.exe 启动")
    print("  2. 拖拽文件到图标上打开")
    print("  3. 命令行: P-Viewer.exe example.json")
    
    print("\n" + "=" * 60)
    return True

if __name__ == "__main__":
    try:
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
