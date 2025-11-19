#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建 P-Viewer 图标
"""

import os

def create_icon():
    """创建简单的 ICO 图标"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建 256x256 的图像
        size = 256
        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制圆形背景
        margin = 20
        draw.ellipse([margin, margin, size-margin, size-margin], 
                     fill='#0078d4', outline='#005a9e', width=4)
        
        # 绘制文字 "P"
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
        
        # 保存为 PNG
        img.save('icon.png', 'PNG')
        print("✓ 已创建 icon.png")
        
        # 尝试转换为 ICO
        try:
            # 创建多个尺寸
            sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
            icons = []
            for s in sizes:
                icons.append(img.resize(s, Image.Resampling.LANCZOS))
            
            # 保存为 ICO
            icons[0].save('icon.ico', format='ICO', sizes=[(s[0], s[1]) for s in sizes])
            print("✓ 已创建 icon.ico")
            return True
        except Exception as e:
            print(f"⚠ 无法创建 ICO 文件: {e}")
            print("  提示: 需要安装 Pillow 库")
            return False
            
    except ImportError:
        print("⚠ 未安装 Pillow 库，无法创建图标")
        print("  安装命令: pip install Pillow")
        return False

if __name__ == "__main__":
    print("P-Viewer 图标生成工具")
    print("=" * 40)
    create_icon()
