# Import necessary modules
from sidebar import Sidebar
from tile import Tile
from tools import Tools
import settings
import random
import pygame
from collections import deque
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
import sys
from timeit import default_timer as timer

import colorsys

def timer_func(func):
    """Decorator for measuring running time of a function, source: https://www.python-engineer.com/posts/measure-elapsed-time/"""

    def wrapper(*args, **kwargs):
        t1 = timer()
        result = func(*args, **kwargs)
        t2 = timer()
        print(f"{func.__name__}() executed in {(t2-t1):.6f}s")
        return result

    return wrapper

# Main class for visualization
class Vizualizator:
    @timer_func
    def __init__(self, main) -> None:
        # Initialization method for the Vizualizator class.
        # Takes a 'main' parameter, which is expected to be an instance of the main application.
        self.main = main
        self.grid: list[list[Tile]] = []  # 2D list to represent the grid of tiles
        self.font = pygame.font.SysFont("Verdana", 18, True)

        self.gridLinesDistribution = [
            round(i * (settings.widthGrid ) / (settings.sideLength))
            for i in range(settings.sideLength + 1)
        ]

        # Draw the initial grid and set up initial state
        self.main.screen.fill(settings.background_colour)
        self.drawGrid()
        self.initGrid()
        self.redrawVisited()
        
        self.sidebar = Sidebar(self, self.main.screen, "DFS", self.font)  # Sidebar for UI
        self.toRedraw = True  # Flag to check whether the screen needs redrawing
        self.tool = "wallBrush"  # Initial tool selected
        self.drawnTiles = []  # List to store tiles drawn during wallBrush operation
        self.selectedAlgo = "DFS"  # Initial algorithm selected
        self.visualDelay = 5 # Visualization delay (in milliseconds)
        self.numberOfTilesPerFrame = 1 # Number of tiles to visualize per frame
        self.coloredSearch = False # Flag for colourful search
        self.colored_search_fisrt_colour = (255,0,0) 

    def generateMaze(self):
        """Generates a maze using Prim's randomized algorithm. Source: https://www.youtube.com/watch?v=cQVH4gcb3O4"""
        
        def get_frontiers(tile):
            """Helper function to get frontiers of a tile"""
            frontiers = []

            if tile.x > 1:
                if self.grid[tile.x - 2][tile.y].isWall == True:
                    frontiers.append(self.grid[tile.x - 2][tile.y])

            if tile.x < settings.sideLength - 2:
                if self.grid[tile.x + 2][tile.y].isWall == True:
                    frontiers.append(self.grid[tile.x + 2][tile.y])

            if tile.y > 1:
                if self.grid[tile.x][tile.y - 2].isWall == True:
                    frontiers.append(self.grid[tile.x][tile.y - 2])

            if tile.y < settings.sideLength - 2:
                if self.grid[tile.x][tile.y + 2].isWall == True:
                    frontiers.append(self.grid[tile.x][tile.y + 2])

            return frontiers

        # Set all tiles to walls initially
        for column in self.grid:
            for tile in column:
                tile.isWall = True
                tile.isStart = False
                tile.isGoal = False
                tile.colour = settings.wall_colour

        # Set a random starting point and mark it as an empty tile
        x, y = random.randint(0, settings.sideLength - 1), random.randint(
            0, settings.sideLength - 1
        )
        self.grid[x][y].isWall = False
        self.grid[x][y].colour = settings.empty_colour

        # Initialize data structures for maze generation
        frontierDict = dict()
        frontiers = get_frontiers(self.grid[x][y])
        for f in frontiers:
            frontierDict[f] = self.grid[x][y]

        # Continue until there are no more frontiers
        while len(frontiers):

            #Uncomment for maze-gen visualization:
            #for column in self.grid:
            #    for tile in column:
            #        tile.drawSelf(self.main.screen)
            #pygame.display.flip()

            randomTile = frontiers.pop(random.randint(0, len(frontiers) - 1))
            randomTile.colour = settings.empty_colour
            randomTile.isWall = False

            fatherOfRandomTile = frontierDict[randomTile]

            middleTile = self.grid[(randomTile.x + fatherOfRandomTile.x) // 2][(randomTile.y + fatherOfRandomTile.y) // 2]  # Middle of two points formula
            middleTile.isWall = False
            middleTile.colour = settings.empty_colour

            newFrontiers = get_frontiers(randomTile)
            for f in newFrontiers:
                frontierDict[f] = randomTile
            frontiers.extend(newFrontiers)

        # Set start and goal points in the generated maze
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
                tile.drawSelf(self.main.screen)

        self.goalTile = lastTile
        lastTile.colour = settings.goal_colour
        lastTile.isGoal = True
        lastTile.drawSelf(self.main.screen)

    def redrawVisited(self, redrawAll = False):
        """Redraw all tiles visited during visualisation. If redrawAll is True, redraws all tiles"""
        if redrawAll:
            for column in self.grid:
                for tile in column:
                    tile.drawSelf(self.main.screen)
            pygame.display.flip()
        else:
            for column in self.grid:
                for tile in column:
                    if not tile.isStart and not tile.isGoal and not tile.isWall:
                        tile.colour = settings.empty_colour
                        tile.drawSelf(self.main.screen)
            pygame.display.flip()

    def space_pressed(self):
        """Handle for space key press to visualize the selected algorithm."""
        self.redrawVisited()
        path, found = self.runVisualization()
        self.visualizePath(path, found)

    def handleEvents(self, event):
        """Handle various events like mouse clicks, key presses, etc."""
        self.sidebar.handle_events(event)

        if event.type == pygame.MOUSEBUTTONUP:
            self.drawnTiles = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Handle different tools (selectStart, selectGoal, wallBrush)
            if self.tool == "selectStart":
                if pygame.mouse.get_pressed()[0]:
                    x, y, self.toRedraw = Tools.setEndPoints(
                        pygame.mouse.get_pos(),
                        self.grid,
                        self.startTile.get_pos(),
                        start=True
                    )
                    if self.toRedraw:
                        self.startTile.drawSelf(self.main.screen)
                        self.startTile = self.grid[x][y]
                        self.startTile.drawSelf(self.main.screen)

            elif self.tool == "selectGoal":
                if pygame.mouse.get_pressed()[0]:
                    x, y, self.toRedraw = Tools.setEndPoints(
                        pygame.mouse.get_pos(),
                        self.grid,
                        self.goalTile.get_pos(),
                        goal=True
                    )
                    if self.toRedraw:
                        self.goalTile.drawSelf(self.main.screen)
                        self.goalTile = self.grid[x][y]
                        self.goalTile.drawSelf(self.main.screen)

            elif self.tool == "wallBrush":
                result = Tools.setWall(
                    pygame.mouse.get_pos(), self.grid, self.drawnTiles
                )
                if result != None:
                    result.drawSelf(self.main.screen)
                self.toRedraw = True

        elif event.type == pygame.MOUSEMOTION:
            # Handle wallBrush tool during mouse motion
            if self.tool == "wallBrush" and pygame.mouse.get_pressed()[0]:
                result = Tools.setWallCurve(
                    event.pos, self.grid, self.drawnTiles, event.rel
                )
                self.toRedraw = True
                for c in result:
                    c.drawSelf(self.main.screen)
            else:
                self.drawnTiles = []

        if event.type == pygame.KEYDOWN:
            # Handle key presses for different actions
            if event.key == pygame.K_s:
                self.tool = "selectStart"
            if event.key == pygame.K_f:
                self.tool = "selectGoal"
            if event.key == pygame.K_d:
                self.tool = "wallBrush"
            if event.key == pygame.K_1:
                self.selectedAlgo = "DFS"
                self.sidebar.set_selected_algo("DFS")
            if event.key == pygame.K_2:
                self.selectedAlgo = "BFS"
                self.sidebar.set_selected_algo("BFS")
            if event.key == pygame.K_3:
                self.selectedAlgo = "Greedy Best First Search"
                self.sidebar.set_selected_algo("Greedy Best First Search")
            if event.key == pygame.K_4:
                self.selectedAlgo = "A*"
                self.sidebar.set_selected_algo("A*")
            if event.key == pygame.K_SPACE:
                self.space_pressed()
            if event.key == pygame.K_c:
                self.redrawVisited()
            if event.key == pygame.K_g:
                self.generateMaze()
                pygame.display.flip()
            if event.key == pygame.K_i:
                self.coloredSearch = not self.coloredSearch
            self.changeVisualizationSpeed(event)

    def visualizePath(self, path: dict, found):
        """Visualizes path, path is a parentDict"""
        if found:
            curr = self.goalTile
            i = 0
            while curr != None:
                #Count path length and recursively recreate path
                if not curr.isStart and not curr.isGoal:
                    self.Alg_check_events()
                    if self.coloredSearch:
                        curr.colour = (127,98,45) # a colour that clearly stands out when the colourful visualization is used
                    else: curr.colour = settings.path_colour
                    curr.drawSelf(self.main.screen)
                    if i % self.numberOfTilesPerFrame == 0:
                        pygame.display.flip()
                        pygame.time.delay(self.visualDelay)
                i += 1
                curr = path[curr]
            print(f"Path len: {i}")
            self.sidebar.print_path_len(i)
        else:
            self.sidebar.print_path_len(None)
        i = 0
        for key in path.keys():
            #Count number of visited tiles
            if key.colour != settings.in_frontier_colour:
                i += 1
        self.sidebar.print_num_visited_tiles(i)

    def changeVisualizationSpeed(self,event):
        """Dynamically changes visualization speed on keyboard input"""
        if event.key == pygame.K_UP:
            if self.numberOfTilesPerFrame == 1:
                self.visualDelay += 3
            else:
                #The slower the visualitaion is, the lower the speed decrease
                self.numberOfTilesPerFrame -= int(max(1, self.numberOfTilesPerFrame / 10))
            print(
                "delay:",
                self.visualDelay,
                "tilesPerFrame:",
                self.numberOfTilesPerFrame,
            )
        if event.key == pygame.K_DOWN:
            if self.visualDelay == 0:
                #The faster the visualitaion is, the bigger the speed increase
                self.numberOfTilesPerFrame += int(max(1, self.numberOfTilesPerFrame / 10))
            else:
                self.visualDelay = max(0, self.visualDelay - 5)
            print(
                "delay:",
                self.visualDelay,
                "tilesPerFrame:",
                self.numberOfTilesPerFrame,
            )

    def Alg_check_events(self):
        """Event handler for any visualization function"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.changeVisualizationSpeed(event)
                
    def manhattan_dist(self, node, goal):
        """Manhattan distance heuristic."""
        return abs(node.x - goal.x) + abs(node.y - goal.y)
    
    def algo_visualize(self,i):
        """Helper function that visualizes any algorithm according to visualization speed"""
        if self.numberOfTilesPerFrame > 1:
            if i % self.numberOfTilesPerFrame == 0:
                pygame.display.flip()
        else:
            pygame.display.flip()
            pygame.time.delay(self.visualDelay)
        return i + 1
    
    def color_shift(self, rgb):
        """Returns a slightly shifted color for creating the colour gradient effect"""
        (h, s, v) = colorsys.rgb_to_hsv(*(i / 255.0 for i in rgb))

        h = (h + 0.005) % 1
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    
    def setCurrsColour(self, current, parentDict):
        """Sets new color to current"""
        if self.coloredSearch:
            if current == self.startTile:
                pass
            elif parentDict[current] == self.startTile:
                current.colour =  self.colored_search_fisrt_colour
                current.drawSelf(self.main.screen)
            else:
                tmp_col = parentDict[current].colour
                tmp_col = self.color_shift(tmp_col)
                current.colour = tmp_col
                current.drawSelf(self.main.screen)
        elif current != self.startTile:
            current.colour = settings.visited_colour
            current.drawSelf(self.main.screen)
        
    @timer_func
    def BFS(self):
        """Breadth First Search"""
        visited = set()
        queue = deque()
        queue.appendleft(self.startTile)
        parentDict = dict()
        parentDict[self.startTile] = None
        visited.add(self.startTile)
        i = 0 # Iteration counter
        while queue:
            self.Alg_check_events()
            current = queue.pop()
            
            if current == self.goalTile:
                return parentDict, True

            self.setCurrsColour(current, parentDict)

            # Enqueue neighbors
            for neighbor in current.get_neighbours(self.grid):
                if neighbor not in visited:
                    if neighbor != self.startTile and neighbor != self.goalTile:
                        neighbor.colour = settings.in_frontier_colour
                        neighbor.drawSelf(self.main.screen)
                        
                    queue.appendleft(neighbor)
                    parentDict[neighbor] = current
                    visited.add(neighbor)
                    
            # Update the screen with newly drawn tiles based on visualization speed
            i = self.algo_visualize(i)

        # If queue got emptied but goal was not found there is no path 
        return parentDict, False

    @timer_func
    def DFS(self):
        """Depth First Search"""
        visited = set()
        stack = [self.startTile]
        parentDict = dict()
        parentDict[self.startTile] = None
        visited.add(self.startTile)
        i = 0 # Iteration counter
        while stack:
            self.Alg_check_events()
            current = stack.pop()

            if current == self.goalTile:
                return parentDict, True

            self.setCurrsColour(current, parentDict)

            # Add neighbors to the stack
            for neighbor in current.get_neighbours(self.grid):
                if neighbor not in visited:
                    if neighbor != self.startTile and neighbor != self.goalTile:
                        neighbor.colour = settings.in_frontier_colour
                        neighbor.drawSelf(self.main.screen)

                    stack.append(neighbor)
                    parentDict[neighbor] = current
                    visited.add(neighbor)

            # Update the screen with newly drawn tiles based on visualization speed
            i = self.algo_visualize(i)

        # If stack got emptied but goal was not found there is no path 
        return parentDict, False

    @timer_func
    def greedy_BeFS(self):
        """Greedy Best First Search"""

        # Define priority queue item as (heuristic, node) tuple
        @dataclass(order=True)
        class PrioritizedItem: 
            priority: int
            item: Any = field(compare=False)

        visited = set()
        priority_queue = PriorityQueue() 
        priority_queue.put(PrioritizedItem(priority=0, item=self.startTile)) 

        parentDict = dict()
        parentDict[self.startTile] = None
        visited.add(self.startTile)
        i = 0 # Iteration counter
        while not priority_queue.empty():
            self.Alg_check_events()
            current = priority_queue.get().item

            if current == self.goalTile:
                return parentDict, True

            self.setCurrsColour(current, parentDict)

            # Add neighbors to priority queue
            for neighbor in current.get_neighbours(self.grid):
                if neighbor not in visited:
                    if neighbor != self.startTile and neighbor != self.goalTile:
                        neighbor.colour = settings.in_frontier_colour
                        neighbor.drawSelf(self.main.screen)

                    priority = self.manhattan_dist(neighbor, self.goalTile)
                    priority_queue.put(PrioritizedItem(priority=priority, item=neighbor))
                    parentDict[neighbor] = current
                    visited.add(neighbor)

            # Update the screen with newly drawn tiles based on visualization speed
            i = self.algo_visualize(i)

        # If priority queue got emptied but goal was not found there is no path
        return parentDict, False

    @timer_func
    def aStar(self):
        """A* algorithm"""

        # Define priority queue item as (heuristic, h_score, node) tuple
        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            h_score: int # Often there are many nodes with the same priority in Priority Q.;breaking ties on lower h results in A* expanding to get closer to the goal ASAP while maintaining optimality  
            item: Any = field(compare=False)

        visited = set()
        priority_queue = PriorityQueue()
        f_score_start = self.manhattan_dist(self.startTile, self.goalTile)
        priority_queue.put(PrioritizedItem(priority=0, h_score=f_score_start, item=self.startTile))

        parentDict = dict()
        parentDict[self.startTile] = None
        visited.add(self.startTile)
        closed = set()
        g_cost_dict = dict()
        g_cost_dict[self.startTile] = 0
        i = 0 # Iteration counter
        while not priority_queue.empty():
            self.Alg_check_events()
            current = priority_queue.get().item
            if current not in closed: 

                if current == self.goalTile:
                    return parentDict, True
                
                self.setCurrsColour(current, parentDict)

                #Add neighbors to priority queue
                for neighbor in current.get_neighbours(self.grid):
                    g_cost = g_cost_dict[current] + 1 # Setting g_cost to be always 0 would turn A* into Greedy best first search
                    h_cost = self.manhattan_dist(neighbor, self.goalTile) # Setting h_cost to be always 0 would turn A* into Uniform Cost Search
                    f_cost = g_cost + h_cost

                    if neighbor not in visited:
                        if neighbor != self.startTile and neighbor != self.goalTile:
                            neighbor.colour = settings.in_frontier_colour
                            neighbor.drawSelf(self.main.screen)
                            
                        priority_queue.put(PrioritizedItem(priority=f_cost, h_score=h_cost, item=neighbor))
                        g_cost_dict[neighbor] = g_cost
                        parentDict[neighbor] = current
                        visited.add(neighbor)

                    elif g_cost < g_cost_dict[neighbor]:
                        # This path is better than the old one (better g cost), update the priority queue; leaves old item with worse priorty in PQ, that gets resolved by closed list
                        priority_queue.put(PrioritizedItem(priority=f_cost, h_score=h_cost, item=neighbor))
                        g_cost_dict[neighbor] = g_cost
                        parentDict[neighbor] = current
                
                #Update the screen with newly drawn tiles based on visualization speed
                i = self.algo_visualize(i)
                closed.add(current)

        # If priority queue got emptied but goal was not found there is no path
        return parentDict, False

    def runVisualization(self):
        """Starts visualisation according to selected algorithm"""
        if self.selectedAlgo == "BFS":
            return self.BFS()
        elif self.selectedAlgo == "A*":
            return self.aStar()
        elif self.selectedAlgo == "DFS":
            return self.DFS()
        elif self.selectedAlgo == "Greedy Best First Search":
            return self.greedy_BeFS()

    def drawGrid(self):
        """Draws grid, precisely grid lines."""
        surf = self.main.screen

        for i in self.gridLinesDistribution:
            pygame.draw.line(surf, settings.grid_lines, (0, i), (settings.widthGrid, i))
            pygame.draw.line(surf, settings.grid_lines, (i, 0), (i, settings.heightGrid))

    def run(self):
        """Main loop, redraws when necessary"""
        if self.toRedraw:
            pygame.display.flip()
            self.toRedraw = False

    def initGrid(self):
        """
        initiliziases grid: grid is a list of column_lists, indexed into as [x][y], x grows from left to right, y top to bot
        """
        for i in range(settings.sideLength):
            column_list = []  # List of all tiles in a single Column
            for j in range(settings.sideLength):
                t = Tile(i, j, settings.empty_colour)
                column_list.append(t)
            self.grid.append(column_list)

        self.grid[0][0].colour = settings.start_colour
        self.grid[0][0].isStart = True
        self.grid[settings.sideLength - 1][settings.sideLength - 1].colour = settings.goal_colour
        self.grid[settings.sideLength - 1][settings.sideLength - 1].isGoal = True
        self.startTile = self.grid[0][0]
        self.goalTile = self.grid[settings.sideLength - 1][settings.sideLength - 1]

        self.startTile.drawSelf(self.main.screen)
        self.goalTile.drawSelf(self.main.screen)
