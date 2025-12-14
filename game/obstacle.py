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

            #!!! другие объекты!!!
            all_files = os.listdir(obstacles_path) #загружаем спрайты
            sprite_files = [] #создаем список не для спрайтов птицы

            for file_name in all_files: #если спрайт не птрицы, добавляем его в список
                if file_name.lower() != 'bird.png':
                    sprite_files.append(file_name)

            if sprite_files:
                sprite_file = os.path.join(obstacles_path, random.choice(sprite_files))
                sprite = SpriteLoader.load_sprite(sprite_file)
                if sprite:
                    self.sprite = sprite

                    self.rect.width = self.sprite.get_width()
                    self.rect.height = self.sprite.get_height()

    def create_random(screen_width, ground_y, speed):
        #screen_width - заданная ширина экрана пользователем
        #ground_y расположение земли

        #определяем тип препятствия (40% шанс на птицу)
        is_bird = random.random() < 0.40

        if is_bird:
            #если птица
            width = 60
            height = 40
            color = (255, 255, 255)
            y = ground_y - random.randint(200, 250) #задаем на оси y, на какой высоте она будет появлятся
            obstacle_type = 'bird'
        else:
            #кость на земле
            width = random.randint(170, 200)
            height = random.randint(170, 200)
            color = (255, 255, 255)
            y = ground_y - 10
            obstacle_type = None

        x = screen_width + width
        #screen_width=1200, width=50 -> x=1250
        #gрепятствие появится на 1250px 50px за правым краем экрана 1200px

        return Obstacle(x, y, width, height, color, speed, obstacle_type)

    def update(self, dt): #движение препятсвий влево
        self.rect.x = self.rect.x - self.speed * dt
    #=speed=300px/сек, dt=0.016сек - 300 * 0.016 = 4.8px
    #за один кадр препятствие сдвинется на 4.8 пикселя влево
