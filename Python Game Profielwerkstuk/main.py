#import libraries
import pygame
from pygame import mixer

import random
from Player import Player
from collectible import collectible

pygame.mixer.pre_init(44100, -16, 1, 512)

#initialize pygame and the game window
pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("Collect coins")

#Loads music and sounds
mixer.music.load("Sounds/background-music.ogg")
collectSound = mixer.Sound("Sounds/shot-sound.ogg")
#Plays the music on loop
mixer.music.play(-1)

#initialize images
background = pygame.image.load("Images/background.png")
collectibleImage = pygame.image.load("Images/collectible.png")

pImage1R = pygame.image.load("Images/Player/StandR.png")
pImage2R = pygame.image.load("Images/Player/run1R.png")
pImage3R = pygame.image.load("Images/Player/run2R.png")
pImage4R = pygame.image.load("Images/Player/run3R.png")

pImage1L = pygame.image.load("Images/Player/StandL.png")
pImage2L = pygame.image.load("Images/Player/run1L.png")
pImage3L = pygame.image.load("Images/Player/run2L.png")
pImage4L = pygame.image.load("Images/Player/run3L.png")

#Creates an array for player images
playerSprite = [pImage1L, pImage2L, pImage3L, pImage4L, pImage1R, pImage2R, pImage3R, pImage4R] 

#initialize game objects
p1 = Player(318,430)
c1 = collectible(-80, -80)
c2 = collectible(-80, -80)
c3 = collectible(-80, -80)
c4 = collectible(-80, -80)
c5 = collectible(-80, -80)

#Variables used for score
playerScore = 0
endScore = 20
cbCount = 0
penalty1 = 0
penalty2 = 0
penalty3 = 0
penalty4 = 0
penalty5 = 0

#Variables used in code
playerDirection = 0
moving = 0
cPixels = 40
waitTimeMin = 0.5
waitTimeMax = 5

#defines clock to manipulate game speed
clock = pygame.time.Clock()

countdownSec = 6
countdownTick = countdownSec * 60

fontStart = pygame.font.Font("freesansbold.ttf", 30)
fontCountdown = pygame.font.Font("freesansbold.ttf", 40)
fontColor = (175,255,210)
def start(x, y):   
    textStart = fontStart.render("Verzamel 20 punten om te winnen!", True, fontColor)
    textCountdown = fontCountdown.render(str(countdownTick // 60), True, fontColor)
    
    startRect = textStart.get_rect(center=(x, y))
    countdownRect = textCountdown.get_rect(center=(x, y + 40))
    screen.blit(textStart, startRect)
    screen.blit(textCountdown, countdownRect)

#Used to display score
fontScore = pygame.font.Font("freesansbold.ttf", 40)
def displayScore(x, y):
    if playerScore == 1:
        score = fontScore.render(str(int(playerScore)) + " punt", True, fontColor)
    elif playerScore == 0.5 or playerScore == 1.5:
        score = fontScore.render(str(playerScore) + " punt", True, fontColor)
    elif playerScore % 1 == 0.5:
        score = fontScore.render(str(playerScore) + " punten", True, fontColor)
    else:
        score = fontScore.render(str(int(playerScore)) + " punten", True, fontColor)
    
    scoreRect = score.get_rect(center=(x, y))
    screen.blit(score, scoreRect)

fontCb = pygame.font.Font("freesansbold.ttf", 24)
def displayCb(x, y):
    cbText = fontCb.render("Er zijn " + str(cbCount) + " muntjes geweest.", True, fontColor)
    cbRect = cbText.get_rect(center=(x, y))
    screen.blit(cbText, cbRect)
    
    
#Collectible code to execute after a collision
def onCollision(cx):
    cx.x = -80
    cx.y = -80
    cx.state = "ready"
    collectSound.play()

#game loop
running = True
while running:
    #Close game after pressing X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #draw background
    screen.blit(background, (0,0))
    
    #limits the game to 60FPS
    clock.tick(60)
    
    #checks for any keyboard input
    keys = pygame.key.get_pressed()
    
    if countdownTick != 0:
        countdownTick -= 1
        start(330, 230)
        
    #moves the player on input
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        moving = 0
    elif keys[pygame.K_LEFT]:
        p1.x -= 6
        playerDirection = 0
        moving = 1
    elif keys[pygame.K_RIGHT]:
        p1.x += 6
        playerDirection = 1
        moving = 1
    elif not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        moving = 0

    #Creates the left and right boundaries for the player
    p1.boundaries(p1.x)

    #Draws the player
    if moving == 0:
        p1.drawStanding(screen, playerSprite, playerDirection)
    if moving == 1:
        p1.drawMoving(screen, playerSprite, playerDirection)
        
    
    #collectible movement
    if playerScore < endScore and countdownTick == 0:
        penalty1 = c1.move(waitTimeMin, waitTimeMax, cPixels)
        penalty2 = c2.move(waitTimeMin, waitTimeMax, cPixels)
        penalty3 = c3.move(waitTimeMin, waitTimeMax, cPixels)
        penalty4 = c4.move(waitTimeMin, waitTimeMax, cPixels)
        penalty5 = c5.move(waitTimeMin, waitTimeMax, cPixels)
    elif playerScore >= endScore:
        c1.endMove
        c2.endMove
        c3.endMove
        c4.endMove
        c5.endMove

    #Draws the collectibles
    if playerScore < endScore and countdownTick == 0:
        c1.draw(screen, collectibleImage)
        c2.draw(screen, collectibleImage)
        c3.draw(screen, collectibleImage)
        c4.draw(screen, collectibleImage)
        c5.draw(screen, collectibleImage)
    
    #creates collision boxes
    p1Rect = pygame.Rect(p1.x, p1.y, 64, 64)
    c1Rect = pygame.Rect(c1.x, c1.y, cPixels, cPixels)
    c2Rect = pygame.Rect(c2.x, c2.y, cPixels, cPixels)
    c3Rect = pygame.Rect(c3.x, c3.y, cPixels, cPixels)
    c4Rect = pygame.Rect(c4.x, c4.y, cPixels, cPixels)
    c5Rect = pygame.Rect(c5.x, c5.y, cPixels, cPixels)
    
    #Collision detection for collectible
    if playerScore < endScore:
        if c1Rect.colliderect(p1Rect):
            onCollision(c1)
            playerScore += 1.0
            cbCount += 1
        if c2Rect.colliderect(p1Rect):
            onCollision(c2)
            playerScore += 1.0
            cbCount += 1
        if c3Rect.colliderect(p1Rect):
            onCollision(c3)
            playerScore += 1.0
            cbCount += 1
        if c4Rect.colliderect(p1Rect):
            onCollision(c4)
            playerScore += 1.0
            cbCount += 1
        if c5Rect.colliderect(p1Rect):
            onCollision(c5)
            playerScore += 1.0
            cbCount += 1
            

    #Score penalty when collectible hits bottom
    if penalty1 == 1 and playerScore != 0:
        playerScore -= 0.5
    if penalty2 == 1 and playerScore != 0:
        playerScore -= 0.5
    if penalty3 == 1 and playerScore != 0:
        playerScore -= 0.5
    if penalty4 == 1 and playerScore != 0:
        playerScore -= 0.5
    if penalty5 == 1 and playerScore != 0:
        playerScore -= 0.5
        
    #Keeps track of the amount of boxes that hit the bottom
    if penalty1 == 1:
        cbCount += 1
    if penalty2 == 1:
        cbCount += 1
    if penalty3 == 1:
        cbCount += 1
    if penalty4 == 1:
        cbCount += 1
    if penalty5 == 1:
        cbCount += 1
    
    #Displays the score
    displayScore(350, 30)
    if playerScore >= endScore:
        displayCb(350, 60)

    #update display
    pygame.display.update()