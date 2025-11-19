#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
P-Viewer - 程序员专用文件查看和编辑工具

支持格式: JSON, Proto
版本: V1.0.0
许可: MIT License
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import json
import sys
import os
import re

# 设置默认编码（处理打包后的情况）
if sys.platform == 'win32':
    import locale
    # 在打包后的 exe 中，stdout 可能是 None
    if sys.stdout is not None and hasattr(sys.stdout, 'encoding') and sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    if sys.stderr is not None and hasattr(sys.stderr, 'encoding') and sys.stderr.encoding != 'utf-8':
        try:
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass

from themes import get_theme


class PViewer:
    """P-Viewer 主类"""
    
    def __init__(self, root, file_path=None):
        """初始化"""
        self.root = root
        self.root.title("P-Viewer V1.0.0")
        self.root.geometry("1200x800")
        
        # 版本信息
        self.version = "V1.0.0"
        
        # 数据和状态
        self.current_file = file_path
        self.file_type = None  # 'json' or 'proto'
        self.json_data = None
        self.proto_content = ""
        self.modified = False
        self.syntax_error_msg = None
        
        # 配置
        self.current_theme = 'github_light'
        self.font_size = 10
        self.config_file = os.path.expanduser('~/.p_viewer_config.json')
        
        # 加载配置
        self.load_config()
        
        # 双视图同步映射
        self.node_to_position = {}
        self.position_to_node = {}
        self.node_to_line = {}
        
        # 防抖定时器
        self.sync_timer = None
        
        # 创建UI
        self.setup_menu()
        self.setup_ui()
        
        # 延迟加载文件
        if file_path and os.path.exists(file_path):
            self.root.after(100, lambda: self.load_file(file_path))
        
        # 应用主题
        self.root.after(200, lambda: self.apply_theme(self.current_theme))
    
    def setup_menu(self):
        """设置菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="保存", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="另存为...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.quit_app)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="撤销", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="重做", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="剪切", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="复制", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="粘贴", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_command(label="全选", command=self.select_all, accelerator="Ctrl+A")
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        
        # 主题子菜单
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="主题", menu=theme_menu)
        theme_menu.add_command(label="GitHub 亮色", command=lambda: self.apply_theme('github_light'))
        theme_menu.add_command(label="GitHub 暗色", command=lambda: self.apply_theme('github_dark'))
        theme_menu.add_command(label="VS Code 亮色", command=lambda: self.apply_theme('vscode_light'))
        theme_menu.add_command(label="VS Code 暗色", command=lambda: self.apply_theme('vscode_dark'))
        
        view_menu.add_separator()
        view_menu.add_command(label="放大", command=lambda: self.zoom_font(1), accelerator="Ctrl++")
        view_menu.add_command(label="缩小", command=lambda: self.zoom_font(-1), accelerator="Ctrl+-")
        view_menu.add_command(label="重置大小", command=self.reset_font, accelerator="Ctrl+0")
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="语法检查", command=self.check_syntax, accelerator="F5")
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
        
        # 绑定快捷键
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-plus>', lambda e: self.zoom_font(1))
        self.root.bind('<Control-equal>', lambda e: self.zoom_font(1))
        self.root.bind('<Control-minus>', lambda e: self.zoom_font(-1))
        self.root.bind('<Control-0>', lambda e: self.reset_font())
        self.root.bind('<F5>', lambda e: self.check_syntax())
    
    def setup_ui(self):
        """设置UI布局"""
        # 状态栏
        self.status_bar = tk.Label(
            self.root,
            text="就绪",
            anchor=tk.W,
            font=('Arial', 11),
            padx=8,
            pady=4
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 主分割窗口
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashwidth=5)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧：结构视图
        tree_frame = tk.Frame(paned)
        paned.add(tree_frame, width=400)
        
        # 工具栏
        tree_toolbar = tk.Frame(tree_frame, height=35)
        tree_toolbar.pack(side=tk.TOP, fill=tk.X)
        tree_toolbar.pack_propagate(False)
        
        tk.Button(
            tree_toolbar,
            text="展开全部",
            command=self.expand_all,
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(
            tree_toolbar,
            text="收起全部",
            command=self.collapse_all,
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 结构树
        self.tree = ttk.Treeview(tree_frame, show='tree')
        tree_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 配置树形视图字体
        self.tree_font = font.Font(family='Courier', size=self.font_size)
        self.tree_style = ttk.Style()
        self.tree_style.configure('Treeview', 
                                   font=self.tree_font,
                                   rowheight=int(self.font_size * 2))
        
        # 绑定事件
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # 右侧：源码编辑器
        editor_frame = tk.Frame(paned)
        paned.add(editor_frame)
        
        # 编辑器工具栏
        editor_toolbar = tk.Frame(editor_frame, height=35)
        editor_toolbar.pack(side=tk.TOP, fill=tk.X)
        editor_toolbar.pack_propagate(False)
        
        tk.Button(
            editor_toolbar,
            text="✓ 语法检查 (F5)",
            command=self.check_syntax,
            relief=tk.FLAT,
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=5, pady=5)
        
        # 编辑器容器
        editor_container = tk.Frame(editor_frame)
        editor_container.pack(fill=tk.BOTH, expand=True)
        
        # 行号
        self.line_numbers = tk.Text(
            editor_container,
            width=5,
            font=('Courier', self.font_size),
            bg='#f6f8fa',
            fg='#57606a',
            state='disabled',
            borderwidth=0,
            highlightthickness=0,
            takefocus=0
        )
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # 编辑器
        self.text_editor = tk.Text(
            editor_container,
            font=('Courier', self.font_size),
            bg='#ffffff',
            fg='#24292f',
            insertbackground='#24292f',
            selectbackground='#ddf4ff',
            borderwidth=0,
            highlightthickness=0,
            wrap='none',
            undo=True,
            maxundo=-1
        )
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        editor_scroll_y = ttk.Scrollbar(editor_container, orient=tk.VERTICAL, command=self._on_scroll)
        editor_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.config(yscrollcommand=editor_scroll_y.set)
        
        editor_scroll_x = ttk.Scrollbar(editor_container, orient=tk.HORIZONTAL, command=self.text_editor.xview)
        editor_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_editor.config(xscrollcommand=editor_scroll_x.set)
        
        # 绑定事件
        self.text_editor.bind('<<Modified>>', self.on_text_modified)
        self.text_editor.bind('<KeyRelease>', self.on_key_release)
        self.text_editor.bind('<ButtonRelease-1>', self.update_cursor_position)
    
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_theme = config.get('theme', 'github_light')
                    self.font_size = config.get('font_size', 10)
        except Exception:
            pass
    
    def save_config(self):
        """保存配置"""
        try:
            config = {
                'theme': self.current_theme,
                'font_size': self.font_size
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
    
    def detect_file_type(self, filepath):
        """检测文件类型"""
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.json':
            return 'json'
        elif ext == '.proto':
            return 'proto'
        return None
    
    def open_file(self):
        """打开文件"""
        if self.modified:
            result = messagebox.askyesnocancel("未保存的更改", "当前文件已修改，是否保存？")
            if result is None:
                return
            elif result:
                self.save_file()
        
        filepath = filedialog.askopenfilename(
            title="打开文件",
            filetypes=[
                ("支持的文件", "*.json;*.proto"),
                ("JSON文件", "*.json"),
                ("Proto文件", "*.proto"),
                ("所有文件", "*.*")
            ]
        )
        
        if filepath:
            self.load_file(filepath)
    
    def load_file(self, filepath):
        """加载文件"""
        self.file_type = self.detect_file_type(filepath)
        
        if self.file_type == 'json':
            self.load_json_file(filepath)
        elif self.file_type == 'proto':
            self.load_proto_file(filepath)
        else:
            messagebox.showerror("不支持的文件", "仅支持 .json 和 .proto 文件")
    
    def load_json_file(self, filepath):
        """加载JSON文件"""
        try:
            self.current_file = filepath
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.json_data = json.loads(content)
            
            self.refresh_json_tree()
            self.refresh_json_source()
            
            self.modified = False
            self.syntax_error_msg = None
            self.update_title()
            self.status_bar.config(text=f"已加载: {os.path.basename(filepath)} (JSON)")
            
        except json.JSONDecodeError as e:
            self.current_file = filepath
            self.json_data = None
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_editor.delete('1.0', tk.END)
                self.text_editor.insert('1.0', content)
                self.text_editor.edit_modified(False)
                
                self.update_line_numbers()
                self.apply_json_highlight()
                
                error_line = e.lineno
                error_col = e.colno
                
                self.text_editor.mark_set(tk.INSERT, f"{error_line}.{error_col}")
                self.text_editor.see(f"{error_line}.{error_col}")
                
                self.text_editor.tag_remove('error', '1.0', tk.END)
                self.text_editor.tag_add('error', f"{error_line}.0", f"{error_line}.end")
                self.text_editor.tag_config('error', background='#fff1f0')
                
                self.syntax_error_msg = f"✗ JSON语法错误: 第{error_line}行"
                self.update_cursor_position()
                self.modified = False
                self.update_title()
                
                messagebox.showwarning("JSON格式错误", 
                    f"文件已打开但无法解析\n错误位置: 第 {error_line} 行，第 {error_col} 列")
                
            except Exception as read_error:
                messagebox.showerror("无法打开文件", f"读取文件失败:\n{str(read_error)}")
        
        except Exception as e:
            messagebox.showerror("无法打开文件", f"打开文件失败:\n{str(e)}")
    
    def load_proto_file(self, filepath):
        """加载Proto文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.current_file = filepath
            self.proto_content = content
            self.modified = False
            
            self.text_editor.delete('1.0', tk.END)
            self.text_editor.insert('1.0', content)
            
            self.refresh_proto_tree()
            self.apply_proto_highlight()
            self.update_line_numbers()
            
            self.update_title()
            self.status_bar.config(text=f"已加载: {os.path.basename(filepath)} (Proto)")
            
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{str(e)}")
    
    def save_file(self):
        """保存文件"""
        if not self.current_file:
            self.save_as_file()
            return
        
        try:
            content = self.text_editor.get('1.0', tk.END).strip()
            
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.modified = False
            self.text_editor.edit_modified(False)
            self.update_title()
            
            if self.file_type == 'json':
                try:
                    parsed_data = json.loads(content)
                    self.json_data = parsed_data
                    self.refresh_json_tree()
                    self.syntax_error_msg = None
                    self.text_editor.tag_remove('error', '1.0', tk.END)
                    self.status_bar.config(text=f"✓ 已保存: {os.path.basename(self.current_file)}")
                except json.JSONDecodeError as e:
                    error_line = e.lineno
                    self.text_editor.mark_set(tk.INSERT, f"{error_line}.0")
                    self.text_editor.see(tk.INSERT)
                    self.text_editor.tag_remove('error', '1.0', tk.END)
                    self.text_editor.tag_add('error', f"{error_line}.0", f"{error_line}.end")
                    self.syntax_error_msg = f"✗ JSON语法错误: 第{error_line}行"
                    self.status_bar.config(text=f"✓ 已保存（有语法错误）: {os.path.basename(self.current_file)}")
            else:
                self.status_bar.config(text=f"✓ 已保存: {os.path.basename(self.current_file)}")
                
        except Exception as e:
            messagebox.showerror("保存失败", f"保存时发生错误:\n{str(e)}")
    
    def save_as_file(self):
        """另存为"""
        default_ext = ".json" if self.file_type == 'json' else ".proto"
        filetypes = [
            ("JSON文件", "*.json"),
            ("Proto文件", "*.proto"),
            ("所有文件", "*.*")
        ] if self.file_type == 'json' else [
            ("Proto文件", "*.proto"),
            ("JSON文件", "*.json"),
            ("所有文件", "*.*")
        ]
        
        filepath = filedialog.asksaveasfilename(
            title="另存为",
            defaultextension=default_ext,
            filetypes=filetypes
        )
        
        if filepath:
            self.current_file = filepath
            self.file_type = self.detect_file_type(filepath)
            self.save_file()
    
    def refresh_json_tree(self):
        """刷新JSON树形视图"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if self.json_data is not None:
            self._build_json_tree('', 'root', self.json_data)
            for item in self.tree.get_children():
                self.tree.item(item, open=True)
    
    def _build_json_tree(self, parent, key, value):
        """递归构建JSON树"""
        icon = self._get_json_icon(value)
        tag = self._get_json_tag(value)
        
        if isinstance(value, dict):
            node = self.tree.insert(parent, 'end', text=f"{icon} {key} {{{len(value)}}}", tags=(tag,))
            for k, v in value.items():
                self._build_json_tree(node, k, v)
        elif isinstance(value, list):
            node = self.tree.insert(parent, 'end', text=f"{icon} {key} [{len(value)}]", tags=(tag,))
            for i, item in enumerate(value):
                self._build_json_tree(node, f"[{i}]", item)
        else:
            display_value = self._format_json_value(value)
            self.tree.insert(parent, 'end', text=f"{icon} {key}: {display_value}", tags=(tag,))
    
    def _get_json_icon(self, value):
        """获取JSON类型图标"""
        if isinstance(value, dict):
            return "Obj"
        elif isinstance(value, list):
            return "Arr"
        elif isinstance(value, str):
            return "Str"
        elif isinstance(value, (int, float)):
            return "Num"
        elif isinstance(value, bool):
            return "Bool"
        elif value is None:
            return "Null"
        return "•"
    
    def _get_json_tag(self, value):
        """获取JSON类型tag"""
        if isinstance(value, dict):
            return "dict"
        elif isinstance(value, list):
            return "list"
        elif isinstance(value, str):
            return "str"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, (int, float)):
            return "number"
        elif value is None:
            return "null"
        return ""
    
    def _format_json_value(self, value):
        """格式化JSON显示值"""
        if isinstance(value, str):
            if len(value) > 50:
                return f'"{value[:50]}..."'
            return f'"{value}"'
        elif isinstance(value, bool):
            return str(value).lower()
        elif value is None:
            return "null"
        return str(value)
    
    def refresh_json_source(self):
        """刷新JSON源码视图"""
        if self.json_data is None:
            return
        
        formatted = json.dumps(self.json_data, ensure_ascii=False, indent=4)
        self.text_editor.delete('1.0', tk.END)
        self.text_editor.insert('1.0', formatted)
        self.text_editor.edit_modified(False)
        
        self.update_line_numbers()
        self.apply_json_highlight()
        self.update_cursor_position()
    
    def refresh_proto_tree(self):
        """刷新Proto结构视图"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.node_to_line.clear()
        
        content = self.text_editor.get('1.0', tk.END)
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            msg_match = re.match(r'\s*message\s+(\w+)', line)
            if msg_match:
                msg_name = msg_match.group(1)
                node = self.tree.insert('', 'end', text=f'Msg {msg_name}', tags=('message',))
                self.node_to_line[node] = i
                
                j = i
                brace_count = 0
                while j < len(lines):
                    if '{' in lines[j]:
                        brace_count += lines[j].count('{')
                    if '}' in lines[j]:
                        brace_count -= lines[j].count('}')
                        if brace_count == 0:
                            break
                    
                    field_match = re.match(r'\s*(repeated\s+)?(\w+)\s+(\w+)\s*=\s*(\d+)', lines[j])
                    if field_match:
                        repeated = field_match.group(1) or ''
                        field_type = field_match.group(2)
                        field_name = field_match.group(3)
                        field_num = field_match.group(4)
                        field_node = self.tree.insert(node, 'end', 
                            text=f'Fld {field_name}: {repeated}{field_type} = {field_num}',
                            tags=('field',))
                        self.node_to_line[field_node] = j + 1
                    j += 1
            
            enum_match = re.match(r'\s*enum\s+(\w+)', line)
            if enum_match:
                enum_name = enum_match.group(1)
                node = self.tree.insert('', 'end', text=f'Enum {enum_name}', tags=('enum',))
                self.node_to_line[node] = i
                
                j = i
                brace_count = 0
                while j < len(lines):
                    if '{' in lines[j]:
                        brace_count += lines[j].count('{')
                    if '}' in lines[j]:
                        brace_count -= lines[j].count('}')
                        if brace_count == 0:
                            break
                    
                    value_match = re.match(r'\s*(\w+)\s*=\s*(\d+)', lines[j])
                    if value_match:
                        value_name = value_match.group(1)
                        value_num = value_match.group(2)
                        value_node = self.tree.insert(node, 'end',
                            text=f'{value_name} = {value_num}',
                            tags=('enum_value',))
                        self.node_to_line[value_node] = j + 1
                    j += 1
            
            svc_match = re.match(r'\s*service\s+(\w+)', line)
            if svc_match:
                svc_name = svc_match.group(1)
                node = self.tree.insert('', 'end', text=f'Svc {svc_name}', tags=('service',))
                self.node_to_line[node] = i
                
                j = i
                brace_count = 0
                while j < len(lines):
                    if '{' in lines[j]:
                        brace_count += lines[j].count('{')
                    if '}' in lines[j]:
                        brace_count -= lines[j].count('}')
                        if brace_count == 0:
                            break
                    
                    rpc_match = re.match(r'\s*rpc\s+(\w+)\s*\(([^)]+)\)\s*returns\s*\(([^)]+)\)', lines[j])
                    if rpc_match:
                        rpc_name = rpc_match.group(1)
                        req_type = rpc_match.group(2)
                        resp_type = rpc_match.group(3)
                        rpc_node = self.tree.insert(node, 'end',
                            text=f'RPC {rpc_name}({req_type}) → {resp_type}',
                            tags=('rpc',))
                        self.node_to_line[rpc_node] = j + 1
                    j += 1
    
    def apply_json_highlight(self):
        """应用JSON语法高亮"""
        content = self.text_editor.get('1.0', tk.END)
        
        for tag in ['key', 'string', 'number', 'bool', 'null']:
            self.text_editor.tag_remove(tag, '1.0', tk.END)
        
        for match in re.finditer(r'"[^"\\]*(?:\\.[^"\\]*)*"', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            line_start = content.rfind('\n', 0, match.start()) + 1
            before = content[line_start:match.start()].strip()
            if before == '' or before.endswith(','):
                self.text_editor.tag_add('key', start, end)
            else:
                self.text_editor.tag_add('string', start, end)
        
        for match in re.finditer(r'\b-?\d+\.?\d*\b', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_editor.tag_add('number', start, end)
        
        for match in re.finditer(r'\b(true|false)\b', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_editor.tag_add('bool', start, end)
        
        for match in re.finditer(r'\bnull\b', content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_editor.tag_add('null', start, end)
    
    def apply_proto_highlight(self):
        """应用Proto语法高亮"""
        content = self.text_editor.get('1.0', tk.END)
        
        for tag in ['keyword', 'type', 'string', 'comment', 'number']:
            self.text_editor.tag_remove(tag, '1.0', tk.END)
        
        keywords = ['syntax', 'package', 'import', 'option', 'message', 'enum', 
                   'service', 'rpc', 'returns', 'repeated', 'optional', 'required',
                   'map', 'oneof', 'reserved', 'extensions', 'extend']
        
        types = ['double', 'float', 'int32', 'int64', 'uint32', 'uint64',
                'sint32', 'sint64', 'fixed32', 'fixed64', 'sfixed32', 'sfixed64',
                'bool', 'string', 'bytes']
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            comment_match = re.search(r'//.*$', line)
            if comment_match:
                start = comment_match.start()
                self.text_editor.tag_add('comment', f'{i}.{start}', f'{i}.end')
            
            for match in re.finditer(r'"[^"]*"', line):
                self.text_editor.tag_add('string', f'{i}.{match.start()}', f'{i}.{match.end()}')
            
            for kw in keywords:
                for match in re.finditer(r'\b' + kw + r'\b', line):
                    self.text_editor.tag_add('keyword', f'{i}.{match.start()}', f'{i}.{match.end()}')
            
            for tp in types:
                for match in re.finditer(r'\b' + tp + r'\b', line):
                    self.text_editor.tag_add('type', f'{i}.{match.start()}', f'{i}.{match.end()}')
            
            for match in re.finditer(r'\b\d+\b', line):
                self.text_editor.tag_add('number', f'{i}.{match.start()}', f'{i}.{match.end()}')
    
    def check_syntax(self):
        """语法检查"""
        if self.file_type == 'json':
            content = self.text_editor.get('1.0', tk.END).strip()
            if not content:
                self.syntax_error_msg = "⚠ 文档为空"
                self.update_cursor_position()
                return
            
            try:
                json.loads(content)
                self.syntax_error_msg = None
                self.text_editor.tag_remove('error', '1.0', tk.END)
                self.status_bar.config(text="✓ JSON语法检查通过")
            except json.JSONDecodeError as e:
                error_line = e.lineno
                error_col = e.colno
                
                self.text_editor.mark_set(tk.INSERT, f"{error_line}.{error_col}")
                self.text_editor.see(tk.INSERT)
                self.text_editor.focus_set()
                
                self.text_editor.tag_remove('error', '1.0', tk.END)
                self.text_editor.tag_add('error', f"{error_line}.0", f"{error_line}.end")
                
                self.syntax_error_msg = f"✗ JSON语法错误: 第{error_line}行"
                self.update_cursor_position()
        
        elif self.file_type == 'proto':
            self.status_bar.config(text="✓ Proto语法检查通过（基础）")
    
    def apply_theme(self, theme_name):
        """应用主题"""
        self.current_theme = theme_name
        theme = get_theme(theme_name)
        
        self.text_editor.config(
            bg=theme['editor_bg'],
            fg=theme['editor_fg'],
            insertbackground=theme.get('insert_bg', theme['editor_fg']),
            selectbackground=theme.get('select_bg', '#add6ff')
        )
        
        self.line_numbers.config(
            bg=theme['line_number_bg'],
            fg=theme['line_number_fg']
        )
        
        syntax = theme.get('syntax', {})
        self.text_editor.tag_config('key', foreground=syntax.get('key', '#0451a5'))
        self.text_editor.tag_config('keyword', foreground=syntax.get('key', '#0451a5'))
        self.text_editor.tag_config('string', foreground=syntax.get('string', '#a31515'))
        self.text_editor.tag_config('number', foreground=syntax.get('number', '#098658'))
        self.text_editor.tag_config('bool', foreground=syntax.get('bool', '#0000ff'))
        self.text_editor.tag_config('type', foreground=syntax.get('bool', '#0000ff'))
        self.text_editor.tag_config('null', foreground=syntax.get('null', '#808080'))
        self.text_editor.tag_config('comment', foreground=syntax.get('null', '#808080'))
        self.text_editor.tag_config('error', background=theme.get('error_highlight', '#ffeaea'))
        
        self.tree.tag_configure('dict', foreground='#0078d4')
        self.tree.tag_configure('list', foreground='#107c10')
        self.tree.tag_configure('str', foreground='#ca5010')
        self.tree.tag_configure('number', foreground='#8764b8')
        self.tree.tag_configure('bool', foreground='#00b7c3')
        self.tree.tag_configure('null', foreground='#8a8886')
        self.tree.tag_configure('message', foreground='#0078d4')
        self.tree.tag_configure('enum', foreground='#107c10')
        self.tree.tag_configure('service', foreground='#ca5010')
        self.tree.tag_configure('field', foreground='#8764b8')
        self.tree.tag_configure('rpc', foreground='#00b7c3')
        
        editor_font = font.Font(family="Courier", size=self.font_size)
        self.text_editor.config(font=editor_font)
        self.line_numbers.config(font=editor_font)
        
        self.save_config()
    
    def on_tree_select(self, event):
        """树节点选择事件"""
        if self.sync_timer:
            self.root.after_cancel(self.sync_timer)
        
        self.sync_timer = self.root.after(100, self._sync_tree_to_source)
    
    def _sync_tree_to_source(self):
        """树到源码的同步"""
        selection = self.tree.selection()
        if not selection:
            return
        
        if self.file_type == 'proto':
            node = selection[0]
            if node in self.node_to_line:
                line_num = self.node_to_line[node]
                self.text_editor.see(f'{line_num}.0')
                self.text_editor.tag_remove('highlight', '1.0', tk.END)
                self.text_editor.tag_add('highlight', f'{line_num}.0', f'{line_num}.end')
                self.text_editor.tag_config('highlight', background='#ffffe0')
    
    def expand_all(self):
        """展开所有节点"""
        def expand_recursive(item):
            self.tree.item(item, open=True)
            for child in self.tree.get_children(item):
                expand_recursive(child)
        
        for item in self.tree.get_children():
            expand_recursive(item)
    
    def collapse_all(self):
        """收起所有节点"""
        def collapse_recursive(item):
            self.tree.item(item, open=False)
            for child in self.tree.get_children(item):
                collapse_recursive(child)
        
        for item in self.tree.get_children():
            collapse_recursive(item)
    
    def undo(self):
        try:
            self.text_editor.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        try:
            self.text_editor.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        self.text_editor.event_generate("<<Cut>>")
    
    def copy(self):
        self.text_editor.event_generate("<<Copy>>")
    
    def paste(self):
        self.text_editor.event_generate("<<Paste>>")
        self.text_editor.after(10, self._apply_highlight)
    
    def select_all(self):
        self.text_editor.tag_add(tk.SEL, "1.0", tk.END)
        self.text_editor.mark_set(tk.INSERT, "1.0")
        self.text_editor.see(tk.INSERT)
        return 'break'
    
    def zoom_font(self, delta):
        """字体缩放"""
        self.font_size = max(6, min(24, self.font_size + delta))
        self.apply_theme(self.current_theme)
        self.update_line_numbers()
    
    def reset_font(self):
        """重置字体大小"""
        self.font_size = 10
        self.apply_theme(self.current_theme)
        self.update_line_numbers()
    
    def _on_scroll(self, *args):
        """同步滚动"""
        self.text_editor.yview(*args)
        self.line_numbers.yview(*args)
    
    def update_line_numbers(self):
        """更新行号"""
        try:
            line_count = int(self.text_editor.index('end-1c').split('.')[0])
            line_numbers_text = '\n'.join(str(i) for i in range(1, line_count + 1))
            
            self.line_numbers.config(state='normal')
            self.line_numbers.delete('1.0', tk.END)
            self.line_numbers.insert('1.0', line_numbers_text)
            self.line_numbers.config(state='disabled')
        except Exception:
            pass
    
    def on_text_modified(self, event=None):
        """文本修改事件"""
        if self.text_editor.edit_modified():
            self.modified = True
            self.update_title()
            self.text_editor.edit_modified(False)
    
    def on_key_release(self, event=None):
        """按键释放事件"""
        if hasattr(self, 'highlight_timer') and self.highlight_timer:
            self.text_editor.after_cancel(self.highlight_timer)
        
        self.update_line_numbers()
        self.update_cursor_position()
        
        self.highlight_timer = self.text_editor.after(50, self._apply_highlight)
    
    def _apply_highlight(self):
        """应用语法高亮"""
        if self.file_type == 'json':
            self.apply_json_highlight()
        elif self.file_type == 'proto':
            self.apply_proto_highlight()
    
    def update_cursor_position(self, event=None):
        """更新光标位置"""
        try:
            cursor_pos = self.text_editor.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            
            if self.current_file:
                filename = os.path.basename(self.current_file)
                file_type_str = f"({self.file_type.upper()})" if self.file_type else ""
                status_text = f"文件: {filename} {file_type_str} | 行: {line}, 列: {int(col)+1}"
            else:
                status_text = f"行: {line}, 列: {int(col)+1}"
            
            if self.syntax_error_msg:
                status_text += f" | {self.syntax_error_msg}"
            
            self.status_bar.config(text=status_text)
        except Exception:
            pass
    
    def update_title(self):
        """更新窗口标题"""
        filename = os.path.basename(self.current_file) if self.current_file else "未命名"
        modified_mark = " *" if self.modified else ""
        file_type_str = f" ({self.file_type.upper()})" if self.file_type else ""
        self.root.title(f"P-Viewer {self.version} - {filename}{file_type_str}{modified_mark}")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = f"""P-Viewer {self.version}

程序员专用文件查看和编辑工具

支持格式:
• JSON - 树形视图 + 语法高亮
• Proto - 结构视图 + 语法高亮

特性:
• 双视图（结构 + 源码）
• 语法高亮
• 主题切换
• 零依赖

MIT License © 2025"""
        messagebox.showinfo("关于", about_text)
    
    def quit_app(self):
        """退出应用"""
        if self.modified:
            result = messagebox.askyesnocancel("未保存的更改", "文件已修改，是否保存？")
            if result is None:
                return
            elif result:
                self.save_file()
        
        self.root.quit()


def main():
    """主函数"""
    root = tk.Tk()
    
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    app = PViewer(root, file_path)
    
    root.mainloop()


if __name__ == "__main__":
    main()
