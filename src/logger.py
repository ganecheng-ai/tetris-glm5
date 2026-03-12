# -*- coding: utf-8 -*-
"""日志系统模块"""
import logging
import os
from datetime import datetime
from typing import Optional


class GameLogger:
    """游戏日志记录器

    提供游戏运行时的日志记录功能，便于问题定位和分析。
    """

    _instance: Optional['GameLogger'] = None
    _initialized: bool = False

    def __new__(cls) -> 'GameLogger':
        """单例模式，确保只有一个日志实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化日志记录器"""
        if self._initialized:
            return

        self._initialized = True
        self.logger = logging.getLogger('tetris')
        self.logger.setLevel(logging.DEBUG)

        # 清除已有的处理器
        self.logger.handlers.clear()

        # 日志目录
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)

        # 日志文件名（按日期）
        log_filename = datetime.now().strftime('tetris_%Y%m%d.log')
        log_path = os.path.join(self.log_dir, log_filename)

        # 文件处理器
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message: str):
        """记录信息级别日志

        Args:
            message: 日志消息
        """
        self.logger.info(message)

    def debug(self, message: str):
        """记录调试级别日志

        Args:
            message: 日志消息
        """
        self.logger.debug(message)

    def warning(self, message: str):
        """记录警告级别日志

        Args:
            message: 日志消息
        """
        self.logger.warning(message)

    def error(self, message: str):
        """记录错误级别日志

        Args:
            message: 日志消息
        """
        self.logger.error(message)

    def game_start(self):
        """记录游戏开始"""
        self.info("=" * 40)
        self.info("游戏启动")
        self.info("=" * 40)

    def game_over(self, score: int, level: int, lines: int):
        """记录游戏结束

        Args:
            score: 最终分数
            level: 最终等级
            lines: 消除行数
        """
        self.info("-" * 40)
        self.info(f"游戏结束 - 分数: {score}, 等级: {level}, 消除: {lines}行")
        self.info("-" * 40)

    def level_up(self, level: int):
        """记录等级提升

        Args:
            level: 新等级
        """
        self.info(f"等级提升! 当前等级: {level}")

    def lines_cleared(self, count: int, score: int):
        """记录消除行

        Args:
            count: 消除行数
            score: 当前分数
        """
        self.debug(f"消除 {count} 行, 当前分数: {score}")

    def score_update(self, score: int):
        """记录分数更新

        Args:
            score: 当前分数
        """
        self.debug(f"分数更新: {score}")

    def pause(self):
        """记录游戏暂停"""
        self.info("游戏暂停")

    def resume(self):
        """记录游戏继续"""
        self.info("游戏继续")

    def restart(self):
        """记录游戏重新开始"""
        self.info("游戏重新开始")

    def hold_block(self, block_type: str):
        """记录保持方块

        Args:
            block_type: 方块类型
        """
        self.debug(f"保持方块: {block_type}")

    def hard_drop(self, distance: int):
        """记录硬降

        Args:
            distance: 下落距离
        """
        self.debug(f"硬降: {distance}格")

    def exit(self):
        """记录游戏退出"""
        self.info("游戏退出")


# 全局日志实例
logger = GameLogger()
