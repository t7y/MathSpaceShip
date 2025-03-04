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
spot_size = 40  # distance the alien moves down if the answer is wrong or timed out

# Bullet (for visual effect only)
bulletImg = pygame.image.load('bullet.png')
bullet_state = "ready"  # "ready" or "fire"
bulletX = playerX
bulletY = playerY

# Score and incorrect answer counters
score_value = 0
incorrect_count = 0
consecutive_incorrect_count = 0  # New variable to count consecutive incorrect answers

font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over/Win font (for win, we'll still use the larger font)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Math Question Variables
question_text = ""
correct_answer = 0
user_answer = ""
math_question_active = True  # always in math question mode

# Timer for answering the question (in milliseconds)
question_timeout = 10000  # 10 seconds
question_start_time = 0  # start time for the current question

# Feedback variables
feedback_message = ""
feedback_start_time = 0
feedback_duration = 1000  # milliseconds (1 second)
waiting_for_feedback = False  # True when feedback is being displayed
last_result = None  # "correct" or "incorrect" or "timeout"
waiting_for_enter = False  # New variable to track if we're waiting for Enter key after incorrect answer

def show_score(x, y):
    score_text = font.render("Score: " + str(score_value), True, (255, 255, 255))
    incorrect_text = font.render("Incorrect: " + str(incorrect_count), True, (255, 255, 255))
    screen.blit(score_text, (x, y))
    screen.blit(incorrect_text, (x, y + 40))

def show_timer(x, y, time_left):
    timer_text = font.render("Time: " + str(time_left), True, (255, 255, 255))
    screen.blit(timer_text, (x, y))

def game_over_text(reason=None):
    # Use a smaller font for game over messages
    game_over_font = pygame.font.Font('freesansbold.ttf', 40)
    if reason == "3_wrong_answers":
        message = "GAME OVER. Too Many Wrong Answers!"
    else:
        message = "GAME OVER"
    over_text = game_over_font.render(message, True, (255, 255, 255))
    # Center the text on the screen
    text_rect = over_text.get_rect(center=(400, 300))
    screen.blit(over_text, text_rect)
    
    # Display final score
    score_font = pygame.font.Font('freesansbold.ttf', 32)
    final_score_text = score_font.render(f"Final Score: {score_value}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(400, 370))
    screen.blit(final_score_text, final_score_rect)
    
    # Display incorrect answers
    incorrect_text = score_font.render(f"Incorrect Answers: {incorrect_count}", True, (255, 255, 255))
    incorrect_rect = incorrect_text.get_rect(center=(400, 420))
    screen.blit(incorrect_text, incorrect_rect)

def game_win_text():
    win_text = over_font.render("YOU WIN!", True, (255, 255, 255))
    text_rect = win_text.get_rect(center=(400, 300))
    screen.blit(win_text, text_rect)
    
    # Display final score
    score_font = pygame.font.Font('freesansbold.ttf', 32)
    final_score_text = score_font.render(f"Final Score: {score_value}", True, (255, 255, 255))
    final_score_rect = final_score_text.get_rect(center=(400, 370))
    screen.blit(final_score_text, final_score_rect)
    
    # Display incorrect answers
    incorrect_text = score_font.render(f"Incorrect Answers: {incorrect_count}", True, (255, 255, 255))
    incorrect_rect = incorrect_text.get_rect(center=(400, 420))
    screen.blit(incorrect_text, incorrect_rect)

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
    global question_text, correct_answer, user_answer, question_start_time
    # For 3rd grade: addition, subtraction, multiplication, and simple division.
    operator = random.choice(["+", "-", "*", "/"])
    if operator == "+":
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        correct_answer = a + b
    elif operator == "-":
        a = random.randint(1, 20)
        b = random.randint(0, a)  # ensure non-negative result
        correct_answer = a - b
    elif operator == "*":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        correct_answer = a * b
    else:  # division, ensure integer result
        b = random.randint(1, 10)
        correct_answer = random.randint(1, 10)
        a = b * correct_answer
        operator = "/"  # override operator to division
    question_text = f"{a} {operator} {b} = ?"
    user_answer = ""
    question_start_time = pygame.time.get_ticks()

# Generate the first math question
generate_math_question()

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    current_time = pygame.time.get_ticks()

    # Calculate remaining time (in seconds)
    time_left = max(0, (question_timeout - (current_time - question_start_time)) // 1000)

    # If not waiting for feedback or enter key, check for timeout.
    if not waiting_for_feedback and not waiting_for_enter and current_time - question_start_time > question_timeout:
        feedback_message = "Timeout!"
        last_result = "incorrect"
        waiting_for_feedback = True
        feedback_start_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for Enter key press when waiting for enter after incorrect answer
        if waiting_for_enter and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            waiting_for_enter = False
            # Incorrect or timeout: increment counter and move alien down.
            incorrect_count += 1
            consecutive_incorrect_count += 1
            if consecutive_incorrect_count >= 3:
                game_over_text("3_wrong_answers")
                pygame.display.update()
                pygame.time.wait(3000)
                running = False
                continue
            enemyY += spot_size
            generate_math_question()
            
        # Process input only if not waiting for feedback or enter key.
        elif not waiting_for_feedback and not waiting_for_enter and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                try:
                    if int(user_answer) == correct_answer:
                        feedback_message = "Correct!"
                        last_result = "correct"
                        # Immediately fire bullet and change enemy image.
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
        feedback_surface = font.render(feedback_message, True, (255, 255, 0))
        screen.blit(feedback_surface, (300, 250))
        if current_time - feedback_start_time > feedback_duration:
            waiting_for_feedback = False
            if last_result == "correct":
                score_value += 1
                consecutive_incorrect_count = 0  # Reset consecutive counter on success
                # Check for win condition
                if score_value >= 20:
                    game_win_text()
                    pygame.display.update()
                    pygame.time.wait(3000)
                    running = False
                    continue
                # Spawn a new alien at the top with normal image.
                enemyX = playerX
                enemyY = random.randint(50, 150)
                current_enemy_img = alien_img_normal
                generate_math_question()
            else:
                # For incorrect answers, transition to waiting for enter state
                waiting_for_enter = True
    
    # Display correct answer and prompt for Enter key if waiting after incorrect answer
    elif waiting_for_enter:
        question_text_surface = font.render(question_text, True, (255, 255, 0))
        correct_answer_text = font.render(f"The correct answer is: {correct_answer}", True, (255, 255, 0))
        press_enter_text = font.render("Press ENTER to continue", True, (255, 255, 0))
        
        # Position the text elements with proper spacing
        screen.blit(question_text_surface, (250, 250))
        screen.blit(correct_answer_text, (250, 300))
        screen.blit(press_enter_text, (250, 350))

    # Game Over check: if the alien gets too close to the spaceship.
    if enemyY >= playerY - 50:
        game_over_text()
        pygame.display.update()
        pygame.time.wait(3000)
        running = False

    # Draw the spaceship and the alien.
    draw_player(playerX, playerY)
    draw_enemy(enemyX, enemyY)

    # Animate bullet if fired.
    if bullet_state == "fire":
        bullet_animation()

    show_score(textX, textY)
    # Display timer in the upper right corner.
    show_timer(650, 10, time_left)

    # Display math question and current answer if not waiting for feedback or enter key.
    if not waiting_for_feedback and not waiting_for_enter:
        question_surface = font.render(question_text, True, (255, 255, 0))
        answer_surface = font.render(user_answer, True, (255, 255, 0))
        screen.blit(question_surface, (250, 300))
        screen.blit(answer_surface, (250, 350))

    pygame.display.update()