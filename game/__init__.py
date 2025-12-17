"""Пакет game - основной игровой модуль для игры Moti Runner.

Содержит все основные классы и компоненты игры: базовые объекты, игрока,
препятствия, управление игрой, загрузку спрайтов и звуков.
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

print("Игровой пакет game загружен")