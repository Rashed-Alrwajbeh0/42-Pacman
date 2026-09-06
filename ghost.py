"""Ghost movement : BFS pathfinding and two chase behaviors.
This module is deliberately decoupled from pygame: it only reasons about
grid positions (x, y) and the Maze/Cell data structures. The actual
rendering/movement interpolation stays in your Ghost/sprite class.
"""

from collections import deque
from typing import Optional

from cell import Cell
from maze import Maze

position = tuple[int, int]
FLEE_DISTANCE_THRESHOLD = 4


def manhattan_distance(a: position, b: position) -> int:
    """Return the Manhattan (grid) distance between two positions"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bfs_path(maza: Maze, start: position, goal: position
             ) -> Optional[list[position]]:
    """Find the shortest walkable path from start to goal (BFS).
    Returns None if no path exists (should not normally happen in a
    connected maze, but guards against edge cases like start == goal
    outside bounds).
    """
    if start == goal:
        return [start]

    visited = {start}
    queue: deque[list[position]] = deque([[start]])

    while queue:
        print(1)
        path = queue.popleft()
        current = path[-1]
        for neighbor in maza.neighbors(*current):
            if neighbor in visited:
                continue
            new_path = path + [neighbor]
            if neighbor == goal:
                return new_path
            visited.add(neighbor)
            queue.append(new_path)

    return None


def next_step_towards(maza: Maze, start: position, goal: position) -> position:
    """Return the next single cell to move to, on the shortest path to goal
    Falls back to staying in place if no path is found
    """
    path = bfs_path(maza, start, goal)
    if path and len(path) > 1:
        return path[1]
    return start


def flee_towards_farthest_neighbor(
        maza: Maze, ghost_pos: position, threat_pos: position
        ) -> position:
    """Pick the walkable neighbor cell that is farthest from threat_pos"""
    neighbors = maza.neighbors(*ghost_pos)
    if not neighbors:
        return ghost_pos
    return max(neighbors, key=lambda n: manhattan_distance(n, threat_pos))


def find_remaining_pacgums(maze: Maze) -> list[position]:
    """Scan the grid and return positions of all remaining pacgums
    NOTE: this is O(width * height). For large mazes, prefer maintaining
    a live set on the Maze/GameState instead of rescanning every call
    (see the "performance" note in the integration section below).
    """
    positions: list[position] = []
    for y in range(maze.height):
        for x in range(maze.width):
            if maze.grid[y][x].content in (Cell.PACGUM, Cell.SUPER_PACGUM):
                positions.append((x, y))
    return positions


def seek_nearest_pacgum(maze: Maze, ghost_pos: position, player_pos: position) -> position:
    """Move the ghost one step towards the nearest remaining pacgum.(player_pos unused)
    Step 1: use Manhattan distance as a cheap heuristic to pick a target
             among all remaining pacgums (no walls considered here).
    Step 2: use BFS to find the *real* shortest walkable path to that
             target, and return the first step of that path.
    """
    targets = find_remaining_pacgums(maze)
    if not targets:
        return ghost_pos
    nearest_target = min(
            targets, key=lambda t: manhattan_distance(ghost_pos, t))
    return next_step_towards(maze, ghost_pos, nearest_target)


def chase_then_flee(
        maze: Maze, ghost_pos: position, player_pos: position,
        flee_distance: int = FLEE_DISTANCE_THRESHOLD,
) -> position:
    """Chase the player via BFS, but flee if they get too close.
     - distance <= flee_distance -> pick the neighbor that maximizes
      distance from the player (flee).
     - distance  > flee_distance -> follow the BFS shortest path to the
      player (chase).
    """
    distance = manhattan_distance(ghost_pos, player_pos)

    if distance <= flee_distance:
        return flee_towards_farthest_neighbor(maze, ghost_pos, player_pos)

    return next_step_towards(maze, ghost_pos, player_pos)
