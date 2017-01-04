#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import re
import sys

ROWS = 'abcdefghjklmnopqrstuvwxyz'

parser = argparse.ArgumentParser(description='A terminal minesweeper clone')
parser.add_argument('-gs', '--gridsize', metavar='WxH',
                    type=str, default='30x16',
                    help='Size of the grid')
parser.add_argument('-m', '--mines', metavar='N',
                    type=int, default=99,
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
    # parser.print_help()
    sys.exit(1)
if mines < 1:
    print('    Error: Number of mines too low')
    # parser.print_help()
    sys.exit(1)


def print_grid():
    # header
    print('   ', end='')
    for x in range(width):
        print('% 4i' % (x+1), end='')
    print('\n    ╔═══' + '╤═══' * (width-1) + '╗')
    for y in range(height):
        # for x in range(width):
        if y > 0:
            print('    ╟───' + '┼───' * (width-1) + '╢')
        print(' ' + ROWS[y] + '  ║   ' + '│   ' * (width-1) + '║')
        # print('')
    print('    ╚═══' + '╧═══' * (width-1) + '╝')

    fdsf = raw_input('\n    Please enter the next move: ')

print_grid()
