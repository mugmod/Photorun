import pygame

class Lever:
    def __init__(self, x, y):
        # Загружаем изображения состояний рычага заранее, чтобы переключение происходило мгновенно
        self.image_off = pygame.image.load("assets/images/objects/lever_off.png").convert_alpha()
        self.image_on = pygame.image.load("assets/images/objects/lever_on.png").convert_alpha()
        self.image = self.image_off  # Изначально рычаг выключен
        self.rect = self.image.get_rect(topleft=(x, y))  # Положение рычага на экране
        self.activated = False  # Флаг состояния: включен/выключен

    def toggle(self):
        # Переключаем состояние и обновляем изображение в соответствии с флагом
        self.activated = not self.activated
        self.image = self.image_on if self.activated else self.image_off

    def draw(self, surface):
        # Отрисовываем текущее изображение рычага на переданной поверхности
        surface.blit(self.image, self.rect)
