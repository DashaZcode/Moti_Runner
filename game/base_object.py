import pygame
from .sprite_loader import SpriteLoader

class BaseObject:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):

        self.rect = pygame.Rect(x, y, width, height) #хранит геометрию объекта
        #Система координат начинается в верхнем левом углу экрана
        self.color = color #атрибут цвета, или по умолчанию белый
        self.width = width #ширина объекта
        self.height = height #высота объекта

        self.sprite = None #для хранения спрайта в будущем
        self.sprites = {} #для хранения нескольких анимаций
        self.current_animation = None #какая анимация "бег"

        self.animation_frame = 0 #индекс анмации "1"
        self.animation_timer = 0 #таймер для анимации

    #используся для загрузки спрайта объекта
    def load_sprite(self, sprite_path):
        self.sprite = SpriteLoader.load_sprite(sprite_path, self.width, self.height)

    #для проигрывания анимаций начиная с текщего
    def set_animation(self, animation_name, reset=True): #изначальное True сброс анимации
        if animation_name in self.sprites and self.sprites[animation_name]: #если анимация есть имени анимаций и у нее есть хотябы 1 кадр
            self.current_animation = animation_name #устанавливаем текущую анимацию
            if reset: #если нужно сбросить анимауию. Всегда да.
                self.animation_frame = 0 #берем 1 кадр анимации
                self.animation_timer = 0 #сброс таймера проигрывания анимации 1 кадра (то есть, чтобы 1 кадр анимации не сбрасывался сразу)
