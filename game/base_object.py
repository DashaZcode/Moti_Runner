"""Модуль base_object - базовый класс для всех игровых объектов.

Содержит класс BaseObject, который предоставляет общую функциональность
для всех игровых объектов: геометрию, анимации, коллизии и отрисовку.
"""

import pygame
from .sprite_loader import SpriteLoader


class BaseObject:
    """Базовый класс для всех игровых объектов.

    Предоставляет общую функциональность для игровых объектов:
    - Геометрию и позиционирование
    - Анимации и спрайты
    - Коллизии
    - Отрисовку

    Attributes:
        rect (pygame.Rect): Прямоугольник, хранящий геометрию объекта.
            Система координат начинается в верхнем левом углу экрана.
        color (tuple): Цвет объекта в формате RGB.
        width (int): Ширина объекта в пикселях.
        height (int): Высота объекта в пикселях.
        sprite (pygame.Surface): Текущий спрайт объекта.
        sprites (dict): Словарь для хранения нескольких анимаций.
            Ключ - имя анимации, значение - список кадров.
        current_animation (str): Имя текущей анимации (например, "бег").
        animation_frame (int): Индекс текущего кадра анимации.
        animation_timer (float): Таймер для смены кадров анимации.
    """

    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        """Инициализация базового объекта.

        Args:
            x (int): Координата X левого верхнего угла.
            y (int): Координата Y левого верхнего угла.
            width (int): Ширина объекта.
            height (int): Высота объекта.
            color (tuple, optional): Цвет объекта в формате RGB. 
                По умолчанию белый (255, 255, 255).
        """
        self.rect = pygame.Rect(x, y, width, height)  # хранит геометрию объекта
        #система координат начинается в верхнем левом углу экрана
        self.color = color  # атрибут цвета, или по умолчанию белый
        self.width = width  # ширина объекта
        self.height = height  # высота объекта

        self.sprite = None  # для хранения спрайта в будущем
        self.sprites = {}  # для хранения нескольких анимаций
        self.current_animation = None  # какая анимация "бег"

        self.animation_frame = 0  # индекс анмации "1"
        self.animation_timer = 0  # таймер для анимации

    def load_sprite(self, sprite_path):
        """Загружает спрайт из файла.

        Используется для загрузки спрайта объекта.

        Args:
            sprite_path (str): Путь к файлу спрайта.
        """
        self.sprite = SpriteLoader.load_sprite(sprite_path, self.width, self.height)

    def set_animation(self, animation_name, reset=True):  # изначальное True сброс анимации
        """Устанавливает текущую анимацию.

        Для проигрывания анимаций начиная с текущего.

        Args:
            animation_name (str): Имя анимации для установки.
            reset (bool, optional): Сбрасывать ли анимацию к началу.
                По умолчанию True (сброс анимации).
        """
        if animation_name in self.sprites and self.sprites[
            animation_name]:  # если анимация есть имени анимаций и у нее есть хотябы 1 кадр
            self.current_animation = animation_name  # устанавливаем текущую анимацию
            if reset:  # если нужно сбросить анимауию. Всегда да.
                self.animation_frame = 0  # сбро на 1 индекс кадра анимации
                self.animation_timer = 0  # сброс таймера проигрывания анимации 1 кадра (то есть, чтобы 1 кадр анимации не сбрасывался сразу)

    def update_animation(self, dt):  # dt - время, прошедшее с прошлого кдра, обычно 0.016
        """Обновляет анимацию объекта.

        Args:
            dt (float): Время, прошедшее с прошлого кадра, обычно 0.016 секунды.
        """
        if self.current_animation and self.current_animation in self.sprites:
            self.animation_timer += dt

            if self.animation_timer >= 0.15:  # если текущий кадр показывался уже 0.15 секунды или больше
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % len(self.sprites[self.current_animation])
                # self.animation_frame + 1 - увеличивыем индекс кадра - берем следующий кадр
                # self.sprites[self.current_animation] - узнаем количество кадров в списке self.sprites["run"] = [кадр1, кадр2], len = 2
                ## Для анимации с 2 кадрами:
                # 0 % 2 = 0
                # 1 % 2 = 1
                # 2 % 2 = 0 - вернулись к началу
                # (0 + 1) % 2 = 1 % 2 = 1
                # ...

    def draw(self, screen):  # screen - поверхность, где рисуются объекты
        """Отрисовывает объект на экране.

        Args:
            screen (pygame.Surface): Поверхность, где рисуются объекты.
        """
        if self.current_animation and self.current_animation in self.sprites:  # проверка есть ли анимация, и есть ли она в словаре
            frames = self.sprites[
                self.current_animation]  # получаем список кадров frames = self.sprites["run"]  # = [кадр0, кадр1]
            screen.blit(frames[self.animation_frame], self.rect)
            # bit - рисует одну картинку на другой
            # рисует текущий кадр в self.rect
            # self.rect.x, self.rect.y = координаты
            # self.rect.width, self.rect.height = размеры
            # frames[0]

        elif self.sprite:  # если у нас один спрайт, то рисуем его
            screen.blit(self.sprite, self.rect)

    def collides_with(self, other):
        """Проверка столкновения с другим объектом colliderect.
        Args:
            other (BaseObject): Другой объект для проверки столкновения.
        Returns:
            bool: True если объекты пересекаются, False если нет.
        """
        return self.rect.colliderect(other.rect)
        # self.rect - текущий объект сталкивается с другим other.rect

    def update(self, dt):  # вызывает родительский метод update_animation для создания дочерних методов
        """Обновляет состояние объекта.
        Вызывает родительский метод update_animation для создания дочерних методов.
        Args:
            dt (float): Время, прошедшее с прошлого кадра.
        """
        self.update_animation(dt)
