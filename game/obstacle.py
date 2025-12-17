"""Модуль obstacle - классы препятствий для игры.

Содержит класс Obstacle, представляющий различные типы препятствий
(летающие и наземные), с функциональностью для случайной генерации
и специальных хитбоксов.
"""

import pygame
import random
import os
from .base_object import BaseObject
from .sprite_loader import SpriteLoader

class Obstacle(BaseObject):
    """Класс препятствий для игры Moti Runner.

    Наследуется от BaseObject и добавляет специфичную для препятствий функциональность:
    - Движение слева направо
    - Разные типы препятствий (летающие и наземные)
    - Случайную генерацию
    - Специальные хитбоксы для разных типов препятствий

    Attributes:
        speed (int): Скорость движения препятствий влево.
        passed (bool): Флаг пройденых препятствий. True - игрок получил очко после прохождения препятствия.
        obstacle_type (str): Тип препятствия. Может быть 'bird' для птиц или None для наземных.
        is_flying (bool): True если это птица, False если наземное препятствие.
    """

    def __init__(self, x, y, width=60, height=80, color=(200, 50, 50), speed=300, obstacle_type=None):
        """Инициализация препятствия.

        Args:
            x (int): Координата X левого верхнего угла.
            y (int): Координата Y левого верхнего угла.
            width (int, optional): Ширина препятствия. По умолчанию 60.
            height (int, optional): Высота препятствия. По умолчанию 80.
            color (tuple, optional): Цвет препятствия в формате RGB.
                По умолчанию (200, 50, 50).
            speed (int, optional): Скорость движения препятствий влево.
                По умолчанию 300.
            obstacle_type (str, optional): Тип препятствия. Может быть 'bird' или None.
                По умолчанию None.
        """

        super().__init__(x, y, width, height, color) #унаследовал атрибуты и методы с родительского класса BaseObject
        self.speed = speed #скорость движения препятствий влево
        self.passed = False #флаг пройденых препятсвий True - получает очко после прохождения препятсвия
        self.obstacle_type = obstacle_type #обработка препятсивй птица ЛЕТИТ, кость СТОИТ
        self.is_flying = False #True если это птица, False если наземное препятствие

        #загружает картинку препятствия из файла и сохраняет в self.sprite
        self.load_obstacle_sprite()

    def load_obstacle_sprite(self):
        """Загружает спрайт препятствия из файла.

        Ищет файлы в папке assets/obstacles и загружает соответствующий спрайт.
        Для птиц использует файл bird.png, для других препятствий выбирает случайный файл.
        """
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
                sprite_file = os.path.join(obstacles_path, random.choice(sprite_files)) #рандомизируем появление объекта
                sprite = SpriteLoader.load_sprite(sprite_file)
                if sprite:
                    self.sprite = sprite

                    self.rect.width = self.sprite.get_width()
                    self.rect.height = self.sprite.get_height()

    def create_random(screen_width, ground_y, speed):
        #screen_width - заданная ширина экрана пользователем
        #ground_y расположение земли
        """Создает случайное препятствие.

        Args:
            screen_width (int): Заданная ширина экрана пользователем.
            ground_y (int): Расположение земли (координата Y уровня земли).
            speed (int): Скорость движения препятствия.

        Returns:
            Obstacle: Новый объект препятствия со случайными параметрами.

        Notes:
            - 40% шанс на птицу
            - Птицы появляются в воздухе на случайной высоте
            - Наземные препятствия (кости) появляются на уровне земли
            - Препятствие создается за правым краем экрана
        """

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
        """Обновляет позицию препятствия.

        Движение препятствий влево.

        Args:
            dt (float): Время, прошедшее с прошлого кадра.

        Example:
            self.rect.x = 1250 за гарницей, speed=300px/сек, dt=0.016сек - 300 * 0.016 = 4.8px
            За один кадр препятствие сдвинется на 4.8 пикселя влево
        """
        self.rect.x = self.rect.x - self.speed * dt
    #self.rect.x = 1250 за гарницей, speed=300px/сек, dt=0.016сек - 300 * 0.016 = 4.8px
    #за один кадр препятствие сдвинется на 4.8 пикселя влево

    def is_offscreen(self): #проверка, вышло ли препятствие за левую границу
        """Проверяет, вышло ли препятствие за левую границу экрана.

        Returns:
            bool: True если препятствие полностью вышло за левый край экрана.

        Note:
            Если объект позиция меньше чем позиция за границой (-), то значит объект вышел за границу.
            50px - справа, -50px слева
        """
        return self.rect.x < -self.rect.width
        #если объект позиця меньше чем позиция за границой (-), то значит объект вышел за границу 50px - справа, -50px слева

    def draw(self, screen): #рисуем препятствие
        """Рисует препятствие на экране.

        Args:
            screen (pygame.Surface): Игровое окно, на котором рисуем.
        """
        #screen - игровое окно, на котомром рисуем
        if self.sprite: #если есть в спрайтах
            screen.blit(self.sprite, self.rect)

    def collides_with(self, other): #проверка столкновения с другим объектом.
        """Проверка столкновения с другим объектом.

        Создает разные хитбоксы для разных типов препятствий.

        Args:
            other (BaseObject): Другой объект для проверки столкновения.

        Returns:
            bool: True если объекты пересекаются с учетом хитбокса.

        Notes:
            - Для птиц: уменьшенный хитбокс (-25, -25)
            - Для наземных препятствий: уменьшенный и смещенный вниз хитбокс
        """
        # !!!создаем хитбоксы
        if self.is_flying:
            #птица
            bird_hitbox = self.rect.inflate(-25, -25) #уменьшаем размер по сравнению с оригиналом
            return bird_hitbox.colliderect(other.rect) #возвращаем столкновение
        else:
            #кости
            ground_hitbox = self.rect.inflate(-30, -20)
            ground_hitbox.y += 15
            return ground_hitbox.colliderect(other.rect)
