from math import pi, sqrt, cos, sin
import pygame
from data import *
from utils import *


def getOffsets(num):
    return (0, -num), (num, 0), (0, num), (-num, 0)


def computePoint(points, offset, angle):
    points = (
        (x * cos(angle) - y * sin(angle), x * sin(angle) + y * cos(angle))
        for x, y in points
    )
    return tuple((x + offset[0], y + offset[1]) for x, y in points)


class Console:
    if not pygame.font.get_init():
        pygame.font.init()
    font = pygame.font.Font(None, 40)
    smallFont = pygame.font.Font(None, 30)
    bigFont = pygame.font.Font(None, 50)
    massMax = 1024
    massMin = 1

    def __init__(self):
        self.bgRect = pygame.rect.Rect(0, 0, consoleWidth, displayHeight)
        self.selectedIndex = 0  #'mass' ,'angle' ,'particle', 'mouse'

        self.locks = (
            [False, False, False, False]
            if not tryVersion
            else [False, True, True, True]
        )
        self.mass = 255
        self.massSqrt = 15
        self.clickRect1 = pygame.rect.Rect(0, 0, consoleWidth, 112)
        self.massText = self.font.render("mass", True, "white")
        self.massLockText = self.font.render("mass", True, bgDark)
        self.x1 = 50 - self.massText.get_width() / 2
        self.boundaryRect1 = pygame.rect.Rect(0, 112, consoleWidth, 8)

        self.angle = 0
        self.clickRect2 = pygame.rect.Rect(0, 120, consoleWidth, 112)
        self.points = (-5, -10), (-5, 3), (-8, 3), (0, 10), (8, 3), (5, 3), (5, -10)
        self.offsets = getOffsets(20)
        self.angleText = self.font.render("angle", True, "white")
        self.angleTextLock = self.font.render("angle", True, bgDark)
        self.x2 = 50 - self.angleText.get_width() / 2
        self.boundaryRect2 = pygame.rect.Rect(0, 232, consoleWidth, 8)

        self.particleIndex = 0
        self.clickRect3 = pygame.rect.Rect(0, 240, consoleWidth, 112)
        self.particleText = self.smallFont.render("particle", True, "white")
        self.particleTextLock = self.smallFont.render("particle", True, bgDark)
        self.anyTextWhite = self.bigFont.render("Any", True, "white")
        self.anyTextGrey = self.bigFont.render("Any", True, grey)
        self.anyTextLock = self.bigFont.render("Any", True, bgDark)
        self.xAny = 50 - self.anyTextWhite.get_width() / 2
        self.yAny = 280 - self.anyTextWhite.get_height() / 2
        self.x3 = 50 - self.particleText.get_width() / 2
        self.boundaryRect3 = pygame.rect.Rect(0, 352, consoleWidth, 8)

        # gravity, create, draw  # distroy, erase
        self.modeIndex = 0
        self.clickRect4 = pygame.rect.Rect(0, 360, consoleWidth, 112)
        self.modeText = self.font.render("mode", True, "white")
        self.modeTextLock = self.font.render("mode", True, bgDark)
        self.mousePoints = tuple(
            (x, y + 360)
            for x, y in
            # ((45, 30), (45, 60), (53, 56), (59, 68), (63, 66), (57, 54), (65, 50))
            ((45, 35), (45, 65), (53, 61), (59, 73), (63, 71), (57, 59), (65, 55))
        )
        self.x4 = 50 - self.modeText.get_width() / 2
        self.boundaryRect4 = pygame.rect.Rect(0, 472, consoleWidth, 8)

    def click(self, pos):
        if self.clickRect1.collidepoint(pos[0], pos[1]):
            if not self.locks[0]:
                self.selectedIndex = 0
        elif self.clickRect2.collidepoint(pos[0], pos[1]):
            if not self.locks[1]:
                self.selectedIndex = 1
        elif self.clickRect3.collidepoint(pos[0], pos[1]):
            if not self.locks[2]:
                self.selectedIndex = 2
        elif self.clickRect4.collidepoint(pos[0], pos[1]):
            if not self.locks[3]:
                self.selectedIndex = 3

    def rightClick(self, pos):
        if self.clickRect1.collidepoint(pos[0], pos[1]):
            if not self.locks[0]:
                self.mass = 255
            self.massSqrt = 15
        elif self.clickRect2.collidepoint(pos[0], pos[1]):
            if not self.locks[1]:
                self.angle = 0
        elif self.clickRect3.collidepoint(pos[0], pos[1]):
            if not self.locks[2]:
                self.particleIndex = 0
        elif self.clickRect4.collidepoint(pos[0], pos[1]):
            if not self.locks[3]:
                self.modeIndex = 0

    def change(self, num):
        if self.selectedIndex == 0:
            self.mass = max(min(self.mass * 1.1**num, self.massMax), self.massMin)
            self.massSqrt = sqrt(self.mass)
        elif self.selectedIndex == 1:
            self.angle = (self.angle + num / 15) % (2 * pi)
        elif self.selectedIndex == 2:
            self.particleIndex = (self.particleIndex + num) % 8
        else:
            self.modeIndex = (self.modeIndex + num) % 3

    def control(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click(event.pos)
            elif event.button == 3:
                self.rightClick(event.pos)
        elif event.type == pygame.MOUSEWHEEL:
            self.change(event.y)

    def homing(self):
        if self.selectedIndex == 0:
            self.mass = 255
            self.massSqrt = 15
        elif self.selectedIndex == 1:
            self.angle = 0
        elif self.selectedIndex == 2:
            self.particleIndex = 0
        else:
            self.modeIndex = 0

    def controlKeyDown(self, key):
        if key == pygame.K_UP:
            self.selectedIndex = (self.selectedIndex - 1) % 4
            while self.locks[self.selectedIndex]:
                self.selectedIndex = (self.selectedIndex - 1) % 4
        elif key == pygame.K_DOWN:
            self.selectedIndex = (self.selectedIndex + 1) % 4
            while self.locks[self.selectedIndex]:
                self.selectedIndex = (self.selectedIndex + 1) % 4
        elif key == pygame.K_LEFT:
            self.change(-1)
        elif key == pygame.K_RIGHT:
            self.change(1)
        elif key == pygame.K_SPACE:
            self.homing()

    def draw1(self, canvas: pygame.Surface):
        color = bgDark if self.locks[0] else white if self.selectedIndex == 0 else grey
        pygame.draw.circle(canvas, color, (50, 40), self.massSqrt)

        if self.locks[0]:
            canvas.blit(self.massLockText, (self.x1, 80))
        else:
            canvas.blit(self.massText, (self.x1, 80))
        pygame.draw.rect(canvas, bgDark, self.boundaryRect1)

    def draw2(self, canvas: pygame.Surface):
        color = bgDark if self.locks[1] else white if self.selectedIndex == 1 else grey
        for i, offset in enumerate((self.offsets)):
            pygame.draw.polygon(
                canvas,
                color,
                computePoint(
                    self.points,
                    (50 + offset[0], 160 + offset[1]),
                    self.angle + i * pi / 2,
                ),
            )

        if self.locks[1]:
            canvas.blit(self.angleTextLock, (self.x2, 200))
        else:
            canvas.blit(self.angleText, (self.x2, 200))
        pygame.draw.rect(canvas, bgDark, self.boundaryRect2)

    def draw3(self, canvas):
        if self.particleIndex != 0:
            color = (
                bgDark
                if self.locks[2]
                else colors[self.particleIndex]
                if self.selectedIndex == 2
                else grey
            )
            radius = 16 + int(self.particleIndex < 4) * 4
            pygame.draw.circle(canvas, color, (50, 280), radius)
        else:
            img = (
                self.anyTextLock
                if self.locks[2]
                else self.anyTextWhite
                if self.selectedIndex == 2
                else self.anyTextGrey
            )
            canvas.blit(img, (self.xAny, self.yAny))

        if self.locks[2]:
            canvas.blit(self.particleTextLock, (self.x3, 320))
        else:
            canvas.blit(self.particleText, (self.x3, 320))
        pygame.draw.rect(canvas, bgDark, self.boundaryRect3)

    def drawCircles(self, canvas, color):
        if self.massSqrt > 20:
            pygame.draw.circle(canvas, color, (45, 395), 24)
            pygame.draw.circle(canvas, bg, (45, 395), 20)
        if self.massSqrt > 10:
            pygame.draw.circle(canvas, color, (45, 395), 16)
            pygame.draw.circle(canvas, bg, (45, 395), 12)
        pygame.draw.circle(canvas, color, (45, 395), 8)
        pygame.draw.circle(canvas, bg, (45, 395), 4)

    def drawParticles(self, canvas: pygame.Surface, color):
        radius1 = int(self.particleIndex < 4) + 4
        radius2 = int(0 < self.particleIndex < 4) + 4
        check = self.massSqrt / 6.4
        # normal
        pygame.draw.circle(canvas, color, (35, 385), radius1)
        # right 1
        if check > 1:
            pygame.draw.circle(canvas, color, (57, 387), radius2)
        # left 1
        if check > 2:
            pygame.draw.circle(canvas, color, (28, 400), radius2)
        # right 2
        if check > 3:
            pygame.draw.circle(canvas, color, (65, 400), radius1)
        # left 2
        if check > 4:
            pygame.draw.circle(canvas, color, (32, 415), radius1)

    def draw4(self, canvas: pygame.Surface):
        color = bgDark if self.locks[3] else white if self.selectedIndex == 3 else grey
        if self.modeIndex == 0:
            self.drawCircles(canvas, color)
        elif self.modeIndex == 1:
            color2 = colors[self.particleIndex] if color == white else color
            self.drawParticles(canvas, color2)
        else:
            pygame.draw.line(canvas, color, (45, 395), (15, 385), 5)
        pygame.draw.polygon(canvas, color, self.mousePoints)

        if self.locks[3]:
            canvas.blit(self.modeTextLock, (self.x4, 440))
        else:
            canvas.blit(self.modeText, (self.x4, 440))
        pygame.draw.rect(canvas, bgDark, self.boundaryRect4)

    def draw(self, canvas):
        pygame.draw.rect(canvas, bg, self.bgRect)
        self.draw1(canvas)
        self.draw2(canvas)
        self.draw3(canvas)
        self.draw4(canvas)
