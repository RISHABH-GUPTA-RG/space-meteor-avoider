import pygame
import random
import math
import time
from pygame import mixer

# intiliazing the pygame
pygame.init()

# creating The screen and setting its size
#size = width, height = 800, 600
screen = pygame.display.set_mode()
background = pygame.image.load('Data\\5532919.jpg')
width,height=screen.get_size()

# isko ched Values
playerspeed = (width-height)/5000
enemyspeed = (width-height)/500
mixer.music.load('Data\\music_zapsplat_space_trivia.mp3')
mixer.music.play()
pygame.display.set_caption('Made By Rishabh Gupta')
icon = pygame.image.load('Data\\rocket.gif')
pygame.display.set_icon(icon)

def iscollide(playerx, playery, enemyx, enemyy):
    distance = math.sqrt(math.pow(enemyx-playerx, 2) +math.pow(enemyy-playery, 2))
    return distance

# player
playerimg = pygame.image.load('Data\\rocket.png')
playerx = width/2-64/2
playery = (4*height)/5-64/2
playerxchange = 0
playerxac=0

def player(x, y):
    screen.blit(playerimg, (x, y))

score = 0
font = pygame.font.Font('Data\\RobotInvadersItalic.ttf', 32)
font2= pygame.font.Font('Data\\Revamped.ttf', 16)
font3= pygame.font.Font('Data\\Scorchedearth.otf', 16)

def show_score():
    score_value = font.render("Score: " + str(int(score)), True, (255, 255, 255))
    screen.blit(font2.render("Made by Rishabh Gupta", True, (255,255,255)), (width-250,10))
    screen.blit(score_value, (10, 10))

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyychange = []
numberofenemies = int((width-height)/20)
for i in range(numberofenemies):
    enemyimg.append(pygame.image.load('Data\\asteroid.png'))
    enemyx.append(random.randint(0, width-64))
    enemyy.append(random.randint(-1000, -400))
    enemyychange.append(enemyspeed)

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# bullet
bulletimg = pygame.image.load('Data//bullet.png')
bulletstate = 'Ready'
bulletx = playerx
bullety = playery
bulletychange = 0

bulletsound="Play"
def bullet(x, y):
    global bulletstate
    bulletstate="Fire"
    bulletx = playerx
    screen.blit(bulletimg, (x, y))

# Doing everthing under while loop otherwise it will close imediately
running = True
while running:
    # rgb
    screen.fill((20, 20, 20))
    screen.blit(background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerxchange = -playerspeed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerxchange = playerspeed
            if event.key == pygame.K_SPACE:
                if bulletstate=="Ready":
                    bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerxchange = 0
                playerxac = 0

    # player acceleration on movement
    playerxac+=playerxchange
    # checking boundries of player so it dosent get lost
    playerx +=  playerxac*0.2
    if playerx < 0:
        playerx = 0
    if playerx > width-64:
        playerx = width-64

    for i in range(numberofenemies):
        # ENEMY movement
        enemy(enemyx[i], enemyy[i], i)

        enemyy[i] += enemyychange[i]
        if enemyy[i] > height:
            score += 0.1
            playerspeed += 0.0001
            enemyspeed += 0.0001
            enemyx[i] = random.randint(0, width-64)
            enemyy[i] = random.randint(-400, 0)

        collison = iscollide(playerx, playery, enemyx[i], enemyy[i])
        if collison <= 50:
            #mixer.music.pause()
            game = mixer.Sound('Data\\2G7CF5V-gamers-fail-game.mp3')
            game.play()
            enemyychange[i] = 0
            playerxchange = 0
            for i in range(numberofenemies):
                enemyychange[i] = 0
            time.sleep(3)
            running = False

        if bulletstate=="Fire":
            Bulletcollision= iscollide(bulletx,bullety,enemyx[i],enemyy[i])
            if Bulletcollision <=40:
                score+=1
                bullety=playery
                collisonsound =mixer.Sound('Data\explosion.wav')
                collisonsound.play()
                enemyx[i] = random.randint(0, width-64)
                enemyy[i] = random.randint(-400, 0)
                bulletstate="Ready"
                bulletsound="Play"

    if bulletstate=="Fire":
        if bulletsound=="Play":
            bulletfiresound =mixer.Sound("Data\\shoot.wav")
            bulletfiresound.play()
            bulletsound="Stop"
            bulletx=playerx
        bullet(bulletx, bullety)
        bullety-=2
        if bullety<0-64:
            bulletstate='Ready'
            bulletsound="Play"
            bullety=playery

    player(playerx, playery)
    show_score()
    pygame.display.update()