import pygame

class MovingPlatform:
    def __init__(self, x, y, width, height, min_y, max_y, speed=2):
        # Загружаем изображение платформы и создаём прямоугольник для позиционирования
        self.image = pygame.image.load("assets/images/objects/platform.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

        # Ограничения движения платформы по вертикали
        self.min_y = min_y
        self.max_y = max_y

        self.speed = speed  # Скорость движения платформы
        self.moving_up = False  # Направление движения (по умолчанию — вниз)
        self.active = False  # Флаг активности платформы; по умолчанию не движется

    def activate(self, moving_up=True):
        # Запускаем движение платформы в указанном направлении
        self.moving_up = moving_up
        self.active = True

    def update(self):
        if not self.active:
            return  # Платформа неактивна — пропускаем обновление

        if self.moving_up:
            self.rect.y -= self.speed
            # Останавливаем движение, если достигнут верхний предел
            if self.rect.top <= self.min_y:
                self.rect.top = self.min_y
                self.active = False
        else:
            self.rect.y += self.speed
            # Останавливаем движение, если достигнут нижний предел
            if self.rect.bottom >= self.max_y:
                self.rect.bottom = self.max_y
                self.active = False

    def draw(self, surface):
        # Отрисовываем платформу на переданной поверхности
        surface.blit(self.image, self.rect)
