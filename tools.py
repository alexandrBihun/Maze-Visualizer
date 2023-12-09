import settings


def binSearch(sorted_list, target):
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_value = sorted_list[mid]

        if mid_value == target:
            return mid, mid  # Target value found at index mid

        elif mid_value < target:
            low = mid + 1
        else:
            high = mid - 1

    # At this point, low > high, and the target lies between high and low
    return high, low

class Tools:
    result = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLenght)) for i in range(settings.sideLenght+1)] ## gets positions of grid lines

    @staticmethod
    def _getCellPos(mousePos):
        return (binSearch(Tools.result, mousePos[0])[0], binSearch(Tools.result, mousePos[1])[0])

    @staticmethod
    def drawWall(mousePos,grid, drawedCells, start = False, finish = False, currStartOrEndPos = None ):
        if mousePos[0] < Tools.result[-1] and mousePos[1] < Tools.result[-1]:
            x,y = Tools._getCellPos(mousePos)
            if start or finish:
                return Tools._drawStartorEnd(x,y,grid,currStartOrEndPos,start,finish)
            elif grid[x][y].value == 0:
                if len(drawedCells) == 0:
                    grid[x][y].isWall = not grid[x][y].isWall
                    drawedCells.append((x,y))
                    return True
                elif grid[drawedCells[0][0]][drawedCells[0][1]].isWall != grid[x][y].isWall: ##assures only one operation is performed at a time - either erasing or drawing
                    if (x,y) not in drawedCells:
                        grid[x][y].isWall = not grid[x][y].isWall
                        return True
        elif finish or start:
            return currStartOrEndPos[0],currStartOrEndPos[1], False
    @staticmethod
    def _drawStartorEnd(x,y,grid, currStartPos, start = False, finish = False):
        if currStartPos != (x,y) and  ((start and grid[x][y].value != 2) or (finish and grid[x][y].value != 1)):
            if start:
                grid[x][y].isWall = False
                grid[x][y].value = 1 
                grid[currStartPos[0]][currStartPos[1]].value = 0
                return x,y,True

            elif finish:
                grid[x][y].isWall = False
                grid[x][y].value = 2
                grid[currStartPos[0]][currStartPos[1]].value = 0
                return x,y, True
        else:
            return currStartPos[0], currStartPos[1], False