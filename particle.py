from random import uniform, randint
from math import pi, sqrt, sin, cos, inf
import pygame
from data import *

class Particle:
    minR = 0.8
    maxSpeed = 6
    minSpeed = 0.05

    @classmethod
    def create(cls, mass: int=0, pos: PointF | None=None,
                velocity: PointF | None=None):
        if mass == 0:
            mass = randint(1, 7)
        if velocity is None:
            speed = uniform(0, 3)
            angle = uniform(0, 2 * pi)
            velocity = speed * cos(angle), speed * sin(angle)
        if pos is None:
            pos = uniform(consoleWidth, displayWidth), uniform(0, displayHeight)
        return cls(mass, pos[0], pos[1], velocity[0], velocity[1])

    def __init__(self, mass, x, y,vx, vy):
        self.mass = mass
        self.color = colors[8 - mass]
        self.fadeColor = fadeColors[8 - mass]
        self.radius = int(mass > 4) + 4
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def _safeSpeed(self):
        speed = sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > self.maxSpeed:
            self.vx = self.vx * self.maxSpeed / speed
            self.vy = self.vy * self.maxSpeed / speed

    def maximizeSpeed(self):
        speed = sqrt(self.vx ** 2 + self.vy ** 2)
        if speed == 0:
            angle = uniform(0, 2 * pi)
            self.vx = self.maxSpeed * cos(angle)
            self.vy = self.maxSpeed * sin(angle)
        else:
            self.vx = self.vx * self.maxSpeed / speed
            self.vy = self.vy * self.maxSpeed / speed

    def changeMassById(self, massId: int):
        mass = randint(1, 7) if massId == 0 else 8 - massId
        self.mass = mass
        self.color = colors[8 - mass]
        self.fadeColor = fadeColors[8 - mass]
        self.radius = int(mass > 4) + 4

    def getA(self, pos, mass, angle):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        r = max(sqrt(dx ** 2 + dy ** 2), self.minR)
        ax0 = mass * self.mass * dx / r ** 3
        ay0 = mass * self.mass * dy / r ** 3
        ax = ax0 * cos(angle) - ay0 * sin(angle)
        ay = ax0 * sin(angle) + ay0 * cos(angle)
        return ax, ay

    def changeSpeedByA(self, deltaTime: float, ax:float, ay:float, setSpeed:float):
        self.vx += ax * FPS * deltaTime / 1000
        self.vy += ay * FPS * deltaTime / 1000
        if setSpeed == inf:
            self.maximizeSpeed()
        elif self.vx == 0 and self.vy == 0 and setSpeed > 1:
            angle = uniform(0, 2 * pi)
            self.vx = self.minSpeed * cos(angle)
            self.vy = self.minSpeed * sin(angle)
        elif self.vx ** 2 + self.vy ** 2 < self.minSpeed ** 2 and setSpeed < 1:
            self.vx = 0
            self.vy = 0
        else:
            self.vx *= setSpeed
            self.vy *= setSpeed
            self._safeSpeed()
        
    def bumpWall(self):
        if self.x < consoleWidth:
            self.x = 2 * consoleWidth -self.x
            self.vx = -self.vx
        elif self.x > displayWidth:
            self.x = 2 * displayWidth - self.x
            self.vx = -self.vx

        if self.y < 0:
            self.y = -self.y
            self.vy = -self.vy
        elif self.y > displayHeight:
            self.y = 2 * displayHeight - self.y
            self.vy = -self.vy

    def safeMove(self, deltaTime: float, collideFunc):
        # self.x += self.vx * FPS * deltaTime / 1000
        # self.y += self.vy * FPS * deltaTime / 1000
        
        self.x, self.y, self.vx, self.vy = collideFunc(
            (self.x, self.y),
            (self.x + self.vx * FPS * deltaTime / 1000, 
             self.y + self.vy * FPS * deltaTime / 1000),
            (self.vx, self.vy))
        self.bumpWall()
    
    def update(self, isStop: bool, massId: int, pos: PointI, mass: float,
               angle: float, setSpeed: float, deltaTime: float, collideFunc):
        if massId != -1:
            self.changeMassById(massId)
        ax, ay = self.getA(pos, mass, angle) if mass else (0, 0)
        self.changeSpeedByA(deltaTime ,ax, ay, setSpeed)
        if not isStop:
            self.safeMove(deltaTime, collideFunc)

    def draw(self, canvas: pygame.Surface, isStop: bool):
        if isStop:
            pygame.draw.circle(canvas, self.fadeColor, (self.x, self.y), self.radius)
        else:
            pygame.draw.circle(canvas, self.color, (self.x, self.y), self.radius)


class ParticleManager:
    maxParticle = 2500

    def __init__(self, num) -> None:
        self.group = {Particle.create() for _ in range(num)}
        self.killGroup = []
        self.stop = False
        self.setSpeed = 1.0 # 0.99, 1.0, 1.01, 0.0, inf(最大速度)
        self.setMassId = -1
        self.mousePos = -1, -1
        self.button = 0
        self.killPos = None
        self.killMass = 0

        self.tryVersion = tryVersion
        self.mouseAddTime = 0

    def controlNum(self, unicode: str) -> None:
        if unicode in tuple('01234567'):
            self.setMassId = int(unicode)

    def controlKeyDown(self, event, index):
        key = event.key
        if key == pygame.K_z:
            for _ in range(10):
                if len(self.group) >= self.maxParticle:
                    break
                self.addParticle(index)
        elif key == pygame.K_x:
            for _ in range(10):
                if not self.group:
                    break
                self.group.pop()
        elif self.tryVersion:
            return
        elif key == pygame.K_q: 
            if len(self.group) < self.maxParticle:
                self.addParticle(index)
        elif key == pygame.K_w:
            if len(self.group) > 0:
                self.group.pop()
        elif key == pygame.K_s:
            self.group.clear()
        elif key == pygame.K_c:
            self.setSpeed = 0.0
        elif key == pygame.K_d:
            self.setSpeed = inf
        elif key == pygame.K_e:
            self.stop = not self.stop
        elif key == pygame.K_f:
            self.setSpeed = -1.0
        else:
            self.controlNum(event.unicode)

    def addParticle(self, index: int, pos: PointI | None =None):
        mass = 0 if index == 0 else 8 - index
        self.group.add(Particle.create(mass, pos))

    def keyPressed(self, keys):
        if keys[pygame.K_a]:
            self.setSpeed = 0.995
        elif keys[pygame.K_b]:
            self.setSpeed = 1.005

    def handleGravity(self, result: int, mousePos: PointI) -> None:
        self.button = result
        self.mousePos = mousePos
    
    def handleParticle(self, result: int, mousePos: PointI, index: int, addCool: float)-> None:
        currentTime = pygame.time.get_ticks()
        if result == 1:
            if currentTime - self.mouseAddTime > addCool and len(self.group) < self.maxParticle:
                self.mouseAddTime = currentTime
                self.addParticle(index, mousePos)
        elif self.group:
            self.killPos = mousePos
            self.killMass = 0 if index == 0 else 8 - index

    def updateWithKill(self, deltaTime: float, mass: int, angle: float, collideFunc) -> None:
        for particle in self.group:
            if ((particle.x - self.killPos[0]) ** 2 + 
                (particle.y - self.killPos[1]) ** 2 < mass * 6
                and (self.killMass == 0 or (particle.mass == self.killMass))):
                self.killGroup.append(particle)
            particle.update(self.stop, self.setMassId, self.mousePos, self.button * mass,
                            angle, self.setSpeed, deltaTime, collideFunc)
        for particle in self.killGroup:
            self.group.remove(particle)
        self.killGroup.clear()

    def reposite(self) -> None:
        self.setSpeed = 1.0
        self.setMassId = -1
        self.button = 0
        self.killPos = None

    def update(self, deltaTime: float, mass: int, angle: float, collideFunc):
        if self.killPos:
            self.updateWithKill(deltaTime, mass, angle, collideFunc)
        else:
            for particle in self.group:
                particle.update(self.stop, self.setMassId, self.mousePos, self.button * mass,
                                angle, self.setSpeed, deltaTime, collideFunc)
        self.reposite()

    def draw(self, surface):
        for particle in self.group:
            particle.draw(surface, self.stop)
