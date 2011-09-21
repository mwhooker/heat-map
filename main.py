from __future__ import division
import copy
import logging
import math
import random


"""
TODO:
    output an image instead of this number grid
"""

log = logging.getLogger(__name__)
ch = logging.StreamHandler()
log.addHandler(ch)
log.setLevel(logging.DEBUG)

MAX_CELL = 10

def print_grid(grid):
    """Print a grid

    >>> grid = [[1,2],[3,4]]
    >>> print_grid(grid)
      x 0 1
    y
    0   1 2
    1   3 4
    """
    #log.debug(repr(grid))
    cell_space = 3
    print '  x ',
    for i in xrange(len(grid)):
        print str(i).rjust(cell_space),
    print '\ny'
    for y,x in iterate_grid(grid):
        if x == 0:
            print "\n", repr(y).ljust(4),
        print repr(grid[y][x]).rjust(cell_space),
    print "\n"
    """
    for y, row in enumerate(grid):
        print repr(y).ljust(4),
        for x, col in enumerate(row):
            print repr(col).rjust(cell_space),
        print ""
    """


def iterate_grid(grid):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            yield((y,x))

def smoothe_grid(g):
    points = {}
    grid = copy.deepcopy(g)
    for y, x in iterate_grid(grid):
        if grid[y][x] > 0:
            points[(y,x)] = grid[y][x]

    for y, x in iterate_grid(grid):
        for py, px in points:
            if (y, x) in points:
                continue
            d = distance(y, x, py, px)
            grid[y][x] = modify(g[y][x], grid[y][x], points[(py, px)], d, 'isqr')
            #log.debug( "%s, %s: %s -> %s" % (y, x, g[y][x], grid[y][x]))

    return grid

def modify(orig, cur, modifyer, distance, type='isqr'):
    """apply a gradient function to a cell

    orig is the starting value of the cell
    cur is the value of the cell in the current pass
    modifyer is the value of the cell we're using to modify cur
    distance is the distance the cell containing "modifyer" is from the cell
        we're modifying
    type is a decay function we should use on the modifyer value
    """
    assert modifyer > 0
    assert distance > 0
    assert cur >= orig



    #log.info("modifying with type %s" % type)
    if type == 'isqr':
        # inverse square: e is [0, MAX]
        e = modifyer / distance ** 2
        #log.debug("%s = %s / %s ** 2" % (e, modifyer, distance))
    elif type == 'gradient':
        e = modifyer - distance
        e = e if e > 0 else 0
    elif type == 'expdecay':
        raise NotImplemented('expdecay not implemented')
    else:
        raise BadArgument("type %s not known. must be one of 'isqr', 'expdecay'" %
                          type)

    if e == 0:
        return cur
    else:
        # how much weight the modifyer should add
        a = float(MAX_CELL - orig) / (float(MAX_CELL) / e)

        # average how much we should add with what's been added in previous
        # iterations
        if cur != orig:
            b = float(a + (cur - orig)) / 2
            #b = math.sqrt(a * (cur - orig))
        else:
            b = a

        ret = orig + b
        return int(ret)


def distance(y, x, py, px):
    """integer distance between points (y,x), (py,px)

    >>> distance(0, 0, 3, 5)
    6
    """

    c = math.sqrt((abs(y - py) ** 2) + (abs(x - px) ** 2))
    return round(c)

def initialize_grid(n, sparcity, max):
    """initialize an nxn grid with integers

    sparcity is a number between 0 and 1 which indicates how many cells should
    be populated
    max is an integer which gives the upper bound for each cell ([0, max])
    """
    grid = []
    for x in xrange(n):
        row = []
        for y in xrange(n):
            if sparcity >= random.random():
                row.append(random.randint(0, max))
            else:
                row.append(0)
        grid.append(row)
    return grid

def mock_grid():
    return [
        [0,4,0,0,0],
        [0,0,0,6,0],
        [0,10,10,0,0],
        [0,0,0,0,0],
        [0,2,0,0,0]
    ]

if __name__ == '__main__':
    #grid = initialize_grid(10, 0.2, MAX_CELL)
    grid = mock_grid()
    print_grid(grid)
    print_grid(smoothe_grid(grid))
