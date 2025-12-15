import pygame
from .sprite_loader import SpriteLoader


class BaseObject:
    """Базовый класс для всех игровых объектов"""

    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        """
        Инициализация базового объекта

        Args:
            x (int): X координата
            y (int): Y координата
            width (int): Ширина объекта
            height (int): Высота объекта
            color (tuple): Цвет по умолчанию (RGB)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.width = width  # ← ВЕРНУЛИ!
        self.height = height  # ← ВЕРНУЛИ!
        self.sprite = None
        self.sprites = {}
        self.current_animation = None
        self.animation_frame = 0
        self.animation_timer = 0

    def load_sprite(self, sprite_path):
        """Загрузка основного спрайта для объекта"""
        self.sprite = SpriteLoader.load_sprite(sprite_path, self.width, self.height)

    def set_animation(self, animation_name, reset=True):
        if animation_name in self.sprites and self.sprites[animation_name]:
            self.current_animation = animation_name
            if reset:
                self.animation_frame = 0
                self.animation_timer = 0

    def update_animation(self, dt):
        """Обновление анимации"""
        if self.current_animation and self.current_animation in self.sprites:
            self.animation_timer += dt
            if self.animation_timer >= 0.15:  # Фиксированное время кадра
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % len(self.sprites[self.current_animation])

    def draw(self, screen):
        """Отрисовка объекта"""
        if self.current_animation and self.current_animation in self.sprites:
            frames = self.sprites[self.current_animation]
            screen.blit(frames[self.animation_frame], self.rect)
        elif self.sprite:
            screen.blit(self.sprite, self.rect)


    def update(self, dt):
        """Обновление состояния объекта"""
        self.update_animation(dt)

    def collides_with(self, other):
        """Проверка столкновения с другим объектом"""
        return self.rect.colliderect(other.rect)