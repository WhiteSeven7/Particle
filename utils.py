import pygame

def createLoack(size, color):
    canvas = pygame.Surface((size, 2 * size))
    canvas.set_alpha(128)
    center = size / 2, size
    r = size / 3
    pygame.draw.circle(canvas, color, center, r)
    pygame.draw.circle(canvas, 'black', center, r - 2)
    pygame.draw.rect(canvas, color, (0, size, size, size))
    canvas.set_colorkey('black')
    # drawLock(canvas, color, size / 2, size)
    return canvas

def drawLock(canvas, color, x, y):
    pygame.draw.circle(canvas, color, (x, y), 7)
    # pygame.draw.circle(canvas, bg, (x, y), 4)
    pygame.draw.rect(canvas, color, (x - 25, y, 50, 40))
