import pygame
import os


class SpriteLoader:
    def load_sprite(path, width=None, height=None):
        sprite = pygame.image.load(path)

        if sprite.get_alpha() is None:
            sprite = sprite.convert()
        else:
            sprite = sprite.convert_alpha()

        if width and height:
            sprite = pygame.transform.scale(sprite, (width, height))

        return sprite

    load_sprite = staticmethod(load_sprite)

    #функция для отражения каждого спрайта
    def flip_sprites(sprites, flip_x=False, flip_y=False):
        return [pygame.transform.flip(sprite, flip_x, flip_y) for sprite in sprites]

    flip_sprites = staticmethod(flip_sprites)

    def get_assets_path():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.join(current_dir, '..', 'assets')

        return assets_path

    get_assets_path = staticmethod(get_assets_path)