'''
Omar Rashwan
CS 5001, Fall 2021
Project - Tile
'''

class Tile:
    '''
    A class for the tiles in the puzzle shuffle game.
    Attributes:
    tileid - The tile ID as entered in a .puz file
    image - the filepath to the image representing the tile
    row - the correct row placement of the tile within a grid
    column - the correct column placement of the tile within a grid
    turtile - the turtle representing the tile graphically
    '''
    def __init__(self, tileid, image, row, column, turtile=None):
        self.tileid = tileid
        self.image = image
        self.row = row
        self.column = column
        self.turtile = turtile
