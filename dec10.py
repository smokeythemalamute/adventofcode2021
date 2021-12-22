# --- Day 10: Syntax Scoring ---
# You ask the submarine to determine the best route out of the deep-sea
# cave, but it only replies:
#
# Syntax error in navigation subsystem on line: all of them
# All of them?! The damage is worse than you thought. You bring up a
# copy of the navigation subsystem (your puzzle input).
#
# The navigation subsystem syntax is made of several lines containing
# chunks. There are one or more chunks on each line, and chunks contain
# zero or more other chunks. Adjacent chunks are not separated by any
# delimiter; if one chunk stops, the next chunk (if any) can
# immediately start. Every chunk must open and close with one of
# four legal pairs of matching characters:
#
# If a chunk opens with (, it must close with ).
# If a chunk opens with [, it must close with ].
# If a chunk opens with {, it must close with }.
# If a chunk opens with <, it must close with >.
#
# So, () is a legal chunk that contains no other chunks, as is [].
# More complex but valid chunks include ([]), {()()()}, <([{}])>,
# [<>({}){}[([])<>]], and even (((((((((()))))))))).
#
# Some lines are incomplete, but others are corrupted. Find and discard
# the corrupted lines first.
#
# A corrupted line is one where a chunk closes with the wrong character
# - that is, where the characters it opens and closes with do not form
# one of the four legal pairs listed above.
#
# Examples of corrupted chunks include (], {()()()>, (((()))}, and
# <([]){()}[{}]). Such a chunk can appear anywhere within a line, and
# its presence causes the whole line to be considered corrupted.
#
# For example, consider the following navigation subsystem:
#
# [({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]
#
# Some of the lines aren't corrupted, just incomplete; you can ignore
# these lines for now. The remaining five lines are corrupted:
#
# {([(<{}[<>[]}>{[]{[(<()> - Expected ], but found } instead.
# [[<[([]))<([[{}[[()]]] - Expected ], but found ) instead.
# [{[{({}]{}}([{[{{{}}([] - Expected ), but found ] instead.
# [<(<(<(<{}))><([]([]() - Expected >, but found ) instead.
# <{([([[(<>()){}]>(<<{{ - Expected ], but found > instead.
#
# Stop at the first incorrect closing character on each corrupted line.
#
# Did you know that syntax checkers actually have contests to see who
# can get the high score for syntax errors in a file? It's true! To
# calculate the syntax error score for a line, take the first illegal
# character on the line and look it up in the following table:
#
# ): 3 points.
# ]: 57 points.
# }: 1197 points.
# >: 25137 points.
#
# In the above example, an illegal ) was found twice (2*3 = 6 points),
# an illegal ] was found once (57 points), an illegal } was found once
# (1197 points), and an illegal > was found once (25137 points). So,
# the total syntax error score for this file is
# 6+57+1197+25137 = 26397 points!

from typing import List


pairs = [("[", "]"), ("(", ")"), ("{", "}"), ("<", ">")]

illegal_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
missing_scores = {")": 1, "]": 2, "}": 3, ">": 4}

opening = [x[0] for x in pairs]

map_to_closing = {x[0]: x[1] for x in pairs}
map_from_closing = {x[1]: x[0] for x in pairs}


class SyntaxError(Exception):
    def __init__(self, line: str, pos: int, message: str) -> None:
        self.line = line
        self.pos = pos
        super().__init__(message)


class IncompleteLineError(Exception):
    def __init__(self, line: str, expecting: List[str], message: str) -> None:
        self.line = line
        self.expecting = expecting
        super().__init__(message)


def verify_syntax(line: str) -> bool:
    stack = []
    for i, c in enumerate(line):
        if c in opening:
            stack += [c]
        if c in map_from_closing:
            expected = map_from_closing[c]
            last = stack[-1]
            if last != expected:
                raise SyntaxError(line, i, f"Expected {expected} got {last}")
            else:
                stack = stack[:-1]
    if len(stack) > 0:
        stack.reverse()
        expecting = [map_to_closing[x] for x in stack]
        raise IncompleteLineError(
            line,
            expecting,
            f"Unclosed sections, expecting {expecting}",
        )


if __name__ == "__main__":
    for filename in ["dec10_test.txt", "dec10_data.txt"]:
        with open(filename) as f:
            lines = f.readlines()

        valid = []
        illegal = 0
        missing = []
        for line in lines:
            try:
                verify_syntax(line)
                valid += [line]
            except SyntaxError as e:
                c = line[e.pos]
                illegal += illegal_scores[c]
            except IncompleteLineError as e:
                score = 0
                for x in e.expecting:
                    score = score * 5 + missing_scores[x]
                missing += [score]

        print(filename, ": illegal_score =", illegal)
        print(filename, ": missing_scores =", sorted(missing)[int(len(missing) / 2)])
