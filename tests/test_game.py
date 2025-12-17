"""Модуль test_game - тесты для игровых компонентов.

Содержит юнит-тесты для проверки корректности работы
основных классов игры: BaseObject, Obstacle, Player и других.
"""

import unittest
import pygame
from game.base_object import BaseObject
from game.obstacle import Obstacle
from game.player import Player
from game.sound_manager import SoundManager

class TestBaseObject(unittest.TestCase):
    def test_collides_with(self):    # Тестирование обнаружения столкновений между объектами
        # Создаем два объекта, которые частично пересекаются
        obj1 = BaseObject(0, 0, 50, 50)            # Квадрат в левом верхнем углу
        obj2 = BaseObject(25, 25, 50, 50)          # Квадрат со смещением (пересекаются)
        # Проверяем, что объекты пересекаются - должно быть True
        self.assertTrue(obj1.collides_with(obj2))  # Пересечение
        # Создаем третий объект далеко от первого
        obj3 = BaseObject(100, 100, 50, 50)      # Квадрат в другом месте
        # Проверяем, что объекты НЕ пересекаются - должно быть False
        self.assertFalse(obj1.collides_with(obj3))  # Нет пересечения

    def test_update_animation(self):      # Тестирование анимации объектов
        obj = BaseObject(0, 0, 50, 50)     # Создаем объект с анимацией
        # Создаем тестовые кадры анимации (два одинаковых спрайта)
        obj.sprites = {'run': [pygame.Surface((50,50)), pygame.Surface((50,50))]}
        obj.set_animation('run')      # Устанавливаем анимацию "бег"
        # Первое обновление анимации (больше порога смены кадра 0.15)
        obj.update_animation(0.2)  # >0.15, frame 1
        self.assertEqual(obj.animation_frame, 1)    # Проверяем, что переключился на второй кадр (индекс 1)
        # Второе обновление анимации
        obj.update_animation(0.2)  # frame 0
        self.assertEqual(obj.animation_frame, 0)    # Проверяем, что вернулись к первому кадру (индекс 0)

class TestObstacle(unittest.TestCase):
    def test_create_random(self):     # Тестирование создания случайного препятствия
        # Создаем случайное препятствие:
        # 800 - ширина экрана, 500 - высота земли, 300 - скорость игры
        obs = Obstacle.create_random(800, 500, 300)
        self.assertGreater(obs.rect.x, 799)            # Проверяем, что препятствие создано за правым краем экрана
        self.assertIn(obs.obstacle_type, [None, 'bird'])          # Проверяем, что тип препятствия корректный (None - обычное, 'bird' - птица)

    def test_update(self):     # Тестирование движения препятствий
        obs = Obstacle(100, 100, speed=300)      # Создаем препятствие на позиции (100, 100) со скоростью 300
        obs.update(0.1)      # Обновляем состояние на 0.1 секунду
        # Проверяем, что препятствие сдвинулось влево:
        # 300 * 0.1 = 30 пикселей, поэтому 100 - 30 = 70
        self.assertEqual(obs.rect.x, 100 - 30)  # 300 * 0.1 = 30

    def test_collides_with_hitbox(self):     # Тестирование столкновений с учетом хитбокса
        obs = Obstacle(0, 0, 100, 100, obstacle_type='bird')       # Создаем препятствие типа 'bird'
        other = BaseObject(10, 10, 50, 50)       # Создаем другой объект, который пересекается с препятствием
        self.assertTrue(obs.collides_with(other))  # Проверяем, что столкновение обнаруживается (с учетом хитбокса)

class TestPlayer(unittest.TestCase):
    def setUp(self):       # Настройка перед каждым тестом - создаем игрока
        self.player = Player(0, 400, jump_height=200, gravity=500)    # x=0, y=400 (высота земли), высота прыжка 200, гравитация 500

    def test_jump(self):
        keys = {pygame.K_SPACE: True}     # Создаем словарь нажатых клавиш (пробел нажат)
        self.player.update(0.016, keys)     # Обновляем состояние игрока
        self.assertTrue(self.player.is_jumping)     # Проверяем, что игрок в состоянии прыжка
        self.assertLess(self.player.rect.y, 400)    # Проверяем, что игрок поднялся выше начальной позиции

    def test_gravity(self):
        self.player.velocity_y = -100    # Устанавливаем начальную вертикальную скорость
        self.player.update(0.016, {})     # Обновляем без нажатых клавиш
        self.assertGreater(self.player.velocity_y, -100)  # Проверяем, что гравитация увеличила скорость (сделала менее отрицательной)

    def test_land(self):    # Тестирование приземления игрока
        self.player.rect.y = 500  # Устанавливаем игрока ниже уровня земли (должен приземлиться)
        self.player.update(0.016, {})    # Обновляем состояние
        self.assertEqual(self.player.rect.y, self.player.ground_y)      # Проверяем, что игрок вернулся на уровень земли
        self.assertFalse(self.player.is_jumping)      # Проверяем, что игрок больше не в состоянии прыжка

class TestSoundManager(unittest.TestCase):      # Тесты для менеджера звуков
    def test_load_sounds(self):     # Тестирование загрузки звуков
        sm = SoundManager()         # Создаем менеджер звуков
        self.assertIsInstance(sm.sounds, dict)  # Звуки загружены (если папка существует)

    def test_play_nonexistent(self):    # Тестирование воспроизведения несуществующего звука
        sm = SoundManager()
        # Нет exception, просто ничего не играет. Тест проверяет, что не возникает исключение
        sm.play('nonexistent')  # Не должно падать

class TestHeart(unittest.TestCase):     # Тесты для класса сердечек (бонусных жизней)
    def test_create_random(self):       # Тестирование создания случайного сердечка
        # Проверяем, что сердечко создаётся за правым краем экрана
        heart = Heart.create_random(800, 500)     # Ширина 800, высота земли 500
        self.assertGreater(heart.rect.x, 799)     # Проверяем, что сердечко за правым краем экрана
        self.assertLess(heart.rect.y, 500 - 100)  # Проверяем, что сердечко не ниже земли
        self.assertGreater(heart.rect.y, 500 - 300)      # Проверяем, что сердечко не слишком высоко

    def test_update(self):      # Тестирование движения сердечка
        # Проверяем движение влево
        heart = Heart(800, 300, size=40)
        heart.speed = 300  # Явно задаём скорость
        heart.update(0.1)  # 0.1 секунды
        expected_x = 800 - 300 * 0.1   # Рассчитываем ожидаемую позицию: 300 px/s * 0.1s = 30 px влево
        self.assertAlmostEqual(heart.rect.x, expected_x, delta=1)

    def test_is_offscreen(self):      # Тестирование проверки выхода за границы экрана
        # За левым краем — offscreen
        heart_off = Heart(-50, 300, size=40)
        self.assertTrue(heart_off.is_offscreen())      # Должно быть True

        # На экране — не offscreen
        heart_on = Heart(400, 300, size=40)
        self.assertFalse(heart_on.is_offscreen())       # Должно быть False

    def test_collides_with_player(self):
        # Создаём фейковый игрок
        player = Player(100, 400)
        heart = Heart(110, 410, size=40)  # Создаем сердечко, которое пересекается с игроком
        self.assertTrue(player.collides_with(heart))     # Должно быть True

        heart_no = Heart(200, 410, size=40)   # Создаем сердечко, которое НЕ пересекается с игроком
        self.assertFalse(player.collides_with(heart_no))    # Должно быть False

if __name__ == '__main__':
    unittest.main()

