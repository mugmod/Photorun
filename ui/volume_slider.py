import pygame
import time

class VolumeMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load("assets/images/Start window/Start_scr.png").convert()

        # Прямоугольник полосы громкости и ползунка
        self.bar_rect = pygame.Rect(660, 500, 600, 20)
        self.slider_rect = pygame.Rect(660, 490, 20, 40)
        self.dragging = False
        self.volume = 0.5  # Начальное значение громкости

        # Инициализируем аудиосистему, если она ещё не активна
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        try:
            # Звук-клик для обратной связи при изменении громкости
            self.test_sound = pygame.mixer.Sound("assets/sounds/clic_sound.mp3")
            self.test_sound.set_volume(self.volume)
        except Exception as e:
            print("Ошибка загрузки звука:", e)
            self.test_sound = None  # Продолжаем работу даже при ошибке

        self.last_play_time = 0  # Контроль частоты воспроизведения клика
        self.font = pygame.font.SysFont(None, 36)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.volume  # Возврат текущего значения при выходе

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return self.volume  # Закрытие меню по ESC

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Начинаем перетаскивание ползунка, если нажали на него
                    if self.slider_rect.collidepoint(event.pos):
                        self.dragging = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False  # Завершаем перетаскивание

                elif event.type == pygame.MOUSEMOTION and self.dragging:
                    # Обновляем позицию ползунка и громкость при движении мыши
                    x = max(self.bar_rect.left, min(event.pos[0], self.bar_rect.right))
                    self.slider_rect.centerx = x
                    rel_x = (x - self.bar_rect.left) / self.bar_rect.width
                    self.volume = round(rel_x, 2)
                    pygame.mixer.music.set_volume(self.volume)

                    # Воспроизводим звук при изменении с интервалом во избежание спама
                    if self.test_sound:
                        current_time = time.time()
                        if current_time - self.last_play_time > 0.2:
                            self.test_sound.set_volume(self.volume)
                            self.test_sound.play()
                            self.last_play_time = current_time

            # Отрисовка элементов интерфейса громкости
            pygame.draw.rect(self.screen, (180, 180, 180), self.bar_rect)       # Фон полосы
            pygame.draw.rect(self.screen, (255, 255, 255), self.slider_rect)    # Ползунок

            label = self.font.render(f"Громкость: {int(self.volume * 100)}%", True, (255, 255, 255))
            self.screen.blit(label, (self.bar_rect.centerx - 100, self.bar_rect.top - 50))

            pygame.display.flip()
            clock.tick(60)
