import pygame
import os
from .sprite_loader import SpriteLoader

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.background_music = None
        try:
            pygame.mixer.init()  # Пытаемся инициализировать звук
            self.load_sounds()
            print("Звук успешно инициализирован")
        except pygame.error as e:
            print(f"Не удалось инициализировать звук: {e}")
            print("Игра продолжит работу без звуков и музыки")
            # Просто продолжаем без звука

    def load_sounds(self):
        assets_path = SpriteLoader.get_assets_path()
        sounds_path = os.path.join(assets_path, 'sounds')
        if os.path.exists(sounds_path):
            for file in os.listdir(sounds_path):
                if file.endswith(('.wav', '.mp3', '.ogg')):
                    name = os.path.splitext(file)[0]
                    try:
                        self.sounds[name] = pygame.mixer.Sound(os.path.join(sounds_path, file))
                    except:
                        pass  # Если файл плохой — пропускаем

    def play(self, name):
        if name in self.sounds:
            try:
                self.sounds[name].play()
            except:
                pass

    def play_background(self, name, loops=-1):
        if name in self.sounds:
            try:
                self.background_music = self.sounds[name]
                self.background_music.play(loops=loops)
            except:
                pass

    def stop_background(self):
        try:
            if self.background_music:
                self.background_music.stop()
        except:
            pass