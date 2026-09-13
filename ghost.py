"""Ghost movement : BFS pathfinding and chase/flee/random behaviors.
This module is deliberately decoupled from pygame: it only reasons about
grid positions (x, y) and the Maze/Cell data structures. The actual
rendering/movement interpolation stays in your Ghost/sprite class.
"""

import random
from collections import deque
from typing import Optional

from cell import Cell
from maze import Maze

position = tuple[int, int]
FLEE_DISTANCE_THRESHOLD = 4
PLAYER_BASE_SPEED = 90.0 


def manhattan_distance(a: position, b: position) -> int:
    """Return the Manhattan (grid) distance between two positions."""
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


def random_walk(
        maza: Maze, ghost_pos: position, player_pos: position,
        previous_pos: Optional[position] = None,
        ) -> position:
    """Move the ghost to a random walkable neighbor cell.

    Args:
        maza: The current Maze, used to find walkable neighbors.
        ghost_pos: The ghost's current (x, y) grid position.
        player_pos: Unused (kept for a consistent behavior signature).
        previous_pos: The cell the ghost was in just before this one,
            used to avoid backtracking immediately.

    Returns:
        A randomly chosen neighbor cell (never the previous one unless
        it's the only walkable neighbor), or ghost_pos if it has none.    """
    neighbors = maza.neighbors(*ghost_pos)
    if not neighbors:
        return ghost_pos
    if previous_pos is not None and len(neighbors) > 1:
        neighbors = [n for n in neighbors if n != previous_pos]
    return random.choice(neighbors)


def find_remaining_pacgums(maze: Maze) -> list[position]:
    """Scan the grid and return positions of all remaining pacgums
    NOTE: this is O(width * height). For large mazes, prefer maintaining
    a live set on the Maze/GameState instead of rescanning every call
    (see the "performance" note in the integration section below).
    """
    positions: list[position] = []
    for y in range(maze.height):
        for x in range(maze.width):
            content_id = maze.grid[y][x].content_id
            if content_id in (Cell.PACGUM, Cell.SUPER_PACGUM):
                positions.append((x, y))
    return positions


def seek_pacgum_near_player(
        maze: Maze, ghost_pos: position, player_pos: position
) -> position:
    """Move ghost towards the pacgum closest to the player.

    Falls back to chasing the player directly once the ghost reaches
    its target gum (so it doesn't freeze camping on the last cell) or
    when no gums remain at all.
    """
    targets = find_remaining_pacgums(maze)
    if not targets:
        return next_step_towards(maze, ghost_pos, player_pos)

    best_gum = min(targets, key=lambda gum: manhattan_distance(gum, player_pos))

    if ghost_pos == best_gum:
        return next_step_towards(maze, ghost_pos, player_pos)

    return next_step_towards(maze, ghost_pos, best_gum)


def chase_then_flee(
        maze: Maze, ghost_pos: position, player_pos: position,
        flee_distance: int = FLEE_DISTANCE_THRESHOLD,
) -> position:
    """Chase the player via BFS, but flee if they get too close.
     - distance <= flee_distance -> pick the neighbor that maximizes
      distance from the player (flee).
     - distance  > flee_distance -> follow the BFS shortest path to
      the player (chase).
    """
    distance = manhattan_distance(ghost_pos, player_pos)

    if distance <= flee_distance:
        return flee_towards_farthest_neighbor(maze, ghost_pos, player_pos)

    return next_step_towards(maze, ghost_pos, player_pos)


def ghost_speed_for_level(
        level: int,
        base_speed: float = PLAYER_BASE_SPEED,
        increment: float = 12.0,
        max_speed: float = 200.0,
) -> float:
    """Compute ghost speed for a given level.

    Level 1 matches the player's speed exactly; each subsequent level
    adds `increment` px/sec, capped at `max_speed` so late levels stay
    winnable instead of becoming impossible.
    """
    return min(base_speed + increment * max(level - 1, 0), max_speed)