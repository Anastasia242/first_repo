import pygame

class Platform:
    def __init__(self, x, y, width, height, platform_type, images_dict, moving=False, move_range=(0, 0),
                 moving_horizontal=False, speed=2, moving_vertical=False):
        self.platform_type = platform_type
        self.images_dict = images_dict
        self.image = self.images_dict.get(self.platform_type)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.moving = moving  # Чи повинна платформа рухатися вертикально
        self.moving_horizontal = moving_horizontal  # Чи повинна платформа рухатися горизонтально
        self.direction = 1  # Напрямок руху платформи (1 - вправо, -1 - вліво)
        self.speed = speed  # Швидкість руху платформи
        self.move_range = move_range  # Діапазон руху платформи
        self.moving_vertical = moving_vertical

        # Створення маски з меншими розмірами
        mask_width = self.rect.width - 25  # зменшити ширину маски на 25 пікселів
        mask_height = self.rect.height - 27  # зменшити висоту маски на 27 пікселів
        self.mask = pygame.mask.Mask((mask_width, mask_height), fill=True)

        # Зміщення маски в центр зображення
        self.mask_rect = pygame.Rect(
            (self.rect.width - mask_width) // 2,
            (self.rect.height - mask_height) // 2,
            mask_width,
            mask_height
        )

    def update(self):
        if self.moving:
            if self.moving_horizontal:
                self.rect.x += self.direction * self.speed
                if self.rect.x <= self.move_range[0]:
                    self.direction = 1
                elif self.rect.x >= self.move_range[1] - self.rect.width:
                    self.direction = -1
            elif self.moving_vertical:
                self.rect.y += self.direction * self.speed
                if self.rect.y <= self.move_range[0]:
                    self.direction = 1
                elif self.rect.y >= self.move_range[1] - self.rect.height:
                    self.direction = -1

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
