import pygame
from health_potion import HealthPotion

class Treasure(pygame.sprite.Sprite):
    def __init__(self, x, y, health_potions_group):
        super().__init__()
        self.image = pygame.image.load("images/treasure_chest_closed_type1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.locked = True
        self.show_potion = False
        self.show_potion_timer = 0
        self.potion = None

    def unlock(self):
        self.locked = False
        self.image = pygame.image.load("images/treasure_chest_open_type1.png").convert_alpha()
        self.show_potion = True
        self.show_potion_timer = pygame.time.get_ticks()  # Встановити таймер
        self.potion = HealthPotion(self.rect.centerx, self.rect.centery - 20)
        health_potions.add(self.potion)  # Додаємо зілля до групи

    def update(self):
        # Приховати зілля через 2 секунди
        if self.show_potion and pygame.time.get_ticks() - self.show_potion_timer > 1000:
            self.show_potion = False
            health_potions.remove(self.potion)
            self.potion = None

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
