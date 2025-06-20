import pygame
import pytmx
import time
from settings import *
from player.player import Player
from level_loader import load_level
from objects.lever import Lever
from objects.moving_block import MovingPlatform
from objects.fan import Fan
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Photorun")
clock = pygame.time.Clock()

game_paused = False
current_volume = 0.5

# Загружаем платформы и данные карты из TMX-файла уровня
platforms, tmx_data = load_level("levels/level one/level1.tmx")
player = Player(100, 900)

tile_w, tile_h = tmx_data.tilewidth, tmx_data.tileheight
map_w, map_h = tmx_data.width, tmx_data.height

# Инициализируем врагов на сцене с разными типами спрайтов
enemies = [
    Enemy(500, 10, sprite_folder="mob1"),
    Enemy(500, 100, sprite_folder="mob2"),
]

lever = Lever(1000, 513)
platform = MovingPlatform(768, 355, 120, 20, min_y=127, max_y=577)
fan = Fan(x=140, y=200, width=80, height=360)

def draw_map():
    # Отрисовка слоёв карты, кроме коллизий
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tile_w, y * tile_h))

def run_game():
    global game_paused, current_volume

    try:
        # Запускаем фоновую музыку с циклическим воспроизведением
        pygame.mixer.music.load("assets/sounds/game_music.mp3")
        pygame.mixer.music.set_volume(current_volume)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Не удалось запустить музыку:", e)

    running = True
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    game_paused = True
                    return

                # Переключаем рычаг и активируем платформу
                if event.key == pygame.K_f:
                    if player.rect.colliderect(lever.rect):
                        lever.toggle()
                        platform.activate(moving_up=lever.activated)

                # Атакуем ближайшего врага в зоне досягаемости
                if event.key == pygame.K_e:
                    for enemy in enemies:
                        if enemy.alive and player.rect.colliderect(enemy.rect.inflate(40, 20)):
                            enemy.take_damage(50)

        draw_map()
        platform.update()
        fan.apply(player)
        player.update(platforms + [platform])

        for enemy in enemies:
            enemy.update(player, platforms + [platform])

        # Проверяем условие проигрыша
        if not player.alive:
            show_game_over_screen()
            return

        # Условие победы — игрок входит в правый верхний 4x4 тайла
        victory_rect = pygame.Rect((map_w - 4) * tile_w, 0, tile_w * 4, tile_h * 4)
        if player.rect.colliderect(victory_rect):
            show_victory_screen()
            return

        player.draw(screen)
        platform.draw(screen)
        lever.draw(screen)
        fan.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.mixer.music.stop()
    pygame.quit()

def show_game_over_screen():
    font = pygame.font.Font(None, 120)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    try:
        sound = pygame.mixer.Sound("assets/sounds/game_over.wav")
        sound.play()
    except Exception as e:
        print("Ошибка загрузки звука поражения:", e)

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

def show_victory_screen():
    font = pygame.font.Font(None, 100)
    text = font.render("YOU WIN!", True, (0, 255, 0))
    text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    try:
        sound = pygame.mixer.Sound("assets/sounds/victory.wav")
        sound.play()
    except Exception as e:
        print("Ошибка загрузки звука победы:", e)

    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

if __name__ == "__main__":
    from ui.menu import MainMenu

    def start_game():
        global game_paused
        game_paused = False
        run_game()

    # Создаём главное меню с привязкой к запуску и управлению громкостью
    menu = MainMenu(screen, start_game_callback=start_game)
    menu.set_volume_ref(lambda: current_volume, lambda v: globals().__setitem__('current_volume', v))
    menu.run()
