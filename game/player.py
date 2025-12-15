import pygame
import os
from .base_object import BaseObject
from .sprite_loader import SpriteLoader


class Player(BaseObject):

    def __init__(self, x, y, width=90, height=120):
        super().__init__(x, y, width, height, (255, 100, 100))

        # Физика
        self.gravity = 1800
        self.jump_force = -1000
        self.velocity_y = 0
        self.is_jumping = False
        self.ground_y = y

        # Неуязвимость после получения урона
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.blink_timer = 0
        self.visible = True

        # Загрузка спрайтов
        self.load_player_sprites()

        # Начальная анимация
        self.set_animation("run")

        # Параметры анимации
        self.animation_frame_time = 0.15

    def load_player_sprites(self):
        """Загрузка всех спрайтов игрока"""
        assets_path = SpriteLoader.get_assets_path()
        player_path = os.path.join(assets_path, 'player')

        # Анимация бега
        run_sprites = []
        for i in range(1, 3):
            sprite_file = os.path.join(player_path, f"run{i}.png")
            sprite = SpriteLoader.load_sprite(sprite_file, self.width, self.height)
            if sprite:
                run_sprites.append(sprite)

        if run_sprites:
            self.sprites["run"] = run_sprites

        # Спрайт прыжка
        jump_sprite = os.path.join(player_path, "jump.png")
        sprite = SpriteLoader.load_sprite(jump_sprite, self.width, self.height)
        if sprite:
            self.sprites["jump"] = [sprite]

        # Если спрайтов нет, создаем цветные прямоугольники
        if not any(self.sprites.values()):
            self._create_fallback_sprites()

    def _create_fallback_sprites(self):
        """Создание простой графики если нет спрайтов"""
        # Анимация бега
        run_sprite1 = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(run_sprite1, (255, 100, 100),
                            (0, 0, self.width, self.height))
        pygame.draw.ellipse(run_sprite1, (255, 150, 150),
                            (10, 10, self.width - 20, self.height - 20))

        run_sprite2 = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(run_sprite2, (255, 120, 120),
                            (0, 0, self.width, self.height))
        pygame.draw.ellipse(run_sprite2, (255, 170, 170),
                            (5, 5, self.width - 10, self.height - 10))

        self.sprites["run"] = [run_sprite1, run_sprite2]

        # Прыжок
        jump_sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(jump_sprite, (255, 100, 100),
                            (0, 0, self.width, self.height))
        pygame.draw.circle(jump_sprite, (255, 150, 150),
                           (self.width // 2, self.height // 2),
                           self.width // 3)
        self.sprites["jump"] = [jump_sprite]

    def jump(self):
        """Прыжок игрока"""
        if not self.is_jumping and not self.invulnerable:
            self.velocity_y = self.jump_force
            self.is_jumping = True
            self.set_animation("jump")

    def update(self, dt):
        """Обновление физики игрока"""
        # Применяем гравитацию
        self.velocity_y += self.gravity * dt

        # Обновляем позицию
        self.rect.y += self.velocity_y * dt

        # Проверяем, стоит ли игрок на земле
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.velocity_y = 0
            self.is_jumping = False

            if self.current_animation != "run":
                self.set_animation("run")

        # Обновляем анимацию
        super().update_animation(dt)

    def update_invulnerability(self, dt):
        """Обновление состояния неуязвимости"""
        if self.invulnerable:
            self.invulnerable_timer -= dt
            self.blink_timer += dt

            # Мерцание каждые 0.1 секунды
            if self.blink_timer >= 0.1:
                self.visible = not self.visible
                self.blink_timer = 0

            # Конец неуязвимости
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.visible = True

    def draw(self, screen):
        """Отрисовка игрока с учетом неуязвимости"""
        if not self.invulnerable or (self.invulnerable and self.visible):
            super().draw(screen)

    def reset(self):
        """Сброс состояния игрока"""
        self.rect.y = self.ground_y
        self.velocity_y = 0
        self.is_jumping = False
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.visible = True
        self.set_animation("run")