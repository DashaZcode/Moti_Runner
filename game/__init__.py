"""Пакет game - основной игровой модуль для игры Moti Runner.

Этот пакет содержит все основные классы и компоненты игры:
- Базовые игровые объекты
- Игрока и его поведение
- Препятствия
- Управление игрой
- Загрузку спрайтов и звуков

Модули:
    base_object: Базовый класс для всех игровых объектов
    player: Класс игрока, управляемого пользователем
    obstacle: Класс препятствий на игровом поле
    game_manager: Основной менеджер игры
    sprite_loader: Загрузчик и обработчик спрайтов
    sound_manager: Менеджер звуков и музыки
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