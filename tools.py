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

freeTileColour = "light gray"
class Tools:
    
    gridLines = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLenght)) for i in range(settings.sideLenght+1)] ## gets positions of grid lines

    @staticmethod
    def _getCellPos(mousePos):
        return (binSearch(Tools.gridLines, mousePos[0])[0], binSearch(Tools.gridLines, mousePos[1])[0])

    @staticmethod
    def drawWall(mousePos,grid, drawedCells, start = False, finish = False, currStartOrEndPos = None ):
        if mousePos[0] < Tools.gridLines[-1] and mousePos[1] < Tools.gridLines[-1]:
            x,y = Tools._getCellPos(mousePos)
            if start or finish:
                return Tools._drawStartorEnd(x,y,grid,currStartOrEndPos,start,finish)
            elif not grid[x][y].isStart and not grid[x][y].isFinish:
                if len(drawedCells) == 0:
                    grid[x][y].isWall = not grid[x][y].isWall
                    if grid[x][y].isWall == True:
                        grid[x][y].colour = "black"
                    else:
                        grid[x][y].colour = freeTileColour
                    drawedCells.append(grid[x][y])
                    return x,y,True
                elif drawedCells[0].isWall != grid[x][y].isWall: ##assures only one operation is performed at a time - either erasing or drawing
                    if grid[x][y] not in drawedCells:
                        grid[x][y].isWall = not grid[x][y].isWall
                        if grid[x][y].isWall == True:
                            grid[x][y].colour = "black"
                        else:
                            grid[x][y].colour = freeTileColour
                        return x,y,True
                else: ##needed for the MOUSEMOTION event handle to work properly
                    return [False]
                    #return x,y,False
            else:
                return [False]
        elif finish or start:
            return currStartOrEndPos[0],currStartOrEndPos[1], False
        else:
            return [False]
    @staticmethod
    def _drawStartorEnd(x,y,grid, currStartPos, start = False, finish = False):
        if currStartPos != (x,y) and  ((start and not grid[x][y].isFinish) or (finish and not grid[x][y].isStart)):
            if start:
                print(grid[x][y].isFinish)
                grid[x][y].isWall = False
                grid[x][y].colour = "green"
                grid[x][y].isStart = True
                grid[currStartPos[0]][currStartPos[1]].colour = freeTileColour
                grid[currStartPos[0]][currStartPos[1]].isStart= False
                return x,y,True

            elif finish:
                grid[x][y].isWall = False
                grid[x][y].colour = "blue"
                grid[x][y].isFinish= True
                grid[currStartPos[0]][currStartPos[1]].colour = freeTileColour
                grid[currStartPos[0]][currStartPos[1]].isFinish = False
                return x,y, True
        else:
            return currStartPos[0], currStartPos[1], False