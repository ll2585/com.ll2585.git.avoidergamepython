import pygame
def pixelPerfectHit(surf1, surf2):# create mask from surface
    mask = pygame.mask.from_surface(surf1.surface)
    
    # translate the position of the missile,
    # since the top left coordinate of the mask is always (0, 0)
    rel_point = sub(surf2.position, surf1.position)
    try: 
        if mask.get_at(rel_point): 
            # point in mask
            return True
    except IndexError: 
        return False

def sub(u, v):
  return [ u[i]-v[i] for i in range(len(u)) ]