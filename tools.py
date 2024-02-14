# Import settings module
import settings

def binSearch(sorted_list, target):
    """Binary searches to find the index of a target in a sorted list or if target not in list returns which two indexes it would fit between."""
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = sorted_list[mid]

        if mid_value == target:
            return mid, mid

        elif mid_value < target:
            low = mid + 1
        else:
            high = mid - 1

    return high, low

class Tools:
    """The Tools class provides the logic behind the tools for drawing/erasing walls, start, and goal."""

    # List containing positions of grid lines
    gridLines = [round(i * (settings.widthGrid) / (settings.sideLength)) for i in range(settings.sideLength + 1)]

    @staticmethod
    def _getCellPos(mousePos):
        """Convert mouse position to grid tile coordinates"""
        return (binSearch(Tools.gridLines, mousePos[0])[0], binSearch(Tools.gridLines, mousePos[1])[0])

    @staticmethod
    def setWall(mousePos, grid, drawnTiles):
        """Sets wall tile. For MOUSEBUTTONDONW event handle. Returns changed tile or None for failure"""
        if mousePos[0] >= 0 and mousePos[1] >= 0 and mousePos[0] <= Tools.gridLines[-1] and mousePos[1] <= Tools.gridLines[-1]:
            x, y = Tools._getCellPos(mousePos)

            if not grid[x][y].isStart and not grid[x][y].isGoal:
                if len(drawnTiles) == 0:
                    # Toggle wall status of selected tile
                    Tools.switchWall(grid[x][y])
                    drawnTiles.append(grid[x][y])
                    return grid[x][y]
            else:
                # Cannot draw/erase wall on start or goal tile
                return
        else:
            # Mouse pos out of range
            return
    
    @staticmethod
    def setWallCurve(mousePos, grid, drawnTiles, rel):
        """Handles MOUSEMOTION wall draw event. Sets nodes with respect to tiles the mouse hovered over between frames. Returns changed tiles"""
        drawnTiles2 = list()
        prev_x = mousePos[0]-rel[0]
        prev_y = mousePos[1]-rel[1]  
        vector_len = int((rel[0]**2 + rel[1]**2)**0.5)
        # Finds tiles mouse hovered over between this and last frame by smoothly adding a fraction of the relative change vector to first pos
        for i in range(vector_len):
            dx = i*rel[0]/vector_len
            dy = i*rel[1]/vector_len
            tmp_x = prev_x+dx
            tmp_y = prev_y+dy
            cell_x, cell_y = Tools._getCellPos((tmp_x,tmp_y))
            if (cell_x,cell_y) not in drawnTiles2:
                drawnTiles2.append((cell_x,cell_y))
        
        drawnTiles3 = list()
        for c in drawnTiles2:
            x = c[0]
            y = c[1]
            # Filters out tiles inappropriate for redrawing
            if x >= 0 and y >= 0 and x < settings.sideLength and y < settings.sideLength:
                if grid[x][y].isStart or grid[x][y].isGoal:
                    continue
                if len(drawnTiles) != 0:
                    if grid[x][y].isWall != drawnTiles[0].isWall:
                        Tools.switchWall(grid[x][y])
                        drawnTiles3.append(grid[x][y])
                else:
                    # Occurs when mouse held down in sidebar and moved to grid space
                    Tools.switchWall(grid[x][y])
                    drawnTiles.append(grid[x][y])
                    drawnTiles3.append(grid[x][y])

        return drawnTiles3
    
    @staticmethod
    def switchWall(tile):
        """Switches tile's wall status"""
        tile.isWall = not tile.isWall
        if tile.isWall == True:
            tile.colour = settings.wall_colour
        else:
            tile.colour = settings.empty_colour
    
    @staticmethod
    def setEndPoints(mousePos, grid, currEndPointPos, start=False, goal=False):
        """Sets new start or goal tile."""
        if mousePos[0] >= 0 and mousePos[1] >= 0 and mousePos[0] <= Tools.gridLines[-1] and mousePos[1] <= Tools.gridLines[-1]:
            x, y = Tools._getCellPos(mousePos)
            if x < settings.sideLength and y < settings.sideLength:
                if currEndPointPos != (x, y) and ((start and not grid[x][y].isGoal) or (goal and not grid[x][y].isStart)):
                    if start:
                        # Sets new start tile
                        grid[x][y].isWall = False
                        grid[x][y].colour = settings.start_colour
                        grid[x][y].isStart = True
                        grid[currEndPointPos[0]][currEndPointPos[1]].colour = settings.empty_colour
                        grid[currEndPointPos[0]][currEndPointPos[1]].isStart = False
                        return x, y, True

                    elif goal:
                        # Sets new goal tile
                        grid[x][y].isWall = False
                        grid[x][y].colour = settings.goal_colour
                        grid[x][y].isGoal = True
                        grid[currEndPointPos[0]][currEndPointPos[1]].colour = settings.empty_colour
                        grid[currEndPointPos[0]][currEndPointPos[1]].isGoal = False
                        return x, y, True
                
        return currEndPointPos[0], currEndPointPos[1], False
