import pygame, sys, random, pygbutton, math
from pygame.locals import *
import PixelPerfect

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
        self._image = AVATAR_IMG.convert_alpha()
        self._x = pygame.mouse.get_pos()[0]
        self._y = pygame.mouse.get_pos()[1]
        self._lastx = self._x
        self._lasty = self._y
        self.mask = pygame.mask.from_surface(self._image)
        self.rect = self._image.get_rect(topleft=(self._x,self._y))
        
    def getLocation(self):
        return pygame.mouse.get_pos()
    
    def moveToMouse(self):
        self._lasty = self._y
        self._lastx = self._x
        self._x, self._y = pygame.mouse.get_pos()
        self.rect.move_ip(self._x - self._lastx, self._y - self._lasty)
        
    def hitEnemy(self, enemy):
        #y first
        return self.simple_overlap(enemy.mask, [0,1]) or self.simple_overlap(enemy.mask, [1,0])
        
    def simple_overlap(self,Mask,offset):
        off = (self.rect.x+offset[0],self.rect.y+offset[1])
        return Mask.overlap_area(self.mask,off)
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self._image = ENEMY_IMG.convert_alpha()
        self._x = x
        self._y = y
        self._lastx = self._x
        self._lasty = self._y
        self._ySpeed = 3
        self.mask = pygame.mask.from_surface(self._image)
        self.rect = self._image.get_rect(topleft=(x,y))
        
    def getLocation(self):
        return self._x, self._y
    
    def moveDown(self):
        self._lasty = self._y
        self._lastx = self._x
        self._y += self._ySpeed
        self.rect.move_ip(self._x - self._lastx, self._y - self._lasty)

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

class Control:
    def __init__(self):
        self.setup()

    
    def setup(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT, GAMESTATE
        
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
    
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        BIGFONT = pygame.font.Font('freesansbold.ttf', 30)
    
        pygame.display.set_caption('Avoider Game')
    
    
        self.showMainScreen()
    

            
    
    def showMainScreen(self):
        self.showTextScreen('Avoider Game')
        button = pygbutton.PygButton((150, 180, 70, 30), 'Start')
        button.draw(DISPLAYSURF)
        while checkForButtonClick(button) == None:
            pygame.display.update()
            FPSCLOCK.tick()
    
    def newGame(self):
        self.state = "GAME"
        self.enemies = []
        self.avatar = Avatar()
        self.scoreClass = Score()
        self.clock = Clock()
        self.bg_mask,self.bg_image = self.make_bg_mask()
        self.runGame()
        self.showRestartScreen(self.scoreClass, self.clock)
            
    def runGame(self):
        while True:
            if self.state == "GAME":
                self.event_loop()
                self.update(DISPLAYSURF)
            elif self.state == "QUIT":
                break
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # drawing everything on the screen
        if random.random() < 0.1:
            randomX = random.randrange(0, WINDOWWIDTH)
            enemy = Enemy(randomX, STARTY)
            self.enemies.append(enemy)
            self.scoreClass.addToValue(10)
        for e in self.enemies:
            e.moveDown()
            pygame.draw.rect(DISPLAYSURF, BLACK, e.rect)
        self.avatar.moveToMouse()
        pygame.draw.rect(DISPLAYSURF, BLACK, self.avatar.rect)
    
        self.drawStatus(self.scoreClass)
        self.clock.addToValue(25)
    
        if self.hit(self.avatar):
            pygame.mouse.set_visible(True)
            
            avatarHasBeenHit = True
        if avatarHasBeenHit:
            self.state = "QUIT"
            
    def hit(self, avatar):
        yoffset = [0, 1]
        xoffset = [1, 0]
        yhit = simple_overlap(avatar,self.bg_mask,yoffset)
        xhit = simple_overlap(avatar,self.bg_mask,xoffset)
        return yhit or xhit
            
    def update(self, Surf):
        Surf.fill(BGCOLOR)
        self.bg_mask,self.bg_image = self.make_bg_mask()
        Surf.blit(self.bg_image,(0,0))
        for e in self.enemies:
            Surf.blit(e._image, e.getLocation())
        Surf.blit(self.avatar._image, self.avatar.getLocation())
        Surf.blit(self.clock.getImage(), (WINDOWWIDTH - 80,  WINDOWHEIGHT- 50))
            
    def showRestartScreen(self,scoreClass, clock):
        self.showTextScreen('Game Over')
        button = pygbutton.PygButton((150, 180, 70, 30), 'Restart')
        button.draw(DISPLAYSURF)
        self.drawStatus(scoreClass)
        self.drawTime(clock)
        while checkForButtonClick(button) == None:
            pygame.display.update()
            FPSCLOCK.tick()

    def drawStatus(self,score):
        # draw the score text
        scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 150, 20)
        DISPLAYSURF.blit(scoreSurf, scoreRect)
    
        
    def drawTime(self,clock):
        # draw the score text
        clockSurf = BASICFONT.render('Seconds Lasted: %s' % clock.getSeconds(), True, TEXTCOLOR)
        clockRect = clockSurf.get_rect()
        clockRect.topleft = (WINDOWWIDTH - 200, 250)
        DISPLAYSURF.blit(clockSurf, clockRect)
            
    
    def showTextScreen(self,text):
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

    def make_bg_mask(self):
        temp = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT)).convert_alpha()
        temp.fill((0,0,0,0))
        for e in self.enemies:
            temp.blit(e._image,e.rect)
        return pygame.mask.from_surface(temp),temp

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


        
def make_bg_mask(enemies):
    temp = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT)).convert_alpha()
    temp.fill((0,0,0,0))
    for e in enemies:
        temp.blit(e._image,e.rect)
    return pygame.mask.from_surface(temp),temp

def simple_overlap(obj, mask2,offset):
    off = (obj.rect.x+offset[0],obj.rect.y+offset[1])
    return mask2.overlap_area(obj.mask,off)

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

    
    
if __name__ == '__main__':
    RunIt = Control()
    RunIt.newGame()