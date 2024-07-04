import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, images_dict, move_range=(0, 0), speed=1):
        super().__init__()
        # Завантаження зображень анімації атаки
        self.attack_frames = [
            images_dict["enemy_attack1"],
            images_dict["enemy_attack2"],
            images_dict["enemy_attack3"],
            images_dict["enemy_attack4"]
        ]
        self.rock_frame = images_dict["enemy_rock"]
        self.death_frames = [
            images_dict["enemy_death2"],
            images_dict["enemy_death1"]
        ]

        self.current_frame = 0
        self.frame_counter = 0
        self.image = self.rock_frame  # Спочатку ворог прикидається каменем
        self.rect = self.image.get_rect(topleft=(x, y))
        self.move_range = move_range
        self.speed = speed
        self.direction = 1  # Напрямок руху ворога (1 - вправо, -1 - вліво)
        self.velocity_y = 0
        self.is_aggressive = False  # Спочатку ворог не агресивний

        # Додавання атрибутів здоров'я
        self.max_health = 100
        self.health = self.max_health

        self.attack_cooldown = 0  # Змінна для відслідковування часу до наступної атаки
        self.attack_interval = 60  # Інтервал між атаками (у кадрах)

        self.is_dead = False
        self.death_animation_duration = 200  # Тривалість анімації смерті (у кадрах)
        self.death_timer = 0

    def move(self):
        if self.is_aggressive:
            self.rect.x += self.direction * self.speed
            if self.rect.x <= self.move_range[0] or self.rect.x >= self.move_range[1]:
                self.direction *= -1  # Зміна напрямку руху

    def apply_gravity(self):
        self.velocity_y += 1  # Гравітація
        if self.velocity_y > 10:  # Максимальна швидкість падіння
            self.velocity_y = 10
        self.rect.y += self.velocity_y

    def attack(self, target):
        damage_amount = 10  # Скільки урону наносить ворог
        target.take_damage(damage_amount)

    def check_collisions(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:  # Падіння
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0

    def update(self, platforms, player):
        if not self.is_dead:
            # Перевірка здоров'я ворога
            if self.health <= 0:
                self.is_dead = True
                self.current_frame = 0  # Почати анімацію смерті з першого кадру
                self.death_timer = 0

            # Якщо ворог не мертвий, він може атакувати та рухатися
            else:
                # Зменшення таймера атаки
                if self.attack_cooldown > 0:
                    self.attack_cooldown -= 1

                # Перевірка відстані до гравця та визначення агресивності
                distance_to_player = abs(self.rect.x - player.rect.x)
                if distance_to_player < 200:  # якщо гравець ближче ніж на 200 пікселів
                    self.is_aggressive = True
                else:
                    self.is_aggressive = False

                # Рух ворога
                if self.is_aggressive:
                    self.move()

                # Перевірка на колізію з гравцем та завдання урону
                if self.rect.colliderect(player.rect) and self.attack_cooldown <= 0:
                    self.attack(player)  # Нанесення урону
                    self.attack_cooldown = self.attack_interval  # Встановлення паузи між атаками

                # Оновлення анімації атаки
                if self.is_aggressive:
                    self.frame_counter += 1
                    if self.frame_counter >= 20:
                        self.frame_counter = 0
                        self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
                    self.image = self.attack_frames[self.current_frame]
                else:
                    self.image = self.rock_frame

                # Застосування гравітації
                self.apply_gravity()

                # Перевірка колізій з платформами
                self.check_collisions(platforms)

        if self.is_dead:
            # Логіка для анімації смерті
            self.death_timer += 1
            if self.death_timer == 1:  # Зміщення при першому кадрі смерті
                self.rect.y += 6  # Невеликий зсув вниз
            if self.death_timer < 30:
                self.image = self.death_frames[0]
            elif self.death_timer < 60:
                self.image = self.death_frames[1]
            else:
                # Зникнення ворога через 2 секунди (120 кадрів)
                if self.death_timer >= 120:
                    self.kill()

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw_health_bar(self, screen):
        bar_width = 100
        bar_height = 10
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 2)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        # Відобразити шкалу здоров'я
        self.draw_health_bar(screen)
