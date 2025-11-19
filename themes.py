"""
P-Viewer - 主题配置

定义4套主题配色方案
"""

THEMES = {
    'github_light': {
        'name': 'GitHub 亮色',
        'editor_bg': '#ffffff',
        'editor_fg': '#24292f',
        'line_number_bg': '#f6f8fa',
        'line_number_fg': '#57606a',
        'insert_bg': '#24292f',
        'select_bg': '#ddf4ff',
        'error_highlight': '#fff1f0',
        'syntax': {
            'key': '#0550ae',
            'string': '#0a3069',
            'number': '#0550ae',
            'bool': '#8250df',
            'null': '#6e7781',
        }
    },
    
    'github_dark': {
        'name': 'GitHub 暗色',
        'editor_bg': '#0d1117',
        'editor_fg': '#e6edf3',
        'line_number_bg': '#161b22',
        'line_number_fg': '#7d8590',
        'insert_bg': '#e6edf3',
        'select_bg': '#1f6feb',
        'error_highlight': '#490b0b',
        'syntax': {
            'key': '#79c0ff',
            'string': '#a5d6ff',
            'number': '#79c0ff',
            'bool': '#d2a8ff',
            'null': '#7d8590',
        }
    },
    
    'vscode_light': {
        'name': 'VS Code 亮色',
        'editor_bg': '#ffffff',
        'editor_fg': '#000000',
        'line_number_bg': '#f3f3f3',
        'line_number_fg': '#237893',
        'insert_bg': '#000000',
        'select_bg': '#add6ff',
        'error_highlight': '#ffeaea',
        'syntax': {
            'key': '#0451a5',
            'string': '#a31515',
            'number': '#098658',
            'bool': '#0000ff',
            'null': '#808080',
        }
    },
    
    'vscode_dark': {
        'name': 'VS Code 暗色',
        'editor_bg': '#1e1e1e',
        'editor_fg': '#d4d4d4',
        'line_number_bg': '#1e1e1e',
        'line_number_fg': '#858585',
        'insert_bg': '#d4d4d4',
        'select_bg': '#264f78',
        'error_highlight': '#5a1d1d',
        'syntax': {
            'key': '#9cdcfe',
            'string': '#ce9178',
            'number': '#b5cea8',
            'bool': '#569cd6',
            'null': '#808080',
        }
    }
}


def get_theme(theme_name):
    """获取主题配置"""
    return THEMES.get(theme_name, THEMES['github_light'])


def get_theme_names():
    """获取所有主题名称"""
    return list(THEMES.keys())
