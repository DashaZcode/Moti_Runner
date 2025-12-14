import pygame

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

    #функция для отражения каждого спрайта !!!инструмент!!!
    def flip_sprites(sprites, flip_x=False, flip_y=False):
        return [pygame.transform.flip(sprite, flip_x, flip_y) for sprite in sprites]
    #transform - модуль для преобразования, flip - отразить
    #анимация бега влево = [
        #кадр1 бег влево,   отражённая версия
        #кадр2 бег влево,... отражённая версия
    # ]

