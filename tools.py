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
    def drawWall(mousePos, grid, drawedCells, start=False, finish=False, currStartOrEndPos=None):
        """Draws wall/start/finish tiles accordingly."""
        if mousePos[0] < Tools.gridLines[-1] and mousePos[1] < Tools.gridLines[-1]:
            x, y = Tools._getCellPos(mousePos)
            if start or finish:
                # Draw start or finish
                return Tools._drawStartorEnd(x, y, grid, currStartOrEndPos, start, finish)
            elif not grid[x][y].isStart and not grid[x][y].isFinish:
                if len(drawedCells) == 0:
                    # Toggle wall status of selected tile
                    grid[x][y].isWall = not grid[x][y].isWall
                    if grid[x][y].isWall == True:
                        grid[x][y].colour = settings.wall_colour
                    else:
                        grid[x][y].colour = settings.empty_colour
                    drawedCells.append(grid[x][y])
                    return x, y, True
                elif drawedCells[0].isWall != grid[x][y].isWall:
                    # Drawing or erasing had already begun -> make sure only one operation is performed at a time - either erasing or drawing
                    if grid[x][y] not in drawedCells:
                        grid[x][y].isWall = not grid[x][y].isWall
                        if grid[x][y].isWall == True:
                            grid[x][y].colour = settings.wall_colour
                        else:
                            grid[x][y].colour = settings.empty_colour
                        return x, y, True
                else:
                    # Needed for the MOUSEMOTION event handle to work properly
                    return [False]
            else:
                # Cannot draw/erase wall on start or finish tile
                return [False]
        elif finish or start:
            # Mouse pos out of range, but tile is start or end, returning (_,_,False) makes caller code not redraw anything
            return currStartOrEndPos[0], currStartOrEndPos[1], False
        else:
            # Mouse pos out of range
            return [False]

    @staticmethod
    def _drawStartorEnd(x, y, grid, currStartPos, start=False, finish=False):
        """Draws the start or finish tile."""
        if currStartPos != (x, y) and ((start and not grid[x][y].isFinish) or (finish and not grid[x][y].isStart)):
            if start:
                grid[x][y].isWall = False
                grid[x][y].colour = settings.start_colour
                grid[x][y].isStart = True
                grid[currStartPos[0]][currStartPos[1]].colour = settings.empty_colour
                grid[currStartPos[0]][currStartPos[1]].isStart = False
                return x, y, True

            elif finish:
                grid[x][y].isWall = False
                grid[x][y].colour = settings.finish_colour
                grid[x][y].isFinish = True
                grid[currStartPos[0]][currStartPos[1]].colour = settings.empty_colour
                grid[currStartPos[0]][currStartPos[1]].isFinish = False
                return x, y, True
        else:
            return currStartPos[0], currStartPos[1], False
