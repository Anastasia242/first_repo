import pygame
import os

class Menu:
    def __init__(self):
        # Ініціалізація параметрів меню
        self.menu_image = self.load_image("images/Menu.png")
        self.menu_items = ["Start", "Options", "Quit"]
        self.selected_item = 0
        self.images = {
            "Start": self.load_image("images/start_menu.png"),
            "Options": self.load_image("images/options_menu.png"),
            "Quit": self.load_image("images/quit_menu.png")
        }
        self.MENU_ITEM_HEIGHT = 60

    def load_image(self, path):
        if not os.path.exists(path):
            print(f"File not found: {path}")
            return pygame.Surface((100, 50))  # Повертаємо заглушку замість зображення
        return pygame.image.load(path).convert_alpha()

    def draw(self, screen):
        # Малювання фону меню
        screen.blit(self.menu_image, (screen.get_width() // 4, screen.get_height() // 4))

        # Малювання елементів меню
        for i, item in enumerate(self.menu_items):
            image = self.images[item]
            if i == self.selected_item:
                image = pygame.transform.scale(image, (
                    int(image.get_width() * 1.2), int(image.get_height() * 1.2)))  # Збільшення зображення на 20%
            image_rect = image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 1.75 + i * self.MENU_ITEM_HEIGHT))
            screen.blit(image, image_rect.topleft)

    def update_selection(self, mouse_pos):
        # Оновлення вибору залежно від позиції миші
        for i, item in enumerate(self.menu_items):
            image = self.images[item]
            image_rect = image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 + i * 60))
            if image_rect.collidepoint(mouse_pos):
                self.selected_item = i

    def get_selected_item(self):
        # Повертаємо вибраний елемент меню
        return self.menu_items[self.selected_item]
