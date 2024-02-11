# Import necessary modules
import pygame
import settings

# Determine the distribution of grid lines in the maze
gridLinesDistribution = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLength)) for i in range(settings.sideLength + 1)]

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

    # Method to draw the tile onto the screen
    def drawSelf(self, surf):
        pygame.draw.rect(surf, self.colour,
                         rect=(gridLinesDistribution[self.x] + settings.offset, gridLinesDistribution[self.y] + settings.offset,
                               gridLinesDistribution[self.x + 1] - gridLinesDistribution[self.x] - settings.offset,
                               gridLinesDistribution[self.y + 1] - gridLinesDistribution[self.y] - settings.offset))
        
    def get_neighbours(self, grid):
        """Get list of tile's neighbours"""
        neighbours = []
        if self.y < settings.sideLength - 1:
            if grid[self.x][self.y + 1].isWall == False:
                neighbours.append(grid[self.x][self.y + 1])
        if self.y > 0:
            if grid[self.x][self.y - 1].isWall == False:
                neighbours.append(grid[self.x][self.y - 1])
        if self.x < settings.sideLength - 1:
            if grid[self.x + 1][self.y].isWall == False:
                neighbours.append(grid[self.x + 1][self.y])
        if self.x > 0:
            if grid[self.x - 1][self.y].isWall == False:
                neighbours.append(grid[self.x - 1][self.y])

        if (self.x + self.y) % 2 != 0:  
            # Makes paths "prettier"; source: https://www.redblobgames.com/pathfinding/a-star/implementation.html#troubleshooting-ugly-path
            neighbours.reverse()

        return neighbours

    # Method to get the position of the tile
    def get_pos(self):
        return (self.x, self.y)

    # String representation of the Tile object
    def __str__(self):
        return f"x:{self.x}, y:{self.y}, isWall:{self.isWall}, colour: {self.colour}"
