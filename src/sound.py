# -*- coding: utf-8 -*-
"""音效系统模块"""
import array
import math
from typing import Optional

import pygame


class SoundManager:
    """音效管理器

    使用pygame生成合成音效，无需外部音频文件。
    """

    _instance: Optional['SoundManager'] = None
    _initialized: bool = False

    # 音效参数配置
    SOUND_CONFIG = {
        'move': {'frequency': 440, 'duration': 50, 'volume': 0.3},
        'rotate': {'frequency': 523, 'duration': 80, 'volume': 0.3},
        'drop': {'frequency': 330, 'duration': 100, 'volume': 0.4},
        'clear': {'frequency': 660, 'duration': 150, 'volume': 0.5},
        'tetris': {'frequency': 880, 'duration': 300, 'volume': 0.6},  # 消除4行
        'game_over': {'frequency': 220, 'duration': 500, 'volume': 0.5},
        'level_up': {'frequency': 1047, 'duration': 200, 'volume': 0.5},
    }

    def __new__(cls) -> 'SoundManager':
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化音效管理器"""
        if self._initialized:
            return

        self._initialized = True
        self.enabled = True
        self.sounds = {}

        # 初始化音频系统
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self._create_sounds()
        except pygame.error:
            # 音频系统不可用
            self.enabled = False

    def _create_sounds(self):
        """创建所有音效"""
        for name, config in self.SOUND_CONFIG.items():
            try:
                sound = self._generate_tone(
                    config['frequency'],
                    config['duration'],
                    config['volume']
                )
                self.sounds[name] = sound
            except (pygame.error, OSError):
                pass

    def _generate_tone(self, frequency: int, duration_ms: int, volume: float) -> pygame.mixer.Sound:
        """生成单音音效

        Args:
            frequency: 频率 (Hz)
            duration_ms: 持续时间 (毫秒)
            volume: 音量 (0.0-1.0)

        Returns:
            pygame Sound对象
        """
        sample_rate = 44100
        n_samples = int(sample_rate * duration_ms / 1000)

        # 生成正弦波
        buf = []
        for i in range(n_samples):
            # 使用正弦波生成
            t = i / sample_rate
            # 添加淡入淡出效果
            envelope = 1.0
            fade_samples = int(sample_rate * 0.01)  # 10ms淡入淡出
            if i < fade_samples:
                envelope = i / fade_samples
            elif i > n_samples - fade_samples:
                envelope = (n_samples - i) / fade_samples

            value = int(32767 * volume * envelope * math.sin(2 * math.pi * frequency * t))
            buf.append(value)

        # 创建立体声音频
        sound_array = array.array('h', buf)

        try:
            return pygame.mixer.Sound(buffer=sound_array)
        except pygame.error:
            # 回退：创建空声音
            return pygame.mixer.Sound(buffer=array.array('h', [0] * 100))

    def play(self, sound_name: str):
        """播放音效

        Args:
            sound_name: 音效名称
        """
        if not self.enabled:
            return

        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass

    def toggle(self) -> bool:
        """切换音效开关

        Returns:
            当前音效状态
        """
        self.enabled = not self.enabled
        return self.enabled

    def set_enabled(self, enabled: bool):
        """设置音效开关

        Args:
            enabled: 是否启用
        """
        self.enabled = enabled


# 全局音效管理器实例
sound_manager = SoundManager()
