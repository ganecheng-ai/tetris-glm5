# -*- coding: utf-8 -*-
"""渲染器模块"""
import os
from typing import Tuple

import pygame

from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_WIDTH, GRID_HEIGHT,
    BLOCK_SIZE, GRID_X_OFFSET, GRID_Y_OFFSET, COLORS,
    BACKGROUND_COLOR, GRID_BG_COLOR, GRID_LINE_COLOR,
    TEXT_COLOR, BORDER_COLOR, FPS
)
from .game import Game
from .blocks import Block
from .sound import sound_manager


class Renderer:
    """渲染器类"""

    def __init__(self):
        """初始化渲染器"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("俄罗斯方块 - Tetris")
        self.clock = pygame.time.Clock()

        # 音效状态
        self.sound_enabled = sound_manager.enabled

        # 加载字体
        self.font_large = self._load_font(48)
        self.font_medium = self._load_font(28)
        self.font_small = self._load_font(20)

        # 创建方块表面缓存（带有渐变效果）
        self.block_surfaces = {}
        self._create_block_surfaces()

    def _load_font(self, size: int) -> pygame.font.Font:
        """加载字体

        Args:
            size: 字体大小

        Returns:
            字体对象
        """
        # 尝试加载中文字体
        chinese_fonts = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            "C:\\Windows\\Fonts\\msyh.ttc",  # Windows
            "/System/Library/Fonts/PingFang.ttc",  # macOS
        ]

        for font_path in chinese_fonts:
            if os.path.exists(font_path):
                try:
                    return pygame.font.Font(font_path, size)
                except (OSError, pygame.error):
                    continue

        # 回退到默认字体
        return pygame.font.Font(None, size)

    def _create_block_surfaces(self):
        """创建带有渐变效果的方块表面"""
        for block_type, color in COLORS.items():
            surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
            self._draw_gradient_block(surface, color)
            self.block_surfaces[block_type] = surface

    def _draw_gradient_block(self, surface: pygame.Surface, color: Tuple[int, int, int]):
        """绘制渐变效果的方块

        Args:
            surface: 要绘制的表面
            color: 方块颜色
        """
        r, g, b = color
        for y in range(BLOCK_SIZE):
            # 计算渐变因子
            factor = 1 - (y / BLOCK_SIZE) * 0.3
            line_color = (
                min(255, int(r * factor + 50 * (1 - factor))),
                min(255, int(g * factor + 50 * (1 - factor))),
                min(255, int(b * factor + 50 * (1 - factor))),
            )
            pygame.draw.line(surface, line_color, (0, y), (BLOCK_SIZE - 1, y))

        # 绘制高光
        highlight_color = (
            min(255, r + 80),
            min(255, g + 80),
            min(255, b + 80),
        )
        pygame.draw.line(surface, highlight_color, (2, 2), (BLOCK_SIZE - 3, 2), 2)
        pygame.draw.line(surface, highlight_color, (2, 2), (2, BLOCK_SIZE - 3), 2)

        # 绘制阴影
        shadow_color = (
            max(0, r - 80),
            max(0, g - 80),
            max(0, b - 80),
        )
        pygame.draw.line(surface, shadow_color, (BLOCK_SIZE - 2, 2),
                         (BLOCK_SIZE - 2, BLOCK_SIZE - 2), 2)
        pygame.draw.line(surface, shadow_color, (2, BLOCK_SIZE - 2),
                         (BLOCK_SIZE - 2, BLOCK_SIZE - 2), 2)

        # 绘制边框
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, BLOCK_SIZE, BLOCK_SIZE), 1)

    def render(self, game: Game):
        """渲染游戏画面

        Args:
            game: 游戏对象
        """
        # 清屏
        self.screen.fill(BACKGROUND_COLOR)

        # 绘制游戏区域背景
        grid_rect = pygame.Rect(
            GRID_X_OFFSET - 2,
            GRID_Y_OFFSET - 2,
            GRID_WIDTH * BLOCK_SIZE + 4,
            GRID_HEIGHT * BLOCK_SIZE + 4
        )
        pygame.draw.rect(self.screen, BORDER_COLOR, grid_rect, 2)

        # 绘制网格背景
        grid_bg_rect = pygame.Rect(
            GRID_X_OFFSET,
            GRID_Y_OFFSET,
            GRID_WIDTH * BLOCK_SIZE,
            GRID_HEIGHT * BLOCK_SIZE
        )
        pygame.draw.rect(self.screen, GRID_BG_COLOR, grid_bg_rect)

        # 绘制网格线
        for x in range(GRID_WIDTH + 1):
            start_pos = (GRID_X_OFFSET + x * BLOCK_SIZE, GRID_Y_OFFSET)
            end_pos = (GRID_X_OFFSET + x * BLOCK_SIZE,
                       GRID_Y_OFFSET + GRID_HEIGHT * BLOCK_SIZE)
            pygame.draw.line(self.screen, GRID_LINE_COLOR, start_pos, end_pos)

        for y in range(GRID_HEIGHT + 1):
            start_pos = (GRID_X_OFFSET, GRID_Y_OFFSET + y * BLOCK_SIZE)
            end_pos = (GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE,
                       GRID_Y_OFFSET + y * BLOCK_SIZE)
            pygame.draw.line(self.screen, GRID_LINE_COLOR, start_pos, end_pos)

        # 绘制已固定的方块
        self._draw_grid(game)

        # 绘制幽灵方块
        self._draw_ghost_block(game)

        # 绘制当前方块
        self._draw_current_block(game)

        # 绘制侧边栏信息
        self._draw_sidebar(game)

        # 绘制游戏状态
        if game.game_over:
            self._draw_game_over()
        elif game.paused:
            self._draw_paused()

        pygame.display.flip()

    def _draw_grid(self, game: Game):
        """绘制已固定的方块

        Args:
            game: 游戏对象
        """
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell = game.grid[y][x]
                if cell is not None:
                    self._draw_block(
                        GRID_X_OFFSET + x * BLOCK_SIZE,
                        GRID_Y_OFFSET + y * BLOCK_SIZE,
                        cell
                    )

    def _draw_current_block(self, game: Game):
        """绘制当前方块

        Args:
            game: 游戏对象
        """
        if game.current_block is None:
            return

        for x, y in game.current_block.get_cells():
            if 0 <= y < GRID_HEIGHT:
                self._draw_block(
                    GRID_X_OFFSET + x * BLOCK_SIZE,
                    GRID_Y_OFFSET + y * BLOCK_SIZE,
                    game.current_block.block_type
                )

    def _draw_ghost_block(self, game: Game):
        """绘制幽灵方块

        Args:
            game: 游戏对象
        """
        ghost_cells = game.get_ghost_position()
        if not ghost_cells:
            return

        block_type = game.current_block.block_type if game.current_block else 'I'
        color = COLORS.get(block_type, (100, 100, 100))

        for x, y in ghost_cells:
            if 0 <= y < GRID_HEIGHT:
                rect = pygame.Rect(
                    GRID_X_OFFSET + x * BLOCK_SIZE + 2,
                    GRID_Y_OFFSET + y * BLOCK_SIZE + 2,
                    BLOCK_SIZE - 4,
                    BLOCK_SIZE - 4
                )
                ghost_color = (color[0], color[1], color[2], 80)
                ghost_surface = pygame.Surface((BLOCK_SIZE - 4, BLOCK_SIZE - 4), pygame.SRCALPHA)
                ghost_surface.fill(ghost_color)
                pygame.draw.rect(ghost_surface, color, (0, 0, BLOCK_SIZE - 4, BLOCK_SIZE - 4), 2)
                self.screen.blit(ghost_surface, rect)

    def _draw_block(self, x: int, y: int, block_type: str):
        """绘制单个方块

        Args:
            x: x坐标
            y: y坐标
            block_type: 方块类型
        """
        if block_type in self.block_surfaces:
            self.screen.blit(self.block_surfaces[block_type], (x, y))

    def _draw_sidebar(self, game: Game):
        """绘制侧边栏信息

        Args:
            game: 游戏对象
        """
        sidebar_x = GRID_X_OFFSET + GRID_WIDTH * BLOCK_SIZE + 30

        # 绘制下一个方块
        self._draw_text("下一个:", sidebar_x, GRID_Y_OFFSET, self.font_medium)
        if game.next_block:
            self._draw_preview_block(game.next_block, sidebar_x + 20, GRID_Y_OFFSET + 40)

        # 绘制保持方块
        self._draw_text("保持:", sidebar_x, GRID_Y_OFFSET + 150, self.font_medium)
        if game.hold_block:
            self._draw_preview_block(game.hold_block, sidebar_x + 20, GRID_Y_OFFSET + 190)

        # 绘制分数
        self._draw_text("分数:", sidebar_x, GRID_Y_OFFSET + 300, self.font_medium)
        self._draw_text(str(game.score), sidebar_x, GRID_Y_OFFSET + 335, self.font_large)

        # 绘制等级
        self._draw_text("等级:", sidebar_x, GRID_Y_OFFSET + 400, self.font_medium)
        self._draw_text(str(game.level), sidebar_x, GRID_Y_OFFSET + 435, self.font_large)

        # 绘制消除行数
        self._draw_text("消除:", sidebar_x, GRID_Y_OFFSET + 500, self.font_medium)
        self._draw_text(str(game.lines_cleared), sidebar_x, GRID_Y_OFFSET + 535, self.font_large)

        # 绘制控制说明
        self._draw_controls(sidebar_x, GRID_Y_OFFSET + 600)

    def _draw_preview_block(self, block: Block, x: int, y: int):
        """绘制预览方块

        Args:
            block: 方块对象
            x: x坐标
            y: y坐标
        """
        preview_size = 20
        for dx, dy in block.SHAPES[block.block_type][0]:
            cell_x = x + dx * preview_size + preview_size * 1.5
            cell_y = y + dy * preview_size + preview_size * 0.5
            rect = pygame.Rect(cell_x, cell_y, preview_size, preview_size)
            color = COLORS.get(block.block_type, (100, 100, 100))

            # 绘制带渐变的预览方块
            surface = pygame.Surface((preview_size, preview_size), pygame.SRCALPHA)
            self._draw_small_gradient_block(surface, color, preview_size)
            self.screen.blit(surface, rect)

    def _draw_small_gradient_block(self, surface: pygame.Surface,
                                   color: Tuple[int, int, int], size: int):
        """绘制小尺寸渐变方块

        Args:
            surface: 表面
            color: 颜色
            size: 大小
        """
        r, g, b = color
        for y in range(size):
            factor = 1 - (y / size) * 0.3
            line_color = (
                min(255, int(r * factor + 30 * (1 - factor))),
                min(255, int(g * factor + 30 * (1 - factor))),
                min(255, int(b * factor + 30 * (1 - factor))),
            )
            pygame.draw.line(surface, line_color, (0, y), (size - 1, y))

        pygame.draw.rect(surface, (0, 0, 0), (0, 0, size, size), 1)

    def _draw_text(self, text: str, x: int, y: int, font: pygame.font.Font, color=None):
        """绘制文本

        Args:
            text: 文本内容
            x: x坐标
            y: y坐标
            font: 字体
            color: 颜色
        """
        if color is None:
            color = TEXT_COLOR
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def _draw_controls(self, x: int, y: int):
        """绘制控制说明

        Args:
            x: x坐标
            y: y坐标
        """
        controls = [
            "← → 移动",
            "↑ 旋转",
            "↓ 软降",
            "空格 硬降",
            "C 保持",
            "P 暂停",
            "R 重开",
            "M 音效"
        ]

        for i, text in enumerate(controls):
            self._draw_text(text, x, y + i * 18, self.font_small, (180, 180, 200))

        # 显示音效状态
        sound_status = "开" if self.sound_enabled else "关"
        self._draw_text(f"音效: {sound_status}", x, y + len(controls) * 18 + 5,
                        self.font_small,
                        (150, 200, 150) if self.sound_enabled else (200, 150, 150))

    def set_sound_enabled(self, enabled: bool):
        """设置音效状态显示

        Args:
            enabled: 是否启用音效
        """
        self.sound_enabled = enabled

    def _draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文字
        text = self.font_large.render("游戏结束", True, (255, 50, 50))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        # 重新开始提示
        restart_text = self.font_medium.render("按 R 重新开始", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)

    def _draw_paused(self):
        """绘制暂停界面"""
        # 半透明遮罩
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # 暂停文字
        text = self.font_large.render("已暂停", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        # 继续提示
        continue_text = self.font_medium.render("按 P 继续", True, (200, 200, 200))
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(continue_text, continue_rect)

    def tick(self) -> int:
        """获取时钟tick

        Returns:
            经过的毫秒数
        """
        return self.clock.tick(FPS)
