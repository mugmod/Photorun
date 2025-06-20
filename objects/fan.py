import pygame

class Fan:
    def __init__(self, x, y, width, height, power=0.7, max_speed=-6):
        self.rect = pygame.Rect(x, y, width, height)
        self.power = power
        # Ограничение максимальной скорости подъёма игрока, чтобы избежать чрезмерного ускорения
        self.max_speed = max_speed  

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        # Полупрозрачный прямоугольник, чтобы визуально обозначить область вентилятора
        self.image.fill((100, 100, 255, 0))

    def apply(self, player):
        if self.rect.colliderect(player.rect):
            # Применяем силу вентилятора, если игрок еще не достиг максимальной подъёмной скорости
            if player.vel.y > self.max_speed:
                player.vel.y -= self.power
        else:
            pass  # Явный else здесь не нужен, можно удалить

    def draw(self, surface):
        # Отображаем вентилятор на переданной поверхности
        surface.blit(self.image, self.rect)
