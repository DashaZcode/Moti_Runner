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
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Moti Runner - игра в стиле Google Chrome Dino'
    )

    parser.add_argument(
        '--player', '-p',
        type=str,
        default='Player1',
        help='Имя игрока'
    )

    parser.add_argument(
        '--speed', '-s',
        type=int,
        default=400,
        help='Начальная скорость'
    )

    parser.add_argument(
        '--width', '-W',
        type=int,
        default=1200,
        help='Ширина окна'
    )

    parser.add_argument(
        '--height', '-H',
        type=int,
        default=800,
        help='Высота окна'
    )

    parser.add_argument(
        '--fps', '-f',
        type=int,
        default=60,
        help='Количество кадров в секунду'
    )

    return parser.parse_args()


def main():
    """Главная функция игры"""
    args = parse_arguments()

    print("=" * 50)
    print("🦊 MOTI RUNNER GAME")
    print("=" * 50)
    print(f"Player: {args.player}")
    print(f"Window: {args.width}x{args.height}")
    print(f"FPS: {args.fps}")
    print("=" * 50)

    # Инициализация Pygame
    pygame.init()

    # Создание окна
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption(f"Moti Runner - {args.player}")

    # Иконка
    try:
        icon = pygame.Surface((32, 32))
        icon.fill((255, 100, 100))
        pygame.draw.rect(icon, (255, 150, 150), (10, 10, 12, 22))
        pygame.display.set_icon(icon)
    except:
        pass

    clock = pygame.time.Clock()

    # Инициализация игры
    game_manager = GameManager(args.width, args.height, args.speed)

    # Игровой цикл
    start_time = time.time()
    running = True

    while running:
        dt = clock.tick(args.fps) / 1000.0

        # Обработка событий
        running = game_manager.handle_events()

        # Обновление игры
        game_manager.update(dt)

        # Отрисовка
        game_manager.draw(screen)
        pygame.display.flip()

        # Проверка завершения игры
        if game_manager.game_over:
            game_duration = int(time.time() - start_time)
            game_result = game_manager.get_game_result()

            # Вывод результатов
            print("\n" + "=" * 50)
            print("🎮 GAME OVER")
            print("=" * 50)
            print(f"Score: {game_result['score']}")
            print(f"Max Speed: {game_result['speed']}")
            print(f"Time: {game_duration}s")
            print("=" * 50)

            # Ожидание рестарта
            print("\n🔄 Press R to restart or ESC to quit")
            waiting = True
            while waiting and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game_manager.reset_game()
                            start_time = time.time()
                            waiting = False
                            print("\n🔄 Game restarted!")
                        elif event.key == pygame.K_ESCAPE:
                            waiting = False
                            running = False

                game_manager.draw(screen)
                pygame.display.flip()
                clock.tick(args.fps)

    # Завершение
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()