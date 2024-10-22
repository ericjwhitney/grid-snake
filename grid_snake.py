"""
Grid Snake Problem
------------------

This constains an example method for solving the Grid Snake problem.

This involves finding a path that passes through each point on a grid,
starting at a given position and finishing at another.
"""
import time

import numpy as np
import numpy.typing as npt

# Written by Eric J. Whitney, October 2024.

# Note: This is relatively easy to extend to N-D.
type GridPt = tuple[int, int]
_search_dirns = [(+1, 0), (-1, 0), (0, +1), (0, -1)]


# -- Driver ------------------------------------------------------------


def main():
    start_pos = (0, 0)
    end_pos = (0, 3)
    size = (5, 5)

    for method in ('recursive', 'non-recursive'):
        print(f"\nSolving with {method} method:")

        start_time = time.time()
        path = solve_snake(start_pos, end_pos, size, method)
        end_time = time.time()

        if path:
            print(f"\tSolution path found: {path}")
            print_path(path, size)
        else:
            print("\tNo solution path found.")

        print(f"\tElapsed time: {end_time - start_time:.2f} seconds")


# -- Solvers -----------------------------------------------------------


def solve_snake(start_pos: GridPt, end_pos: GridPt, size: GridPt,
                method: str = 'recursive') -> list[GridPt]:
    """
    Find a solution `snake` (if it exists) that passes through each
    point on a grid of points, starting at `start_pos` and finishing at
    `end_pos`

    Args
    ----
    start_pos : tuple[int, ...]
        The starting position on the grid.

    end_pos : tuple[int, ...]
        The ending position on the grid.

    size : tuple[int, ...]
        The size of the grid (`I` x `J`).

    method : str = 'recursive' or 'non-recursive'
        The method used to solve the problem.

    Returns
    -------
    path : list[tuple[int, ...], ...]
        The solution path, if it exists.  The path contains the indices
        of each grid point visited in order. If there is no solution, an
        empty list is returned.
    """
    if not valid_pos(start_pos, size):
        raise ValueError(f"Invalid start position: {start_pos}")

    if not valid_pos(end_pos, size):
        raise ValueError(f"Invalid end position: {end_pos}")

    if start_pos == end_pos:
        raise ValueError("Start and end positions must be different.")

    if method == 'recursive':
        visited = np.zeros(size, dtype=bool)
        path = []
        success = _recursive(start_pos, end_pos, visited, path)
        return path if success else []

    elif method == 'non-recursive':
        return _non_recursive(start_pos, end_pos, size)

    else:
        raise ValueError(f"Unknown method: {method}")


def _recursive(pos: GridPt, end_pos: GridPt, visited: npt.NDArray[bool],
               path: list[GridPt]) -> bool:
    # Initially `path` must be empty and `visited` must contain all
    # `False` values of (size[0], size[1], ...).
    size = visited.shape

    # Check if this is a valid point, not yet visited.
    if not valid_pos(pos, size) or visited[*pos]:
        return False

    # Mark the position as visited and add the position to the path.
    visited[*pos] = True
    path.append(pos)

    # If this is the end position and we have visited all the other
    # positions then we have found the solution. As the path should
    # contain all points exactly once, simply checking the path length
    # is more efficient than summing the 'visited' array.
    if pos == end_pos and len(path) == size[0] * size[1]:
        return True

    # Otherwise, try all the possible directions from here.
    for δ in _search_dirns:
        next_pos = (pos[0] + δ[0], pos[1] + δ[1])
        if _recursive(next_pos, end_pos, visited, path):
            return True

    # No solution found in any direction.  Backtrack and remove the
    # position from the path.
    visited[*pos] = False
    path.pop()
    return False


def _non_recursive(start_pos: GridPt, end_pos: GridPt,
                   size: GridPt) -> list[GridPt]:
    # Returns solution path or empty list.

    # Setup the path and visited array.
    path = [start_pos]
    path_dirn = [0]  # Store the search direction along path.
    visited = np.zeros(size, dtype=bool)
    visited[*start_pos] = True
    n_dirns = len(_search_dirns)

    while True:
        # If we are at the end position and we have visited all the
        # points then we have found the solution.
        pos = path[-1]
        if pos == end_pos and len(path) == size[0] * size[1]:
            return path

        # Have we exhausted all the search directions for this position?
        if path_dirn[-1] >= n_dirns:
            # Backtrack: Clear this position and remove from path.
            visited[*pos] = False
            path.pop()
            path_dirn.pop()

            if not path:
                # If we have exhausted our options, return no solution.
                return []
            else:
                # Advance the search direction for the previous point
                # and continue.
                path_dirn[-1] += 1
                continue

        # Try the current seach direction.
        δ = _search_dirns[path_dirn[-1]]
        next_pos = (pos[0] + δ[0], pos[1] + δ[1])

        # If the new position is out-of-bounds or has already been
        # visited, advance the search direction and try again.
        if not valid_pos(next_pos, size) or visited[*next_pos]:
            path_dirn[-1] += 1
            continue

        # This is a valid new point.  Add the new position to the path,
        # add a new search direction and mark it as visited.
        path.append(next_pos)
        path_dirn.append(0)
        visited[*next_pos] = True

    # Exhausted all possible points and directions.
    return []


# -- Misc. Functions ---------------------------------------------------

def valid_pos(pos: GridPt, size: GridPt) -> bool:
    """Returns `True` if `pos` is a valid position on the grid."""
    return (0 <= pos[0] < size[0]) and (0 <= pos[1] < size[1])


def print_path(path: list[GridPt], size: GridPt):
    # Setup empty grid and add basic points. Expand grid horizontally
    # for better appearance.
    chrs_size = (2 * size[0] - 1, 4 * size[1] - 3)
    chrs = np.full(chrs_size, ' ', dtype=str)
    chrs[0:chrs_size[0]:2, 0:chrs_size[1]:4] = '○'

    # Add start and end point.
    chrs[path[0][0] * 2, path[0][1] * 4] = 'S'
    chrs[path[-1][0] * 2, path[-1][1] * 4] = 'E'

    # Add path.
    for pt1, pt2 in zip(path, path[1:]):
        # Work out the symbol position by starting at point 1 and adding
        # the offset.
        δ = (pt2[0] - pt1[0], pt2[1] - pt1[1])
        symbol_pos = (pt1[0] * 2 + δ[0], pt1[1] * 4 + δ[1] * 2)
        match δ:
            case (1, 0):
                chrs[symbol_pos] = '↓'
            case (-1, 0):
                chrs[symbol_pos] = '↑'
            case (0, 1):
                chrs[symbol_pos] = '→'
            case (0, -1):
                chrs[symbol_pos] = '←'

    # Show result.
    print()
    for row in chrs:
        print(''.join(row))
    print()


# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
