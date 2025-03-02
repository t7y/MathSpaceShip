import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player (Spaceship) - remains fixed at the bottom center
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480

# Enemy (Alien) - starts at the same x position as the spaceship
enemyImg = pygame.image.load('alien.png')
enemyX = playerX
enemyY = random.randint(50, 150)
spot_size = 40  # distance the alien moves down if the answer is wrong

# Bullet (for visual effect only)
bulletImg = pygame.image.load('bullet.png')
bullet_state = "ready"  # "ready" or "fire"
bulletX = playerX
bulletY = playerY

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over font
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Math Question Variables
question_text = ""
correct_answer = 0
user_answer = ""
math_question_active = True  # Always in math question mode

# Feedback variables
feedback_message = ""
feedback_start_time = 0
feedback_duration = 1000  # milliseconds (1 second)
waiting_for_feedback = False  # True when feedback is being displayed
last_result = None  # "correct" or "incorrect"


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state, bulletX, bulletY
    bullet_state = "fire"
    bulletX = x
    bulletY = y
    screen.blit(bulletImg, (bulletX + 16, bulletY + 10))


def bullet_animation():
    global bulletY, bullet_state
    if bullet_state == "fire":
        screen.blit(bulletImg, (bulletX + 16, bulletY + 10))
        bulletY -= 15
        if bulletY < 0:
            bullet_state = "ready"
            bulletY = playerY


def generate_math_question():
    global question_text, correct_answer, user_answer
    operator = random.choice(["+", "-", "*"])
    if operator == "+":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        correct_answer = a + b
    elif operator == "-":
        a = random.randint(1, 10)
        b = random.randint(1, a)  # ensure non-negative result
        correct_answer = a - b
    else:  # multiplication
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        correct_answer = a * b
    question_text = f"{a} {operator} {b} = ?"
    user_answer = ""


# Generate the first math question
generate_math_question()

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Only allow input if not waiting for feedback
        if not waiting_for_feedback and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    if int(user_answer) == correct_answer:
                        feedback_message = "Correct!"
                        last_result = "correct"
                    else:
                        feedback_message = "Incorrect!"
                        last_result = "incorrect"
                except ValueError:
                    feedback_message = "Incorrect!"
                    last_result = "incorrect"
                # Start feedback timer and disable further input
                waiting_for_feedback = True
                feedback_start_time = pygame.time.get_ticks()
            elif event.key == pygame.K_BACKSPACE:
                user_answer = user_answer[:-1]
            else:
                # Accept only digits for the answer.
                if event.unicode.isdigit():
                    user_answer += event.unicode

    # During feedback, display the message until the timer elapses.
    if waiting_for_feedback:
        current_time = pygame.time.get_ticks()
        feedback_surface = font.render(feedback_message, True, (255, 255, 0))
        screen.blit(feedback_surface, (300, 250))
        # Check if feedback duration has passed
        if current_time - feedback_start_time > feedback_duration:
            waiting_for_feedback = False
            # Process the result after feedback:
            if last_result == "correct":
                # Correct: fire bullet (visual and sound) and reset alien at top.
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                fire_bullet(playerX, playerY)
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                score_value += 1
                enemyX = playerX
                enemyY = random.randint(50, 150)
            else:
                # Incorrect: move alien closer.
                enemyY += spot_size
            # Generate a new math question for the next turn.
            generate_math_question()

    # Check game over condition: if alien gets too close to the spaceship.
    if enemyY >= playerY - 50:
        game_over_text()
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    # Draw spaceship, alien, and animate bullet if active.
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    if bullet_state == "fire":
        bullet_animation()

    show_score(textX, textY)

    # Display math question and current answer input if not waiting for feedback.
    if not waiting_for_feedback:
        question_surface = font.render(question_text, True, (255, 255, 0))
        answer_surface = font.render(user_answer, True, (255, 255, 0))
        screen.blit(question_surface, (250, 300))
        screen.blit(answer_surface, (250, 350))

    pygame.display.update()