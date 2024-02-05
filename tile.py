# Import necessary modules
import pygame
import settings

offset = 1  # For 0, the maze has no edges; for 1, normal edges; for i > 1, 'tile effect'.

# Define the Tile class for representing individual tiles in the maze
class Tile():
    def __init__(self, x, y, colour) -> None:
        # Initialize tile attributes
        self.x = x
        self.y = y
        self.isWall = False
        self.isStart = False
        self.isFinish = False
        self.colour = colour

        # Determine the distribution of grid lines in the maze
        self.gridLinesDistribution = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLength)) for i in range(settings.sideLength + 1)]

    # Method to draw the tile onto the screen
    def drawSelf(self, surf):
        pygame.draw.rect(surf, self.colour,
                         rect=(self.gridLinesDistribution[self.x] + offset, self.gridLinesDistribution[self.y] + offset,
                               self.gridLinesDistribution[self.x + 1] - self.gridLinesDistribution[self.x] - offset,
                               self.gridLinesDistribution[self.y + 1] - self.gridLinesDistribution[self.y] - offset))

    # Method to get the position of the tile
    def get_pos(self):
        return (self.x, self.y)

    # String representation of the Tile object
    def __str__(self):
        return f"x:{self.x}, y:{self.y}, isWall:{self.isWall}, colour: {self.colour}"
