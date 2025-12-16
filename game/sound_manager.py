import pygame
import os


class SoundManager:
    """Упрощенный менеджер звуков"""

    def __init__(self):     # Инициализация менеджера звуков с настройками по умолчанию
        self.sounds = {}    # Словарь для хранения загруженных звуковых эффектов
        self.music_playing = False     # Флаг: играет ли фоновая музыка сейчас
        self.sound_enabled = True      # Флаг: включены ли звуковые эффекты
        self.music_enabled = True      # Флаг: включена ли фоновая музыка
        self.volume = 0.5              # Общая громкость от 0.0 (тихо) до 1.0 (максимум)

    def load_sounds(self):
        """Загрузка звуков"""
        sounds_path = "assets/sounds"     # Путь к папке со звуками

        if not os.path.exists(sounds_path):     # Проверяем, существует ли папка со звуками
            return False      # Если папки нет - возвращаем ошибку

        for file in os.listdir(sounds_path):       # Проходим по всем файлам в папке
            if file.endswith('.wav') or file.endswith('.mp3'):       # Фильтруем только звуковые файлы (wav или mp3)
                name = file.split('.')[0]      # Извлекаем имя звука без расширения (например, "jump" из "jump.wav")
                try:
                    path = os.path.join(sounds_path, file)      # Собираем полный путь к файлу
                    self.sounds[name] = pygame.mixer.Sound(path)     # Загружаем звук и сохраняем в словарь
                except:
                    pass     # Если не удалось загрузить файл - пропускаем его

        return len(self.sounds) > 0      # Возвращаем True если хотя бы один звук был загружен

    def preload(self):
        """Инициализация звука"""
        if not pygame.mixer.get_init():     # Проверяем, инициализирован ли микшер pygame (звуковая система)
            try:
                pygame.mixer.init()     # Пытаемся инициализировать звуковую систему
            except:                     # Если не удалось - отключаем все звуки
                self.sound_enabled = False
                self.music_enabled = False
                return False      # Возвращаем ошибку

        return self.load_sounds()      # Загружаем звуковые эффекты

    def play_sound(self, name):
        """Воспроизведение звука"""
        if self.sound_enabled and name in self.sounds:     # Проверяем: включены ли звуки и есть ли такой звук в словаре
            try:
                self.sounds[name].play()     # Воспроизводим звук
            except:
                pass      # Если не удалось воспроизвести - игнорируем ошибку

    def play_music(self, loop=-1):
        """Воспроизведение музыки"""
        if self.music_enabled:    # Проверяем, включена ли музыка
            try:
                music_path = "assets/sounds/background.mp3"    # Путь к файлу фоновой музыки
                if os.path.exists(music_path):    # Проверяем существование файла
                    pygame.mixer.music.load(music_path)       # Загружаем музыку
                    pygame.mixer.music.set_volume(self.volume * 0.3)    # Устанавливаем громкость (музыка тише звуков)
                    # Воспроизводим музыку
                    # loop=-1 означает бесконечное повторение
                    pygame.mixer.music.play(loop)
                    self.music_playing = True    # Устанавливаем флаг, что музыка играет
            except:
                pass     # Если не удалось загрузить или воспроизвести музыку

    def set_volume(self, volume):
        """Установка громкости"""
        self.volume = max(0.0, min(1.0, volume))     # Ограничиваем громкость в диапазоне от 0.0 до 1.0
        pygame.mixer.music.set_volume(self.volume * 0.3)    # Устанавливаем громкость музыки (делаем её тише звуков)

        for sound in self.sounds.values():    # Устанавливаем громкость для всех звуковых эффектов
            sound.set_volume(self.volume)

    def toggle_sound(self):
        """Переключение звуков"""
        self.sound_enabled = not self.sound_enabled    # Меняем состояние на противоположное
        return self.sound_enabled     # Возвращаем новое состояние

    def toggle_music(self):
        """Переключение музыки"""
        self.music_enabled = not self.music_enabled    # Меняем состояние музыки на противоположное

        if self.music_enabled and not self.music_playing:     # Если музыку включили и она не играет - запускаем
            self.play_music()
        elif not self.music_enabled and self.music_playing:   # Если музыку выключили и она играет - останавливаем
            pygame.mixer.music.stop()
            self.music_playing = False

        return self.music_enabled    # Возвращаем новое состояние

    def stop_music(self):
        """Остановка музыки"""
        pygame.mixer.music.stop()    # Останавливаем воспроизведение музыки
        self.music_playing = False    # Сбрасываем флаг воспроизведения
    