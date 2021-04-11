
from __future__ import annotations

from typing import List, Optional, Set

# You may remove this import if you don't use it in your code.
from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    # You may NOT change the interface to the solve method.
    # Note the optional parameter seen and its type.
    # Your implementations of this method in the two subclasses should use seen
    # to keep track of all puzzle states that you encounter during the
    # solution process.
    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """

        path = [puzzle]
        if puzzle.is_solved() and (seen is None or str(puzzle) not in seen):
            return path
        if seen is None:
            seen = set()
        seen = seen.copy()
        if str(puzzle) in seen:
            return []
        extensions = Queue()
        for extension in puzzle.extensions():
            extensions.enqueue(path + [extension])
        if extensions.is_empty():
            return []
        seen.add(str(puzzle))
        while not extensions.is_empty():
            extension = extensions.dequeue()
            if str(extension[-1]) in seen:
                continue
            if extension[-1].is_solved():
                return extension
            if extension[-1].fail_fast():
                seen.add(str(extension[-1]))
                continue
            sub_result = DfsSolver().solve(extension[-1], seen)
            if sub_result != []:
                result = extension + sub_result[1:]
                # no_seen = True
                # for i in result:
                #     if str(i) in seen:
                #         no_seen = False
                # if no_seen:
                #     return result
                return result
            seen.add(str(extension[-1]))
        return []


class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """

        path = [puzzle]
        if puzzle.is_solved() and (seen is None or str(puzzle) not in seen):
            return path
        if seen is None:
            seen = set()
        seen = seen.copy()
        if str(puzzle) in seen:
            return []
        extensions = Queue()
        for extension in puzzle.extensions():
            extensions.enqueue(path + [extension])
        seen.add(str(puzzle))
        while not extensions.is_empty():
            extension = extensions.dequeue()
            if str(extension[-1]) in seen:
                continue
            if extension[-1].is_solved():
                return extension
            if extension[-1].fail_fast():
                continue
            for sub_extensions in extension[-1].extensions():
                extensions.enqueue(extension + [sub_extensions])
            seen.add(str(extension[-1]))
        return []
