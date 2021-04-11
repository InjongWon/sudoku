
from timeit import timeit
from solver import BfsSolver, DfsSolver
from sudoku_puzzle import SudokuPuzzle
from word_ladder_puzzle import WordLadderPuzzle

if __name__ == '__main__':

    puzzles = [SudokuPuzzle(4,
                            [["1", " ", " ", "2"],
                             [" ", " ", " ", "1"],
                             [" ", " ", " ", " "],
                             [" ", " ", "2", " "]],
                            {"1", "2", "3", "4"}),
               SudokuPuzzle(9,
                            [[" ", " ", " ", "7", " ", "8", " ", "1", " "],
                             [" ", " ", "7", " ", "9", " ", " ", " ", "6"],
                             ["9", " ", "3", "1", " ", " ", " ", " ", " "],
                             ["3", "5", " ", "8", " ", " ", "6", " ", "1"],
                             [" ", " ", " ", " ", " ", " ", " ", " ", " "],
                             ["1", " ", "6", " ", " ", "9", " ", "4", "8"],
                             [" ", " ", " ", " ", " ", "1", "2", " ", "7"],
                             ["8", " ", " ", " ", "7", " ", "4", " ", " "],
                             [" ", "6", " ", "3", " ", "2", " ", " ", " "]],
                            {"1", "2", "3", "4", "5", "6", "7", "8", "9"}),
               WordLadderPuzzle("same", "cost")
               ]
    headers = ["Puzzle Type", "Solver", "len(sol)", "time"]
    print("|".join(headers))
    print("|".join(["-" * len(header) for header in headers]))

    for puzzle in puzzles:
        for solver in [DfsSolver, BfsSolver]:
            puzzle_solver = solver()
            sol = puzzle_solver.solve(puzzle)
            n_samples = 1
            duration = timeit('puzzle_solver.solve(puzzle)',
                              globals=globals(),
                              number=n_samples) / n_samples

            print(f"{type(puzzle).__name__[:-6]:>11}|{solver.__name__[:-6]:>6}|"
                  f"{len(sol) if sol else -1:>8}|{duration:2.5f}")
