class Player:

    #Defines used variables
    x = 0
    y = 0
    state = 1
    time = 8

    #Runs when Player initializes
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    #Makes sure the player can't leave the screen
    def boundaries(self, x):
        if x <= 4:
            self.x = 4
        if x >= 632:
            self.x = 632

    #Draws the player while standing
    def drawStanding(self, screen, playerSprite, direction):
        screen.blit(playerSprite[0 + direction*4], (self.x, self.y))

    #Draws the player in with a moving animation
    def drawMoving(self, screen, playerSprite, direction):

        #Delay timer
        if self.time != 0:
            self.time -= 1

        #Change animation to next frame
        if self.time == 0 and self.state != 3:
            self.state += 1
            self.time = 8

        #Restart animation
        if self.time == 0 and self.state == 3:
            self.state = 1
            self.time = 8

        screen.blit(playerSprite[self.state + direction*4], (self.x, self.y))