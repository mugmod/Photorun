import pytmx
import pygame

def load_level(path):
    # Загружаем данные из TMX-файла уровня, созданного в редакторе Tiled
    tmx_data = pytmx.load_pygame(path)
    platforms = []

    for layer in tmx_data.visible_layers:
        # Ищем слой, обозначенный как "platforms", чтобы получить коллизии
        if layer.name == "platforms":
            for x, y, gid in layer:
                if gid != 0:
                    # Создаём прямоугольники для каждой платформы, основываясь на координатах тайлов
                    tile_rect = pygame.Rect(
                        x * tmx_data.tilewidth,
                        y * tmx_data.tileheight,
                        tmx_data.tilewidth,
                        tmx_data.tileheight
                    )
                    platforms.append(tile_rect)

    # Возвращаем список прямоугольников платформ и объект с полными данными уровня (для возможного рендера)
    return platforms, tmx_data
