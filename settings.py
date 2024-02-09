sideLength = 50 #Number of tiles in the side — 300 is probably the maximum for a nice maze, feel free to experiment with sizes. 990 renders correctly, anything beyond that doesnt fit the pixels of the screen - the algorithms still work but some tiles are not displayed.
offset = 0  # For 0, the maze has no edges; for 1, normal edges; for i > 1, 'tile effect'.

#Settings for window size; the sidebar has hardcoded positions of UI elements => they may not render correctly when these settings change. If you have less than 1920x1080 resolution I recommend 
# setting widthGrid and heightGrid to 700
width_menu = 300
widthGrid = heightGrid = 990

#Setting of colors for individual types of tiles.
start_colour = "rosybrown2"
finish_colour = "lightslateblue"
path_colour = "yellow1"
visited_colour = (255,0,0)
in_frontier_colour = "olivedrab3"
wall_colour = (0,0,0)
empty_colour = "snow2"
background_colour = "light gray"
grid_lines = "gray17" 

screen_size = widthGrid+width_menu,heightGrid