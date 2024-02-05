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
- 'r' restartuje celou aplikaci
- '↑' zpomalí vizualizaci
- '↓' zrychlí vizualizaci 
Některé funkce se dají ovládat i pomocí UI tlačítek. 
V souboru settings.py lze upravovat pokročilé možnosti, zejména počet vykreslovaných políček.