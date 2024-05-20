import pygame
from random import uniform
from math import sqrt
from data import *
from segment import LineSegment, intersect_antipole, antipole



class ObstacleLine:
    def __init__(self, p0: PointI, p1: PointI) -> None:
        self.segment = LineSegment(p0, p1)
        vector = p1[0] - p0[0], p1[1] - p0[1]
        self.length = sqrt(vector[0] ** 2 + vector[1] ** 2)
        self.direction = (vector[0] / self.length, vector[1] / self.length)

    def collide(self, pos: PointF, pos2: PointF,
                velocity: PointF) -> tuple[
                    PointF,PointF, PointF, 'ObstacleLine'
                ]:
        moveLine = LineSegment(pos, pos2)
        result = intersect_antipole(moveLine, self.segment)
        if result is None:
            return None
        velocity_antipole = antipole(velocity, self.segment)
        return result[0], result[1], velocity_antipole, self

    def draw(self, canvas: pygame.Surface, isStop: bool) -> None:
        if isStop:
            pygame.draw.line(canvas, fadeWhite, self.segment.start, self.segment.end, 3)
        else:
            pygame.draw.line(canvas, white, self.segment.start, self.segment.end, 3)

    def dropCheck(self, mousePos: PointI, checkDistance: float) -> bool:
        x = mousePos[0] - self.segment.start[0]
        y = mousePos[1] - self.segment.start[1]
        dot = x * self.direction[0] + y * self.direction[1] 
        cross = x * self.direction[1] - y * self.direction[0]
        dotR = -3 < dot < self.length + 3
        crossR = -3 < cross < 3
        return dotR and crossR

class ObstacleManager:
    maxNum = 64

    def __init__(self) -> None:
        self.group = set()
        self.drawPoint = None
        self.mousePosForDrop = None
        self.checkDistance = -1
        self.killGroup = []

    def controlKeyDown(self, key, particleEmpty: bool) -> None:
        if key == pygame.K_s and particleEmpty:
            self.group.clear()

    def control(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.drawPoint = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                end = pygame.mouse.get_pos()
                if self.drawPoint and self.drawPoint != end and len(self.group) < self.maxNum:
                    self.group.add(ObstacleLine(self.drawPoint, end))
                self.drawPoint = None

    def cancelDraw(self, rightButton: bool) -> None:
        if rightButton:
            self.drawPoint = None

    def dropObstacle(self, mousePos: PointI, checkDistance: float) -> None:
        if self.group:
            self.mousePosForDrop = mousePos
            self.checkDistance = checkDistance

    def draw(self, canvas: pygame.Surface, isStop: bool) -> None:
        for ol in self.group:
            ol.draw(canvas, isStop)
        if self.drawPoint is not None:
            pygame.draw.line(canvas, grey, self.drawPoint, pygame.mouse.get_pos(), 3)

    def collide(self, pos: PointF, pos2: PointF, velocity: tuple[float, float ],
                last: ObstacleLine | None=None) -> tuple[float, float, float, float]:

        resultList = []
        for ol in self.group:
            if ol is last:
                continue
            resultOne = ol.collide(pos, pos2, velocity)
            if resultOne:
                resultList.append(resultOne)
        if not resultList:
            return pos2[0], pos2[1], velocity[0], velocity[1]
        result = min(
            resultList, key=lambda r:(r[0][0] - pos[0]) ** 2 + (r[0][1] - pos[1]) ** 2
        )
        pos, pos2, velocity, last = result
        return self.collide(pos, pos2, velocity, last)

    def update(self) -> None:
        if not self.mousePosForDrop:
            return
        # 清除障碍物
        for ol in self.group:
            if ol.dropCheck(self.mousePosForDrop, self.checkDistance):
                self.killGroup.append(ol)
        for ol in self.killGroup:
            self.group.remove(ol)
        self.killGroup.clear()
        self.mousePosForDrop = None
