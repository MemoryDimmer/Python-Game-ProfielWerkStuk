import random
class collectible:
    
    #Defines used variables
    x = 0
    y = 0
    waitTime = 0
    state = "ready"
    
    #Runs when the collectible is initialized
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #draws the collectible
    def draw(self, screen, playerImage):
        screen.blit(playerImage, (self.x, self.y))
    
    #moves the collectible and outputs a penalty score if it hits the bottom
    def move(self, waitTimeMin, waitTimeMax, cPixels):
        score = 0

        #Applies a random time before the collectible spawns
        if self.x == -80 and self.y == -80 and self.state == "ready":
            self.waitTime = random.randint(int(waitTimeMin*60), int((waitTimeMax+1)*60))
            self.state = "preparing"

        #Countdown timer
        if self.waitTime != 0:
            self.waitTime -= 1

        #Puts collectible at the top of the screen
        if self.waitTime == 0 and self.state == "preparing":
            self.x = random.randint(4, 696 - cPixels)
            self.y = 4
            self.state = "moving"

        #Collectible movement
        if self.y != -80:
            self.y += 2

        #Triggered when collectible hits the bottom
        if self.y == 496 - cPixels:
            self.x = -80
            self.y = -80
            self.state = "ready"
            score = 1
            return score
    
    #Puts boxes at start coordinates when game ends
    def endMove(self):
        self.x = -80
        self.y = -80