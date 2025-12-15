"""
Пакет game - содержит все игровые классы для Moti Runner
"""

from .base_object import BaseObject
from .player import Player
from .obstacle import Obstacle
from .game_manager import GameManager
from .sprite_loader import SpriteLoader
from .sound_manager import SoundManager

__all__ = [
    'BaseObject',
    'Player',
    'Obstacle',
    'GameManager',
    'SpriteLoader',
    'SoundManager'
]

print("✅ Игровой пакет game загружен")