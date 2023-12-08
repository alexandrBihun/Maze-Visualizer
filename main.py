import pygame
import sys
import settings
from vizualizator import Vizualizator


class AppMain:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(settings.screen_size)
        self.clock = pygame.time.Clock()
        self.vizualizator = Vizualizator(self)

    """def new_game(self):
        self.tic_tac_toe = Vizualizator(self)"""

    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
                    #self.new_game()
            self.vizualizator.handleEvents(event)


    def run(self):
        while True:
            self.vizualizator.run()
            self.check_for_events()
            pygame.display.flip()
            self.clock.tick(60)



if __name__ == '__main__':
    app = AppMain()
    app.run()