import pygame
import pygame.mixer

pygame.init()
pygame.mixer.init()

shot_sound = pygame.mixer.Sound("shot.mp3")
explosion_sound = pygame.mixer.Sound('explosion.mp3')
fail_sound = pygame.mixer.Sound("fail.mp3")

pygame.mixer.music.load("soundtrack.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

shot_sound.set_volume(0.6)

FPS = 120

clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))

screen_rect = screen.get_rect()

MAIN_BACKGROUND_COLOR = (255, 255, 255)
MISSLE_COLOR = (255, 0, 0)
SHIP_COLOR = (0, 0, 255)

GAME_OVER_COLOR = (0, 0, 0)
WIN_COLOR = (0, 255, 0)

background_color = MAIN_BACKGROUND_COLOR

ship = pygame.Rect(300, 200, 50, 100)

ship.right = screen_rect.right

ship.centery = screen_rect.centery

missle = pygame.Rect(50, 50, 10, 10)

missle.left = screen_rect.left

missle.centery = screen_rect.centery

missle_speed_x = 0
missle_speed_y = 0

ship_speed_y = 0

ship_allive = True
missle_allive = True

missle_launched = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not missle_launched:
                missle_launched = True
                missle_speed_y = 0
                missle_speed_x = 3
                pygame.mixer.music.stop()
                shot_sound.play()

            elif event.key == pygame.K_w and not missle_launched:
                missle_speed_y = -2

            elif event.key == pygame.K_s and not missle_launched:
                missle_speed_y = 2

        if missle_allive:
            missle.move_ip(missle_speed_x, missle_speed_y)
            if not missle.colliderect(screen_rect):
                missle_allive = False

                background_color = GAME_OVER_COLOR
                pygame.mixer.music.stop()
                fail_sound.play()

            if ship_allive and missle.colliderect(ship):
                missle_allive = False
                ship_allive = False
                background_color = WIN_COLOR
                explosion_sound.play()

        if ship_allive:
            ship.move_ip(0, ship_speed_y)
            if ship.bottom > screen_rect.bottom or ship.top < screen_rect.top:
                ship_speed_y = -ship_speed_y

        screen.fill(background_color)

        if ship_allive:
            pygame.draw.rect(screen, SHIP_COLOR, ship)

        if missle_allive:
            pygame.draw.rect(screen, MISSLE_COLOR, missle)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
















