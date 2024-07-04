import pygame

class Inventory:
    def __init__(self):
        self.items = []
        self.background_image = pygame.image.load("images/inventory_background.png").convert_alpha()
        self.item_images = {
            'key': pygame.image.load("images/key_type1_invent.png").convert_alpha(),
            'health_potion': pygame.image.load("images/health_potion.png").convert_alpha()
        }

    def add_item(self, item):
        self.items.append(item)
        print(f"Added {item} to inventory")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item} from inventory")

    def use_item(self, item, player):
        if item in self.items:
            if item == 'health_potion':
                # Використання зілля здоров'я з обмеженням на максимальне здоров'я
                player.health = min(player.health + 20, player.max_health)
                self.remove_item(item)
                print(f"Used {item}. Player's health is now {player.health}.")

    def draw(self, screen):
        # Малювання фону інвентаря
        screen.blit(self.background_image, (screen.get_width() // 4, screen.get_height() // 4))

        # Малювання елементів інвентаря
        inventory_font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.items):
            item_x = screen.get_width() // 4 + 10
            item_y = screen.get_height() // 4 + 10 + i * 40
            if item in self.item_images:
                item_image = self.item_images[item]
                # Збільшуємо координати, щоб ключ був трошки нижче та правіше
                item_x += 75  # Зміщення вправо
                item_y += 150  # Зміщення вниз
                screen.blit(item_image, (item_x, item_y))
            else:
                text_surface = inventory_font.render(item, True, (255, 255, 255))
                screen.blit(text_surface, (item_x, item_y))
