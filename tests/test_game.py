# -*- coding: utf-8 -*-
"""游戏逻辑单元测试"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from src.game import Game
from src.blocks import Block
from src.constants import GRID_WIDTH, GRID_HEIGHT


class TestBlock(unittest.TestCase):
    """方块类测试"""

    def test_block_creation(self):
        """测试方块创建"""
        block = Block('I')
        self.assertEqual(block.block_type, 'I')
        self.assertEqual(block.rotation, 0)
        self.assertEqual(block.x, 4)
        self.assertEqual(block.y, 0)

    def test_block_rotation(self):
        """测试方块旋转"""
        block = Block('T')
        original_rotation = block.rotation
        block.rotate()
        self.assertEqual(block.rotation, (original_rotation + 1) % 4)

    def test_block_move(self):
        """测试方块移动"""
        block = Block('L')
        original_x = block.x
        original_y = block.y
        block.move(1, 1)
        self.assertEqual(block.x, original_x + 1)
        self.assertEqual(block.y, original_y + 1)

    def test_block_copy(self):
        """测试方块复制"""
        block = Block('S')
        block.rotate()
        block.move(2, 3)
        new_block = block.copy()
        self.assertEqual(new_block.block_type, block.block_type)
        self.assertEqual(new_block.rotation, block.rotation)
        self.assertEqual(new_block.x, block.x)
        self.assertEqual(new_block.y, block.y)


class TestGame(unittest.TestCase):
    """游戏类测试"""

    def setUp(self):
        """测试前准备"""
        self.game = Game()

    def test_game_initialization(self):
        """测试游戏初始化"""
        self.assertIsNotNone(self.game.current_block)
        self.assertIsNotNone(self.game.next_block)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.paused)

    def test_grid_size(self):
        """测试网格大小"""
        self.assertEqual(len(self.game.grid), GRID_HEIGHT)
        self.assertEqual(len(self.game.grid[0]), GRID_WIDTH)

    def test_move_left(self):
        """测试左移"""
        initial_x = self.game.current_block.x
        result = self.game.move_left()
        # 可能成功或失败（取决于初始位置）
        if result:
            self.assertEqual(self.game.current_block.x, initial_x - 1)

    def test_move_right(self):
        """测试右移"""
        initial_x = self.game.current_block.x
        result = self.game.move_right()
        if result:
            self.assertEqual(self.game.current_block.x, initial_x + 1)

    def test_move_down(self):
        """测试下移"""
        result = self.game.move_down()
        self.assertTrue(result or self.game.game_over or self.game.current_block.y > 0)

    def test_rotate(self):
        """测试旋转"""
        self.game.rotate()
        # 旋转可能成功或失败，但不应该崩溃

    def test_hard_drop(self):
        """测试硬降"""
        self.game.hard_drop()
        # 硬降后应该锁定方块
        self.assertIsNotNone(self.game.current_block)

    def test_hold(self):
        """测试保持方块"""
        result = self.game.hold()
        self.assertTrue(result)
        self.assertFalse(self.game.can_hold)
        # 第二次保持应该失败
        result2 = self.game.hold()
        self.assertFalse(result2)

    def test_pause_toggle(self):
        """测试暂停切换"""
        self.assertFalse(self.game.paused)
        self.game.toggle_pause()
        self.assertTrue(self.game.paused)
        self.game.toggle_pause()
        self.assertFalse(self.game.paused)

    def test_restart(self):
        """测试重新开始"""
        self.game.score = 100
        self.game.level = 5
        self.game.restart()
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)

    def test_ghost_position(self):
        """测试幽灵方块位置"""
        ghost = self.game.get_ghost_position()
        self.assertTrue(len(ghost) > 0)


if __name__ == '__main__':
    unittest.main()