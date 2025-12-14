import pygame
import os

class SpriteLoader:
    def load_sprite(path, width=None, height=None):
        #path - путь к файлу изображения
        sprite = pygame.image.load(path) #атрибут для хранения изображения

        if sprite.get_alpha() is None: #если файл прозрачный возвращает 255, если нет 0. Если непрозрачный
            sprite = sprite.convert() #конвертируем без прозрачности

        else: #если файл имеет прозрачность
            sprite = sprite.convert_alpha() # конвентируем как прозрачный

        if width and height:
            sprite = pygame.transform.scale(sprite, (width, height))
        # для всех файлов, если не указан размер, то он останется изначальным. Если указан, то он будет менять размер на указанный
        return sprite

    load_sprite = staticmethod(load_sprite)

    #функция для отражения каждого спрайта !!!инструмент!!!
    def flip_sprites(sprites, flip_x=False, flip_y=False):
        return [pygame.transform.flip(sprite, flip_x, flip_y) for sprite in sprites]
    #transform - модуль для преобразования, flip - отразить
    #анимация бега влево = [
        #кадр1 бег влево,   отражённая версия
        #кадр2 бег влево,... отражённая версия
    # ]
    flip_sprites = staticmethod(flip_sprites)

    #инструмент для получения пути
    def get_assets_path():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        #os.path.dirname получаем папку, где лежит файл - "C:\project\game\run.py" → "C:\project\game\"
        #получаем путь и делаем его абсолютым(от корня до фала) - "run.py" → "C:\project\game\run.py"

        assets_path = os.path.join(current_dir, '..', 'assets') #выходим в родительску папку и получаем путь с assets
        #os.path.join("C:\project\game\", "..", "assets") → "C:\project\assets"
        return assets_path

    get_assets_path = staticmethod(get_assets_path)
