import pygame
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Завантаження зображень анімації ходьби
        self.walking_frames = [
            pygame.image.load("images/walk1.png").convert_alpha(),
            pygame.image.load("images/walk2.png").convert_alpha(),
            pygame.image.load("images/walk3.png").convert_alpha(),
            pygame.image.load("images/walk4.png").convert_alpha(),
            pygame.image.load("images/walk5.png").convert_alpha()
        ]
        # Завантаження зображень анімації спокою
        self.idle_frame = pygame.image.load("images/idle.png").convert_alpha()

        # Завантаження зображень анімації стрибка
        self.jumping_frames = [
            pygame.image.load("images/jump1.png").convert_alpha(),
            pygame.image.load("images/jump2.png").convert_alpha(),
            pygame.image.load("images/jump3.png").convert_alpha()
        ]

        self.attack_frames = [
            pygame.image.load("images/attack3.png").convert_alpha()
        ]

        self.death_frames = [
            pygame.image.load("images/death_ch1.png").convert_alpha(),
            pygame.image.load("images/death_ch2.png").convert_alpha(),
            pygame.image.load("images/death_ch3.png").convert_alpha(),
            pygame.image.load("images/death_ch4.png").convert_alpha(),
            pygame.image.load("images/death_ch5.png").convert_alpha()
        ]

        self.current_frame = 0
        self.frame_counter = 0
        self.image = self.idle_frame  # Ініціалізація атрибута self.image
        self.rect = self.image.get_rect(topleft=(x, y))  # Використання self.image для створення self.rect
        self.velocity_y = 0
        self.velocity_x = 0
        self.on_ground = False
        self.moving_left = False
        self.moving_right = False
        self.facing_right = True  # Додаємо змінну для напрямку руху
        self.jumping = False
        self.attacking = False
        self.dying = False
        self.dead = False
        self.enemy = None  # Посилання на ворога

        # Додавання атрибутів здоров'я
        self.max_health = 100
        self.health = self.max_health
        self.inventory = Inventory()
        self.has_key = False  # Змінна для перевірки наявності ключа

        # Швидкість анімації смерті
        self.death_animation_speed = 20

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def jump(self):
        if self.on_ground and not self.dying and not self.dead:
            self.velocity_y = -16
            self.on_ground = False
            self.jumping = True

    def attack(self):
        if self.enemy is not None:
            self.enemy.take_damage(10)  # нанесення урону ворогові
        if not self.attacking and not self.dying and not self.dead:
            self.attacking = True
            self.current_frame = 0
            self.frame_counter = 0
            # Збільшуємо швидкість пересування по горизонталі під час атаки
            if self.facing_right:
                self.velocity_x += 5
            else:
                self.velocity_x -= 5

    def apply_gravity(self):
        if not self.dying and not self.dead:
            self.velocity_y += 1  # Гравітація
            if self.velocity_y > 10:  # Максимальна швидкість падіння
                self.velocity_y = 10
            self.rect.y += self.velocity_y

    def check_collisions(self, platforms):
        self.on_ground = False
        for platform in platforms:
            # Оновлення для перевірки зменшеної маски платформи
            platform_mask_rect = platform.mask_rect.move(platform.rect.topleft)
            if self.rect.colliderect(platform_mask_rect):
                if self.velocity_y > 0:  # Падіння
                    self.rect.bottom = platform_mask_rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jumping = False  # Завершуємо стрибок

    def check_key_pickup(self, keys):
        for key in keys:
            if pygame.sprite.collide_mask(self, key):
                if not key.picked_up:
                    self.inventory.add_item('key')
                    key.picked_up = True
                    keys.remove(key)
                    print(f"Key added to inventory. Current items: {self.inventory.items}")

    def check_treasure_interaction(self, treasures):
        for treasure in treasures:
            if pygame.sprite.collide_mask(self, treasure):
                if 'key' in self.inventory.items and treasure.locked:
                    treasure.unlock()
                    print("Treasure unlocked!")
                elif treasure.locked:
                    print("You need a key to unlock this treasure!")

    def update(self, platforms, keys, treasures, enemies, key_area, treasure_area, inventory, treasure):
        # перевірка відстані до ворога та оновлення посилання
        for enemy in enemies:
            distance_to_enemy = abs(self.rect.x - enemy.rect.x)
            if distance_to_enemy < 200:  # якщо гравець ближче ніж на 200 пікселів
                self.enemy = enemy
                break
        else:
            self.enemy = None

        # Якщо гравець помер, не виконувати інші дії
        if self.dead:
            return

        # Горизонтальний рух
        if self.moving_left:
            self.velocity_x = -2
            self.facing_right = False
        elif self.moving_right:
            self.velocity_x = 2
            self.facing_right = True
        else:
            self.velocity_x = 0

        self.move(self.velocity_x, 0)

        # Застосування гравітації
        self.apply_gravity()

        # Перевірка колізій
        self.check_collisions(platforms)
        self.check_key_pickup(keys)
        self.check_treasure_interaction(treasures)

        # Оновлення анімації смерті
        if self.dying:
            self.frame_counter += 1
            if self.frame_counter >= self.death_animation_speed:
                self.frame_counter = 0
                self.current_frame += 1
                if self.current_frame >= len(self.death_frames):
                    self.current_frame = len(self.death_frames) - 1
                    self.dead = True  # Гравець помер
            self.image = self.death_frames[self.current_frame]

            # Підняття передостаннього та останнього кадрів анімації смерті
            if self.current_frame == len(self.death_frames) - 2:  # Передостанній кадр
                self.rect.y -= 2  # Зміщення кадру вгору
            elif self.dead:  # Останній кадр
                self.rect.y -= 15  # Зміщення кадру вгору

            return  # Зупинити оновлення інших анімацій
        # Оновлення анімації
        if self.jumping:
            self.frame_counter += 1
            if self.frame_counter >= 10:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                self.image = self.jumping_frames[self.current_frame]
            # Припинення стрибка після досягнення останнього кадру
            if self.current_frame == len(self.jumping_frames) - 1:
                self.jumping = False
                self.current_frame = 0
                self.image = self.jumping_frames[self.current_frame]
            self.image = self.jumping_frames[self.current_frame]
        elif self.moving_left or self.moving_right:
            self.frame_counter += 1
            if self.frame_counter >= 10:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
            self.image = self.walking_frames[self.current_frame]
        elif self.attacking:
            self.frame_counter += 1
            if self.frame_counter >= 10:
                self.frame_counter = 0
                self.current_frame += 1
                if self.current_frame >= len(self.attack_frames):
                    self.current_frame = 0
                    self.attacking = False  # Завершення атаки
            self.image = self.attack_frames[self.current_frame]
        else:
            self.image = self.idle_frame

    def take_damage(self, amount):
        if not self.dying and not self.dead:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.dying = True  # Почати анімацію смерті
                self.current_frame = 0
                self.frame_counter = 0

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 2)

    def draw(self, screen):
        flipped_image = pygame.transform.flip(self.image, not self.facing_right, False)
        screen.blit(flipped_image, self.rect.topleft)
        self.draw_health_bar(screen)
