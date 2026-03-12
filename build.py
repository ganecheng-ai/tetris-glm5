# -*- coding: utf-8 -*-
"""构建脚本"""
import PyInstaller.__main__
import os
import sys


def build():
    """构建可执行文件"""
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(current_dir, "src", "tetris.py")

    # PyInstaller 参数
    args = [
        main_script,
        "--name=tetris",
        "--onefile",
        "--windowed",
        "--clean",
    ]

    # macOS 特定参数
    if sys.platform == "darwin":
        args.append("--osx-bundle-identifier=com.tetris.game")

    # 执行构建
    PyInstaller.__main__.run(args)


if __name__ == "__main__":
    build()