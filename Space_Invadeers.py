import pygame, math, random, sys
from pygame import mixer
from button import Button

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (800, 600))

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Font for menu
font_menu = pygame.font.SysFont("arialblack", 40)

pygame.display.set_caption("Main Menu")

game_pause = False
player_name = ""

# Menu of the game
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def reset_game():
    global playerX, playerY, playerX_Change, bulletX, bulletY, Bullet_state, score_value, enemyX, enemyY, enemyX_change, enemyY_change
    playerX = 370
    playerY = 500
    playerX_Change = 0

    bulletX = 0
    bulletY = 480
    Bullet_state = "ready"

    score_value = 0

    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    for i in range(num_of_enemy):
        enemyX.append(random.randint(0, 735))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(0.2)
        enemyY_change.append(30)

def play():
    reset_game()
    global playerX, playerY, playerX_Change, bulletX, bulletY, Bullet_state, score_value
    running = True
    while running:
        # RGB stands for red, green, and blue
        screen.fill((0, 0, 0))
        # Background image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
            # If keystroke is pressed, check whether it's right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_Change = -0.5
                if event.key == pygame.K_RIGHT:
                    playerX_Change = 0.5
                if event.key == pygame.K_SPACE:
                    if Bullet_state == "ready":  # Get the current x coordinate of the spaceship
                        bullet_Sound = mixer.Sound("laser.wav")
                        bullet_Sound.play() 
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_Change = 0       

        playerX += playerX_Change
        if playerX < 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement
        for i in range(num_of_enemy):
            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemy):
                    enemyY[j] = 10000
                game_over_text()
                save_score(player_name, score_value)
                game_over_menu()
                running = False
                break
                
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.2
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX , bulletY)
            if collision:
                explosion_Sound = mixer.Sound("explosion.wav")
                explosion_Sound.play()
                bulletY = 480
                Bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150) 
            
            enemy(enemyX[i], enemyY[i], i)
        
        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            Bullet_state = "ready"
        if Bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        
        player(playerX, playerY)
        show_score(textX, textY)
        pygame.display.update()

def leader_boards():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))

        OPTIONS_TEXT = get_font(20).render("Leaderboard", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 100))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        y_offset = 150
        with open("files.txt", "r") as file:
            for line in file.readlines():
                name, score = line.strip().split(":")
                score_text = get_font(20).render(f"{name}: {score}", True, "White")
                screen.blit(score_text, (300, y_offset))
                y_offset += 30

        OPTIONS_BACK = Button(image=None, pos=(400, 500), text_input="BACK", font=get_font(30), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def game_over_menu():
    while True:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()

        GAME_OVER_TEXT = get_font(80).render("GAME OVER", True, "Red")
        GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(400, 100))

        PLAY_AGAIN_BUTTON = Button(None, pos=(400, 250), text_input="PLAY AGAIN", font=get_font(50), base_color="White", hovering_color="Green")
        BACK_TO_MENU_BUTTON = Button(None, pos=(400, 400), text_input="BACK TO MENU", font=get_font(50), base_color="White", hovering_color="Green")

        screen.blit(GAME_OVER_TEXT, GAME_OVER_RECT)

        for button in [PLAY_AGAIN_BUTTON, BACK_TO_MENU_BUTTON]:
            button.changeColor(GAME_OVER_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_AGAIN_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    play()
                if BACK_TO_MENU_BUTTON.checkForInput(GAME_OVER_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(None,pos=(400, 250),text_input="PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        Leaderboards = Button(None,pos=(400, 400),text_input="LEADER BOARDS", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(None,pos=(400, 550),text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, Leaderboards, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    get_player_name()
                if Leaderboards.checkForInput(MENU_MOUSE_POS):
                    leader_boards()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def get_player_name():
    global player_name
    player_name = ""
    input_active = True
    while input_active:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        name_text = get_font(20).render("Enter your name: " + player_name, True, "White")
        name_rect = name_text.get_rect(center=(400, 300))
        screen.blit(name_text, name_rect)
        pygame.display.update()
    
    play()

def save_score(name, score):
    with open("files.txt", "a") as file:
        file.write(f"{name}:{score}\n")

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = 370
playerY = 500
playerX_Change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 2
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load("art.png"))
    enemyX.append(random.randint(0, 735))  
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(30)

# Bullet
BulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.3
Bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))
    
def game_over_text():
    over_text = over_font.render("Game Over", True , (255, 255, 255))
    screen.blit(over_text, (200, 250))
    
def player(x, y):
    screen.blit(playerImg, (x, y)) 

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))
    
def fire_bullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

main_menu()
