Grid Snake Problem
==================

*Written by Eric J. Whitney, October 2024*

A simple example of solving the Grid Snake problem. This involves finding a 
path that passes through each point on a grid, starting at a given position and 
finishing at another.

Example
-------
For a 5x5 grid, starting at (0, 0) and ending at (0, 4), the solution
path would be:

    Solution path found: [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), 
    (3, 1), (2, 1), (1, 1), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), 
    (4, 3), (4, 4), (3, 4), (3, 3), (2, 3), (2, 4), (1, 4), (1, 3), (0, 3), 
    (0, 4)]


    S   ○ → ○   ○ → E
    ↓   ↑   ↓   ↑    
    ○   ○   ○   ○ ← ○
    ↓   ↑   ↓       ↑
    ○   ○   ○   ○ → ○
    ↓   ↑   ↓   ↑    
    ○   ○   ○   ○ ← ○
    ↓   ↑   ↓       ↑
    ○ → ○   ○ → ○ → ○

However, with the same grid and start point and changing the end point to 
(0, 3), the problem becomes unsolvable:

    Solving with recursive method:
        No solution path found.
        Elapsed time: 0.34 seconds
    
    Solving with non-recursive method:
        No solution path found.
        Elapsed time: 0.40 seconds
