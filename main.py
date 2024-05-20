import sys
import pygame
from console import Console
from obstacleLine import ObstacleManager
from particle import ParticleManager
from data import *
from utils import *

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(displaySize)
        if tryVersion:
            pygame.display.set_caption("ParticleSimulationTrying")
            pygame.display.set_icon(pygame.image.load("png/iconTry.png"))
        else:
            pygame.display.set_caption("ParticleSimulation")
            pygame.display.set_icon(pygame.image.load("png/icon.png"))
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(200, 100)

        self.console = Console()
        self.obstacles = ObstacleManager()
        self.particles = ParticleManager(150)

        self.buttonDownPos = 0, 0

        self.deltaTime = 1000 / FPS
        pygame.display.flip() 

    def gameQuit(self):
        if pygame.font.get_init():
            pygame.font.quit()
        pygame.quit()
        sys.exit()

    def mousePressed(self) -> None:
        if self.buttonDownPos[0] < consoleWidth:
            return
        buttons = pygame.mouse.get_pressed()
        self.obstacles.cancelDraw(buttons[2])
        result = (buttons[0] - buttons[2])
        if not result:
            return
        mousePos = pygame.mouse.get_pos()
        if self.console.modeIndex == 0:
            self.particles.handleGravity(result, mousePos)
        elif self.console.modeIndex == 1:
            self.particles.handleParticle(result, mousePos, self.console.particleIndex,
                                          500 / self.console.massSqrt)
        elif self.console.modeIndex == 2 and result == -1:
            self.obstacles.dropObstacle(mousePos, self.console.massSqrt)

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameQuit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameQuit()
                else:
                    self.obstacles.controlKeyDown(event.key, not self.particles.group)
                    self.console.controlKeyDown(event.key)
                    # c,d,e,f,q,w,z,x,0~7
                    self.particles.controlKeyDown(event, self.console.particleIndex)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.buttonDownPos = event.pos
                # button down,  wheel
                self.console.control(event)
                # button down, button up
                if self.console.modeIndex == 2:
                    self.obstacles.control(event)
        keys = pygame.key.get_pressed()
        # a,b
        self.particles.keyPressed(keys)
        self.mousePressed()

    def update(self):
        self.particles.update(self.deltaTime, self.console.mass, self.console.angle,
                              self.obstacles.collide)
        self.obstacles.update()

    def draw(self):
        self.display.fill('black')
        self.obstacles.draw(self.display, self.particles.stop)
        self.particles.draw(self.display)
        self.console.draw(self.display)

        pygame.display.flip()

    def run(self):
        while True:
            self.control()
            self.update()
            self.draw()
            self.deltaTime = self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
