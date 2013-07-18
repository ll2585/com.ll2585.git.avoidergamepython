import pygame, sys, random
from pygame.locals import *

FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 400 # size of window's width in pixels
WINDOWHEIGHT = 300 # size of windows' height in pixels


#          R    G    B
GRAY   = (201, 204, 204)
BGCOLOR = GRAY # background color on the screen

ENEMY_IMG = pygame.image.load('enemy.png')
enemyLocationX = 100
enemyLocationY = -15

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
    
def hit(self, group):
    return pygame.sprite.spritecollideany(self, group)

def main():
    global FPSCLOCK, DISPLAYSURF
    
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    pygame.display.set_caption('AvoiderGame')

    avatar = Avatar()
    enemyGroup = pygame.sprite.Group()

    while True:
        DISPLAYSURF.fill(BGCOLOR)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if random.random() < 0.1:
            randomX = random.randrange(0, 400)
            enemy = Enemy(randomX, -15)
            enemyGroup.add(enemy)
        print (enemyGroup)
        for e in enemyGroup:
            e.moveDown()
            DISPLAYSURF.blit(e._image, e.getLocation())
        avatar.rect.move_ip(pygame.mouse.get_pos()[0]- avatar.rect.centerx, pygame.mouse.get_pos()[1]- avatar.rect.centery)
        DISPLAYSURF.blit(avatar.image, avatar.getLocation())
        if hit(avatar, enemyGroup):
            break
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
if __name__ == '__main__':
    main()