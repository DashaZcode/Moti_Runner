import pygame
from .player import Player
from .obstacle import Obstacle
from .sprite_loader import SpriteLoader
from .sound_manager import SoundManager
import os


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

    def load_background_sprites(self): #загрузка фоновых спрайтов

        assets_path = SpriteLoader.get_assets_path()
        background_path = os.path.join(assets_path, 'background')

        sprites = {
            'ground': None, #оземля, пока не загружено
            'cloud': None, #облака
            'mountain': None #горы
        }

        #ЗАГРУЖАЕМ ФАЙЛЫ В СЛОВАРЬ
        #земля
        ground_file = os.path.join(background_path, 'ground.png')
        sprites['ground'] = SpriteLoader.load_sprite(ground_file)

        #облако
        cloud_file = os.path.join(background_path, 'cloud.png')
        sprites['cloud'] = SpriteLoader.load_sprite(cloud_file, 150, 90)

        #горы
        mountain_file = os.path.join(background_path, 'mountain.png')
        sprites['mountain'] = SpriteLoader.load_sprite(mountain_file, 300, 225)

        return sprites

    def load_ui_sprites(self): #Загрузка UI спрайтов

        assets_path = SpriteLoader.get_assets_path()
        ui_path = os.path.join(assets_path, 'ui')

        sprites = {
            'heart': None, #сердце
            'game_over': None, #сердце
        }

        #сердечко для жизней
        heart_file = os.path.join(ui_path, 'heart.png')
        sprites['heart'] = SpriteLoader.load_sprite(heart_file, 45, 45)

        #game Over
        game_over_file = os.path.join(ui_path, 'game_over.png')
        sprites['game_over'] = SpriteLoader.load_sprite(game_over_file, 600, 150)

        return sprites