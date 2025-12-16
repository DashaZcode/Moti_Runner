import pygame
from .player import Player
from .obstacle import Obstacle
from .sprite_loader import SpriteLoader
from .sound_manager import SoundManager
import os
import random


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

    def create_initial_clouds(self): #создание начальных облаков
        for _ in range(5): #цикл 5 раз без переменной
            x = random.randint(0, self.screen_width)
            #случайное расположение облаков от 0 до ширины экрана
            #сли screen_width=1200, x может быть любым

            #генерируем сучайную высоту и скорость
            y = random.randint(50, 300)
            speed = random.randint(30, 70)

            #добавляем новое облако в список self.clouds
            self.clouds.append({'x': x, 'y': y, 'speed': speed})

    def handle_events(self): #обработка событий

        #йикл for, который проходит по ВСЕМ событиям в очереди событий pygame
        for event in pygame.event.get():

            #если это событие закрытия окна QUIT
            if event.type == pygame.QUIT:
                #возвращаем False - завершение
                return False

            #если событие нажатие на клавиатуру KEYDOWN
            elif event.type == pygame.KEYDOWN:

                #Если это ПРОБЕЛ, игра НЕ закончена (not self.game_over), игра НЕ на паузе (not self.is_paused)
                if event.key == pygame.K_SPACE and not self.game_over and not self.is_paused:
                    #воспроизводим звук прыжка
                    self.sound_manager.play_sound('jump')
                    #вызываем метод jump() для прыжка
                    self.player.jump()

                #если нажата клавиша R (K_r) И игра закончена
                elif event.key == pygame.K_r and self.game_over:
                    #звук кнопки
                    self.sound_manager.play_sound('button')
                    #перезапускаем игру
                    self.reset_game()

                #если нажата клавиша ESC
                elif event.key == pygame.K_ESCAPE:
                    #возвращаем False для выхода из игры
                    return False

                #если нажата клавиша P (K_p)
                elif event.key == pygame.K_p:
                    #переключаем состояние паузы включить/выключить
                    self.toggle_pause()

        #если ни одно из событий не привело к выходу из игры, возвращаем True, чтобы главный цикл продолжил работу
        return True

    def toggle_pause(self): #включение/выключение паузы
        self.is_paused = not self.is_paused #нажимаем клавишу P, вызывается toggle_pause():
        if self.is_paused:
            self.sound_manager.play_sound('pause')
            print("Пауза")
        else:
            self.sound_manager.play_sound('resume')
            print("Игра работает")

    def update(self, dt): #игра
        if self.game_over or self.is_paused: #если на паузе или игрок умер, выходим из мтеода
            return

        #вызываем игрока и пишем его время
        self.player.update(dt)

        #накапливает время с момента создания последнего препятствия
        self.obstacle_timer += dt

        #если накопленое время превышает 1.5 интервал
        if self.obstacle_timer >= self.obstacle_interval:
             #добавляет новый объект в конце списка
            self.obstacles.append(Obstacle.create_random(self.screen_width, self.ground_y, self.game_speed))
            self.obstacle_timer = 0 #сбрасывает таймер препятствия в 0, чтобы начать отсчет до следующего препятствия

        #обновляем препятствия
        for obstacle in self.obstacles[:]: #копируем список для удаления препятсвий
            obstacle.update(dt) #перпятсвие движется влево каждый кадр

            if self.player.collides_with(obstacle): #если грок столкнулся с препятствием
                self.sound_manager.play_sound('collision')
                self.lives -= 1  #уменьшаем жизни

                #удаляем препятствие при столкновении
                self.obstacles.remove(obstacle)

                if self.lives <= 0: #если 0 жиней
                    self.game_over = True #заканчиваем игру
                    return
                else:
                    #игрок получает неуязвимость после потери жизни
                    self.player.invulnerable = True #игрок не может получать урон
                    self.player.invulnerable_timer = 1.0  #1 секунда неуязвимости

            #увеличиваем счет, если прошли препятствие

            #Правая сторона препятствия ЛЕВЕЕ левой стороны игрока
            if not obstacle.passed and obstacle.rect.x + obstacle.rect.width < self.player.rect.x:
                #obstacle.passed - препятствие еще не пройдено
                #obstacle.rect.x + obstacle.rect.width -  левая координата препятствия + ширина препятствия = правая координата препятствия
                # < self.player.rect.x - левая координата игрока
                obstacle.passed = True
                self.score += 1
                self.sound_manager.play_sound('score')

                #увеличиваем скорость каждые n очков
                if self.score % self.speed_increase_interval == 0:
                    #Если счет делится без остатка на интервалл, увеличиваем скорость
                    self.game_speed += 50
                    self.obstacle_interval = max(1.0, self.obstacle_interval - 0.05)
                    #eменьшаем интервал между препятствиями на 0.05 секунды
                    #max(1.0, ...) - гарантирует что интервал не станет меньше 1.0 секунды

            #удаляем препятствия за экраном
            if obstacle.is_offscreen():
                self.obstacles.remove(obstacle)

        #обновляем игрока неуязвимость
        self.player.update_invulnerability(dt)


    def draw_background(self, screen):
        #screen - игровок окно
        #фон
        for y in range(self.screen_height):
            #pапускает цикл по всем горизонтальным строкам экрана — от y = 0 (самый верх)
            #до y = self.screen_height - 1 самый низ
            color = (255, 200, 255)
            pygame.draw.line(screen, color, (0, y), (self.screen_width, y))
            #рисует горизонтальную линию
            #от точки (0, y) (левый край строки) до (self.screen_width, y) (правый край строки)

        #горы
        if self.background_sprites['mountain']:
            for i in range(4):
                x = i * 400  #рисуем горы 4 раза
                screen.blit(self.background_sprites['mountain'], (x, self.ground_y - 225))
                #рисуем по левой границе горизонтали x на высоте475px (1200 - 225) ОТ ВВЕРХА ЭКРАНА

        #облака
        cloud_sprite = self.background_sprites['cloud']
        for cloud in self.clouds:
            if cloud_sprite:
                screen.blit(cloud_sprite, (cloud['x'], cloud['y']))
        #self.clouds = [
        #{'x': 500, 'y': 100, 'speed': 40},  Облако 1
        #{'x': 300, 'y': 200, 'speed': 60},  Облако 2
        #береберам список заромандезированных облаков

        #земля
        if self.background_sprites['ground']:
            ground_width = self.background_sprites['ground'].get_width() #запрос ширины картинки
            #цикл для рисования земли от левого до правого края экран
            #ground_width = 200 (ширина картинки земли)
            # self.screen_width = 1200 (ширина экрана)
            #for x in range(0, 1200, 200):

            for x in range(0, self.screen_width, ground_width):
                #self.screen_width - ширина экрана
                #ширина картинки
                screen.blit(self.background_sprites['ground'], (x, self.ground_y)) #от левого края от вверхнеего края 700
                # (то есть внизу займет 100 пикслей)

    #рисуем все
    def draw(self, screen):
        #фон
        self.draw_background(screen)

        #препятствия
        for obstacle in self.obstacles:
            obstacle.draw(screen)

        #игрок
        self.player.draw(screen)

        #HUD
        self.draw_hud(screen)

        #Game Over
        if self.game_over:
            self.draw_game_over(screen)
        #пауза
        elif self.is_paused:
            self.draw_pause_menu(screen)


    def draw_hud(self, screen) :
        # Создаем текст с текущим счетом розовым цветом
        score_text = self.font.render(f'SCORE: {self.score}', True, (200, 100, 150))
        screen.blit(score_text, (30, 30))        # Рисуем текст в левом верхнем углу (координаты 30, 30)

        # Преобразуем скорость в целое число для отображения
        speed_text = self.font.render(f'SPEED: {int(self.game_speed)}', True, (200, 100, 150))
        screen.blit(speed_text, (30, 80))         # Рисуем под счетом (с отступом 50 пикселей по вертикали)

        # Отображаем количество оставшихся жизней
        lives_text = self.font.render(f'LIVES: {self.lives}', True, (200, 100, 150))
        screen.blit(lives_text, (30, 130))       # Рисуем под скоростью

        # Отображение сердечек
        if self.ui_sprites['heart'] :         # Проверяем, есть ли спрайт сердца в словаре UI-спрайтов
            for i in range(self.lives) :
                screen.blit(self.ui_sprites['heart'], (250 + i * 50, 125))              # Рисуем сердечки по количеству жизней (каждое сердце - 50 пикселей правее предыдущего) справа от текста с жизнями

        # Управление - УБИРАЕМ DOWN - Duck
        # Список подсказок по управлению
        controls = [
            "SPACE - Jump",
            "P - Pause",
            "R - Restart",
            "ESC - Quit"
        ]

        # Рисуем каждую подсказку в правом верхнем углу
        for i, control in enumerate(controls) :
            text = self.font.render(control, True, (220, 140, 190))         # Создаем текст для каждой команды управления
            screen.blit(text, (self.screen_width - text.get_width() - 30, 30 + i * 50))         # Располагаем справа с отступом 30 пикселей от края
                                                                                             # Выравниваем по правому краю, вычитая ширину текста

        # Индикатор паузы
        # Если игра на паузе - показываем большой текст "PAUSED" по центру
        if self.is_paused :
            pause_text = self.big_font.render("PAUSED", True, (255, 100, 150))
            screen.blit(pause_text,                      # Центрируем текст по горизонтали и вертикали
                        (self.screen_width // 2 - pause_text.get_width() // 2,
                         self.screen_height // 2 - 50))

    def draw_pause_menu(self, screen) :
        # Полупрозрачный overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((50, 0, 30, 180))       # Заливаем темно-розовым с прозрачностью (180 из 255)
        screen.blit(overlay, (0, 0))          # Рисуем затемнение поверх всего экрана

        # Заголовок - только текст, без спрайта
        pause_text = self.big_font.render('PAUSED', True, (255, 100, 150))
        screen.blit(pause_text,                       # Центрируем заголовок в верхней части экрана
                    (self.screen_width // 2 - pause_text.get_width() // 2,
                     self.screen_height // 2 - 200))

        # Опции меню
        options = [
            "Press P to Resume",
            "M - Toggle Music",
            "S - Toggle Sound",
            "+/- - Adjust Volume",
            "ESC - Quit Game"
        ]

        # Рисуем каждую опцию по центру экрана
        for i, option in enumerate(options) :
            option_text = self.font.render(option, True, (255, 200, 220))
            screen.blit(option_text,                          # Располагаем опции вертикально с интервалом 60 пикселей
                        (self.screen_width // 2 - option_text.get_width() // 2,
                         self.screen_height // 2 - 50 + i * 60))

        # Статус звука
        # Выбираем иконки в зависимости от включенного звука/музыки
        sound_icon = "🔊" if self.sound_manager.sound_enabled else "🔇"
        music_icon = "🎵" if self.sound_manager.music_enabled else "🔇"
        status_text = self.font.render(              # Создаем строку со статусом аудио
            f'Sound: {sound_icon}  Music: {music_icon}  Volume: {int(self.sound_manager.volume * 100)}%',
            True, (255, 180, 200))
        screen.blit(status_text,          # Выводим статус внизу экрана
                    (self.screen_width // 2 - status_text.get_width() // 2,
                     self.screen_height // 2 + 250))

    def draw_game_over(self, screen) :
        # Полупрозрачное затемнение
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((50, 0, 30, 150))       # Темно-розовый с меньшей прозрачностью
        screen.blit(overlay, (0, 0))

        # Звук Game Over (проигрываем один раз)
        # Проверяем, был ли уже проигран звук (чтобы не повторять)
        if not hasattr(self, 'game_over_sound_played') :
            self.sound_manager.play_sound('game_over')         # Проигрываем звук "game over"
            self.game_over_sound_played = True                 # Устанавливаем флаг, что звук уже проигран

        # Game Over текст или спрайт
        # Если есть спрайт для "Game Over" - используем его
        if self.ui_sprites['game_over'] :
            x = self.screen_width // 2 - self.ui_sprites['game_over'].get_width() // 2           # Центрируем спрайт по горизонтали
            y = self.screen_height // 2 - 200           # Фиксированная позиция по вертикали
            screen.blit(self.ui_sprites['game_over'], (x, y))
        else :            # Если спрайта нет - рисуем текст
            game_over_text = self.big_font.render('GAME OVER', True, (255, 100, 150))
            screen.blit(game_over_text,
                        (self.screen_width // 2 - game_over_text.get_width() // 2,
                         self.screen_height // 2 - 150))

        # Статистика
        stats = [
            f"Final Score: {self.score}",             # Финальный счет
            f"Max Speed: {int(self.game_speed)}",     # Максимальная скорость
            f"Obstacles Passed: {self.score}",        # Препятствий пройдено:
            f"Lives Lost: {3 - self.lives}" if self.lives < 3 else f"Lives: {self.lives}/3"       # Если жизни потеряны - показываем сколько, иначе показываем полные жизни
        ]

        # Рисуем статистику по центру экрана
        for i, stat in enumerate(stats) :
            stat_text = self.font.render(stat, True, (255, 200, 220))
            screen.blit(stat_text,
                        (self.screen_width // 2 - stat_text.get_width() // 2,
                         self.screen_height // 2 - 20 + i * 60))

        # Инструкция, что делать дальше
        restart_text = self.font.render('Press R to restart or ESC to quit', True, (255, 180, 200))
        screen.blit(restart_text,
                    (self.screen_width // 2 - restart_text.get_width() // 2,
                     self.screen_height // 2 + 180))


    def reset_game(self):
        self.player.reset()
        self.obstacles.clear()
        self.clouds.clear()
        self.score = 0
        self.lives = 3  # Восстанавливаем жизни
        self.game_over = False
        self.is_paused = False
        self.obstacle_timer = 0
        self.game_speed = 400
        self.obstacle_interval = 1.8

        if hasattr(self, 'game_over_sound_played'): #если уже играла музыка проигрыша, удаляем ее
            del self.game_over_sound_played

        self.create_initial_clouds()
        print("Game reset")

    def get_game_result(self):
        #получение результатов игры
        return {
            'score': self.score,
            'speed': int(self.game_speed),
            'lives': self.lives
        }