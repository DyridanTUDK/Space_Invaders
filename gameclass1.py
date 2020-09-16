import pygame
#imported random
import random
#
import math

from pygame import mixer
# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#background image
background = pygame.image.load('background.png')

#Title and Icon
pygame.display.set_caption("Space Invaders")
Icon = pygame.image.load("ufo.png")
pygame.display.set_icon(Icon)

#player
playerIMG = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

#bullets
#ready = you cant see
#fire = you can see
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = -18
bullet_state = "ready"


#draws the player
def player(x, y):
    screen.blit(playerIMG, (x, y))

#draws the enemy
def enemy(x, y):
    screen.blit(enemyIMG[i], (x, y))
#draw bullet:
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

#score
def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

# game over
def game_over_text():
    over_text = over_font.render('GAME OVER',True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Collision function
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:


    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Movement using keystrokes
        if event.type == pygame.KEYDOWN:
            print("key pressed")
            if event.key == pygame.K_LEFT:
                print("left key pressed")
                playerX_change = -6
            if event.key ==  pygame.K_RIGHT:
                print("right key pressed")
                playerX_change = +6
            if event.key == pygame.K_SPACE:
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or  event.key == pygame.K_LEFT:
                print("key is released")
                playerX_change = 0
    #add movement to the player
    playerX += playerX_change


    #code for checking border
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        # gameover
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        # Movement of the enemy
        enemyX[i] += enemyX_change[i]
        # border check for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound('explosion.wav')
            explosionSound.play()
            bulletY = 480
            bullet_state = 'ready'
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            score_value += 1

        enemy(enemyX[i], enemyY[i])


    # bullet movement
    if bulletY <= 0:
        bulletY =480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change


    # creating player
    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
