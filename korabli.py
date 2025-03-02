import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TARGET_SIZE = 50
BULLET_SPEED = 10
BULLET_WIDTH = 5
BULLET_HEIGHT = 5
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Загрузка звуковых эффектов
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
win_sound = pygame.mixer.Sound("win.wav")
lose_sound = pygame.mixer.Sound("lose.wav")


# Класс Игрок
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        # Ограничение движения игрока
        self.rect.x = max(0, min(SCREEN_WIDTH - PLAYER_WIDTH, self.rect.x))


# Класс Цель
class Target:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - TARGET_SIZE), 0, TARGET_SIZE, TARGET_SIZE)
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        # Перезапуск цели, если она ушла вниз
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, SCREEN_WIDTH - TARGET_SIZE)


# Класс Снаряд
class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BULLET_WIDTH, BULLET_HEIGHT)

    def update(self):
        self.rect.y -= BULLET_SPEED


# Функция проверки столкновения
def check_collision(bullets, target):
    for bullet in bullets:
        if bullet.rect.colliderect(target.rect):
            bullets.remove(bullet)
            return True
    return False


# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting Game")

# Создание объектов
player = Player()
target = Target()
bullets = []
score = 0
game_over = False

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-5)
    if keys[pygame.K_RIGHT]:
        player.move(5)
    if keys[pygame.K_SPACE] and not game_over:  # стрельба
        bullets.append(Bullet(player.rect.centerx, player.rect.top))
        shoot_sound.play()

    # Обновление объектов
    if not game_over:
        target.update()
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.y < 0:  # Удаление снарядов, вышедших за экран
                bullets.remove(bullet)

        # Проверка на поражение цели
        if check_collision(bullets, target):
            score += 1
            hit_sound.play()
            target = Target()  # Замена цели при попадании

        # Условие поражения
        if target.rect.y >= SCREEN_HEIGHT - TARGET_SIZE:
            game_over = True
            lose_sound.play()

    # Отрисовка объектов
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, player.rect)
    pygame.draw.rect(screen, RED, target.rect)
    for bullet in bullets:
        pygame.draw.rect(screen, GREEN, bullet.rect)

    # Отображение результата
    if game_over:
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

    pygame.display.flip()
    pygame.time.Clock().tick(60)