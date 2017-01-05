#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import re
import sys
import random

ROWS = 'abcdefghjklmnopqrstuvwxyz'

parser = argparse.ArgumentParser(description='A terminal minesweeper clone')
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


class Cell(object):
    def __init__(self, coords, grid, is_mine):
        self.grid = grid
        self.coords = coords
        self.is_mine = is_mine

    def compute(self):
        self.adjacent = random.randint(0, 8)

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
    print(grid)
    # grid = [[Cell((x, y)) for y in range(height)] for x in range(width)]

    # grid = [[random.randint(0, 8) for y in range(height)] for x in range(width)]
    return grid


def compute_grid(grid):
    for x in range(width):
        for y in range(height):
            grid[x][y].compute()


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
            is_mine = 'X' if grid[x][y].is_mine else ' '
            print(' %s ' % is_mine, end='')
        print('║')
        # print('')
    print('    ╚═══' + '╧═══' * (width-1) + '╝')


game_ended = False

if __name__ == '__main__':
    grid = generate_grid(width, height, mines)
    compute_grid(grid)
    print(grid)
    while not game_ended:
        print_grid(grid)
        next_move = raw_input('\n    Please enter the next move: ')
        compute_grid(next_move)
