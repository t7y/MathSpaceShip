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

# Enemy Images
alien_img_normal = pygame.image.load('alien.png')
alien_img_sad = pygame.image.load('sad_alien.png')
current_enemy_img = alien_img_normal  # current image for the alien

# Enemy (Alien) - starts at the same x position as the spaceship
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
# Always in math question mode (turn-based)
math_question_active = True

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


def draw_player(x, y):
    screen.blit(playerImg, (x, y))


def draw_enemy(x, y):
    screen.blit(current_enemy_img, (x, y))


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

        # Process input only if not waiting for feedback.
        if not waiting_for_feedback and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    if int(user_answer) == correct_answer:
                        feedback_message = "Correct!"
                        last_result = "correct"
                        # Immediately fire the bullet and change alien image.
                        bulletSound = mixer.Sound("laser.wav")
                        bulletSound.play()
                        fire_bullet(playerX, playerY)
                        explosionSound = mixer.Sound("explosion.wav")
                        explosionSound.play()
                        current_enemy_img = alien_img_sad
                    else:
                        feedback_message = "Incorrect!"
                        last_result = "incorrect"
                except ValueError:
                    feedback_message = "Incorrect!"
                    last_result = "incorrect"
                waiting_for_feedback = True
                feedback_start_time = pygame.time.get_ticks()
            elif event.key == pygame.K_BACKSPACE:
                user_answer = user_answer[:-1]
            else:
                if event.unicode.isdigit():
                    user_answer += event.unicode

    # Display feedback if waiting.
    if waiting_for_feedback:
        current_time = pygame.time.get_ticks()
        feedback_surface = font.render(feedback_message, True, (255, 255, 0))
        screen.blit(feedback_surface, (300, 250))
        if current_time - feedback_start_time > feedback_duration:
            waiting_for_feedback = False
            if last_result == "correct":
                score_value += 1
                # Spawn a new alien at the top with normal image.
                enemyX = playerX
                enemyY = random.randint(50, 150)
                current_enemy_img = alien_img_normal
            else:
                # Incorrect: move alien down one spot.
                enemyY += spot_size
            # Generate a new math question.
            generate_math_question()

    # Game Over check.
    if enemyY >= playerY - 50:
        game_over_text()
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    # Draw the spaceship and alien.
    draw_player(playerX, playerY)
    draw_enemy(enemyX, enemyY)

    # Animate bullet if fired.
    if bullet_state == "fire":
        bullet_animation()

    show_score(textX, textY)

    # Display math question and current answer if not waiting for feedback.
    if not waiting_for_feedback:
        question_surface = font.render(question_text, True, (255, 255, 0))
        answer_surface = font.render(user_answer, True, (255, 255, 0))
        screen.blit(question_surface, (250, 300))
        screen.blit(answer_surface, (250, 350))

    pygame.display.update()