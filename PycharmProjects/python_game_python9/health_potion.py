import pygame

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(
            'images/health_potion.png').convert_alpha()  # Завантаження зображення зілля здоров'я
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def apply_health(self, player):
        # Застосування зілля здоров'я до гравця з обмеженням на максимальне здоров'я
        player.health = min(player.health + 20, player.max_health)
