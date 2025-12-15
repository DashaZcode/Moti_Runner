import pygame
import argparse
import os
from game.player import Player
from game.obstacle import Obstacle
from game.sound_manager import SoundManager
from game.sprite_loader import SpriteLoader

WIDTH, HEIGHT = 800, 600
FPS = 60
GROUND_Y = HEIGHT - 100  # Уровень "земли" для игрока
OBSTACLE_INTERVAL = 1.5  # Базовый интервал появления препятствий

def save_score(name, score):
    with open('scores.txt', 'a', encoding='utf-8') as f:
        f.write(f"{name}: {score}\n")

def main(args):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Moti Runner')
    clock = pygame.time.Clock()

    sound_manager = SoundManager()
    sound_manager.play_background('background_music')  # имя файла без расширения

    assets_path = SpriteLoader.get_assets_path()
    background_path = os.path.join(assets_path, 'background')

    # Небо
    sky_color = (135, 206, 235)  # Светло-голубое

    # Горы (медленный слой)
    mountain = None
    mountain_x = 0
    mountain_path = os.path.join(background_path, 'mountain.png')
    if os.path.exists(mountain_path):
        mountain = pygame.image.load(mountain_path).convert_alpha()
        mountain = pygame.transform.scale(mountain, (WIDTH * 2, HEIGHT))
        print("Горы загружены")

    # Облака (средний слой)
    cloud = None
    cloud_x = 0
    cloud_path = os.path.join(background_path, 'cloud.png')
    if os.path.exists(cloud_path):
        cloud = pygame.image.load(cloud_path).convert_alpha()
        cloud = pygame.transform.scale(cloud, (WIDTH * 3, HEIGHT // 2))
        print("Облака загружены")

    # Земля (быстрый слой)
    ground = None
    ground_x = 0
    ground_path = os.path.join(background_path, 'ground.png')
    if os.path.exists(ground_path):
        ground = pygame.image.load(ground_path).convert_alpha()
        ground = pygame.transform.scale(ground, (WIDTH * 2, 200))
        print("Земля загружена")

    player = Player(100, GROUND_Y - 80)
    obstacles = []
    obstacle_timer = 0
    score = 0
    running = True
    game_over = False

    while running:
        dt = clock.tick(FPS) / 1000
        obstacle_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not player.is_jumping:
            sound_manager.play('jump')

        # Генерация препятствий
        if obstacle_timer >= OBSTACLE_INTERVAL / args.difficulty:
            obstacles.append(Obstacle.create_random(WIDTH, GROUND_Y, args.speed))
            obstacle_timer = 0

        # Обновление объектов
        player.update(dt, keys)
        for obs in obstacles[:]:
            obs.update(dt)
            if obs.is_offscreen():
                obstacles.remove(obs)
            if not obs.passed and obs.rect.right < player.rect.left:
                obs.passed = True
                score += 1
            if player.collides_with(obs):
                sound_manager.play('collision')
                save_score(args.name, score)
                game_over = True
                running = False

        # === ОТРИСОВКА ===
        screen.fill(sky_color)  # Небо

        # Горы (медленно)
        if mountain:
            screen.blit(mountain, (mountain_x, HEIGHT - mountain.get_height()))
            screen.blit(mountain, (mountain_x + mountain.get_width(), HEIGHT - mountain.get_height()))
            mountain_x -= 50 * dt
            if mountain_x <= -mountain.get_width():
                mountain_x = 0

        # Облака (средне)
        if cloud:
            screen.blit(cloud, (cloud_x, 50))
            screen.blit(cloud, (cloud_x + cloud.get_width(), 50))
            cloud_x -= 100 * dt
            if cloud_x <= -cloud.get_width():
                cloud_x = 0

        # Земля (быстро, синхронно с препятствиями)
        if ground:
            screen.blit(ground, (ground_x, GROUND_Y - ground.get_height() + 100))
            screen.blit(ground, (ground_x + ground.get_width(), GROUND_Y - ground.get_height() + 100))
            ground_x -= args.speed * dt
            if ground_x <= -ground.get_width():
                ground_x = 0
        else:
            pygame.draw.rect(screen, (100, 100, 100), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))

        # Игрок и препятствия
        player.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        # Счёт
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    # === ЭКРАН GAME OVER ===
    if game_over:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        return

            screen.fill(sky_color)
            if mountain:
                screen.blit(mountain, (mountain_x, HEIGHT - mountain.get_height()))
                screen.blit(mountain, (mountain_x + mountain.get_width(), HEIGHT - mountain.get_height()))
            if cloud:
                screen.blit(cloud, (cloud_x, 50))
                screen.blit(cloud, (cloud_x + cloud.get_width(), 50))
            if ground:
                screen.blit(ground, (ground_x, GROUND_Y - ground.get_height() + 100))
                screen.blit(ground, (ground_x + ground.get_width(), GROUND_Y - ground.get_height() + 100))

            font_big = pygame.font.SysFont(None, 70)
            font_small = pygame.font.SysFont(None, 50)
            go_text = font_big.render("Game Over!", True, (255, 0, 0))
            score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
            hint_text = font_small.render("Нажмите Enter или Q для выхода", True, (255, 255, 255))

            screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + 70))

            pygame.display.flip()

    sound_manager.stop_background()
    pygame.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Moti Runner')
    parser.add_argument('--name', default='Player', help='Имя игрока')
    parser.add_argument('--speed', type=int, default=300, help='Скорость препятствий (px/s)')
    parser.add_argument('--difficulty', type=float, default=1.0, help='Сложность (чем больше — чаще препятствия)')
    args = parser.parse_args()
    main(args)
