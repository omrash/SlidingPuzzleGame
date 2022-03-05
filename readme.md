FILES:
puzzle_game.py
puzzle_gui.py
Tile.py
error_logger.py

I chose to separate the game logic and the graphical representation of the game into two distinct files. This was helpful in keeping the different functions that run the game organized, and allowed me to keep track of what aspect of the game I was working on at any given moment. The Tile class is its own file as per the CS5001 style guide. When I was implementing the error_logger, I felt that it would be better to keep it separate from game logic as it wasn't essential to how the game ran.


Notable data structure usage:
grid: a nested list meant to represent current tile placement on the screen. If a tile is moved graphically, it is also swapped within the grid.
puzzle_data: a dictionary that contains metadata regarding the tile.
ui: a dictionary that contains the ui elements as turtles.


The Tile class:
I chose to only use one class for this project, it seemed like using more wasn't really necessary. Each Tile object has five attributes: 
tileid - The tile ID as entered in a .puz file.
image - the filepath to the image representing the tile.
row - the correct row placement of the tile within a grid.
column - the correct column placement of the tile within a grid.
turtile - the turtle representing the tile graphically.

Since the grid data structure is representative of a tile's current position on the board, there is no need to store the current row or column as an attribute of the Tile object. I believe this is also a cleaner implementation as each swap does not change attributes, which can get difficult to track.
