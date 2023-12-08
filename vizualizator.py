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
        self.initGrid()

        self.font = pygame.font.SysFont('Verdana' , 100, True)
        self.bgColor = ("light gray")

        self.toRedraw = True
        self.tool = "wallBrush"
        self.result = [round(0 + i * (settings.widthGrid - 0) / (settings.sideLenght)) for i in range(settings.sideLenght+1)]

        self.drawedCells = []

    def handleEvents(self,event):
        self.sidebar.handle_events(event)

    def drawGrid(self):
        self.main.screen.fill(self.bgColor)

        for i in self.result:
            pygame.draw.line(self.main.screen, (182,187,196), (0, i),(settings.widthGrid ,i))
            pygame.draw.line(self.main.screen, (182,187,196), (i, 0), (i, settings.heightGrid))

    def drawWall(self, x,y):
        pygame.draw.rect(self.main.screen,"black",rect=(self.result[x],self.result[y], self.result[x+1] - self.result[x] , self.result[y+1] - self.result[y]))

    def drawObjects(self):
        for column in self.grid:
            for cell in column:
                if cell.isWall == True:
                    self.drawWall(cell.x,cell.y)

    def draw(self):
        self.drawGrid()
        self.drawObjects()
        
    
    def run_processes(self):
        if self.tool == "wallBrush":
            if pygame.mouse.get_pressed()[0]:
                self.toRedraw = Tools.drawWall(pygame.mouse.get_pos(),self.grid,self.drawedCells) ##edits grid object and unnecessarily invokes redrawing of entire grid for every painted cell 
            else:
                self.drawedCells = []

    def run(self):
        if self.toRedraw:
            print("drawing")
            self.draw()
            self.toRedraw = False
        self.run_processes()

            
    def initGrid(self):
        """
        initiliziases grid: grid is a list of column_lists, indexed into as [x][y], x grows from left to right, y top to bot
        """
        for i in range(settings.sideLenght):
            column_list = []#list of all tiles in a single Column
            for j in range(settings.sideLenght):
                t = Tile(i,j)
                column_list.append(t)
            self.grid.append(column_list)