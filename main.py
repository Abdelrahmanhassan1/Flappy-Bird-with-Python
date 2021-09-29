import pygame
import sys

# These numbers can be changed and the game will fit everything :)
WIN_WIDTH = 576
WIN_HEIGHT = 720
BASE_HEIGHT = WIN_HEIGHT // 7


# Some important functions:
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, WIN_HEIGHT - BASE_HEIGHT))
    screen.blit(floor_surface, (floor_x_pos + WIN_WIDTH, WIN_HEIGHT - BASE_HEIGHT))


pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

# We need to load the background image
bg_surface = pygame.image.load('./Assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (WIN_WIDTH, WIN_HEIGHT))

floor_surface = pygame.image.load('./Assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (WIN_WIDTH, BASE_HEIGHT))
floor_x_pos = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # This is for drawing the background image
    screen.blit(bg_surface, (0, 0))
    # then we need to plot the base surface:
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -WIN_WIDTH:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
