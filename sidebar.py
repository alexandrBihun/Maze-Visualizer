# Import necessary modules
import settings
import pygame

# Define the Sidebar class
class Sidebar():
    def __init__(self, main, screen, selectedAlgo, font):
        # Initialize class attributes
        self.main = main
        self.screen = screen
        self.selectedAlgo = selectedAlgo
        self.font = font
        self.alg_choices = ["DFS", "BFS", "Greedy Best First Search", "A*"]
        
        # Initialize Text objects for displaying information
        self.texts = {
            0: Text("Selected algorithm:", "black", settings.widthGrid + 10, 50, font),
            1: Text(self.selectedAlgo, "black", settings.widthGrid + 10, 100, font),
        }

        # Initialize Button objects
        self.buttons = []
        button_surface = pygame.image.load("button1.png")
        button_surface = pygame.transform.scale(button_surface, (60, 60))
        self.switch_alg_button = Button(button_surface, settings.widthGrid + 10, 150)
        
        button_surface = pygame.image.load("run_button.png")
        button_surface = pygame.transform.scale(button_surface, (3 * 70, 3 * 30))
        self.run_button = Button(button_surface, settings.widthGrid + 45, 800)

        button_surface = pygame.image.load("toggle_grid_button.png")
        button_surface = pygame.transform.scale(button_surface, (3 * 70, 3 * 30))
        self.grid_lines_button = Button(button_surface, settings.widthGrid + 45, 700)
        self.buttons.extend((self.switch_alg_button, self.run_button,self.grid_lines_button))

        # Draw the initial state of the sidebar
        self.redraw_sidebar()

    # Display the length of the path found (or a message if no path is found)
    def print_path_len(self, i):
        if i == None:
            self.texts[2] = Text("No path found", "black", settings.widthGrid + 10, 230, self.font)
            self.redraw_sidebar()
        else:
            self.texts[2] = Text(f"Path found! Length: {i}", "black", settings.widthGrid + 10, 230, self.font)
            self.redraw_sidebar()

    # Display the number of visited tiles
    def print_num_visited_tiles(self, i):
        self.texts[3] = Text(f"N visited tiles: {i}", "black", settings.widthGrid + 10, 280, self.font)
        self.redraw_sidebar()

    # Set the selected algorithm and update the display
    def set_selected_algo(self, selectedAlgo):
        if selectedAlgo in self.alg_choices:
            self.texts[1].set_text(selectedAlgo)
            self.redraw_sidebar()
            self.selectedAlgo = selectedAlgo
            pygame.display.flip()
            self.main.selectedAlgo = self.selectedAlgo

    # Redraw the sidebar with updated information
    def redraw_sidebar(self):
        pygame.draw.rect(self.screen, settings.background_colour, (settings.widthGrid + 1, 0, settings.width_menu, settings.heightGrid))
        for b in self.buttons:
            b.update(self.screen)
        for t in self.texts.values():
            t.draw_text(self.screen)
        pygame.display.flip()

    # Handle mouse events for UI elements
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.switch_alg_button.checkForInput(pos):
                # Switch to the next algorithm in the list
                self.set_selected_algo(self.alg_choices[(self.alg_choices.index(self.selectedAlgo) + 1) % len(self.alg_choices)])
            if self.run_button.checkForInput(pos):
                # Trigger the main's space_pressed method
                self.main.space_pressed()
            if self.grid_lines_button.checkForInput(pos):
                # Toggle grid lines
                settings.offset = not settings.offset
                self.main.drawGrid()
                self.main.redrawVisited(True)
                self.redraw_sidebar()

# Define the Text class for displaying text on the screen
class Text():
    def __init__(self, text, text_col, x, y, font):
        self.x = x
        self.y = y
        self.text_col = text_col
        self.text = text
        self.font = font
        self.img = self.font.render(self.text, True, self.text_col)
        self.text_rect = self.img.get_rect()
        self.text_rect.topleft = (x, y)

    # Draw text on the screen
    def draw_text(self, screen):
        screen.blit(self.img, (self.x, self.y))

    # Set the text and update the image and rect
    def set_text(self, text):
        self.text = text
        self.img = self.font.render(self.text, True, self.text_col)
        self.text_rect = self.img.get_rect()
        self.text_rect.topleft = (self.x, self.y) 

    # Get the rect object of the text
    def get_text_rect(self):
        return self.text_rect

# Define the Button class for handling clickable buttons
class Button():
    def __init__(self, image, x_pos, y_pos):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos, y_pos)
    
    # Update the button on the screen
    def update(self, screen):
        screen.blit(self.image, self.rect)

    # Check if mouse position is within the button area
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
