import pygame
import settings
class Tile():
    def __init__(self, x, y,colour) -> None:
        self.x = x
        self.y = y
        self.isWall = False  ##TODO bitfield instead of 3 three bools
        self.isStart = False
        self.isFinish = False
        self.colour = colour

        self.gridLinesDistribution = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLenght)) for i in range(settings.sideLenght+1)]

    def drawSelf(self,surf):
        pygame.draw.rect(surf,self.colour,rect=(self.gridLinesDistribution[self.x]+2,self.gridLinesDistribution[self.y]+2, self.gridLinesDistribution[self.x+1] - self.gridLinesDistribution[self.x] - 2 , self.gridLinesDistribution[self.y+1] - self.gridLinesDistribution[self.y] -2))

    def __str__(self):
        return f"x:{self.x},y:{self.y},iW:{self.isWall}, colour: {self.colour} \n"