import pygame
import random
import math

from pygame import mixer

#Inicializar el pygame
pygame.init()

#GameWindow
screen = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#Background
background = pygame.image.load('back.jpg')

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Bullets
bullet = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = "ready"


#Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change= 0


#Enemy

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numOfEnemies = 6

#Score
score = 0
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10


#GameOver text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x,y):
    score= font.render("Score: " + str(score_value), True, (255,255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))



for i in range(numOfEnemies):




    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.1)
    enemyY_change.append(40)



def enemy(x,y, i):
    screen.blit(enemyImg[i], (x, y))

def player(x,y):
    screen.blit(playerImg, (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = (math.sqrt(math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)) )
    if distance < 27:
        return True
    else:
        return False


#Game loop, para poder cerrar la ventana
running = True
while running:
    # Background color RGB red green blue
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -0.2
            if event.key == pygame.K_d:
                playerX_change = +0.2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

#Player move collision
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

#Enemy movement

    for i in range(numOfEnemies):

        # Game Over
        if enemyY[i] > 200:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            game_over_text()
            break


        enemyX[i] += enemyX_change[i]


        if enemyX[i] <= 0:
            enemyX_change[i] = 0.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -0.1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state= "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change




    player(playerX,playerY)
    show_score(textX, testY)
    pygame.display.update()