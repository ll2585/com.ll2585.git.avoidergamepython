import pygame, sys, random, pygbutton, math
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 400 # size of window's width in pixels
WINDOWHEIGHT = 300 # size of windows' height in pixels


#             R    G    B
GRAY      = (201, 204, 204)
DARKRED   = (150,  0 ,  0 )
BLACK     = ( 0,   0 ,  0 )
WHITE     = (255, 255, 255)

BGCOLOR = GRAY # background color on the screen
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = DARKRED

ENEMY_IMG = pygame.image.load('enemy.png')
STARTY = -15


AVATAR_IMG = pygame.image.load('avatar.png')

class Avatar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = AVATAR_IMG
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
    def getLocation(self):
        return pygame.mouse.get_pos()
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._image = ENEMY_IMG
        self.rect = self._image.get_rect()
        self._x = x
        self._y = y
        self._lastx = self._x
        self._lasty = self._y
        
    def getLocation(self):
        return self._x, self._y
    
    def moveDown(self):
        self._lasty = self._y
        self._y += 3
        self.rect.move_ip(self._lastx - self.rect.centerx, self._lasty - self.rect.centery)

class Score():
    def __init__(self):
        self.reset()
        
    def reset(self):
        self._value = 0;
    
    def addToValue(self, amt):
        self._value += amt
        
    def __str__(self):
        return str(self._value)
    
class Clock():
    def __init__(self):
        self.reset()
        
    def reset(self):
        self._value = 0;
    
    def addToValue(self, amt):
        self._value += amt
    
    def getImage(self):
        curImage = str(math.floor(self._value/1000)%12)
        clock = pygame.image.load('clock/stopwatch%s.png' %curImage)
        return clock
        
    def getSeconds(self):
        return math.floor(self._value/1000)
    
    def __str__(self):
        return str(self._value)
    
def hit(self, group):
    return pygame.sprite.spritecollideany(self, group)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def showMainScreen():
    showTextScreen('Avoider Game')
    button = pygbutton.PygButton((150, 180, 70, 30), 'Start')
    button.draw(DISPLAYSURF)
    while checkForButtonClick(button) == None:
        pygame.display.update()
        FPSCLOCK.tick()
        
def showRestartScreen(scoreClass, clock):
    showTextScreen('Game Over')
    button = pygbutton.PygButton((150, 180, 70, 30), 'Restart')
    button.draw(DISPLAYSURF)
    drawStatus(scoreClass)
    drawTime(clock)
    while checkForButtonClick(button) == None:
        pygame.display.update()
        FPSCLOCK.tick()
        
def showTextScreen(text):
    # This function displays large text in the
    # center of the screen until a key is pressed.
    # Draw the text drop shadow
    
    DISPLAYSURF.fill(BLACK)
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # Draw the text
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    

def checkForButtonClick(button):
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    checkForQuit()

    for event in pygame.event.get():
        if 'click' in button.handleEvent(event):
            return event
    return None

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def terminate():
    pygame.quit()
    sys.exit()

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def drawStatus(score):
    # draw the score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
'''
    # draw the level text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)
   ''' 
    
def drawTime(clock):
    # draw the score text
    clockSurf = BASICFONT.render('Seconds Lasted: %s' % clock.getSeconds(), True, TEXTCOLOR)
    clockRect = clockSurf.get_rect()
    clockRect.topleft = (WINDOWWIDTH - 200, 250)
    DISPLAYSURF.blit(clockSurf, clockRect)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 30)
    
    pygame.display.set_caption('Avoider Game')
    showMainScreen()

    while True: # game loop
        scoreClass = Score()
        clock = Clock()
        runGame(scoreClass, clock)
        showRestartScreen(scoreClass, clock)

def runGame(scoreClass, clock):
    
    avatar = Avatar()
    enemyGroup = pygame.sprite.Group()
    
    
    while True: # game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # drawing everything on the screen
        DISPLAYSURF.fill(BGCOLOR)
        if random.random() < 0.1:
            randomX = random.randrange(0, WINDOWWIDTH)
            enemy = Enemy(randomX, STARTY)
            enemyGroup.add(enemy)
            scoreClass.addToValue(10)
        for e in enemyGroup:
            e.moveDown()
            DISPLAYSURF.blit(e._image, e.getLocation())
        avatar.rect.move_ip(pygame.mouse.get_pos()[0]- avatar.rect.centerx, pygame.mouse.get_pos()[1]- avatar.rect.centery)
        DISPLAYSURF.blit(avatar.image, avatar.getLocation())
        drawStatus(scoreClass)
        clock.addToValue(25)
        DISPLAYSURF.blit(clock.getImage(), (WINDOWWIDTH - 80,  WINDOWHEIGHT- 50))
        if hit(avatar, enemyGroup):
            return # can't fit a new piece on the board, so game over
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
    
    
if __name__ == '__main__':
    main()