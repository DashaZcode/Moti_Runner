import pygame
import random
import os
from .base_object import BaseObject
from .sprite_loader import SpriteLoader

class Obstacle(BaseObject):

    def __init__(self, x, y, width=60, height=80, color=(200, 50, 50), speed=300, obstacle_type=None):

        super().__init__(x, y, width, height, color) #унаследовал атрибуты и методы с родительского класса BaseObject
        self.speed = speed #скорость движения препятствий влево
        self.passed = False #флаг пройденых препятсвий True - получает очко после прохождения препятсвия
        self.obstacle_type = obstacle_type #обработка препятсивй птица ЛЕТИТ, кость СТОИТ
        self.is_flying = False #True если это птица, False если наземное препятствие

        #загружает картинку препятствия из файла и сохраняет в self.sprite
        self.load_obstacle_sprite()

    