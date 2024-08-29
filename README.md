# Maze Visualizer
Maze-visualizer je aplikace, kterou jsem napsal jako praktickou část pro mojí maturitní práci. Je napsaná v Pythonu s knihovnou Pygame. Účelem tohoto projektu je interaktivní a zábavnou formou pomoci porozumět nejznámějším pathfinding algoritmům.

### Požadavky:
* knihovna Pygame: `pip install pygame`
* Python 3.10 a výš: Stáhněte na oficiální stránce Pythonu (https://www.python.org/downloads/).

### Spouštění:
Spusťte: `python3 main.py` v adresáři s projektem


### Ovládání:
Ovládá se klávesnicí:
- Tlačítky 1, 2, 3, 4 se mění vybraný algoritmus (DFS, BFS, Greedy Best First Search, A*)
- Mezerník spustí vizualizaci
- 'g' vygeneruje bludiště
- 's' vybere nástroj pro vybírání startu
- 'f' vybere nástroj pro vybírání cíle
- 'd' vybere nástroj pro kreslení a gumování stěn
- 'c' smaže políčka vybarvená dokončenou vizualizací
- 'i' zapne/vypne barevný mód vizualizace
- 'r' restartuje celou aplikaci
- '↑' zpomalí vizualizaci
- '↓' zrychlí vizualizaci 

Některé funkce se dají ovládat i pomocí UI tlačítek.

V souboru settings.py lze upravovat pokročilé možnosti, zejména počet vykreslovaných políček.

# Maze Visualizer - EN
Maze-visualizer is an application I developed as a practical part of my graduation project. It is written in Python using the Pygame library. The purpose of this project is to help users understand the most well-known pathfinding algorithms in an interactive and engaging way.

### Requirements:
* Pygame library: `pip install pygame`
* Python 3.10 or higher: Download it from the official Python website (https://www.python.org/downloads/).

### Running the Application:
Run: `python3 main.py` in the project directory.

### Controls:
The application is controlled using the keyboard:
- Keys 1, 2, 3, 4 switch between the selected algorithm (DFS, BFS, Greedy Best First Search, A*)
- Spacebar starts the visualization
- 'g' generates a maze
- 's' selects the tool for setting the start point
- 'f' selects the tool for setting the endpoint
- 'd' selects the tool for drawing and erasing walls
- 'c' clears the cells colored by the completed visualization
- 'i' toggles the color mode of the visualization on or off
- 'r' restarts the entire application
- '↑' slows down the visualization
- '↓' speeds up the visualization

Some features can also be controlled via UI buttons.

Advanced options, such as the number of rendered cells, can be adjusted in the settings.py file.
