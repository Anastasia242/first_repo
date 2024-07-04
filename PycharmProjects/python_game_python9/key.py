import pygame

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/key_type1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.picked_up = False

    def update(self):
        if self.picked_up:
            self.kill()  # Видаляємо з усіх груп

    def draw(self, screen):
        if not self.picked_up:
            screen.blit(self.image, self.rect.topleft)
