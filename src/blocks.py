# -*- coding: utf-8 -*-
"""方块定义模块"""
from typing import List, Tuple

from .constants import COLORS


class Block:
    """方块类"""

    # 方块形状定义 (相对于旋转中心的坐标)
    # 每个方块有4个旋转状态
    SHAPES = {
        'I': [
            [(0, -1), (0, 0), (0, 1), (0, 2)],
            [(-1, 0), (0, 0), (1, 0), (2, 0)],
            [(0, -1), (0, 0), (0, 1), (0, 2)],
            [(-1, 0), (0, 0), (1, 0), (2, 0)],
        ],
        'O': [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (1, 1)],
        ],
        'T': [
            [(0, -1), (0, 0), (0, 1), (-1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, 1)],
            [(0, -1), (0, 0), (0, 1), (1, 0)],
            [(-1, 0), (0, 0), (1, 0), (0, -1)],
        ],
        'S': [
            [(0, 0), (0, 1), (-1, 0), (-1, -1)],
            [(-1, 0), (0, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (-1, 0), (-1, -1)],
            [(-1, 0), (0, 0), (0, 1), (1, 1)],
        ],
        'Z': [
            [(0, 0), (0, -1), (-1, 0), (-1, 1)],
            [(-1, 0), (0, 0), (0, -1), (1, -1)],
            [(0, 0), (0, -1), (-1, 0), (-1, 1)],
            [(-1, 0), (0, 0), (0, -1), (1, -1)],
        ],
        'J': [
            [(0, 0), (0, -1), (0, 1), (-1, 1)],
            [(-1, 0), (0, 0), (1, 0), (1, 1)],
            [(0, 0), (0, -1), (0, 1), (1, -1)],
            [(-1, 0), (0, 0), (1, 0), (-1, -1)],
        ],
        'L': [
            [(0, 0), (0, -1), (0, 1), (-1, -1)],
            [(-1, 0), (0, 0), (1, 0), (1, -1)],
            [(0, 0), (0, -1), (0, 1), (1, 1)],
            [(-1, 0), (0, 0), (1, 0), (-1, 1)],
        ],
    }

    def __init__(self, block_type: str):
        """初始化方块

        Args:
            block_type: 方块类型 ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
        """
        self.block_type = block_type
        self.rotation = 0  # 当前旋转状态 (0-3)
        self.x = 4  # 方块中心x坐标 (网格坐标)
        self.y = 0  # 方块中心y坐标 (网格坐标)

    def get_cells(self) -> List[Tuple[int, int]]:
        """获取当前方块的四个单元格坐标

        Returns:
            四个单元格的(x, y)坐标列表
        """
        shape = self.SHAPES[self.block_type][self.rotation]
        return [(self.x + dx, self.y + dy) for dx, dy in shape]

    def rotate(self, direction: int = 1):
        """旋转方块

        Args:
            direction: 旋转方向，1为顺时针，-1为逆时针
        """
        self.rotation = (self.rotation + direction) % 4

    def move(self, dx: int, dy: int):
        """移动方块

        Args:
            dx: x方向移动量
            dy: y方向移动量
        """
        self.x += dx
        self.y += dy

    def get_color(self) -> Tuple[int, int, int]:
        """获取方块颜色

        Returns:
            RGB颜色元组
        """
        return COLORS[self.block_type]

    def copy(self) -> 'Block':
        """复制方块

        Returns:
            新的方块对象
        """
        new_block = Block(self.block_type)
        new_block.rotation = self.rotation
        new_block.x = self.x
        new_block.y = self.y
        return new_block
