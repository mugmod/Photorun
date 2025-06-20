import pygame
import os
import time

class Enemy:
    def __init__(self, x, y, sprite_folder="mob1"):
        self.scale = 2
        self.width = 40 * self.scale
        self.height = 56 * self.scale

        # Загружаем первый кадр из спрайт-листа врага или создаём заглушку
        path = os.path.join("assets/images/enemies", sprite_folder, "walk.png")
        if os.path.exists(path):
            sheet = pygame.image.load(path).convert_alpha()
            frame = sheet.subsurface(pygame.Rect(0, 0, sheet.get_width() // 10, sheet.get_height()))
            self.image = pygame.transform.scale(frame, (self.width, self.height))
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))  # Красный прямоугольник при отсутствии изображения

        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel = pygame.Vector2(0, 0)
        self.speed = 1.5
        self.jump_force = -10
        self.gravity = 0.5
        self.on_ground = False  # Контроль возможности прыжка

        self.health = 100
        self.alive = True  # Флаг активности врага

        # Параметры ближней атаки
        self.attack_range = 50
        self.attack_cooldown = 1.0  # Задержка между ударами (сек)
        self.last_attack = 0  # Время последней атаки

    def update(self, player, platforms):
        if not self.alive:
            return  # Мёртвые враги не двигаются и не атакуют

        # Преследуем игрока по оси X
        dx = player.rect.centerx - self.rect.centerx
        if abs(dx) > 4:
            self.vel.x = self.speed if dx > 0 else -self.speed
        else:
            self.vel.x = 0

        # Прыгаем, если игрок выше на значительное расстояние и враг на земле
        dy = player.rect.centery - self.rect.centery
        if dy < -60 and self.on_ground:
            self.vel.y = self.jump_force

        # Атака, если игрок в пределах досягаемости
        if abs(dx) < self.attack_range and abs(dy) < 60:
            now = time.time()
            if now - self.last_attack > self.attack_cooldown:
                player.take_damage(20)
                self.last_attack = now

        # Обновление позиции по X и обработка горизонтальных столкновений
        self.rect.x += self.vel.x
        self._collide_horizontal(platforms)

        # Применяем гравитацию и обрабатываем вертикальные столкновения
        self.vel.y += self.gravity
        self.rect.y += self.vel.y
        self._collide_vertical(platforms)

    def _collide_horizontal(self, platforms):
        for obj in platforms:
            target = getattr(obj, "rect", obj)
            if self.rect.colliderect(target):
                if self.vel.x > 0:
                    self.rect.right = target.left
                elif self.vel.x < 0:
                    self.rect.left = target.right

    def _collide_vertical(self, platforms):
        self.on_ground = False  # Сначала считаем, что враг в воздухе
        for obj in platforms:
            target = getattr(obj, "rect", obj)
            if self.rect.colliderect(target):
                if self.vel.y > 0:
                    self.rect.bottom = target.top
                    self.vel.y = 0
                    self.on_ground = True  # Подтверждаем контакт с землёй
                elif self.vel.y < 0:
                    self.rect.top = target.bottom
                    self.vel.y = 0

    def take_damage(self, amount):
        if not self.alive:
            return
        self.health -= amount
        if self.health <= 0:
            self.alive = False  # Враг отключается при обнулении здоровья

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)
