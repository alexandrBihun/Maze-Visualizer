from sidebar import Sidebar
from tile import Tile
import pygame
import settings
from tools import Tools

class Vizualizator():
    def __init__(self, main) -> None:
        self.main = main
        self.grid: list[list[Tile]] = []
        self.sidebar = Sidebar()
        
        self.font = pygame.font.SysFont('Verdana' , 100, True)
        self.bgColor = ("light gray")
        self.gridLinesDistribution = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLenght)) for i in range(settings.sideLenght+1)]

        self.drawGrid(self.main.screen)
        self.initGrid()

        self.toRedraw = True
        self.tool = "wallBrush"
        self.drawedCells = []
        self.selectedAlgo = "DFS"
        self.visited = set()
        self.visualDelay = 1

    def drawTileOntoSurface(self, x,y):  #mozna misto x,y jen tile
        self.grid[x][y].drawSelf(self.main.screen)

    def redrawVisited(self): 
        for tile in self.visited:
            if not tile.isStart and not tile.isFinish and not tile.isWall:  
                tile.colour = "light gray"
                self.drawTileOntoSurface(tile.x,tile.y)
        pygame.display.flip()

    def handleEvents(self,event):
        self.sidebar.handle_events(event)

        if event.type == pygame.MOUSEBUTTONUP:
            self.drawedCells = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.tool == "selectStart":
                if pygame.mouse.get_pressed()[0]:
                    x,y, self.toRedraw = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells, start = True, currStartOrEndPos= self.start)
                    if self.toRedraw:
                        self.drawTileOntoSurface(*self.start)
                        self.start = (x,y)
                        self.drawTileOntoSurface(x,y)

            elif self.tool == "selectFinish":
                if pygame.mouse.get_pressed()[0]:
                    x,y, self.toRedraw = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells, finish = True, currStartOrEndPos= self.finish)
                    if self.toRedraw:
                        self.drawTileOntoSurface(*self.finish)
                        self.finish = (x,y)
                        self.drawTileOntoSurface(x,y)

            elif self.tool == "wallBrush":
                result = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells)
                if len(result)>2 and result[2]:
                    self.toRedraw = result[2]
                    if len(self.drawedCells)>0:
                        self.drawTileOntoSurface(result[0],result[1])
                            
        elif event.type == pygame.MOUSEMOTION:
            if self.tool == "wallBrush" and pygame.mouse.get_pressed()[0]:
                result = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells)
                print(result)
                if len(result)>2 and result[2]:
                    self.toRedraw = result[2]
                    if len(self.drawedCells)>0:
                        self.drawTileOntoSurface(result[0],result[1])
            else:
                self.drawedCells = []

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.tool = "selectStart"
            if event.key == pygame.K_f:
                self.tool = "selectFinish"
            if event.key == pygame.K_d:
                self.tool = "wallBrush"
            if event.key == pygame.K_1:
                self.selectedAlgo = "DFS"
            if event.key == pygame.K_2:
                self.selectedAlgo = "BFS"
            if event.key == pygame.K_3:
                self.selectedAlgo = "A*"
            if event.key == pygame.K_SPACE:
                self.redrawVisited()
                path = self.runVisualization()
                if path == None:
                    print("No path found")
                else: 
                    self.visualizePath(path)
            if event.key == pygame.K_c:
                self.redrawVisited()
            if event.key == pygame.K_UP:
                self.visualDelay += 5
                print(self.visualDelay)
            if event.key == pygame.K_DOWN:
                self.visualDelay = max(0,self.visualDelay-1)
                print(self.visualDelay)
    
    def visualizePath(self, path: dict): 
        curr = self.grid[self.finish[0]][self.finish[1]]

        while curr != None:
            if not curr.isStart and not curr.isFinish:
                curr.colour = "yellow"
                self.drawTileOntoSurface(curr.x,curr.y)
                print(curr.x,curr.y)
                pygame.display.flip()
                pygame.time.delay(self.visualDelay)

            curr = path[curr]

    def get_neighbours(self,node): ##node is tile object, returns node pointers 
        neighbours = []

        if node.x>0:
            if self.grid[node.x-1][node.y].isWall == False:
                neighbours.append(self.grid[node.x-1][node.y])

        if node.x<settings.sideLenght-1:
            if self.grid[node.x+1][node.y].isWall == False:
                neighbours.append(self.grid[node.x+1][node.y])
                
        if node.y>0:
            if self.grid[node.x][node.y-1].isWall == False:
                neighbours.append(self.grid[node.x][node.y-1])

        if node.y<settings.sideLenght-1:
            if self.grid[node.x][node.y+1].isWall == False:
                neighbours.append(self.grid[node.x][node.y+1])

        return neighbours
    
    def DFS(self):  
        stack = [self.grid[self.start[0]][self.start[1]]]
        visited = set()
        parentDict = dict()
        count = 0
        clock = pygame.time.Clock() #TODO check if there is a better way for animation delaying ;; clock drastically lowers cpu usage, other possibility: pygame.time.delay()
        last = pygame.time.get_ticks()

        parentDict[self.grid[self.start[0]][self.start[1]]] = None

        previous = None
        while stack:
            clock.tick(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            now = pygame.time.get_ticks()
            if now - last >= self.visualDelay:
                last = now
                count += 1
                
                current = stack.pop()
                i, j = current.x,current.y
                if (i,j) != self.start and (i,j) != self.finish:
                    self.grid[i][j].colour = "orange"
                    self.drawTileOntoSurface(i,j)

                if previous != None:
                    i, j = previous.x,previous.y
                    if (i,j) != self.start and (i,j) != self.finish:
                        self.grid[i][j].colour = "red"
                        self.drawTileOntoSurface(i,j)

                previous = current
                
                pygame.display.flip()

                if current == self.grid[self.finish[0]][self.finish[1]]:
                    self.visited = visited
                    return parentDict

                if current not in visited:
                    visited.add(current)

                    # add neighbors to the stack
                    for neighbor in self.get_neighbours(current):
                        if neighbor not in visited and neighbor not in stack:
                            stack.append(neighbor)
                            parentDict[neighbor] = current
                
        self.visited = visited
        return None
    
    def runVisualization(self):
        """Starts visualisation accordigly to selected alg"""
        if self.selectedAlgo == "BFS":
            return self.BFS()
        elif self.selectedAlgo == "A*":
            return self.aStar()
        elif self.selectedAlgo == "DFS":
            return self.DFS()

    def drawGrid(self,surf):  
        surf.fill(self.bgColor)

        for i in self.gridLinesDistribution:
            pygame.draw.line(surf, (182,187,196), (0, i),(settings.widthGrid ,i))
            pygame.draw.line(surf, (182,187,196), (i, 0), (i, settings.heightGrid))
    
    def draw(self): 
        pygame.display.flip()
        
    def run(self): 
        if self.toRedraw:
            print("drawing")
            self.draw()
            self.toRedraw = False
            
    def initGrid(self): 
        """
        initiliziases grid: grid is a list of column_lists, indexed into as [x][y], x grows from left to right, y top to bot
        """
        for i in range(settings.sideLenght):
            column_list = []#list of all tiles in a single Column
            for j in range(settings.sideLenght):
                t = Tile(i,j,"light gray")
                column_list.append(t)
            self.grid.append(column_list)
        
        self.grid[0][0].colour = "green"
        self.grid[0][0].isStart = True
        self.grid[settings.sideLenght-1][settings.sideLenght-1].colour = "blue"
        self.grid[settings.sideLenght-1][settings.sideLenght-1].isFinish = True
        self.start = (0,0)
        self.finish = (settings.sideLenght-1, settings.sideLenght-1) ##maybe change both start and finish to tile pointers

        self.drawTileOntoSurface(0,0)
        self.drawTileOntoSurface(settings.sideLenght-1, settings.sideLenght-1)