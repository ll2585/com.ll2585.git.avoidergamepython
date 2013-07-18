import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400,300))
pygame.display.set_caption('AvoiderGame')

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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._image = ENEMY_IMG
        self.rect = self._image.get_rect()
        self._x = 100
        self._y = -15
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
    
avatar = Avatar()
enemy = Enemy()
 
while True:
    DISPLAYSURF.fill(BGCOLOR)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.blit(enemy._image, enemy.getLocation())
    avatar.rect.move_ip(pygame.mouse.get_pos()[0]- avatar.rect.centerx, pygame.mouse.get_pos()[1]- avatar.rect.centery)
    DISPLAYSURF.blit(avatar.image, avatar.getLocation())
    gems = pygame.sprite.Group()
    gems.add(enemy)
    if hit(avatar, gems):
        break
    enemy.moveDown()
    pygame.display.update()
    fpsClock.tick(FPS)