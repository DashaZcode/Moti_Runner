import pygame
from .player import Player
from .obstacle import Obstacle
from .sprite_loader import SpriteLoader
from .sound_manager import SoundManager


class GameManager:

    def __init__(self, screen_width=1200, screen_height=800, initial_speed=400):

        #сохраняем ширину экрана в атрибуте объекта
        self.screen_width = screen_width
        #высоту
        self.screen_height = screen_height
        #определяем высоту, если выота всего экрана=800, то ground_y находится выше=700
        self.ground_y = screen_height - 100

        #згрузка фоновых спрайтов
        self.background_sprites = self.load_background_sprites()

        #инициализация звуковой системы
        self.sound_manager = SoundManager()
        self.sound_manager.preload()

        #создаем игрока
        self.player = Player(100, self.ground_y)
        #создает игрока на позиции:
        #x=100px пикселей от левого края
        #y=self.ground_y на уровне земли

        #игровые параметры
        self.obstacles = [] #список препятсвий
        self.clouds = [] #список облаков
        self.score = 0 #начальный счет игрока
        self.lives = 3  #жизни
        self.game_speed = initial_speed #скорость или по уомлчанию или пользовательская
        self.game_over = False #флаг заврешения игры
        self.is_paused = True #флаг паузы, игра на паузе
        self.obstacle_timer = 0 #таймер для генерации препятствий, время с последнего созданного препятствия
        self.cloud_timer = 0 #таймер для облаков
        self.obstacle_interval = 1.5 #Каждые 1.5 секунды будет появляться новое препятствие
        self.speed_increase_interval = 5 #каждые 5 набраных очков скорость будет увеличиваться

        #шрифты
        self.font = pygame.font.SysFont(None, 48) #обычный шрифт всего текста
        self.big_font = pygame.font.SysFont(None, 96) #шрифт для большого текста

        self.ui_sprites = self.load_ui_sprites() #загрузка UI спрайтов

        self.create_initial_clouds() #создаем начальные облака

        self.sound_manager.play_music() #запуск фоновой музыки
