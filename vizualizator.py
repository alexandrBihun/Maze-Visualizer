from sidebar import Sidebar
from tile import Tile
import pygame
import settings
from tools import Tools
import random
from collections import deque
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
import sys

def invert_dict(original_dict):
    inverted_dict = {}
    
    for key, value in original_dict.items():
        if value not in inverted_dict:
            inverted_dict[value] = [key]
        else:
            inverted_dict[value].append(key)
    
    return inverted_dict

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
        self.visualDelay = 5

    def generateMaze(self):
        def get_frontiers(tile):
            frontiers = []

            if tile.x>1:
                if self.grid[tile.x-2][tile.y].isWall == True:
                    frontiers.append(self.grid[tile.x-2][tile.y])

            if tile.x<settings.sideLenght-2:
                if self.grid[tile.x+2][tile.y].isWall == True:
                    frontiers.append(self.grid[tile.x+2][tile.y])
                    
            if tile.y>1:
                if self.grid[tile.x][tile.y-2].isWall == True:
                    frontiers.append(self.grid[tile.x][tile.y-2])

            if tile.y<settings.sideLenght-2:
                if self.grid[tile.x][tile.y+2].isWall == True:
                    frontiers.append(self.grid[tile.x][tile.y+2])

            return frontiers
        

        for column in self.grid:
            for tile in column:
                tile.isWall = True
                tile.isStart = False
                tile.isFinish = False
                tile.colour = "black"
        x,y = random.randint(0,settings.sideLenght-1),random.randint(0,settings.sideLenght-1)
        self.grid[x][y].isWall = False
        self.grid[x][y].colour = self.bgColor

        frontierDict = dict()
        print("first:",self.grid[x][y],"\n")
        frontiers = get_frontiers(self.grid[x][y])
        for f in frontiers:
            frontierDict[f] = self.grid[x][y]
        
        while len(frontiers):
            
            #uncomment for maze-gen visualization:
            #for column in self.grid:
            #    for tile in column:
            #        self.drawTileOntoSurface(tile.x,tile.y)
            #pygame.display.flip()
            

            randomTile = frontiers.pop(random.randint(0,len(frontiers)-1))
            randomTile.colour = self.bgColor
            randomTile.isWall = False

            fatherOfRandomTile = frontierDict[randomTile]

            middleTile = self.grid[(randomTile.x+fatherOfRandomTile.x)//2][(randomTile.y+fatherOfRandomTile.y)//2] ## middle of two points formula
            middleTile.isWall = False
            middleTile.colour = self.bgColor
            
            newFrontiers = get_frontiers(randomTile)
            for f in newFrontiers:
                frontierDict[f] = randomTile
            frontiers.extend(newFrontiers)

        startFound = False
        lastTile = None
        for column in self.grid:
            for tile in column:
                if not tile.isWall:
                    if startFound == False:
                        tile.isStart = True
                        tile.colour = "green"
                        startFound = True 
                        self.startTile = self.grid[tile.x][tile.y]
                    lastTile = tile
                self.drawTileOntoSurface(tile.x,tile.y)

        self.finishTile = self.grid[lastTile.x][lastTile.y]
        lastTile.colour = "blue"
        lastTile.isFinish = True
        self.drawTileOntoSurface(lastTile.x,lastTile.y)
                
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
                    x,y, self.toRedraw = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells, start = True, currStartOrEndPos= self.startTile.get_pos())
                    if self.toRedraw:
                        self.drawTileOntoSurface(*self.startTile.get_pos())
                        self.startTile = self.grid[x][y]
                        self.drawTileOntoSurface(x,y)

            elif self.tool == "selectFinish":
                if pygame.mouse.get_pressed()[0]:
                    x,y, self.toRedraw = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells, finish = True, currStartOrEndPos= self.finishTile.get_pos())
                    if self.toRedraw:
                        self.drawTileOntoSurface(*self.finishTile.get_pos())
                        self.finishTile = self.grid[x][y]
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
                self.selectedAlgo = "greedy"
            if event.key == pygame.K_4:
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
            if event.key == pygame.K_g:
                self.generateMaze()
                self.draw()
            if event.key == pygame.K_UP:
                self.visualDelay += 5
                print(self.visualDelay)
            if event.key == pygame.K_DOWN:
                self.visualDelay = max(0,self.visualDelay-5)
                print(self.visualDelay)
    
    def visualizePath(self, path: dict): 
        curr = self.finishTile
        i=0
        while curr != None:
            if not curr.isStart and not curr.isFinish:
                curr.colour = "yellow"
                self.drawTileOntoSurface(curr.x,curr.y)
                pygame.display.flip()
                pygame.time.delay(self.visualDelay)
            i+=1
            curr = path[curr]
        print(f"Path len: {i}")

    def get_neighbours(self,node):
        """node is tile object, returns node pointers"""
        neighbours = []

        if (node.x+node.y)%2 == 0 or True: 
            if node.y<settings.sideLenght-1:
                if self.grid[node.x][node.y+1].isWall == False:
                    neighbours.append(self.grid[node.x][node.y+1])
            if node.y>0:
                if self.grid[node.x][node.y-1].isWall == False:
                    neighbours.append(self.grid[node.x][node.y-1])
            if node.x<settings.sideLenght-1:
                if self.grid[node.x+1][node.y].isWall == False:
                    neighbours.append(self.grid[node.x+1][node.y])
            if node.x>0:
                if self.grid[node.x-1][node.y].isWall == False:
                    neighbours.append(self.grid[node.x-1][node.y])

        if (node.x+node.y)%2 != 0: #https://www.redblobgames.com/pathfinding/a-star/implementation.html#troubleshooting-ugly-path
            neighbours.reverse()

        return neighbours
    
    def Alg_check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.visualDelay += 5
                        print(self.visualDelay)
                    if event.key == pygame.K_DOWN:
                        self.visualDelay = max(0,self.visualDelay-5)
                        print(self.visualDelay)
    
    def manhattan_dist(self, node, goal):
        """Manhattan distance heuristic."""
        return abs(node.x - goal.x) + abs(node.y - goal.y)
    
    def DFS(self):  
        stack = [self.startTile]
        visited = set()
        parentDict = dict()
        clock = pygame.time.Clock() #TODO check if there is a better way for animation delaying ;; clock drastically lowers cpu usage, other possibility: pygame.time.delay()
        last = pygame.time.get_ticks()

        parentDict[self.startTile] = None

        previous = None
        while stack:
            clock.tick(1000)
            self.Alg_check_events()
            now = pygame.time.get_ticks()
            if now - last >= self.visualDelay:
                last = now
                
                current = stack.pop()
                if current != self.startTile and current != self.finishTile:
                    current.colour = "orange"
                    self.drawTileOntoSurface(*current.get_pos())

                if previous != None:
                    if previous != self.startTile and previous != self.finishTile:
                        previous.colour = "red"
                        self.drawTileOntoSurface(*previous.get_pos())

                previous = current
                
                pygame.display.flip()

                if current == self.finishTile:
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

    def BFS(self):
        visited = set()
        queue = deque()
        queue.appendleft(self.startTile)
        parentDict = dict()
        parentDict[self.startTile] = None

        distanceDict = dict()
        distanceDict[self.startTile] = 0

        while queue:
            self.Alg_check_events()
            current = queue.pop()
            
            if current == self.finishTile:
                visited.clear()
                i = 0
                invDict = invert_dict(distanceDict)
                while i in invDict.keys():
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    for c in invDict[i]:
                        if not c.isStart  and not c.isFinish:
                            visited.add(c)
                            c.colour = "red"
                            self.drawTileOntoSurface(c.x,c.y)
                    pygame.display.flip()
                    pygame.time.delay(self.visualDelay)
                    i+=1

                self.visited = visited

                return parentDict

            visited.add(current)

            for neighbor in self.get_neighbours(current):
                if neighbor not in visited and neighbor not in queue:
                    queue.appendleft(neighbor)
                    parentDict[neighbor] = current
                    distanceDict[neighbor] = distanceDict[current] + 1

        visited.clear()
        i = 0
        invDict = invert_dict(distanceDict)
        while i in invDict.keys():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            for c in invDict[i]:
                if not c.isStart  and not c.isFinish:
                    visited.add(c)
                    c.colour = "red"
                    self.drawTileOntoSurface(c.x,c.y)
            pygame.display.flip()
            pygame.time.delay(self.visualDelay)
            i+=1

        self.visited = visited
        
        return None

    def greedy_BeFS(self):

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            item: Any=field(compare=False)

        visited = set()
        priority_queue = PriorityQueue()
        priority_queue.put(PrioritizedItem(priority=0, item=self.startTile))  # Priority queue with (heuristic, node) tuple
        
        parentDict = dict()
        parentDict[self.startTile] = None
        visited.add(self.startTile)
        while not priority_queue.empty():
            self.Alg_check_events()
            current = priority_queue.get().item

            if current == self.finishTile:
                print("found greedy")
                self.visited = visited
                return parentDict

            if current != self.startTile:
                current.colour = "red"
                self.drawTileOntoSurface(current.x,current.y)
                pygame.display.flip()
                pygame.time.delay(self.visualDelay)

            for neighbor in self.get_neighbours(current):
                if neighbor not in visited:
                    priority = self.manhattan_dist(neighbor, self.finishTile)
                    
                    priority_queue.put(PrioritizedItem(priority=priority,item=neighbor))
                    visited.add(neighbor)
                    parentDict[neighbor] = current

        return None

    def aStar(self):

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            h_score: int
            item: Any=field(compare=False)

        visited = set()
        priority_queue = PriorityQueue()
        f_score_start = self.manhattan_dist(self.startTile, self.finishTile)
        priority_queue.put(PrioritizedItem(priority=0,h_score= f_score_start,item=self.startTile))  # Priority queue with (heuristic, node) tuple

        parentDict = dict()
        parentDict[self.startTile] = None
        visited.add(self.startTile)

        g_cost_dict = dict()
        g_cost_dict[self.startTile] = 0

        while not priority_queue.empty():
            self.Alg_check_events()
            current = priority_queue.get().item
            print("curr:", current)

            if current == self.finishTile:
                print("found A*")
                self.visited = visited
                return parentDict

            if current != self.startTile and current.colour!= "red":
                current.colour = "red"
                self.drawTileOntoSurface(current.x,current.y)
                pygame.display.flip()
                pygame.time.delay(self.visualDelay)

            for neighbor in self.get_neighbours(current):
                g_cost = g_cost_dict[current] + 1
                h_cost= self.manhattan_dist(neighbor, self.finishTile)
                f_cost = g_cost + h_cost

                if neighbor not in visited:# and neighbor not in priority_queue.queue:
                    priority_queue.put(PrioritizedItem(priority=f_cost,h_score=h_cost, item=neighbor))
                    g_cost_dict[neighbor] = g_cost
                    parentDict[neighbor] = current
                    visited.add(neighbor)
                    if neighbor.x == 2 and neighbor.y == 2:
                        print(f_cost)
                elif g_cost < g_cost_dict[neighbor]:
                    print("YOOOOOOOOOOOOOOOOOOOOOOOOOOo")
                    # This path is better, update the priority queue
                    priority_queue.put(PrioritizedItem(priority=f_cost,h_score=h_cost, item=neighbor))
                    g_cost_dict[neighbor] = g_cost
                    parentDict[neighbor] = current
                    visited.add(neighbor)


                """
                if neighbor not in visited:# and neighbor not in priority_queue.queue:
                    g_cost[neighbor] = g_cost[current] + 1
                    print(g_cost[neighbor], g_cost[neighbor])
                    priority = self.manhattan_dist(neighbor, self.finishTile) + g_cost[neighbor]
                    
                    priority_queue.put(PrioritizedItem(priority=priority,item=neighbor))
                    #visited.add(neighbor)
                    parentDict[neighbor] = current"""

        return None
    
    def runVisualization(self):
        """Starts visualisation according to selected alg"""
        if self.selectedAlgo == "BFS":
            return self.BFS()
        elif self.selectedAlgo == "A*":
            return self.aStar()
        elif self.selectedAlgo == "DFS":
            return self.DFS()
        elif self.selectedAlgo == "greedy":
            return self.greedy_BeFS()

    def drawGrid(self,surf):  
        surf.fill(self.bgColor)

        for i in self.gridLinesDistribution:
            pygame.draw.line(surf, (74,56,14), (0, i),(settings.widthGrid ,i))
            pygame.draw.line(surf, (74,56,14), (i, 0), (i, settings.heightGrid))
    
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

        self.startTile = self.grid[0][0]
        self.finishTile = self.grid[settings.sideLenght-1][settings.sideLenght-1]

        self.drawTileOntoSurface(0,0)
        self.drawTileOntoSurface(settings.sideLenght-1, settings.sideLenght-1)