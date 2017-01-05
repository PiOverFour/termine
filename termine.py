#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import re
import sys
import random


# from http://stackoverflow.com/a/21659588
# input getter
def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys
    import tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


getch = _find_getch()


class Cell(object):

    COLORS = {
        0: ' ',
        1: '\033[1m\033[34m1\033[0m',
        2: '\033[1m\033[32m2\033[0m',
        3: '\033[1m\033[31m3\033[0m',
        4: '\033[94m4\033[0m',
        5: '\033[91m5\033[0m',
        6: '\033[34m6\033[0m',
        7: '7',
        8: '\033[1m\033[97m8\033[0m'
    }

    def __init__(self, coords, grid, is_mine):
        self.grid = grid
        self.coords = coords
        self.is_mine = is_mine
        self.is_flagged = False

    def compute_adjacent(self):
        if self.is_mine:
            return
        self.adjacent = 0
        print(self.coords)
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                # print(grid[x+self.coords[0]][y+self.coords[1]].is_mine)
                # try:
                x = dx + self.coords[0]
                y = dy + self.coords[1]
                if x < 0 or y < 0 or x >= width or y >= width:
                    continue
                if grid[x][y].is_mine:
                    self.adjacent += 1
                print(x, y, grid[x][y].is_mine)
                # except:
                #     continue
        # self.adjacent = random.randint(0, 8)

    def get_output(self):
        output = ' '
        if self.is_mine:
            output = 'X'
        else:
            output = self.COLORS[self.adjacent]
        return output

    def open(self):
        pass


def generate_grid(width, height, mines):
    grid = []
    mines = [True if (n < mines) else False for n in range(width*height)]
    random.shuffle(mines)
    for x in range(width):
        row = []
        for y in range(height):
            row.append(Cell((x, y), grid, mines[y*width+x]))
        grid.append(row)
    return grid


def compute_grid(grid):
    for x in range(width):
        for y in range(height):
            grid[x][y].compute_adjacent()


def step(next_move):
    if next_move in ('q', u'\003'):
        sys.exit()
    elif (next_move) == 'A' and current_coords[1] > 0:
        # up
        current_coords[1] -= 1
    elif (next_move) == 'B' and current_coords[1] < height - 1:
        # down
        current_coords[1] += 1
    elif (next_move) == 'C' and current_coords[0] < width - 1:
        # right
        current_coords[0] += 1
    elif (next_move) == 'D' and current_coords[0] > 0:
        # left
        current_coords[0] -= 1
    # print(next_move)


def print_grid(grid):
    # header
    print('   ', end='')
    # draw horizontal coordinates
    for x in range(width):
        print('% 4i' % (x+1), end='')

    print('\n    ╔═══' + '╤═══' * (width-1) + '╗')
    for y in range(height):
        if y > 0:
            print('    ╟───' + '┼───' * (width-1) + '╢')
        # draw vertical coordinates
        print(' ' + ROWS[y] + '  ║', end='')
        for x in range(width):
            if x:
                print('│', end='')
            output = grid[x][y].get_output()
            output = ' %s ' % output
            if current_coords[0] == x and current_coords[1] == y:
                output = '\033[47m' + output + '\033[49m'
            # is_mine = 'X' if grid[x][y].is_mine else ' '
            print(output, end='')
        print('║')
        # print('')
    print('    ╚═══' + '╧═══' * (width-1) + '╝')


if __name__ == '__main__':
    ROWS = 'abcdefghjklmnopqrstuvwxyz'

    parser = argparse.ArgumentParser(
        description='A terminal minesweeper clone')
    parser.add_argument('-gs', '--gridsize', metavar='WxH',
                        type=str, default='8x8',
                        help='Size of the grid')
    parser.add_argument('-m', '--mines', metavar='N',
                        type=int, default=10,
                        help='Number of mines')
    args = parser.parse_args()

    mines = args.mines
    match = re.match('([0-9]+)x([0-9]+)', args.gridsize)
    try:
        width, height = (int(g) for g in match.groups())
    except:
        print('    Please specify a grid size of form WidthxHeight')
        sys.exit(1)

    # print(width, height, type(height))
    if mines > width * height:
        print('    Error: Number of mines too high')
        sys.exit(1)
    if mines < 1:
        print('    Error: Number of mines too low')
        sys.exit(1)

    grid = generate_grid(width, height, mines)
    compute_grid(grid)
    current_coords = [0, 0]

    game_ended = False
    while not game_ended:
        print_grid(grid)
        # next_move = raw_input('\n    Please enter the next move: ')
        next_move = getch()
        step(next_move)
