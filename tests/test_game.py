import unittest
import pygame
from game.base_object import BaseObject
from game.obstacle import Obstacle
from game.player import Player
from game.sound_manager import SoundManager

class TestBaseObject(unittest.TestCase):
    def test_collides_with(self):
        obj1 = BaseObject(0, 0, 50, 50)
        obj2 = BaseObject(25, 25, 50, 50)
        self.assertTrue(obj1.collides_with(obj2))  # Пересечение
        obj3 = BaseObject(100, 100, 50, 50)
        self.assertFalse(obj1.collides_with(obj3))  # Нет пересечения

    def test_update_animation(self):
        obj = BaseObject(0, 0, 50, 50)
        obj.sprites = {'run': [pygame.Surface((50,50)), pygame.Surface((50,50))]}
        obj.set_animation('run')
        obj.update_animation(0.2)  # >0.15, frame 1
        self.assertEqual(obj.animation_frame, 1)
        obj.update_animation(0.2)  # frame 0
        self.assertEqual(obj.animation_frame, 0)

class TestObstacle(unittest.TestCase):
    def test_create_random(self):
        obs = Obstacle.create_random(800, 500, 300)
        self.assertGreater(obs.rect.x, 799)  # За экраном
        self.assertIn(obs.obstacle_type, [None, 'bird'])

    def test_update(self):
        obs = Obstacle(100, 100, speed=300)
        obs.update(0.1)
        self.assertEqual(obs.rect.x, 100 - 30)  # 300 * 0.1 = 30

    def test_collides_with_hitbox(self):
        obs = Obstacle(0, 0, 100, 100, obstacle_type='bird')
        other = BaseObject(10, 10, 50, 50)
        self.assertTrue(obs.collides_with(other))  # С хитбоксом

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(0, 400, jump_height=200, gravity=500)

    def test_jump(self):
        keys = {pygame.K_SPACE: True}
        self.player.update(0.016, keys)
        self.assertTrue(self.player.is_jumping)
        self.assertLess(self.player.rect.y, 400)  # Поднялся

    def test_gravity(self):
        self.player.velocity_y = -100
        self.player.update(0.016, {})
        self.assertGreater(self.player.velocity_y, -100)  # Гравитация добавлена

    def test_land(self):
        self.player.rect.y = 500  # Ниже ground
        self.player.update(0.016, {})
        self.assertEqual(self.player.rect.y, self.player.ground_y)
        self.assertFalse(self.player.is_jumping)

class TestSoundManager(unittest.TestCase):
    def test_load_sounds(self):
        sm = SoundManager()
        self.assertIsInstance(sm.sounds, dict)  # Звуки загружены (если папка существует)

    def test_play_nonexistent(self):
        sm = SoundManager()
        # Нет exception, просто ничего не играет
        sm.play('nonexistent')  # Не должно падать

if __name__ == '__main__':
    unittest.main()

