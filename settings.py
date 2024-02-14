sideLength = 50 #Sets grid dimensions: grid size = sideLength x sideLength. 990 renders correctly, anything beyond that does not fit the pixels of the screen - the algorithms still work but some tiles will not get displayed.
offset = 0  # For 0, the maze has no edges; for 1, normal edges; for i > 1, 'tile effect'.

#Settings for window size; the sidebar has hardcoded positions of UI elements => they may not render correctly when these settings change. For resolutions less than 1920x1080 setting widthGrid and heightGrid to 700 should be adequate.
width_menu = 300
widthGrid = heightGrid = 990

#Setting of colors for individual types of tiles.
start_colour = "rosybrown2"
goal_colour = "lightslateblue"
path_colour = "yellow1"
visited_colour = (255,0,0)
in_frontier_colour = "olivedrab3"
wall_colour = (0,0,0)
empty_colour = "snow2"
background_colour = "light gray"
grid_lines = "gray17" 

screen_size = widthGrid+width_menu,heightGrid