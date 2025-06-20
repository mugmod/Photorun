import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        new_size = (60, 84)  # Унификация размера кадров персонажа

        # Подготовка кадров анимации бега вправо и зеркальных копий для движения влево
        self.frames_right = [
            pygame.transform.scale(pygame.image.load("assets/images/player/run1.png").convert_alpha(), new_size),
            pygame.transform.scale(pygame.image.load("assets/images/player/run2.png").convert_alpha(), new_size)
        ]
        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames_right]

        # Направление взгляда и состояние анимации
        self.facing_right = True
        self.frame_index = 0
        self.animation_time = 200  # Интервал переключения кадров (мс)
        self.last_update = pygame.time.get_ticks()

        self.image = self.frames_right[0]
        self.rect = self.image.get_rect(topleft=(x, y))  # Положение игрока

        self.vel = pygame.Vector2(0, 0)
        self.gravity = 0.5
        self.jump_speed = -10  # Отрицательное значение для движения вверх
        self.on_ground = False  # Проверка, можно ли прыгать

        # Параметры здоровья
        self.max_health = 100
        self.current_health = 100
        self.alive = True

    def input(self):
        # Обработка ввода для перемещения и прыжка
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -5
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.vel.x = 5
            self.facing_right = True
        else:
            self.vel.x = 0

        # Прыжок возможен только при контакте с землёй
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = self.jump_speed
            self.on_ground = False

    def update_animation(self):
        # Обновление анимации при движении с учётом времени
        now = pygame.time.get_ticks()
        if self.vel.x != 0 and now - self.last_update > self.animation_time:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.frames_right)
            frames = self.frames_right if self.facing_right else self.frames_left
            self.image = frames[self.frame_index]
        elif self.vel.x == 0:
            # Остановка на первом кадре, если игрок не двигается
            self.image = self.frames_right[0] if self.facing_right else self.frames_left[0]

    def take_damage(self, amount):
        # Применение урона и смерть при достижении нуля
        if not self.alive:
            return
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
            self.alive = False

    def draw_health(self, surface):
        # Отображение полоски здоровья с числовым значением
        bar_width = 300
        bar_height = 25
        x, y = 40, 20

        ratio = self.current_health / self.max_health
        inner_width = bar_width * ratio

        pygame.draw.rect(surface, (50, 50, 50), (x, y, bar_width, bar_height))  # Фон
        pygame.draw.rect(surface, (255, 0, 0), (x, y, inner_width, bar_height))  # Заполненная часть
        pygame.draw.rect(surface, (255, 255, 255), (x, y, bar_width, bar_height), 2)  # Граница

        font = pygame.font.SysFont("consolas", 20)
        hp_text = f"{self.current_health} / {self.max_health}"
        text_surf = font.render(hp_text, True, (255, 255, 255))
        surface.blit(text_surf, (x + bar_width + 10, y))

    def apply_gravity(self, platforms):
        # Гравитация и вертикальные столкновения с платформами
        self.vel.y += self.gravity
        self.rect.y += self.vel.y

        self.on_ground = False  # Сброс состояния перед проверкой
        for platform in platforms:
            target = platform.rect if hasattr(platform, "rect") else platform
            if self.rect.colliderect(target):
                if self.vel.y < 0:
                    # Удар об нижнюю часть платформы
                    self.rect.top = target.bottom
                    self.vel.y = 0
                elif self.vel.y > 0:
                    # Приземление на платформу
                    self.rect.bottom = target.top
                    self.vel.y = 0
                    self.on_ground = True

    def update(self, platforms):
        self.input()

        # Горизонтальное перемещение и обработка столкновений
        self.rect.x += self.vel.x
        for platform in platforms:
            target = platform.rect if hasattr(platform, "rect") else platform
            if self.rect.colliderect(target):
                if self.vel.x > 0:
                    self.rect.right = target.left
                elif self.vel.x < 0:
                    self.rect.left = target.right

        # Ограничение в пределах экрана
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        self.apply_gravity(platforms)
        self.update_animation()

    def draw(self, screen):
        # Отрисовка игрока и его здоровья
        screen.blit(self.image, self.rect)
        self.draw_health(screen)
