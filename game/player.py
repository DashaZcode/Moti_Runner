import pygame
from .base_object import BaseObject
from .sprite_loader import SpriteLoader
import os


class Player(BaseObject) :
    def __init__(self, x, y, width=80, height=80, color=(0, 255, 0), jump_height=350, gravity=900) :
        super().__init__(x, y, width, height, color)
        self.jump_speed = -jump_height  # Отрицательная для подъёма
        self.velocity_y = 0
        self.gravity = gravity
        self.is_jumping = False
        self.ground_y = y  # Уровень земли
        self.load_sprites()  # Загрузка анимаций
        self.set_animation('run')  # Старт с бега

    def load_sprites(self) :
        assets_path = SpriteLoader.get_assets_path()
        player_path = os.path.join(assets_path, 'player')
        if os.path.exists(player_path) :
            # Анимация бега (предполагаем run1.png, run2.png)
            run_files = [f for f in os.listdir(player_path) if f.startswith('run')]
            self.sprites['run'] = [SpriteLoader.load_sprite(os.path.join(player_path, f)) for f in sorted(run_files)]
            # Спрайт прыжка (jump.png)
            jump_file = os.path.join(player_path, 'jump.png')
            if os.path.exists(jump_file) :
                self.sprites['jump'] = [SpriteLoader.load_sprite(jump_file)]  # Одна картинка для прыжка

    def update(self, dt, keys) :
        super().update(dt)

        # Прыжок
        if keys[pygame.K_SPACE] and not self.is_jumping :
            self.velocity_y = self.jump_speed
            self.is_jumping = True
            self.set_animation('jump', reset=True)

        # Гравитация и падение
        self.velocity_y += self.gravity * dt
        self.rect.y += self.velocity_y * dt

        # Возврат на землю
        if self.rect.y >= self.ground_y :
            self.rect.y = self.ground_y
            self.velocity_y = 0
            self.is_jumping = False
            self.set_animation('run')  # Возврат к бегу

    def collides_with(self, other) :
        hitbox = self.rect.inflate(-20, -30)  # Можно подогнать: -20 по ширине, -30 по высоте (чтобы ноги/голова не цепляли)
        hitbox.y += 15  # Сдвигаем хитбокс чуть вниз (если нужно, чтобы прыжок над низкими препятствиями работал лучше)
        return hitbox.colliderect(other.rect)

