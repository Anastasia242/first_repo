# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import pygame
import sys
from menu import Menu
from inventory import Inventory
from platform import Platform
from player import Player
from key import Key
from treasure import Treasure
from health_potion import HealthPotion
from enemy import Enemy

# Ініціалізація Pygame
pygame.init()

# Задання розміру екрану
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAX_FALL_SPEED = 10  # максимально допустима швидкість падіння

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

GRAVITY = 0.5  # Гравітація

# Зміна кадрів анімації ходьби
ANIMATION_FRAME_RATE = 5

# Створення списку платформ
platform_images = {
    "platform_type_1": pygame.image.load("images/platform_1.png").convert_alpha(),
    "platform_type_2": pygame.image.load("images/platform_2.png").convert_alpha(),
    "platform_type_3": pygame.image.load("images/platform_3.png").convert_alpha(),
    "platform_type_5": pygame.image.load("images/platform_2.png").convert_alpha(),
    "platform_type_big": pygame.image.load("images/platform_big1.png").convert_alpha(),
    "platform_type_6": pygame.image.load("images/platform6.png").convert_alpha(),
    "platform_type_7": pygame.image.load("images/platform_7.png").convert_alpha(),
    "platform_type_8": pygame.image.load("images/platform_8.png").convert_alpha()
}

platforms = [
    Platform(100, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 20, "platform_type_big", platform_images, moving=False),
    Platform(850, 200, 200, 20, "platform_type_2", platform_images, moving=True, move_range=(150, 450),
             moving_vertical=True, speed=2),  # Рухається в межах 150-350
    Platform(50, 130, 200, 20, "platform_type_7", platform_images, moving=False),  # Не рухається
    Platform(650, 400, 200, 20, "platform_type_1", platform_images, moving=False),
    Platform(1000, 400, 200, 20, "platform_type_5", platform_images, moving=False),
    Platform(1000, 200, 200, 20, "platform_type_6", platform_images, moving=False),
    Platform(500, 200, 200, 20, "platform_type_2", platform_images, moving=True, move_range=(150, 450),
             moving_vertical=True, speed=2),
    Platform(1100, 500, 200, 20, "platform_type_8", platform_images, moving=False)
]

# Завантаження зображень ворога
images_dict = {
    "enemy_attack1": pygame.image.load("images/ice_golem2.png").convert_alpha(),
    "enemy_attack2": pygame.image.load("images/ice_golem3.png").convert_alpha(),
    "enemy_attack3": pygame.image.load("images/ice_golem4.png").convert_alpha(),
    "enemy_attack4": pygame.image.load("images/ice_golem5.png").convert_alpha(),
    "enemy_rock": pygame.image.load("images/ice_golem_idle.png").convert_alpha(),
    "enemy_death1": pygame.image.load("images/enemy_death1.png").convert_alpha(),
    "enemy_death2": pygame.image.load("images/enemy_death2.png").convert_alpha()
}

# Створення екземпляра ворога на платформі
enemy_platform = pygame.Rect(1150, SCREEN_HEIGHT - 500, 200, 20)  # координати та розмір платформи
enemy = Enemy(x=enemy_platform.x + 50, y=enemy_platform.y - 50, width=50, height=50, images_dict=images_dict,
              move_range=(enemy_platform.x, enemy_platform.x + enemy_platform.width - 50), speed=2)

# Додавання ворога
enemies = pygame.sprite.Group()
enemies.add(enemy)
keys = pygame.sprite.Group()
treasures = pygame.sprite.Group()
# Створення групи для зілля здоров'я
health_potions = pygame.sprite.Group()

# ключі
key = Key(1340, 430)
keys.add(key)

# скарби
treasure = Treasure(100, 60, health_potions)
treasures.add(treasure)

# Визначення координат ключа та скарбниці
key_x, key_y = 100, 200
key_width, key_height = 50, 50

treasure_x, treasure_y = 300, 400
treasure_width, treasure_height = 80, 80

# Підготовка області ключа і області скарбниці
key_area = pygame.Rect(key_x, key_y, key_width, key_height)
treasure_area = pygame.Rect(treasure_x, treasure_y, treasure_width, treasure_height)

# Створення екземпляра персонажа
player = Player(150, SCREEN_HEIGHT - 300, 10, 10)

# Ініціалізація змінних
background_x = 0
MOVEMENT_SPEED = 5

# стани гри
IN_GAME = 0
IN_MENU = 1
IN_INVENTORY = 2

# Початковий стан гри
game_state = IN_GAME

# Створення екземплярів класів Menu та Inventory
menu = Menu()
inventory = Inventory()

# Ініціалізація позицій фонів
background1_x = 0
background2_x = SCREEN_WIDTH

# Швидкість прокрутки фону
BACKGROUND_SCROLL_SPEED = 5

treasure_open_key = pygame.K_5  # клавіша '5' для відкриття скарбу

# Основний цикл гри
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moving_left = True
            elif event.key == pygame.K_RIGHT:
                player.moving_right = True
            elif event.key == pygame.K_SPACE:
                player.jump()
            elif event.key == pygame.K_ESCAPE:
                if game_state == IN_GAME:
                    game_state = IN_MENU  # Змінюємо стан гри на "Меню"
                elif game_state == IN_MENU:
                    game_state = IN_GAME  # Змінюємо стан гри на "В грі"
            elif event.key == pygame.K_1:  # Перевірка для входу в інвентар
                if game_state == IN_GAME:
                    game_state = IN_INVENTORY  # Змінюємо стан гри на "Інвентар"
                elif game_state == IN_INVENTORY:
                    game_state = IN_GAME  # Змінюємо стан гри на "В грі"
            elif event.key == pygame.K_2:  # Клавіша для атаки
                player.attack()
            elif event.key == treasure_open_key:  # Перевірка для відкриття скарбу
                # Перевірка, чи гравець знаходиться біля скарбу і він є заблокованим
                for treasure in treasures:
                    if pygame.sprite.collide_rect(player, treasure):
                        if treasure.locked:
                            if 'key' in inventory.items:
                                inventory.remove_item('key')
                                treasure.unlock()
                                # Випадання зілля здоров'я
                                if treasure.potion:
                                    inventory.add_item('health_potion')

                                treasure.rect.y -= 60  # зсуву вгору
                                print("Treasure unlocked!")
                            else:
                                print("You need a key to unlock this treasure!")
                        else:
                            print("Treasure is already unlocked")
            elif event.key == pygame.K_3:  # Клавіша для використання зілля здоров'я
                if 'health_potion' in inventory.items:
                    inventory.use_item('health_potion', player)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.moving_left = False
            elif event.key == pygame.K_RIGHT:
                player.moving_right = False
        elif event.type == pygame.MOUSEMOTION:
            if game_state == IN_MENU:
                menu.update_selection(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Ліва кнопка миші
                mouse_clicked = True

    # Оновлення гри
    player.update(platforms, keys, treasures, enemies, key_area, treasure_area, inventory, treasure)

    # Перевірка зіткнень гравця з ключами
    collected_keys = pygame.sprite.spritecollide(player, keys, False)
    for key in collected_keys:
        if not key.picked_up:
            inventory.add_item('key')  # Додаємо ключ до інвентаря
            key.picked_up = True

    # Оновлення зіль здоров'я
    health_potions.update()

    for key in keys:
        key.update()

    for treasure in treasures:
        treasure.update()

    for platform in platforms:
        platform.update()

    # Оновлення ворогів
    for enemy in enemies:
        enemy.update(platforms, player)

    # Завантаження фонового зображення
    background = pygame.image.load("images/Background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Оновлення позиції фонів, якщо персонаж рухається
    if player.moving_left:
        background1_x += BACKGROUND_SCROLL_SPEED
        background2_x += BACKGROUND_SCROLL_SPEED
        for platform in platforms:
            platform.rect.x += BACKGROUND_SCROLL_SPEED  # Зсув платформ вправо
        for enemy in enemies:
            enemy.rect.x += BACKGROUND_SCROLL_SPEED  # Зсув ворогів вправо
        for key in keys:
            key.rect.x += BACKGROUND_SCROLL_SPEED
        for treasure in treasures:
            treasure.rect.x += BACKGROUND_SCROLL_SPEED
    elif player.moving_right:
        background1_x -= BACKGROUND_SCROLL_SPEED
        background2_x -= BACKGROUND_SCROLL_SPEED
        for platform in platforms:
            platform.rect.x -= BACKGROUND_SCROLL_SPEED  # Зсув платформ вліво
        for enemy in enemies:
            enemy.rect.x -= BACKGROUND_SCROLL_SPEED  # Зсув ворогів вліво
        for key in keys:
            key.rect.x -= BACKGROUND_SCROLL_SPEED
        for treasure in treasures:
            treasure.rect.x -= BACKGROUND_SCROLL_SPEED
        for potion in health_potions:
            potion.rect.x -= BACKGROUND_SCROLL_SPEED

    # Якщо перший фон вийшов за межі екрана, перемістити його вправо
    if background1_x <= -SCREEN_WIDTH:
        background1_x = background2_x + SCREEN_WIDTH

    # Якщо другий фон вийшов за межі екрана, перемістити його вправо
    if background2_x <= -SCREEN_WIDTH:
        background2_x = background1_x + SCREEN_WIDTH

    # Малювання фонів
    screen.blit(background, (background1_x, 0))
    screen.blit(background, (background2_x, 0))

    # Малювання платформ
    for platform in platforms:
        platform.draw(screen)

    # Малювання персонажа
    player.draw(screen)

    treasures.draw(screen)
    keys.draw(screen)
    enemies.draw(screen)
    health_potions.draw(screen)

    # Малювання ворогів
    for enemy in enemies:
        enemy.draw(screen)

    # Відображення елементів (меню, інвентар)
    if game_state == IN_GAME:
        pass
    elif game_state == IN_MENU:
        menu.draw(screen)  # Малюємо меню
    elif game_state == IN_INVENTORY:
        inventory.draw(screen)  # Малюємо інвентар

    # Перевірка, чи помер гравець
    if player.dead:
        font = pygame.font.Font(None, 74)
        text = font.render("You Lost", True, (255, 0, 0))
        screen.blit(text, (250, 250))

    # Оновлення відображення
    pygame.display.flip()
    pygame.time.Clock().tick()

# Завершення Pygame
pygame.quit()
sys.exit()
