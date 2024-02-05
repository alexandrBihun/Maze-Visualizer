# Import necessary modules
import pygame
import sys
import settings
from vizualizator import Vizualizator

# Main class for launching the entire application
class AppMain:
    def __init__(self) -> None:
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("Pathfinding Visualizator")

        # Set up the main screen
        self.screen = pygame.display.set_mode(settings.screen_size)
        
        # Create a clock object for controlling the frame rate
        self.clock = pygame.time.Clock()
        
        # Create a Vizualizator object to handle visualization
        self.vizualizator = Vizualizator(self)

    # Reset the visualization
    def reset(self):
        self.vizualizator = Vizualizator(self)

    # Check for user events
    def check_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the application if the window is closed
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Reset the visualization if the 'r' key is pressed
                if event.key == pygame.K_r:
                    self.reset()
            # Pass events to the Vizualizator for handling
            self.vizualizator.handleEvents(event)

    # Main application loop
    def run(self):
        while True:
            self.vizualizator.run()
            self.check_for_events()

            # Cap the frame rate at 60 frames per second
            self.clock.tick(60)

# Entry point of the script
if __name__ == '__main__':
    # Create an instance of AppMain and run the application
    app = AppMain()
    app.run()
