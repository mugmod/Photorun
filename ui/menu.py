import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.volume_slider import VolumeMenu

pygame.init()

class ImageButton:
    def __init__(self, image_path, pos, callback, scale=0.6):
        # Загружаем и масштабируем изображение кнопки под нужный размер
        original_img = pygame.image.load(image_path).convert_alpha()
        w, h = original_img.get_size()
        self.original_image = pygame.transform.smoothscale(original_img, (int(w * scale), int(h * scale)))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)

        self.callback = callback  # Функция, вызываемая при нажатии
        self.alpha = 0  # Прозрачность для эффекта появления
        self.fade_speed = 5  # Скорость постепенного проявления

    def draw(self, surface):
        # Плавное проявление кнопки при первом отображении
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + self.fade_speed)
            self.image.set_alpha(self.alpha)
        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        # Обработка нажатия на кнопку
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class MainMenu:
    def __init__(self, screen, start_game_callback):
        self.screen = screen
        self.start_game_callback = start_game_callback
        self.background = pygame.image.load("assets/images/Start window/Start_scr.png").convert()

        center_x = SCREEN_WIDTH // 2
        start_y = 500
        gap = 170
        button_scale = 0.3

        # Инициализация кнопок: старт, настройки громкости, выход
        self.buttons = [
            ImageButton("assets/images/Start window/Start_game_scr.png", (center_x, start_y), self.start_game, button_scale),
            ImageButton("assets/images/Start window/Value_scr.png",      (center_x - 17, start_y + gap), self.show_volume, button_scale),
            ImageButton("assets/images/Start window/Exit_scr.png",       (center_x, start_y + 2 * gap), self.exit_game, button_scale)
        ]

        self.get_volume = None  # Связи с системами звука подставляются динамически
        self.set_volume = None

    def set_volume_ref(self, getter, setter):
        # Устанавливаем функции для получения и установки громкости
        self.get_volume = getter
        self.set_volume = setter

    def start_game(self):
        self.start_game_callback()

    def show_volume(self):
        # Показываем меню громкости и применяем изменения
        new_vol = VolumeMenu(self.screen).run()
        if new_vol is not None and self.set_volume:
            self.set_volume(new_vol)

    def exit_game(self):
        # Завершение игры
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                for btn in self.buttons:
                    btn.handle_event(event)

            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)
