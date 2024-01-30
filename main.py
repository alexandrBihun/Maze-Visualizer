import pygame
import sys
import settings
from vizualizator import Vizualizator


class AppMain:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Path Finding Visualizator")
        self.screen = pygame.display.set_mode(settings.screen_size)
        self.clock = pygame.time.Clock()
        self.vizualizator = Vizualizator(self)

    def reset(self):
        self.vizualizator = Vizualizator(self)

    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
            self.vizualizator.handleEvents(event)


    def run(self):
        while True:
            self.vizualizator.run()
            self.check_for_events()
            #pygame.display.flip() redundant
            self.clock.tick(60)



if __name__ == '__main__':
    app = AppMain()
    app.run()