'''
Omar Rashwan
CS 5001, Fall 2021
Project - Puzzle GUI
'''

import turtle
import time
import os.path
from error_logger import error_handler

TILE_SPACING = 5
# pixels between each tile

t = turtle.Turtle()
s = turtle.Screen()

UI_BOX = (-375, -250, 375, -375)
LEADERBOARD_BOX = (375, -225, 225, 375)
GAMEBOARD = (200, -225, -375, 375)
# coordinates for each box

def box(t, x1, y1, x2, y2):
    # a function to draw a box
    t.speed(0)
    t.up()
    t.goto(x1, y1)
    t.down()
    t.goto(x1, y2)
    t.goto(x2, y2)
    t.goto(x2, y1)
    t.goto(x1, y1)
    t.up()

def window_setup():
    # the function that sets up the game window
    s.screensize(800,800)
    splash()
    box(t, UI_BOX[0], UI_BOX[1], UI_BOX[2], UI_BOX[3])
    box(t, LEADERBOARD_BOX[0], LEADERBOARD_BOX[1],
        LEADERBOARD_BOX[2], LEADERBOARD_BOX[3])
    box(t, GAMEBOARD[0], GAMEBOARD[1], GAMEBOARD[2], GAMEBOARD[3])
    ui = {}
    ui['reset'] = reset_button()
    ui['load'] = load_button()
    ui['quit'] = quit_button()
    display_leaderboard()
    ui['moves'] = move_counter()
    ui['thumbnail'] = thumbnail_turtle()
    return ui

def move_counter():
    # spawns the move counter
    x = UI_BOX[0] + 25
    y = (UI_BOX[1] + UI_BOX[3])/2
    move_counter = turtle.Turtle(visible=False)
    move_counter.penup()
    move_counter.goto(x, y)
    move_counter.write('Moves: 0', False, 'left', ('Arial', 15, 'bold'))
    return move_counter

def update_moves(moves, counter):
    # updates the move counter
    counter.clear()
    counter.write(f'Moves: {moves}', False, 'left', ('Arial', 15, 'bold'))

def button(x, y):
    # boilerplate button function
    button = turtle.Turtle()
    button.penup()
    button.speed(0)
    button.hideturtle()
    button.goto(x, y)
    button.showturtle()
    return button
    
def reset_button():
    # spawns the reset button
    reset_button = button(50, -312.5)
    s.addshape('Resources/resetbutton.gif')
    reset_button.shape('Resources/resetbutton.gif')
    
    return reset_button

def load_button():
    # spawns the load button
    load_button = button(150, -312.5)
    s.addshape('Resources/loadbutton.gif')
    load_button.shape('Resources/loadbutton.gif')

    return load_button

def quit_button():
    # spawns the quit button
    quit_button = button(250, -312.5)
    s.addshape('Resources/quitbutton.gif')
    quit_button.shape('Resources/quitbutton.gif')

    return quit_button

def quit_message():
    # displays the message upon quit
    s.addshape('Resources/quitmsg.gif')
    quitmsg = turtle.Turtle(shape='Resources/quitmsg.gif')
    time.sleep(3)
    quitmsg.hideturtle()

def win_message():
    # displays the message upon winning
    s.addshape('Resources/winner.gif')
    win = turtle.Turtle(shape='Resources/winner.gif')
    time.sleep(3)

def lose_message():
    # displays the message upon losing
    s.addshape('Resources/Lose.gif')
    lose = turtle.Turtle(shape='Resources/Lose.gif')
    time.sleep(3)

def splash():
    # the splash screen that runs on startup
    s.bgcolor("black")
    s.addshape("Resources/splash_screen.gif")
    time.sleep(1)
    t.shape("Resources/splash_screen.gif")
    time.sleep(5)
    t.hideturtle()
    time.sleep(1)
    s.bgcolor("white")

def offset(length, size):
    # calculates the offset for tile placement centered within the gameboard
    center_x = (GAMEBOARD[0] + GAMEBOARD[2]) / 2
    center_y = (GAMEBOARD[1] + GAMEBOARD[3]) / 2
    x_offset = center_x + (((length / 2) + 0.5) * -(size + TILE_SPACING))
    y_offset = center_y + (((length / 2) + 0.5) * (size + TILE_SPACING))
    return x_offset, y_offset

def place_tiles(grid, size):
    # places the puzzle tiles in the gameboard
    x_offset, y_offset = offset(len(grid), size)
    for i in range(len(grid)):
        for j in range(len(grid)):
            x = (j + 1) * (size + TILE_SPACING) + x_offset
            y = (i + 1) * -(size + TILE_SPACING) + y_offset
            s.addshape(grid[i][j].image)
            grid[i][j].turtile = turtle.Turtle(shape=grid[i][j].image,
                                            visible=False)
            grid[i][j].turtile.speed(0)
            grid[i][j].turtile.penup()
            n = size/2
            box(grid[i][j].turtile, x - n, y + n, x + n, y - n)
            grid[i][j].turtile.goto(x, y)
            grid[i][j].turtile.showturtle()
    return grid

def thumbnail(image, turtle):
    # updates the thumbnail
    s.addshape(image)
    turtle.shape(image)
    turtle.showturtle()

def thumbnail_turtle():
    # spawns the thumbnail
    thumbnail = turtle.Turtle(visible=False)
    thumbnail.penup()
    thumbnail.speed(0)
    thumbnail.goto(350, 350)
    return thumbnail

def display_leaderboard():
    '''
    Reads a leaderboard.txt file if it exists and shows the first NAME_LIMIT
    names in a list. Also limits character length of entries to 20 characters.

    If the leaderboard.txt file is not found, will display an error message on
    startup.
    '''
    NAME_LIMIT = 30
    file = 'leaderboard.txt'
    y = LEADERBOARD_BOX[3]
    
    if os.path.exists(file):
        display = []
        t.goto(230, y - 100)
        t.write('Leaderboard:', False, 'left', ('Arial', 15, 'bold'))
        
        with open(file, mode='r') as leaderboard:
            for entry in leaderboard:
                display.append(entry.strip())

        y = y - 125
        i = 0
        display = sorted(display)
        
        for i in range(len(display)):
            display[i] = display[i][:20]
            t.goto(230, y)
            t.write(display[i], False, 'left', ('Arial', 14, 'bold'))

            y -= 15
            i += 1

            if i >= NAME_LIMIT:
                break
            
    else:
        s.addshape('Resources/leaderboard_error.gif')
        error_message = turtle.Turtle(shape='Resources/leaderboard_error.gif')
        time.sleep(3)
        error_message.hideturtle()
        error_handler(2, 'puzzle_gui.display_leaderboard()')

def file_error():
    # file error when a puz file is not found or malformed
    s.addshape('Resources/file_error.gif')
    error_message = turtle.Turtle(shape='Resources/file_error.gif')
    time.sleep(3)
    error_message.hideturtle()

def file_warning():
    # file warning when the list of puz files is too long
    s.addshape('Resources/file_warning.gif')
    warning_message = turtle.Turtle(shape='Resources/file_warning.gif')
    time.sleep(3)
    warning_message.hideturtle()

def roll_credits():
    # shows the credits and quits the game
    s.clear()
    s.bgcolor("black")
    s.addshape('Resources/credits.gif')
    credit_image = turtle.Turtle('Resources/credits.gif')
    time.sleep(5)
    s.bye()

