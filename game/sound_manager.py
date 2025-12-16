import pygame
import os


class SoundManager:
    """Упрощенный менеджер звуков"""

    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        self.music_enabled = True
        self.volume = 0.5

    def load_sounds(self):
        """Загрузка звуков"""
        sounds_path = "assets/sounds"

        if not os.path.exists(sounds_path):
            return False

        for file in os.listdir(sounds_path):
            if file.endswith('.wav') or file.endswith('.mp3'):
                name = file.split('.')[0]
                try:
                    path = os.path.join(sounds_path, file)
                    self.sounds[name] = pygame.mixer.Sound(path)
                except:
                    pass

        return len(self.sounds) > 0

    def preload(self):
        """Инициализация звука"""
        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except:
                self.sound_enabled = False
                self.music_enabled = False
                return False

        return self.load_sounds()

    def play_sound(self, name):
        """Воспроизведение звука"""
        if self.sound_enabled and name in self.sounds:
            try:
                self.sounds[name].play()
            except:
                pass

    def play_music(self, loop=-1):
        """Воспроизведение музыки"""
        if self.music_enabled:
            try:
                music_path = "assets/sounds/background.mp3"
                if os.path.exists(music_path):
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.volume * 0.3)
                    pygame.mixer.music.play(loop)
                    self.music_playing = True
            except:
                pass

    def set_volume(self, volume):
        """Установка громкости"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume * 0.3)

        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def toggle_sound(self):
        """Переключение звуков"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def toggle_music(self):
        """Переключение музыки"""
        self.music_enabled = not self.music_enabled

        if self.music_enabled and not self.music_playing:
            self.play_music()
        elif not self.music_enabled and self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

        return self.music_enabled

    def stop_music(self):
        """Остановка музыки"""
        pygame.mixer.music.stop()
        self.music_playing = False