import pygame
import os
from .base_object import BaseObject
from .sprite_loader import SpriteLoader


class Player(BaseObject):   # Класс игрока, управдяемого пользователем

    def __init__(self, x, y, width=90, height=120):    # Инициализация игрока
        # Вызываем конструктор родительского класса BaseObject
        # с начальной позицией, размером и цветом по умолчанию
        super().__init__(x, y, width, height, (255, 100, 100))

        # Физика
        self.gravity = 1800    # Сила гравитации (пикселей в секунду в квадрате)
        self.jump_force = -1000   # Сила прыжка (отрицательная - вверх)
        self.velocity_y = 0      # Вертикальная скорость
        self.is_jumping = False      # Флаг: находится ли игрок в прыжке
        self.ground_y = y       # Уровень земли (исходная позиция по Y)

        # Неуязвимость после получения урона
        self.invulnerable = False  # Флаг неуязвимости
        self.invulnerable_timer = 0  # Таймер действия неуязвимости
        self.blink_timer = 0  # Таймер для мерцания (мигания)
        self.visible = True  # Флаг видимости для мерцания

        # Загрузка графических спрайтов
        self.load_player_sprites()

        # Начальная анимация
        self.set_animation("run")

        # Параметры анимации
        self.animation_frame_time = 0.15    # Время между кадрами анимации (секунды)

    def load_player_sprites(self):
        """Загрузка всех спрайтов игрока"""
        # Получаем путь к папке с ресурсами игры
        assets_path = SpriteLoader.get_assets_path()
        # Формируем путь к папке со спрайтами игрока
        player_path = os.path.join(assets_path, 'player')

        # Анимация бега
        run_sprites = []  # Список для хранения кадров анимации бега
        for i in range(1, 3) :  # Ожидаем файлы run1.png и run2.png
            sprite_file = os.path.join(player_path, f"run{i}.png")
            # Пытаемся загрузить и масштабировать спрайт
            sprite = SpriteLoader.load_sprite(sprite_file, self.width, self.height)
            if sprite :  # Если спрайт успешно загружен
                run_sprites.append(sprite)

        if run_sprites:      # Если удалось загрузить спрайты бега - сохраняем их
            self.sprites["run"] = run_sprites

        # Спрайт прыжка
        jump_sprite = os.path.join(player_path, "jump.png")
        sprite = SpriteLoader.load_sprite(jump_sprite, self.width, self.height)
        if sprite:
            self.sprites["jump"] = [sprite]     # Спрайт прыжка - один кадр

        # Если не удалось загрузить ни одного спрайта
        if not any(self.sprites.values()):
            self._create_fallback_sprites()     # Создаем простую графику (запасной вариант)

    def _create_fallback_sprites(self):
        """Создание простой графики если нет спрайтов"""
        # Анимация бега - первый кадр
        run_sprite1 = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Рисуем эллипс (тело игрока)
        pygame.draw.ellipse(run_sprite1, (255, 100, 100),
                            (0, 0, self.width, self.height))
        # Рисуем внутренний эллипс (акцент)
        pygame.draw.ellipse(run_sprite1, (255, 150, 150),
                            (10, 10, self.width - 20, self.height - 20))

        # Анимация бега - второй кадр (немного отличается)
        run_sprite2 = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(run_sprite2, (255, 120, 120),
                            (0, 0, self.width, self.height))
        pygame.draw.ellipse(run_sprite2, (255, 170, 170),
                            (5, 5, self.width - 10, self.height - 10))

        self.sprites["run"] = [run_sprite1, run_sprite2]    # Сохраняем кадры анимации бега

        # Прыжок
        jump_sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.ellipse(jump_sprite, (255, 100, 100),
                            (0, 0, self.width, self.height))
        # Рисуем круг внутри эллипса
        pygame.draw.circle(jump_sprite, (255, 150, 150),
                           (self.width // 2, self.height // 2),
                           self.width // 3)
        self.sprites["jump"] = [jump_sprite]

    def jump(self):
        """Прыжок игрока"""
        # Проверяем условия для прыжка:
        # 1. Игрок не в прыжке
        # 2. Игрок не в состоянии неуязвимости
        if not self.is_jumping and not self.invulnerable :
            self.velocity_y = self.jump_force  # Придаем скорость вверх
            self.is_jumping = True  # Устанавливаем флаг прыжка
            self.set_animation("jump")  # Переключаем на анимацию прыжка

    def update(self, dt):
        """Обновление физики игрока"""
        # Применяем гравитацию - увеличиваем вертикальную скорость
        self.velocity_y += self.gravity * dt

        # Обновляем позицию - двигаем игрока по вертикали
        self.rect.y += self.velocity_y * dt

        # Проверяем, стоит ли игрок на земле
        if self.rect.y >= self.ground_y:    # Если игрок ниже уровня земли - ставим его на землю
            self.rect.y = self.ground_y
            self.velocity_y = 0  # Сбрасываем скорость
            self.is_jumping = False  # Сбрасываем флаг прыжка

            if self.current_animation != "run":     # Если не проигрывается анимация бега - переключаемся на нее
                self.set_animation("run")

        # Обновляем анимацию    (вызываем метод родительского класса)
        super().update_animation(dt)

    def update_invulnerability(self, dt):
        """Обновление состояния неуязвимости"""
        if self.invulnerable :  # Если игрок в состоянии неуязвимости
            # Уменьшаем таймер неуязвимости
            self.invulnerable_timer -= dt
            # Увеличиваем таймер мерцания
            self.blink_timer += dt

            # Мерцание каждые 0.1 секунды
            if self.blink_timer >= 0.1 :
                self.visible = not self.visible  # Переключаем видимость
                self.blink_timer = 0  # Сбрасываем таймер мерцания

            # Если время неуязвимости истекло
            if self.invulnerable_timer <= 0 :
                self.invulnerable = False  # Выключаем неуязвимость
                self.visible = True  # Гарантируем видимость

    def draw(self, screen):
        """Отрисовка игрока с учетом неуязвимости"""
        # Рисуем игрока только если:
        # 1. Он не неуязвим, ИЛИ
        # 2. Он неуязвим, но сейчас должен быть виден (мерцание)
        if not self.invulnerable or (self.invulnerable and self.visible) :
            super().draw(screen)      # Вызываем метод отрисовки родительского класса


    def reset(self):
            """Сброс состояния игрока"""
            self.rect.y = self.ground_y  # Возвращаем на уровень земли
            self.velocity_y = 0  # Сбрасываем скорость
            self.is_jumping = False  # Сбрасываем флаг прыжка
            self.invulnerable = False  # Выключаем неуязвимость
            self.invulnerable_timer = 0  # Сбрасываем таймер неуязвимости
            self.visible = True  # Гарантируем видимость
            self.set_animation("run")  # Устанавливаем анимацию бега
