# -*- coding: utf-8 -*-
"""游戏逻辑模块"""
import random
from typing import List, Tuple, Optional
from .blocks import Block
from .constants import (
    GRID_WIDTH, GRID_HEIGHT, INITIAL_FALL_SPEED,
    MIN_FALL_SPEED, SPEED_DECREASE, SCORE_PER_LINE
)
from .logger import logger
from .sound import sound_manager
from .high_score import high_score_manager


class Game:
    """游戏类"""

    def __init__(self):
        """初始化游戏"""
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)
        ]
        self.current_block: Optional[Block] = None
        self.next_block: Optional[Block] = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = INITIAL_FALL_SPEED
        self.game_over = False
        self.paused = False
        self.hold_block: Optional[Block] = None
        self.can_hold = True
        self.high_score_rank = 0

        # 初始化方块
        self._spawn_block()

        # 记录游戏开始
        logger.game_start()

    def _spawn_block(self):
        """生成新方块"""
        if self.next_block is None:
            self.next_block = self._create_random_block()

        self.current_block = self.next_block
        self.next_block = self._create_random_block()
        self.can_hold = True

        # 检查是否可以放置
        if not self._can_place(self.current_block):
            self.game_over = True
            sound_manager.play('game_over')
            logger.game_over(self.score, self.level, self.lines_cleared)
            # 记录高分
            self.high_score_rank = high_score_manager.add_score(
                self.score, self.level, self.lines_cleared
            )

    def _create_random_block(self) -> Block:
        """创建随机方块

        Returns:
            新的方块对象
        """
        block_types = list(Block.SHAPES.keys())
        return Block(random.choice(block_types))

    def _can_place(self, block: Block) -> bool:
        """检查方块是否可以放置在当前位置

        Args:
            block: 要检查的方块

        Returns:
            是否可以放置
        """
        for x, y in block.get_cells():
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True

    def _lock_block(self):
        """锁定当前方块到网格"""
        if self.current_block is None:
            return

        color = self.current_block.block_type
        for x, y in self.current_block.get_cells():
            if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                self.grid[y][x] = color

        # 清除完整的行
        self._clear_lines()

        # 生成新方块
        self._spawn_block()

    def _clear_lines(self):
        """清除完整的行并更新分数"""
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(GRID_WIDTH)):
                lines_to_clear.append(y)

        if lines_to_clear:
            # 更新分数
            num_lines = len(lines_to_clear)
            self.score += SCORE_PER_LINE.get(num_lines, num_lines * 100)
            self.lines_cleared += num_lines

            # 记录消除行
            logger.lines_cleared(num_lines, self.score)

            # 播放消行音效
            if num_lines == 4:
                sound_manager.play('tetris')
            else:
                sound_manager.play('clear')

            # 更新等级和速度
            old_level = self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(
                MIN_FALL_SPEED,
                INITIAL_FALL_SPEED - (self.level - 1) * SPEED_DECREASE
            )

            # 记录等级提升
            if self.level > old_level:
                sound_manager.play('level_up')
                logger.level_up(self.level)

            # 清除行并下移
            for y in lines_to_clear:
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(GRID_WIDTH)])

    def move_left(self) -> bool:
        """向左移动

        Returns:
            是否成功移动
        """
        if self.current_block is None or self.paused or self.game_over:
            return False

        self.current_block.move(-1, 0)
        if not self._can_place(self.current_block):
            self.current_block.move(1, 0)
            return False
        sound_manager.play('move')
        return True

    def move_right(self) -> bool:
        """向右移动

        Returns:
            是否成功移动
        """
        if self.current_block is None or self.paused or self.game_over:
            return False

        self.current_block.move(1, 0)
        if not self._can_place(self.current_block):
            self.current_block.move(-1, 0)
            return False
        sound_manager.play('move')
        return True

    def move_down(self) -> bool:
        """向下移动（软降）

        Returns:
            是否成功移动
        """
        if self.current_block is None or self.paused or self.game_over:
            return False

        self.current_block.move(0, 1)
        if not self._can_place(self.current_block):
            self.current_block.move(0, -1)
            self._lock_block()
            return False
        return True

    def rotate(self) -> bool:
        """旋转方块

        Returns:
            是否成功旋转
        """
        if self.current_block is None or self.paused or self.game_over:
            return False

        original_rotation = self.current_block.rotation
        self.current_block.rotate(1)

        # 尝试墙踢（Wall Kick）
        kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]
        for dx, dy in kicks:
            self.current_block.move(dx, dy)
            if self._can_place(self.current_block):
                sound_manager.play('rotate')
                return True
            self.current_block.move(-dx, -dy)

        # 无法旋转，恢复原状
        self.current_block.rotation = original_rotation
        return False

    def hard_drop(self):
        """硬降（直接落到底部）"""
        if self.current_block is None or self.paused or self.game_over:
            return

        while self._can_place(self.current_block):
            self.current_block.move(0, 1)
        self.current_block.move(0, -1)
        sound_manager.play('drop')
        self._lock_block()

    def hold(self) -> bool:
        """保持当前方块

        Returns:
            是否成功保持
        """
        if not self.can_hold or self.paused or self.game_over:
            return False

        if self.current_block is None:
            return False

        current_type = self.current_block.block_type
        if self.hold_block is None:
            self.hold_block = Block(current_type)
            self._spawn_block()
        else:
            hold_type = self.hold_block.block_type
            self.hold_block = Block(current_type)
            self.current_block = Block(hold_type)
            self.current_block.x = 4
            self.current_block.y = 0

        self.can_hold = False
        logger.hold_block(current_type)
        return True

    def update(self) -> bool:
        """更新游戏状态（自动下落）

        Returns:
            游戏是否继续
        """
        if self.paused or self.game_over:
            return False

        return self.move_down()

    def toggle_pause(self):
        """切换暂停状态"""
        if not self.game_over:
            self.paused = not self.paused
            if self.paused:
                logger.pause()
            else:
                logger.resume()

    def restart(self):
        """重新开始游戏"""
        logger.restart()
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)
        ]
        self.current_block: Optional[Block] = None
        self.next_block: Optional[Block] = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = INITIAL_FALL_SPEED
        self.game_over = False
        self.paused = False
        self.hold_block: Optional[Block] = None
        self.can_hold = True
        self.high_score_rank = 0
        self._spawn_block()
        logger.game_start()

    def get_ghost_position(self) -> List[Tuple[int, int]]:
        """获取幽灵方块位置（预览落点）

        Returns:
            幽灵方块的单元格坐标列表
        """
        if self.current_block is None:
            return []

        ghost = self.current_block.copy()
        while self._can_place(ghost):
            ghost.move(0, 1)
        ghost.move(0, -1)
        return ghost.get_cells()
