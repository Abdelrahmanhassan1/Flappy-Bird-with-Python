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


def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= (WIN_HEIGHT - BASE_HEIGHT):
        return False
    return True


def rotate_bird(surface):
    new_bird = pygame.transform.rotozoom(surface, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIN_WIDTH//2 - 10, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIN_WIDTH // 2 - 10, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('High Score: ' + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(WIN_WIDTH // 2 - 10, WIN_HEIGHT // 2 + 50))
        screen.blit(high_score_surface, high_score_rect)


def update_score(game_score, game_high_score):
    if game_score > game_high_score:
        game_high_score = game_score
    return game_high_score


# Starting the game
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('Arial', 40)

# Game Variables:
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0

# We need to load the background image
bg_surface = pygame.image.load('./Assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (WIN_WIDTH, WIN_HEIGHT))

floor_surface = pygame.image.load('./Assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (WIN_WIDTH, BASE_HEIGHT))
floor_x_pos = 0

# Now let's change this to animate the bird
#    bird_surface = pygame.image.load('./Assets/bluebird-midflap.png').convert_alpha()
#   #    If we want to change the size of the bird
#   # bird_surface = pygame.transform.scale2x(bird_surface)
#    bird_rect = bird_surface.get_rect(center=(50, WIN_HEIGHT//2 + 50))
# The new bird surfaces to animate the bird:
bird_downflap = pygame.image.load('./Assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('./Assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('./Assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, WIN_HEIGHT//2 + 50))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Adding the pipes:
pipe_surface = pygame.image.load('./Assets/pipe-green.png')
# pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

SPAWN_PIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, millis=1200)
pipe_height = [500, 400, 450, 350, 520]

game_over_surface = pygame.transform.scale2x(pygame.image.load('./Assets/gameover.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT // 2 - 50))

flap_sound = pygame.mixer.Sound('./audio/wing.wav')
death_sound = pygame.mixer.Sound('./audio/hit.wav')
score_sound = pygame.mixer.Sound('./audio/point.wav')
score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # if player is pressing the space button and the game is still working
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()

            # Here the player is trying to play while the game is over:
            # So we reset every thing clearing the pipe list and resetting the position of the bird
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, WIN_HEIGHT//2 + 50)
                bird_movement = 0
                score = 0

        # This is when the user passes a pipe we need to add a new pipe to the screen
        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    # This is for drawing the background image
    screen.blit(bg_surface, (0, 0))

    # The loop of the game
    # Changing the bird position by adding movement to its rectangle
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collisions(pipe_list)
        # Moving the pipes:
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # then we need to plot the base surface:
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -WIN_WIDTH:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
