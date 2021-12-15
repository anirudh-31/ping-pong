import pygame
import sys
from random import *

# initializing pygame
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

# setting up the clock
clock = pygame.time.Clock()

# setting up the game window and adding its name and icon
screen_width = 1280
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PING PONG")
icon = pygame.image.load("ping-pong.png")
pygame.display.set_icon(icon)

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Speed Variables
ball_speed_x = 7 * choice((-1, 1))
ball_speed_y = 7 * choice((-1, 1))
player_speed = 0
opponent_speed = 7

# colors
bg_color = (0, 0, 0)
light_grey = (200, 200, 200)

# Sounds
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")


# Functions
def ball_restart():
    global ball_speed_x, ball_speed_y, score_timer

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    if current_time - score_timer < 700:
        number_three = game_font.render("3", True, light_grey)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 700 < current_time - score_timer < 1400:
        number_two = game_font.render("2", True, light_grey)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    if 1400 < current_time - score_timer < 2100:
        number_one = game_font.render("1", True, light_grey)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_timer < 2100:
        ball_speed_x = ball_speed_y = 0

    else:
        ball_speed_y = 7 * choice((-1, 1))
        ball_speed_x = 7 * choice((-1, 1))
        score_timer = None


def ball_movement():
    # reversing the vertical movements of the ball if it hits the top and bottom boundaries
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_timer

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        pong_sound.play()
        ball_speed_y *= -1
    # reversing the horizontal movement of the ball if it hits the side boundaries
    if ball.left <= 0:
        score_sound.play()
        player_score += 1
        score_timer = pygame.time.get_ticks()
    if ball.right >= screen_width:
        score_sound.play()
        opponent_score += 1
        score_timer = pygame.time.get_ticks()
    # reversing the horizontal movement of the ball if it collides with the opponent or player
    if ball.colliderect(player) and ball_speed_x > 0:
        pong_sound.play()
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pong_sound.play()
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_movement():
    global player_speed
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_movement():
    global opponent_speed, screen_height
    if opponent.top <= ball.y:
        opponent.top += opponent_speed
    if opponent.bottom >= ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


# score variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)
score_timer = True

# game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # movements
    ball_movement()
    player_movement()
    opponent_movement()

    # visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.aaline(screen, (36, 33, 33), (screen_width / 2, 0), (screen_width / 2, screen_height))
    pygame.draw.ellipse(screen, light_grey, ball)

    if score_timer:
        ball_restart()

    player_text = game_font.render(str(player_score), True, light_grey)
    screen.blit(player_text, (660, 370))
    opponent_text = game_font.render(str(opponent_score), True, light_grey)
    screen.blit(opponent_text, (600, 370))

    # ending the game
    if player_score == 6 or opponent_score == 6:
        if player_score == 6:
            screen.fill((0, 0, 0))
            won = game_font.render("YOU WON", True, light_grey)
            screen.blit(won, (screen_width / 2 - won.get_width() / 2, screen_height / 2 - won.get_height() / 2))
            running = False

        if opponent_score == 6:
            screen.fill((0, 0, 0))
            won = game_font.render("YOU LOST", True, light_grey)
            screen.blit(won, (screen_width / 2 - won.get_width() / 2, screen_height / 2 - won.get_height() / 2))
            running = False

    # updating the screen
    pygame.display.update()
    clock.tick(60)
