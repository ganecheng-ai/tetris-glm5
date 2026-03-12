# -*- coding: utf-8 -*-
"""常量定义模块"""

# 窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
FPS = 60

# 游戏区域设置
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
GRID_X_OFFSET = 50
GRID_Y_OFFSET = 50

# 方块颜色 (RGB)
COLORS = {
    'I': (0, 255, 255),      # 青色
    'O': (255, 255, 0),      # 黄色
    'T': (128, 0, 128),      # 紫色
    'S': (0, 255, 0),        # 绿色
    'Z': (255, 0, 0),        # 红色
    'J': (0, 0, 255),        # 蓝色
    'L': (255, 165, 0),      # 橙色
}

# 背景颜色
BACKGROUND_COLOR = (30, 30, 50)
GRID_BG_COLOR = (20, 20, 40)
GRID_LINE_COLOR = (50, 50, 70)
TEXT_COLOR = (255, 255, 255)
BORDER_COLOR = (100, 100, 150)

# 游戏速度 (毫秒)
INITIAL_FALL_SPEED = 500
MIN_FALL_SPEED = 50
SPEED_DECREASE = 50

# 分数设置
SCORE_PER_LINE = {
    1: 100,
    2: 300,
    3: 500,
    4: 800,
}

# 控制键
KEY_LEFT = 'left'
KEY_RIGHT = 'right'
KEY_UP = 'up'
KEY_DOWN = 'down'
KEY_SPACE = 'space'
KEY_P = 'p'
KEY_R = 'r'
KEY_ESCAPE = 'escape'