sideLength = 50#Number of tiles in the 'edge' — 100 is probably the maximum for a nice maze, 500 takes a moment to load, and 800 freezes the PC.

#Settings for window size; the sidebar has hardcoded positions of UI elements => they may not render correctly when these settings change.
width_menu = 300
widthGrid, heightGrid = 990,990

#Setting of colors for individual types of tiles.
start_colour = "rosybrown2"
finish_colour = "lightslateblue"
path_colour = "yellow1"
visited_colour = (255,0,0)
in_frontier_colour = "olivedrab3"
wall_colour = (0,0,0)
empty_colour = "snow2"
background_colour = "light gray"

screen_size = widthGrid+width_menu,heightGrid