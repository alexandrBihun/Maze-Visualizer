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
from timeit import default_timer as timer

def timer_func(func):
    def wrapper(*args, **kwargs):
        t1 = timer()
        result = func(*args, **kwargs)
        t2 = timer()
        print(f'{func.__name__}() executed in {(t2-t1):.6f}s')
        return result
    return wrapper

class Vizualizator():
    def __init__(self, main) -> None:
        self.main = main
        self.grid: list[list[Tile]] = []
        self.sidebar = Sidebar()
        
        self.font = pygame.font.SysFont('Verdana' , 100, True)
        self.bgColor = settings.background_colour
        self.gridLinesDistribution = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLenght)) for i in range(settings.sideLenght+1)]

        self.drawGrid(self.main.screen)
        self.initGrid()
        self.redrawVisited()

        self.toRedraw = True
        self.tool = "wallBrush"
        self.drawedCells = []
        self.selectedAlgo = "DFS"
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
                tile.colour = settings.wall_colour
        x,y = random.randint(0,settings.sideLenght-1),random.randint(0,settings.sideLenght-1)
        self.grid[x][y].isWall = False
        self.grid[x][y].colour = settings.empty_colour

        frontierDict = dict()
        print("first:",self.grid[x][y],"\n")
        frontiers = get_frontiers(self.grid[x][y])
        for f in frontiers:
            frontierDict[f] = self.grid[x][y]
        
        while len(frontiers):
            
            #uncomment for maze-gen visualization:
            #for column in self.grid:
            #    for tile in column:
            #        self.drawTileOntoSurface(tile)
            #pygame.display.flip()
            

            randomTile = frontiers.pop(random.randint(0,len(frontiers)-1))
            randomTile.colour = settings.empty_colour
            randomTile.isWall = False

            fatherOfRandomTile = frontierDict[randomTile]

            middleTile = self.grid[(randomTile.x+fatherOfRandomTile.x)//2][(randomTile.y+fatherOfRandomTile.y)//2] ## middle of two points formula
            middleTile.isWall = False
            middleTile.colour = settings.empty_colour
            
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
                        tile.colour = settings.start_colour
                        startFound = True 
                        self.startTile = tile
                    lastTile = tile
                self.drawTileOntoSurface(tile)

        self.finishTile = lastTile
        lastTile.colour = settings.finish_colour
        lastTile.isFinish = True
        self.drawTileOntoSurface(lastTile)
                
    def drawTileOntoSurface(self, tile):
        tile.drawSelf(self.main.screen)

    def redrawVisited(self): 
        for column in self.grid:
            for tile in column:
                if not tile.isStart and not tile.isFinish and not tile.isWall:  
                    tile.colour = settings.empty_colour
                    self.drawTileOntoSurface(tile)
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
                        self.drawTileOntoSurface(self.startTile)
                        self.startTile = self.grid[x][y]
                        self.drawTileOntoSurface(self.startTile)

            elif self.tool == "selectFinish":
                if pygame.mouse.get_pressed()[0]:
                    x,y, self.toRedraw = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells, finish = True, currStartOrEndPos= self.finishTile.get_pos())
                    if self.toRedraw:
                        self.drawTileOntoSurface(self.finishTile)
                        self.finishTile = self.grid[x][y]
                        self.drawTileOntoSurface(self.finishTile)

            elif self.tool == "wallBrush":
                result = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells)
                if len(result)>2 and result[2]:
                    self.toRedraw = result[2]
                    if len(self.drawedCells)>0:
                        self.drawTileOntoSurface(self.grid[result[0]][result[1]])
                            
        elif event.type == pygame.MOUSEMOTION:
            if self.tool == "wallBrush" and pygame.mouse.get_pressed()[0]:
                result = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells)
                if len(result)>2 and result[2]:
                    self.toRedraw = result[2]
                    if len(self.drawedCells)>0:
                        self.drawTileOntoSurface(self.grid[result[0]][result[1]])
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
                self.Alg_check_events()
                curr.colour = settings.path_colour
                self.drawTileOntoSurface(curr)
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
    
    @timer_func
    def DFS(self):  
        stack = [self.startTile]
        visited = set()
        parentDict = dict()
        parentDict[self.startTile] = None

        while stack:
            self.Alg_check_events()
                
            current = stack.pop()
            if current != self.startTile and current != self.finishTile:
                current.colour = settings.visited_colour
                self.drawTileOntoSurface(current)
    
            pygame.display.flip()
            pygame.time.delay(self.visualDelay)

            if current == self.finishTile:
                return parentDict

            if current not in visited:
                visited.add(current)

                # add neighbors to the stack
                for neighbor in self.get_neighbours(current):
                    if neighbor not in visited and neighbor not in stack:
                        if neighbor != self.startTile and neighbor != self.finishTile:
                            neighbor.colour = settings.in_frontier_colour
                            self.drawTileOntoSurface(neighbor)
                        stack.append(neighbor)
                        parentDict[neighbor] = current
                
        return None
    
    @timer_func
    def BFS(self):
        visited = set()
        queue = deque()
        queue.appendleft(self.startTile)
        parentDict = dict()
        parentDict[self.startTile] = None

        visited.add(self.startTile)
        while queue:
            self.Alg_check_events()
            current = queue.pop()
            
            if current == self.finishTile:
                return parentDict

            if current != self.startTile:
                current.colour = settings.visited_colour
                self.drawTileOntoSurface(current)
                pygame.display.flip()
                pygame.time.delay(self.visualDelay)

            for neighbor in self.get_neighbours(current):
                if neighbor not in visited:
                    if neighbor != self.startTile and neighbor != self.finishTile:
                        neighbor.colour = settings.in_frontier_colour
                        self.drawTileOntoSurface(neighbor)
                        
                    queue.appendleft(neighbor)
                    parentDict[neighbor] = current
                    visited.add(neighbor)

        return None

    @timer_func
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
                return parentDict

            if current != self.startTile:
                current.colour = settings.visited_colour
                self.drawTileOntoSurface(current)
                pygame.display.flip()
                pygame.time.delay(self.visualDelay)

            for neighbor in self.get_neighbours(current):
                if neighbor not in visited:
                    if neighbor != self.startTile and neighbor != self.finishTile:
                        neighbor.colour = settings.in_frontier_colour
                        self.drawTileOntoSurface(neighbor)
                    priority = self.manhattan_dist(neighbor, self.finishTile)
                    priority_queue.put(PrioritizedItem(priority=priority,item=neighbor))
                    visited.add(neighbor)
                    parentDict[neighbor] = current

        return None

    @timer_func
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
        redrawedCurr = False
        while not priority_queue.empty():
            self.Alg_check_events()
            current = priority_queue.get().item
            
            if current == self.finishTile:
                print("found A*")
                return parentDict

            if current != self.startTile and current.colour!= settings.visited_colour:
                redrawedCurr = True
                current.colour = settings.visited_colour
                self.drawTileOntoSurface(current)
                

            for neighbor in self.get_neighbours(current):
                g_cost = g_cost_dict[current] + 1
                h_cost= self.manhattan_dist(neighbor, self.finishTile)
                f_cost = g_cost + h_cost

                if neighbor not in visited:
                    if neighbor != self.startTile and neighbor != self.finishTile:
                        neighbor.colour = settings.in_frontier_colour
                        self.drawTileOntoSurface(neighbor)
                    priority_queue.put(PrioritizedItem(priority=f_cost,h_score=h_cost, item=neighbor))
                    g_cost_dict[neighbor] = g_cost
                    parentDict[neighbor] = current
                    visited.add(neighbor)
                    if neighbor.x == 2 and neighbor.y == 2:
                        print(f_cost)
                elif g_cost < g_cost_dict[neighbor]:
                    # This path is better, update the priority queue
                    priority_queue.put(PrioritizedItem(priority=f_cost,h_score=h_cost, item=neighbor))
                    g_cost_dict[neighbor] = g_cost
                    parentDict[neighbor] = current
                    visited.add(neighbor)
            if redrawedCurr:
                pygame.display.flip()
                pygame.time.delay(self.visualDelay)
                redrawedCurr = False
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
                t = Tile(i,j,settings.empty_colour)
                column_list.append(t)
            self.grid.append(column_list)
        
        self.grid[0][0].colour = settings.start_colour
        self.grid[0][0].isStart = True
        self.grid[settings.sideLenght-1][settings.sideLenght-1].colour = settings.finish_colour
        self.grid[settings.sideLenght-1][settings.sideLenght-1].isFinish = True

        self.startTile = self.grid[0][0]
        self.finishTile = self.grid[settings.sideLenght-1][settings.sideLenght-1]

        self.drawTileOntoSurface(self.startTile)
        self.drawTileOntoSurface(self.finishTile)