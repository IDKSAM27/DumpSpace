# made in 2 min
import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Game Settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Survival Game")

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Load Images
background_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "background.png"))
# background_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "background.png"))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Ensure it fits the screen

player_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "player.png"))
zombie_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "zombie.png"))
bullet_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "bullet.png"))

# Player Class
class Player:
    def __init__(self):
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.speed = 4
        self.health = 100

    def move(self, keys):
        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed

    def draw(self):
        screen.blit(player_img, (self.x, self.y))
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.health * 0.4, 5))  # Health bar

# Zombie Class
class Zombie:
    def __init__(self):
        self.x, self.y = random.choice([(random.randint(0, WIDTH), random.choice([0, HEIGHT])),
                                        (random.choice([0, WIDTH]), random.randint(0, HEIGHT))])
        self.speed = 1.5
        self.health = 50

    def move(self, player):
        angle = math.atan2(player.y - self.y, player.x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

    def draw(self):
        screen.blit(zombie_img, (self.x, self.y))
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, 30, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.health * 0.3, 5))

# Bullet Class
class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x, self.y = x, y
        angle = math.atan2(target_y - y, target_x - x)
        self.speed_x = 6 * math.cos(angle)
        self.speed_y = 6 * math.sin(angle)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        screen.blit(bullet_img, (self.x, self.y))

# Game Variables
player = Player()
zombies = []
bullets = []
score = 0

# Main Game Loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.blit(background_img, (0, 0))  # Draw Background Image

    # Spawn Zombies
    if random.randint(1, 100) < 3:
        zombies.append(Zombie())

    # Handle Events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet(player.x, player.y, *pygame.mouse.get_pos())
            bullets.append(bullet)

    # Move and Draw Player
    player.move(keys)
    player.draw()

    # Move and Draw Zombies
    for zombie in zombies[:]:
        zombie.move(player)
        zombie.draw()
        if math.hypot(player.x - zombie.x, player.y - zombie.y) < 30:  # Collision detection
            player.health -= 0.5
        if player.health <= 0:
            running = False  # Game Over

    # Move and Draw Bullets
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()

        # Check if Bullet Hits Zombie
        for zombie in zombies[:]:
            if math.hypot(bullet.x - zombie.x, bullet.y - zombie.y) < 25:
                zombies.remove(zombie)
                bullets.remove(bullet)
                score += 1
                break  # Prevent multiple deletions

    # Display Score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
print(f"Game Over! Your Score: {score}")



# import pygame
# import random
# import math
# import os

# # Initialize Pygame
# pygame.init()

# # Game Settings
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Zombie Survival Game")

# # Colors
# WHITE = (255, 255, 255)
# RED = (200, 0, 0)
# GREEN = (0, 200, 0)
# BLACK = (0, 0, 0)

# # Load Images
# player_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "player.png"))
# zombie_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "zombie.png"))
# bullet_img = pygame.image.load(os.path.join("Skills4Future", "pygame", "bullet.png"))

# # Player Class
# class Player:
#     def __init__(self):
#         self.x, self.y = WIDTH // 2, HEIGHT // 2
#         self.speed = 4
#         self.health = 100

#     def move(self, keys):
#         if keys[pygame.K_w]: self.y -= self.speed
#         if keys[pygame.K_s]: self.y += self.speed
#         if keys[pygame.K_a]: self.x -= self.speed
#         if keys[pygame.K_d]: self.x += self.speed

#     def draw(self):
#         screen.blit(player_img, (self.x, self.y))
#         pygame.draw.rect(screen, RED, (self.x, self.y - 10, 40, 5))
#         pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.health * 0.4, 5))  # Health bar

# # Zombie Class
# class Zombie:
#     def __init__(self):
#         self.x, self.y = random.choice([(random.randint(0, WIDTH), random.choice([0, HEIGHT])),
#                                         (random.choice([0, WIDTH]), random.randint(0, HEIGHT))])
#         self.speed = 1.5
#         self.health = 50

#     def move(self, player):
#         angle = math.atan2(player.y - self.y, player.x - self.x)
#         self.x += self.speed * math.cos(angle)
#         self.y += self.speed * math.sin(angle)

#     def draw(self):
#         screen.blit(zombie_img, (self.x, self.y))
#         pygame.draw.rect(screen, RED, (self.x, self.y - 10, 30, 5))
#         pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.health * 0.3, 5))

# # Bullet Class
# class Bullet:
#     def __init__(self, x, y, target_x, target_y):
#         self.x, self.y = x, y
#         angle = math.atan2(target_y - y, target_x - x)
#         self.speed_x = 6 * math.cos(angle)
#         self.speed_y = 6 * math.sin(angle)

#     def move(self):
#         self.x += self.speed_x
#         self.y += self.speed_y

#     def draw(self):
#         screen.blit(bullet_img, (self.x, self.y))

# # Game Variables
# player = Player()
# zombies = []
# bullets = []
# score = 0

# # Main Game Loop
# running = True
# clock = pygame.time.Clock()

# while running:
#     clock.tick(60)
#     screen.fill(WHITE)

#     # Spawn Zombies
#     if random.randint(1, 100) < 3:
#         zombies.append(Zombie())

#     # Handle Events
#     keys = pygame.key.get_pressed()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             bullet = Bullet(player.x, player.y, *pygame.mouse.get_pos())
#             bullets.append(bullet)

#     # Move and Draw Player
#     player.move(keys)
#     player.draw()

#     # Move and Draw Zombies
#     for zombie in zombies[:]:
#         zombie.move(player)
#         zombie.draw()
#         if math.hypot(player.x - zombie.x, player.y - zombie.y) < 30:  # Collision detection
#             player.health -= 0.5
#         if player.health <= 0:
#             running = False  # Game Over

#     # Move and Draw Bullets
#     for bullet in bullets[:]:
#         bullet.move()
#         bullet.draw()

#         # Check if Bullet Hits Zombie
#         for zombie in zombies[:]:
#             if math.hypot(bullet.x - zombie.x, bullet.y - zombie.y) < 25:
#                 zombies.remove(zombie)
#                 bullets.remove(bullet)
#                 score += 1
#                 break  # Prevent multiple deletions

#     # Display Score
#     font = pygame.font.Font(None, 36)
#     text = font.render(f"Score: {score}", True, BLACK)
#     screen.blit(text, (10, 10))

#     pygame.display.flip()

# pygame.quit()
# print(f"Game Over! Your Score: {score}")