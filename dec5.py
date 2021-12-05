# --- Day 5: Hydrothermal Venture ---
# You come across a field of hydrothermal vents on the ocean floor!
# These vents constantly produce large, opaque clouds, so it would
# be best to avoid them if possible.
#
# They tend to form in lines; the submarine helpfully produces a list
# of nearby lines of vents (your puzzle input) for you to review. For
# example:
#
# 0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2
#
# Each line of vents is given as a line segment in the format
# x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the
# line segment and x2,y2 are the coordinates of the other end.
# These line segments include the points at both ends. In other words:
#
# An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
# An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
#
# For now, only consider horizontal and vertical lines: lines where
# either x1 = x2 or y1 = y2.
#
# So, the horizontal and vertical lines from the above list would
# produce the following diagram:
#
# .......1..
# ..1....1..
# ..1....1..
# .......1..
# .112111211
# ..........
# ..........
# ..........
# ..........
# 222111....
#
# In this diagram, the top left corner is 0,0 and the bottom right
# corner is 9,9. Each position is shown as the number of lines which
# cover that point or . if no line covers that point. The top-left
# pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom
# row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.
#
# To avoid the most dangerous areas, you need to determine the number
# of points where at least two lines overlap. In the above example,
# this is anywhere in the diagram with a 2 or larger - a total of 5
# points.
#
# Consider only horizontal and vertical lines. At how many points do
# at least two lines overlap?
#
# --- Part Two ---
#
# Unfortunately, considering only horizontal and vertical lines
# doesn't give you the full picture; you need to also consider
# diagonal lines.
#
# Because of the limits of the hydrothermal vent mapping system, the
# lines in your list will only ever be horizontal, vertical, or a
# diagonal line at exactly 45 degrees. In other words:
#
# An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
# An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
# Considering all lines from the above example would now produce
# the following diagram:
#
# 1.1....11.
# .111...2..
# ..2.1.111.
# ...1.2.2..
# .112313211
# ...1.2....
# ..1...1...
# .1.....1..
# 1.......1.
# 222111....
# You still need to determine the number of points where at least
# two lines overlap. In the above example, this is still anywhere
# in the diagram with a 2 or larger - now a total of 12 points.
#
# Consider all of the lines. At how many points do at least two lines overlap?


import re
from typing import Callable, Dict, List, Tuple
from collections import defaultdict
import math


def simple_lerp(x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
    if x1 == x2:
        starty, endy = (y1, y2) if y1 < y2 else (y2, y1)
        return map(lambda y: (x1, starty + y), range(endy - starty + 1))
    elif y1 == y2:
        startx, endx = (x1, x2) if x1 < x2 else (x2, x1)
        return map(lambda x: (startx + x, y1), range(endx - startx + 1))
    else:
        # Cannot handle non-horizontal/vertical lines
        return []


def rangef(start: float, end: float, n: int):
    i = 0
    delta = end - start
    while i < n:
        yield start + (delta * (float(i) / float(n)))
        i += 1
    yield end


def lerp(x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
    starty, endy = (y1, y2) if y1 < y2 else (y2, y1)
    startx, endx = (x1, x2) if x1 < x2 else (x2, x1)
    deltax, deltay = endx - startx, endy - starty
    n = max(deltax, deltay)
    return zip(
        map(round, rangef(x1, x2, n)),
        map(round, rangef(y1, y2, n)),
    )


def print_map(grid: Dict[Tuple[int, int], int]):
    maxx, maxy = 0, 0
    for x, y in grid.keys():
        maxx = max(maxx, x)
        maxy = max(maxy, y)

    for y in range(maxy + 1):
        print(
            "".join(
                [str(grid[(x, y)]) if grid[x, y] > 0 else "." for x in range(maxx + 1)]
            )
        )


input_re = r"(\d+),(\d+) -> (\d+),(\d+)"


def parse(line: str) -> Tuple[int, int, int, int]:
    return tuple(
        map(
            int,
            re.search(input_re, line).groups(),
        )
    )


def run(
    name: str,
    filename: str,
    fn: Callable[[Tuple[int, int, int, int]], List[Tuple[int, int]]],
) -> Dict[Tuple[int, int], int]:
    grid = defaultdict(int)
    with open(filename) as f:
        for input in f.readlines():
            points = list(fn(parse(input)))
            if debug:
                print(name, ":", filename, ":", input.strip(), "=", points)
            for p in points:
                grid[p] += 1
    if debug:
        print(name, ":", filename, ":")
        print_map(grid)
    overlaps = len([x for x in grid.values() if x > 1])
    return grid, overlaps


if __name__ == "__main__":
    for filename, debug in [("dec5_test.txt", True), ("dec5_data.txt", False)]:
        grid, overlaps = run("part1", filename, lambda p: simple_lerp(*p))
        print("part1 :", filename, ":", overlaps, "overlaps")
        grid, overlaps = run("part2", filename, lambda p: lerp(*p))
        print("part2 :", filename, ":", overlaps, "overlaps")
