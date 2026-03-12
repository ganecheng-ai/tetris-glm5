# -*- coding: utf-8 -*-
"""高分记录模块"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class HighScoreManager:
    """高分记录管理器

    管理游戏高分记录的存储和加载，支持持久化保存。
    """

    _instance: Optional['HighScoreManager'] = None
    _initialized: bool = False

    MAX_SCORES = 10  # 保存最高10条记录

    def __new__(cls) -> 'HighScoreManager':
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """初始化高分管理器"""
        if self._initialized:
            return

        self._initialized = True
        self.scores: List[Dict] = []
        self._data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self._score_file = os.path.join(self._data_dir, 'high_scores.json')
        self._load_scores()

    def _load_scores(self):
        """从文件加载高分记录"""
        os.makedirs(self._data_dir, exist_ok=True)

        if os.path.exists(self._score_file):
            try:
                with open(self._score_file, 'r', encoding='utf-8') as f:
                    self.scores = json.load(f)
            except (json.JSONDecodeError, OSError):
                self.scores = []
        else:
            self.scores = []

    def _save_scores(self):
        """保存高分记录到文件"""
        os.makedirs(self._data_dir, exist_ok=True)
        try:
            with open(self._score_file, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def add_score(self, score: int, level: int, lines: int) -> int:
        """添加新的分数记录

        Args:
            score: 分数
            level: 等级
            lines: 消除行数

        Returns:
            排名位置（1开始），如果未进入排行榜返回0
        """
        new_record = {
            'score': score,
            'level': level,
            'lines': lines,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        # 查找插入位置
        rank = 0
        for i, record in enumerate(self.scores):
            if score > record['score']:
                self.scores.insert(i, new_record)
                rank = i + 1
                break

        # 如果没有找到更低的分数，追加到末尾
        if rank == 0 and len(self.scores) < self.MAX_SCORES:
            self.scores.append(new_record)
            rank = len(self.scores)

        # 限制记录数量
        if len(self.scores) > self.MAX_SCORES:
            self.scores = self.scores[:self.MAX_SCORES]

        self._save_scores()
        return rank

    def get_high_scores(self) -> List[Dict]:
        """获取高分列表

        Returns:
            高分记录列表
        """
        return self.scores.copy()

    def get_top_score(self) -> int:
        """获取最高分

        Returns:
            最高分，如果没有记录返回0
        """
        if self.scores:
            return self.scores[0]['score']
        return 0

    def is_high_score(self, score: int) -> bool:
        """检查分数是否能进入排行榜

        Args:
            score: 要检查的分数

        Returns:
            是否能进入排行榜
        """
        if len(self.scores) < self.MAX_SCORES:
            return True
        return score > self.scores[-1]['score']

    def clear_scores(self):
        """清除所有高分记录"""
        self.scores = []
        self._save_scores()


# 全局高分管理器实例
high_score_manager = HighScoreManager()
