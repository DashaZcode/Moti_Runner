#!/usr/bin/env python3
"""
Главный файл игры Moti Runner
"""

import pygame
import sys
import time
import argparse
from game.game_manager import GameManager


def parse_arguments():
    """Парсинг аргументов командной строки"""      # Создаем парсер для обработки аргументов при запуске игры
    parser = argparse.ArgumentParser(
        description='Moti Runner - игра в стиле Google Chrome Dino'
    )

    parser.add_argument(            # Аргумент для имени игрока
        '--player', '-p',
        type=str,
        default='Player1',
        help='Имя игрока'
    )

    parser.add_argument(           # Аргумент для начальной скорости игры
        '--speed', '-s',
        type=int,
        default=400,
        help='Начальная скорость'
    )

    parser.add_argument(      # Аргумент для ширины игрового окна
        '--width', '-W',
        type=int,
        default=1200,
        help='Ширина окна'
    )

    parser.add_argument(        # Аргумент для высоты игрового окна
        '--height', '-H',
        type=int,
        default=800,
        help='Высота окна'
    )

    parser.add_argument(         # Аргумент для FPS (кадров в секунду)
        '--fps', '-f',
        type=int,
        default=60,
        help='Количество кадров в секунду'
    )

    return parser.parse_args()         # Возвращаем распарсенные аргументы


def main():
    """Главная функция игры"""
    args = parse_arguments()        # Получаем аргументы командной строки

    # Вывод информации о запуске игры в консоль
    print("=" * 50)
    print("🦊 MOTI RUNNER GAME")
    print("=" * 50)
    print(f"Player: {args.player}")     # Имя игрока
    print(f"Window: {args.width}x{args.height}")       # Размер окна
    print(f"FPS: {args.fps}")       # Частота кадров
    print("=" * 50)

    # Инициализация Pygame (запуск игрового движка)
    pygame.init()

    # Создание окна
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption(f"Moti Runner - {args.player}")      # Установка заголовка окна с именем игрока

    # Иконка окна
    try:
        icon = pygame.Surface((32, 32))      # Создаем простую иконку 32x32 пикселя
        icon.fill((255, 100, 100))      # Заливаем розовым цветом
        pygame.draw.rect(icon, (255, 150, 150), (10, 10, 12, 22))       # Рисуем прямоугольник внутри иконки
        pygame.display.set_icon(icon)     # Устанавливаем иконку для окна
    except:
        pass       # Если не удалось установить иконку - пропускаем ошибку

    clock = pygame.time.Clock()     # Создаем объект для контроля времени (таймер для FPS)

    # Инициализация игры
    game_manager = GameManager(args.width, args.height, args.speed)

    # Игровой цикл
    start_time = time.time()     # Запоминаем время начала игры
    running = True       # Флаг работы игрового цикла

    while running:     # Главный цикл игры
        # dt = delta time (время с прошлого кадра в секундах)
        # tick(60) ограничивает FPS до 60 и возвращает время в миллисекундах
        dt = clock.tick(args.fps) / 1000.0

        # Обработка событий (нажатия клавиш, закрытие окна и т.д.)
        # handle_events() возвращает False если нужно выйти из игры
        running = game_manager.handle_events()

        # Обновление игровой логики (передвижение объектов, физика и т.д.)
        game_manager.update(dt)

        # Отрисовка
        game_manager.draw(screen)
        pygame.display.flip()     # Обновление экрана (показываем нарисованное)

        # Проверка завершения игры
        if game_manager.game_over:     # Если игра окончена
            game_duration = int(time.time() - start_time)      # Вычисляем продолжительность игры в секундах
            game_result = game_manager.get_game_result()       # Получаем результаты игры

            # Вывод результатов
            print("\n" + "=" * 50)
            print("🎮 GAME OVER")
            print("=" * 50)
            print(f"Score: {game_result['score']}")     # Финальный счет
            print(f"Max Speed: {game_result['speed']}")     # Максимальная скорость
            print(f"Time: {game_duration}s")       # Время игры
            print("=" * 50)

            # Ожидание рестарта или выхода
            print("\n🔄 Press R to restart or ESC to quit")
            waiting = True    # Флаг ожидания
            while waiting and running:     # Обработка событий в режиме ожидания
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:     # Закрытие окна
                        waiting = False
                        running = False
                    elif event.type == pygame.KEYDOWN:     # Нажатие клавиши
                        if event.key == pygame.K_r:        # R - рестарт
                            game_manager.reset_game()      # Сброс игры
                            start_time = time.time()       # Сброс таймера
                            waiting = False                # Выход из режима ожидания
                            print("\n🔄 Game restarted!")
                        elif event.key == pygame.K_ESCAPE:  # ESC - выход
                            waiting = False
                            running = False

                # Продолжаем отрисовку экрана Game Over
                game_manager.draw(screen)
                pygame.display.flip()
                clock.tick(args.fps)    # Поддерживаем FPS

    # Завершение
    pygame.quit()    # Закрытие Pygame
    sys.exit()       # Выход из программы


if __name__ == '__main__':
    main()
