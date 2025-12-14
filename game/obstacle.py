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

    def load_obstacle_sprite(self):
        assets_path = SpriteLoader.get_assets_path() #получаем путь к папке assets
        obstacles_path = os.path.join(assets_path, 'obstacles') #объединяем путь к папке с перепятсвиями "C:\projects\moti_runner\assets\obstacles"

        if os.path.exists(obstacles_path): #есть ли путь к файлу
            if self.obstacle_type == 'bird':
                sprite_file = os.path.join(obstacles_path, "bird.png")

                if os.path.exists(sprite_file):
                    sprite = SpriteLoader.load_sprite(sprite_file)

                    if sprite:
                        self.sprite = sprite #загрузили картинку
                        self.is_flying = True #летающая птица

                        self.rect.width = self.sprite.get_width() #возвращает ширину спрайта в пикселях
                        self.rect.height = self.sprite.get_height() #высоту
                        return
    