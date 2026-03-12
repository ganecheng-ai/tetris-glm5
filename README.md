# Tetris 俄罗斯方块 🎮

一个使用 Python 和 Pygame 开发的经典俄罗斯方块游戏，支持简体中文界面，画面精美。

![Tetris Screenshot](https://via.placeholder.com/400x500?text=Tetris+Game)

## ✨ 特性

- 🎮 经典俄罗斯方块玩法
- 🎨 精美的渐变方块效果
- 🇨🇳 简体中文界面
- 👻 幽灵方块预览落点
- 📦 支持保持方块功能
- 📊 分数、等级、消行统计
- 🏆 高分记录持久化保存
- 📝 完善的日志系统
- 🔊 合成音效系统（支持开关）
- 🖥️ 跨平台支持 (Windows, Linux, macOS)

## 🎯 操作说明

| 按键 | 功能 |
|------|------|
| ← | 左移 |
| → | 右移 |
| ↑ | 旋转 |
| ↓ | 软降（加速下落） |
| 空格 | 硬降（直接落到底部） |
| C | 保持方块 |
| P | 暂停/继续 |
| R | 重新开始 |
| M | 音效开关 |
| ESC | 退出游戏 |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Pygame 2.5.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行游戏

```bash
python -m src.tetris
```

或者

```bash
cd src
python tetris.py
```

## 📦 下载

请访问 [Releases](https://github.com/ganecheng-ai/tetris-glm5/releases) 页面下载最新版本的可执行文件。

### 支持的平台

- Windows (x64): `tetris-windows-x64.exe`
- Linux (x64): `tetris-linux-x64`
- macOS (x64): `tetris-macos-x64`

## 🏗️ 构建项目

```bash
pip install pyinstaller
python build.py
```

## 📁 项目结构

```
tetris-glm5/
├── src/
│   ├── __init__.py       # 包初始化
│   ├── tetris.py         # 游戏主程序
│   ├── blocks.py         # 方块定义
│   ├── game.py           # 游戏逻辑
│   ├── renderer.py       # 渲染器
│   ├── constants.py      # 常量定义
│   ├── logger.py         # 日志系统
│   ├── sound.py          # 音效系统
│   └── high_score.py     # 高分系统
├── logs/                  # 日志文件目录
├── data/                  # 游戏数据（高分记录）
├── assets/
│   └── fonts/            # 字体文件
├── tests/
│   └── test_game.py      # 单元测试
├── .github/
│   └── workflows/
│       └── release.yml   # 发布工作流
├── prompt.md             # 指令文件
├── plan.md               # 开发计划
├── README.md             # 项目说明
├── requirements.txt       # Python依赖
└── build.py              # 构建脚本
```

## 🎮 游戏规则

1. 使用方向键移动和旋转方块
2. 填满一行即可消除该行并获得分数
3. 同时消除多行可获得更高分数
4. 每10行提升一个等级，速度加快
5. 方块堆到顶部游戏结束

### 计分规则

| 消除行数 | 分数 |
|----------|------|
| 1 行 | 100 |
| 2 行 | 300 |
| 3 行 | 500 |
| 4 行 | 800 |

## 📝 开发计划

详见 [plan.md](plan.md)

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**Made with ❤️ by Claude Code**