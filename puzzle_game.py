'''
Omar Rashwan
CS 5001, Fall 2021
Project - Shuffle Puzzle
'''

import random
import turtle
import os.path
from os import listdir
from Tile import Tile
from puzzle_gui import *
from error_logger import error_handler

DEFAULT_PUZ = "mario.puz"
# the default puz file

VALID_GRIDS = (4, 9, 16)
# a tuple containing valid grid sizes

MIN_SIZE = 50
MAX_SIZE = 110
# minimum and maximum tile size

def load_puzzle(puzzle_file):
    '''
    Loads a puz file into two dictionaries, puzzle_data and tiles. puzzle_data
    contains the metadata for the puzzle (name, thumbnail, number, size, and
    the blank tile ID), tiles contains the tiles and their image filepaths.
    '''
    puzzle_data = {}
    tiles = {}
    with open(puzzle_file, mode='r') as puzzle:
        for line in puzzle:
            line = line.split()
            
            if line[0] == "name:" or line[0] == "thumbnail:":
                puzzle_data[line[0][0:-1]] = line[1]
            elif line[0] == "number:" or line[0] == "size:":
                puzzle_data[line[0][0:-1]] = int(line[1])
            else:
                tiles[int(line[0][0:-1])] = line[1]
                
            if 'blank' in line[1]:
                puzzle_data['blank'] = int(line[0][0:-1])
                
    return puzzle_data, tiles

def check_valid_puz(puzzle_file):
    '''
    Checks to see if a puz file exists, and if it does exists, checks to see
    that it is within the constraints of the game and is not malformed.
    '''
    if os.path.exists(puzzle_file) == False:
        return False
    
    puzzle_data, tiles = load_puzzle(puzzle_file)
    if puzzle_data['number'] not in VALID_GRIDS:
        return False
    if puzzle_data['number'] != len(tiles):
        return False
    if puzzle_data['size'] < MIN_SIZE or puzzle_data['size'] > MAX_SIZE:
        return False
    for key in tiles:
        if os.path.exists(tiles[key]) == False:
            return False
    return True

def tile_objectification(tiles):
    # converts the tiles in the dictionary into objects of the Tile class
    for tile in tiles:
        row = int((tile - 1) // (len(tiles) ** 0.5))
        column = int((tile - 1) % (len(tiles) ** 0.5))
        tiles[tile] = Tile(tile, tiles[tile], row, column)
    return tiles

def grid_construct(size, tiles):
    # takes the tiles and places them into a nested list that emulates a grid
    size = int(size ** 0.5)
    grid = []
    for i in range(size):
        grid.append([])
    for i in range(len(tiles)):
        grid[i // size].append(tiles[i + 1])
    return grid

def index_find(grid, value):
    '''
    Finds the index of a value in nested lists; all values must be unique, else
    returns the index of the first instance of the value in the nested lists.
    '''
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].tileid == value:
                return i,j

def shuffle_grid(grid, blank):
    '''
    This shuffle algorithm finds the position of the blank tile in the grid,
    then swaps it with an adjacent tile for a default 100 times. This ensures
    that the puzzle has a solution, which isn't certain if shuffling randomly.
    '''
    size = int(len(grid) ** 2)
    i = 0
    SHUFFLE = 100

    while i < SHUFFLE:
        row, column = index_find(grid, blank)
        row_or_column = random.randint(1, 100) % 2

        if row_or_column == 0:
            new_row = row + random.randint(-1, 1)
            if new_row < len(grid) and new_row >= 0:
                grid[new_row][column], grid[row][column] = (
                 grid[row][column], grid[new_row][column])
                i += 1
        elif row_or_column == 1:
            new_column = column + random.randint(-1, 1)
            if new_column < len(grid) and new_column >= 0:
                grid[row][new_column], grid[row][column] = (
                 grid[row][column], grid[row][new_column])
                i += 1

def is_adjacent(tile_1, tile_2):
    # checks adjacency of two tiles in the same row or column, returns a bool
    if ((tile_1[0] == tile_2[0] - 1 or tile_1[0] == tile_2[0] + 1)
            and tile_1[1] == tile_2[1]):
        return True
    elif ((tile_1[1] == tile_2[1] - 1 or tile_1[1] == tile_2[1] + 1)
            and tile_1[0] == tile_2[0]):
        return True

    return False

def swap(tile_1, tile_2, grid):
    # swaps two tiles in both the grid and on the screen
    turtile_1 = grid[tile_1[0]][tile_1[1]].turtile
    turtile_2 = grid[tile_2[0]][tile_2[1]].turtile

    tile_1_pos = turtile_1.pos()
    tile_2_pos = turtile_2.pos()

    turtile_1.goto(tile_2_pos[0], tile_2_pos[1])
    turtile_2.goto(tile_1_pos[0], tile_1_pos[1])

    grid[tile_1[0]][tile_1[1]], grid[tile_2[0]][tile_2[1]] = (
        grid[tile_2[0]][tile_2[1]], grid[tile_1[0]][tile_1[1]])
        
def win_condition(grid):
    '''
    Checks that the position of all tiles within the grid are equal to their
    correct position according to the tile.row and tile.column attributes
    '''
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            tile = grid[i][j]
            if tile.row != i or tile.column != j:
                return False
    return True

def save_leaderboard(moves, name):
    # saves a winner's name and # of moves to the leaderboard.txt file
    leaderboard = []
    if os.path.exists('leaderboard.txt'):
        with open('leaderboard.txt', mode='r') as leaderboard_file:
            for entry in leaderboard_file:
                leaderboard.append(entry.strip())
    new_entry = f'{moves}: {name}'
    leaderboard.append(new_entry)
    leaderboard = sorted(leaderboard)

    with open('leaderboard.txt', mode='w') as leaderboard_file:
        for entry in leaderboard:
            leaderboard_file.write(entry + '\n')

def you_win(moves, name):
    # game logic function for a win
    win_message()
    save_leaderboard(moves, name)
    roll_credits()

def you_lose():
    # game logic function for a loss
    lose_message()
    roll_credits()

def reset_puzzle(grid):
    '''
    Resets the puzzle by using the swap function with correct tile positions,
    loops until all tiles are in the correct position according to the
    win_condition function
    '''
    while win_condition(grid) is not True:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                x, y = grid[i][j].row, grid[i][j].column
                swap((i, j), (x, y), grid)

def puzzle_scan():
    '''
    scans for .puz files in the same directory as the file, returns a list of
    puz files & a bool indicating if the list is too long to be displayed fully
    '''
    puzzles = []
    for file in listdir():
        if file[-4::] == '.puz':
            puzzles.append(file)

    toolong = len(puzzles) > 10

    puzzles = puzzles[:10]
    puzzles = '\n'.join(puzzles)
    
    return puzzles, toolong

def puzzle_game(puz, ui, name, max_moves):
    '''
    The core puzzle game function. Loads the puz file, then enters into a loop
    that takes clicks on tiles, and the ui elements. Nested functions handle
    clicks on a tile, reset, load, and quit.
    '''
    
    puzzle_info, tiles = load_puzzle(puz)
    size = puzzle_info["number"]
    tiles = tile_objectification(tiles)
    grid = grid_construct(size, tiles)
    shuffle_grid(grid, puzzle_info['blank'])
    place_tiles(grid, puzzle_info["size"])
    thumbnail(puzzle_info['thumbnail'], ui['thumbnail'])
    moves = 0
    
    def tile_click(x, y):
        '''
        Function for handling tile clicks, converts coordinates into grid
        placement then checks for adjacency to the blank tile. If adjacent, the
        tiles are swapped and moves are incremented by 1. The checks if max
        moves have been exceeded, elif checks win_condition.
        '''
        x_offset, y_offset = offset(size ** 0.5, puzzle_info["size"])
        j = int(round(((x - x_offset)
                       / (puzzle_info["size"] + TILE_SPACING)) - 1))
        i = int(round(((y - y_offset)
                       / -(puzzle_info["size"] + TILE_SPACING)) - 1))
        clicked_tile = i,j
        blank_tile = index_find(grid, puzzle_info['blank'])
        if is_adjacent(clicked_tile, blank_tile):
            swap(clicked_tile, blank_tile, grid)
            nonlocal moves
            moves += 1
            update_moves(moves, ui['moves'])
            if moves > max_moves:
                you_lose()
            elif win_condition(grid):
                you_win(moves, name)

    def reset(x, y):
        # click handler that resets the puzzle
        reset_puzzle(grid)

    def load_game(x, y):
        # click handler for loading a new puzzle
        puzzles, toolong = puzzle_scan()
        if toolong:
            file_warning()
        msg = 'Enter the name of the puzzle you wish to load. Choices are:\n'
        puz = s.textinput('Load Puzzle', f'{msg}{puzzles}')
        if puz is not None:
            if check_valid_puz(puz):
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        grid[i][j].turtile.clear()
                        grid[i][j].turtile.hideturtle()
                update_moves(0, ui['moves'])
                ui['thumbnail'].hideturtle()
                puzzle_game(puz, ui, name, max_moves)
            else:
                file_error()
                error_handler(1, 'puzzle_game.load_game()')
            
    
    def quit_game(x, y):
        # click handler for quitting the game
        quit_message()
        roll_credits()
            
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].turtile.onclick(tile_click)
    ui['reset'].onclick(reset)
    ui['quit'].onclick(quit_game)
    ui['load'].onclick(load_game)

def main():
    
    ui = window_setup()
    name = None
    while name == None:
        name = s.textinput('CS5001 Puzzle Slide - Name', 'Your Name:')
    max_moves = None
    while max_moves == None:
        max_moves = s.numinput('CS5001 Puzzle Slide - Moves', 'Enter the numb'+
                               'er of moves (chances) you want (5 - 200)',
                               minval=5, maxval=200)
    puzzle_game(DEFAULT_PUZ, ui, name, max_moves)


if __name__ == "__main__":
    main()
