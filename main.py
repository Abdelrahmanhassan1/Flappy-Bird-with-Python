import pygame
import sys
import random

# These numbers can be changed and the game will fit everything :)
WIN_WIDTH = 576
WIN_HEIGHT = 720
BASE_HEIGHT = WIN_HEIGHT // 7


# Some important functions:
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, WIN_HEIGHT - BASE_HEIGHT))
    screen.blit(floor_surface, (floor_x_pos + WIN_WIDTH, WIN_HEIGHT - BASE_HEIGHT))


def create_pipe():
    random_height_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_height_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_height_pos - 200))
    return bottom_pipe, top_pipe


# Here we are taking the list of pipes and then we are moving them somehow to the left
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= WIN_HEIGHT - 100:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# Starting the game
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

# Game Variables:
gravity = 0.15
bird_movement = 0

# We need to load the background image
bg_surface = pygame.image.load('./Assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (WIN_WIDTH, WIN_HEIGHT))

floor_surface = pygame.image.load('./Assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (WIN_WIDTH, BASE_HEIGHT))
floor_x_pos = 0

bird_surface = pygame.image.load('./Assets/bluebird-midflap.png').convert()
#    If we want to change the size of the bird
# bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(50, WIN_HEIGHT//2 + 50))

# Adding the pipes:
pipe_surface = pygame.image.load('./Assets/pipe-green.png')
# pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, millis=1200)
pipe_height = [500, 400, 450, 350, 520]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 6

        # This is when the user passes a pipe we need to add a new pipe to the screen
        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())

    # This is for drawing the background image
    screen.blit(bg_surface, (0, 0))

    # Changing the bird position by adding movement to its rectangle
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    # Moving the pipes:
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # then we need to plot the base surface:
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -WIN_WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
