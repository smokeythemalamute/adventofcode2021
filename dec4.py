# --- Day 4: Giant Squid ---
# You're already almost 1.5km (almost a mile) below the surface of the ocean,
# already so deep that you can't see any sunlight. What you can see, however,
# is a giant squid that has attached itself to the outside of your submarine.
#
# Maybe it wants to play bingo?
#
# Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
# Numbers are chosen at random, and the chosen number is marked on all boards
# on which it appears. (Numbers may not appear on all boards.) If all numbers
# in any row or any column of a board are marked, that board wins. (Diagonals
# don't count.)
#
# The submarine has a bingo subsystem to help passengers (currently, you and
# the giant squid) pass the time. It automatically generates a random order
# in which to draw numbers and a random set of boards (your puzzle input).
# For example:
#
# 7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
#
# 22 13 17 11  0
#  8  2 23  4 24
# 21  9 14 16  7
#  6 10  3 18  5
#  1 12 20 15 19
#
#  3 15  0  2 22
#  9 18 13 17  5
# 19  8  7 25 23
# 20 11 10 24  4
# 14 21 16 12  6
#
# 14 21 17 24  4
# 10 16 15  9 19
# 18  8 23 26 20
# 22 11 13  6  5
#  2  0 12  3  7
#
# After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
# winners, but the boards are marked as follows (shown here adjacent to each
# other to save space):
#
# 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
# 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
#
# After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there
# are still no winners:
#
# 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
# 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
#
# Finally, 24 is drawn:
#
# 22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
#  8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
# 21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
#  6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
#  1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
#
# At this point, the third board wins because it has at least one complete
# row or column of marked numbers (in this case, the entire top row is
# marked: 14 21 17 24 4).
#
# The score of the winning board can now be calculated. Start by finding
# the sum of all unmarked numbers on that board; in this case, the sum is
# 188. Then, multiply that sum by the number that was just called when the
# board won, 24, to get the final score, 188 * 24 = 4512.
#
# To guarantee victory against the giant squid, figure out which board will
# win first. What will your final score be if you choose that board?
#
# --- Part Two ---
# On the other hand, it might be wise to try a different strategy: let the
# giant squid win.
#
# You aren't sure how many bingo boards a giant squid could play at once,
# so rather than waste time counting its arms, the safe thing to do is to
# figure out which board will win last and choose that one. That way, no
# matter which boards it picks, it will win for sure.
#
# In the above example, the second board is the last to win, which happens
# after 13 is eventually called and its middle column is completely marked.
# If you were to keep playing until this point, the second board would have
# a sum of unmarked numbers equal to 148 for a final score of
# 148 * 13 = 1924.
#
# Figure out which board will win last. Once it wins, what would its final
# score be?

from __future__ import annotations
from typing import Callable, List, Tuple
from functools import reduce
import re


def transpose(matrix: List[List[int]]):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


class BingoCard:
    def from_input(lines: List[str]):
        return BingoCard([[int(x) for x in re.split("\D+", row)] for row in lines])

    def __init__(self, grid: List[List[int]]):
        self.grid = grid

    def _horiz_match(grid: List[List[int]], numbers: List[int]) -> bool:
        matches = [[x in numbers for x in row] for row in grid]
        return reduce(
            lambda acc, row: acc or reduce(lambda a, b: a and b, row), matches, False
        )

    def has_won(self, numbers: List[int]):
        won_rows = BingoCard._horiz_match(self.grid, numbers)
        won_cols = BingoCard._horiz_match(transpose(self.grid), numbers)
        return won_rows or won_cols

    def not_matching(self, numbers: List[int]) -> List[int]:
        return [x for x in reduce(lambda a, x: a + x, self.grid) if x not in numbers]


class Winner:
    def __init__(self, card: BingoCard, picks: List[int]) -> None:
        self.card = card
        self.picks = picks
        self.score = picks[-1] * sum(card.not_matching(picks))

    def __repr__(self) -> str:
        return f"Winner(score={self.score})"


class BingoGame:
    def __init__(self, filename: str) -> None:
        with open(filename) as f:
            self.picks = [int(x) for x in f.readline().strip().split(",")]

            self.cards = []
            while f.readline() != "":
                input = [f.readline().strip() for l in range(5)]
                self.cards.append(BingoCard.from_input(input))

        self.turn = 1
        self.remaining = self.cards.copy()

    def find_next_winners(self) -> Tuple[List[Winner], int]:
        winners = []
        while len(winners) == 0 and self.turn < len(self.picks):
            picks = self.picks[: self.turn]
            winners = [card for card in self.remaining if card.has_won(picks)]
            self.turn += 1
        for w in winners:
            self.remaining.remove(w)
        return [Winner(w, picks) for w in winners], self.turn - 1

    def find_next_winners_until(
        self, fn: Callable[[BingoGame], bool]
    ) -> Tuple[List[Winner], int]:
        all_winners = []
        while not fn(self):
            winners, _ = game.find_next_winners()
            all_winners += winners
        return all_winners, self.turn - 1


if __name__ == "__main__":
    for filename in ["dec4_test.txt", "dec4_data.txt"]:
        game = BingoGame(filename)
        p1 = game.find_next_winners()

        game = BingoGame(filename)
        game.find_next_winners_until(lambda g: len(g.remaining) == 1)
        p2 = game.find_next_winners()

        print(
            filename,
            ":",
            {"p1": p1, "p2": p2},
        )
