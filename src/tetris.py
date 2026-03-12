# -*- coding: utf-8 -*-
"""俄罗斯方块游戏主程序"""
import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from src.game import Game
from src.renderer import Renderer
from src.constants import INITIAL_FALL_SPEED
from src.logger import logger


def main():
    """主函数"""
    renderer = Renderer()
    game = Game()

    fall_time = 0
    fall_speed = INITIAL_FALL_SPEED

    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game.game_over:
                    if event.key == pygame.K_r:
                        game.restart()
                elif game.paused:
                    if event.key == pygame.K_p:
                        game.toggle_pause()
                else:
                    if event.key == pygame.K_LEFT:
                        game.move_left()
                    elif event.key == pygame.K_RIGHT:
                        game.move_right()
                    elif event.key == pygame.K_UP:
                        game.rotate()
                    elif event.key == pygame.K_DOWN:
                        game.move_down()
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                    elif event.key == pygame.K_c:
                        game.hold()
                    elif event.key == pygame.K_p:
                        game.toggle_pause()
                    elif event.key == pygame.K_r:
                        game.restart()

        # 自动下落
        if not game.paused and not game.game_over:
            dt = renderer.tick()
            fall_time += dt
            if fall_time >= game.fall_speed:
                game.update()
                fall_time = 0

        # 渲染
        renderer.render(game)

    # 记录游戏退出
    logger.exit()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()