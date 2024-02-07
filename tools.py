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
    """The Tools class provides the logic behind the tools for drawing/erasing walls, start, and finish."""

    # List containing positions of grid lines
    gridLines = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLength)) for i in range(settings.sideLength + 1)]

    @staticmethod
    def _getCellPos(mousePos):
        """Convert mouse position to grid cell coordinates."""
        return (binSearch(Tools.gridLines, mousePos[0])[0], binSearch(Tools.gridLines, mousePos[1])[0])

    @staticmethod
    def drawWall(mousePos, grid, drawedCells):
        """Draws wall/start/finish tiles accordingly."""
        if mousePos[0] >= 0 and mousePos[1] >= 0 and mousePos[0] <= Tools.gridLines[-1] and mousePos[1] <= Tools.gridLines[-1]:
            x, y = Tools._getCellPos(mousePos)

            if not grid[x][y].isStart and not grid[x][y].isFinish:
                if len(drawedCells) == 0:
                    # Toggle wall status of selected tile
                    grid[x][y].isWall = not grid[x][y].isWall
                    if grid[x][y].isWall == True:
                        grid[x][y].colour = settings.wall_colour
                    else:
                        grid[x][y].colour = settings.empty_colour
                    drawedCells.append(grid[x][y])
                    return grid[x][y]
                elif drawedCells[0].isWall != grid[x][y].isWall:
                    # Drawing or erasing had already begun -> make sure only one operation is performed at a time - either erasing or drawing
                    #if grid[x][y] not in drawedCells:
                    grid[x][y].isWall = not grid[x][y].isWall
                    if grid[x][y].isWall == True:
                        grid[x][y].colour = settings.wall_colour
                    else:
                        grid[x][y].colour = settings.empty_colour
                    #drawedCells.append(grid[x][y])
                    return grid[x][y]
            else:
                # Cannot draw/erase wall on start or finish tile
                return
        else:
            # Mouse pos out of range
            return
    
    @staticmethod
    def drawWallCurve(mousePos, grid, drawedCells, rel):
        drawedCells2 = list()
        prev_x = mousePos[0]-rel[0]
        prev_y = mousePos[1]-rel[1]  ##prev + rel = cur
        vector_len = int((rel[0]**2 + rel[1]**2)**0.5)
        for i in range(vector_len):
            dx = i*rel[0]/vector_len
            dy = i*rel[1]/vector_len
            tmp_x = prev_x+dx
            tmp_y = prev_y+dy
            cell_x, cell_y = Tools._getCellPos((tmp_x,tmp_y))
            if (cell_x,cell_y) not in drawedCells2:
                drawedCells2.append((cell_x,cell_y))
        
        drawedCells3 = list()
        for c in drawedCells2:
            x = c[0]
            y = c[1]
            if x >= 0 and y >= 0 and x < settings.sideLength and y < settings.sideLength:
                if grid[x][y].isStart or grid[x][y].isFinish:
                    continue
                if len(drawedCells) != 0:
                    if grid[x][y].isWall != drawedCells[0].isWall:
                        Tools.switchWall(grid[x][y])
                        drawedCells3.append(grid[x][y])
                else:
                    Tools.switchWall(grid[x][y])
                    drawedCells.append(grid[x][y])
                    drawedCells3.append(grid[x][y])

        return drawedCells3
    
    @staticmethod
    def switchWall(tile):
        tile.isWall = not tile.isWall
        if tile.isWall == True:
            tile.colour = settings.wall_colour
        else:
            tile.colour = settings.empty_colour
    
    @staticmethod
    def drawEndPoints(mousePos, grid, currEndPointPos, start=False, finish=False):
        """Draws the start or finish tile."""
        if mousePos[0] >= 0 and mousePos[1] >= 0 and mousePos[0] <= Tools.gridLines[-1] and mousePos[1] <= Tools.gridLines[-1]:
            x, y = Tools._getCellPos(mousePos)
            if x < settings.sideLength and y < settings.sideLength:
                if currEndPointPos != (x, y) and ((start and not grid[x][y].isFinish) or (finish and not grid[x][y].isStart)):
                    if start:
                        grid[x][y].isWall = False
                        grid[x][y].colour = settings.start_colour
                        grid[x][y].isStart = True
                        grid[currEndPointPos[0]][currEndPointPos[1]].colour = settings.empty_colour
                        grid[currEndPointPos[0]][currEndPointPos[1]].isStart = False
                        return x, y, True

                    elif finish:
                        grid[x][y].isWall = False
                        grid[x][y].colour = settings.finish_colour
                        grid[x][y].isFinish = True
                        grid[currEndPointPos[0]][currEndPointPos[1]].colour = settings.empty_colour
                        grid[currEndPointPos[0]][currEndPointPos[1]].isFinish = False
                        return x, y, True
                
        return currEndPointPos[0], currEndPointPos[1], False
