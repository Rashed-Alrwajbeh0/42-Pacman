*This activity has been created as part of the 42 curriculum by \<aoqaily\>, \<ralrawaj\>.*

# Pac-Man

## Description
A playable, object-oriented Python re-creation of the 1980 arcade classic. The player guides Pac-Man through a maze eating pacgums while four ghosts, each running a distinct AI strategy, hunt him down. Super-pacgums make ghosts edible briefly. The game is won after 10 levels, lost when all lives are gone.

Distinguishing features: mazes generated at runtime by an external `mazegenerator` package (level 1 fixed-seed, later levels random), game parameters driven by a JSON config, a persistent top-10 highscore table, remappable controls, and a cheat mode for review.

## Instructions
**Requirements:** Python 3.10+, `pygame-ce` (not `pygame` — the game uses APIs only in pygame-ce ≥ 2.5), `pydantic`, `mazegenerator`.

```bash
python3 -m venv venv
source venv/bin/activate
make install   # installs requirements.txt, incl. mazegenerator wheel
make run       # or: python3 pac-man.py config.json
```

The program takes exactly one JSON config path as its single argument. All errors (missing file/key, bad value) are reported as clear messages, never as tracebacks.

Other targets: `make debug` (pdb), `make clean`, `make lint`, `make lint-strict`.

**Controls:** Arrow keys to move, Space to pause. All movement keys are remappable/resettable from the Controls screen.

## Configuration
JSON file; lines starting with `#` are treated as comments.

| Key | Type | Default | Meaning |
|---|---|---|---|
| `highscore_filename` | str | "output" | Highscore file name |
| `lives` | int | 3 | Starting lives |
| `pacgum` | int | 50 | Pacgums per maze |
| `points_per_pacgum` | int | 10 | Score per pacgum |
| `points_per_super_pacgum` | int | 50 | Score per super-pacgum |
| `points_per_ghost` | int | 200 | Score per edible ghost eaten |
| `level_max_time` | int | 120 | Seconds per level |

Validation is forgiving (via pydantic validators in `config.py`): a missing key uses the default with a warning; an invalid value is clamped to the default with a warning; unknown keys are ignored with a warning; a malformed file falls back entirely to defaults. The game never crashes on bad config.

## Highscore
Scores are stored as a JSON **list of independent records** (`{"name": ..., "score": ...}`), not a name-keyed dictionary. On game end the player enters a name, the record is appended, the list is sorted descending, and only the top 10 are persisted.

**Why a list, not a dict:** a dictionary keyed by name silently overwrites entries — two players named `ahmad`, or the same player replaying, would lose a prior score. A list treats the name as a label, not an identity, so duplicates coexist like on a real arcade cabinet, and ranking depends purely on score. JSON was chosen over a database for simplicity, readability, and git-diffability at this scale. Loading is defensive: any missing/empty/invalid/non-list file resolves to an empty table rather than an exception.

## Maze Generation
Mazes are produced entirely by the assigned external package, called as:
```python
MazeGenerator(size=(width, height), perfect=False, seed=seed)
```
`perfect=False` is required by the subject so the maze has loops instead of being a dead-end tree. `seed=42` for level 1 (reproducible), `seed=0` after (randomized). Generator failures are caught and re-raised as a readable `RuntimeError`.

Each cell is returned as a wall bitmask (bit 0=N, 1=E, 2=S, 3=W) decoded by `Cell`; a value of 15 (all walls) is treated as solid. The grid is row-major, indexed `grid[y][x]`. Super-pacgums go in the four corners, regular pacgums are scattered into reachable non-corner cells (bounded placement loop to avoid infinite loops on tiny mazes), the player starts centered, ghosts start in the corners.

## Implementation
Movement happens in pixel space (not per-cell jumps) for smooth motion, with ghost speed scaled by `dt` so it's frame-rate independent. Pac-Man keeps moving in his current direction if a turn is blocked (arcade-accurate behavior).

Ghost AI (pure, pygame-free, BFS-based pathfinding in `ghost.py`):

| Ghost | Strategy |
|---|---|
| Red | Chases via BFS but flees within 4 cells |
| Orange | Pure BFS pursuit |
| Pink | Targets the gum nearest the player |
| Cyan | Random walk, no immediate backtracking |

Each ghost has 4 states: Chasing, Edible (after a super-pacgum), Eaten (returning home), Waiting. Score only increases and carries across levels. Every external resource (files, images, config) degrades safely instead of raising — no traceback should ever reach the user.

## General Software Architecture
```
pac-man.py    Entry point: arg validation, pygame init, top-level loop
├── config.py     Config model + JSON loading/validation (pydantic)
├── menu.py       Main menu + routing to all screens
│   ├── game.py           Core game loop
│   │   ├── maze.py       Maze generation, gum placement, drawing
│   │   │   └── cell.py   Cell + Gum/Pac_Gum/Super_Pac_Gum/PacMan
│   │   ├── ghost.py          Pure pathfinding + behaviors (no pygame)
│   │   ├── ghost_entity.py   Ghost state machine, movement, rendering
│   │   ├── hud.py / pause.py / render.py
│   ├── scores.py / controls.py / instructions.py / end_screens.py
└── highscore.py  Persistent top-10 storage
```
Key design choice: `ghost.py` (pure grid logic) is separated from `ghost_entity.py` (pygame rendering/state), so AI strategies can be added and tested without a display. `config.py` is a leaf dependency imported everywhere but depending on nothing game-related.

## Cheat Mode
Activated via right-click on the Pac-Man artwork on the main menu. F1 invincibility, F2 skip level, F3 +1 life, F4 speed boost, F5 freeze ghosts, F6 toggle timer.

## Project Management
Work was split along module boundaries (config/validation, maze integration, ghost AI, UI screens) and integrated through pair walkthroughs. Planning material, progress tracking, risk analysis, task split, and the acceptance test plan live in `project_management/`.

## Resources
- [pygame-ce documentation](https://pyga.me/docs/)
- [pydantic documentation](https://docs.pydantic.dev/)
- The Pac-Man Dossier (ghost AI/timing reference)
- Breadth-first search (Youtube)
- PEP 257 — Docstring Conventions
- The assigned A-Maze-ing package's own documentation

**AI usage:** AI was used only as a reviewing/debugging aid, not to write unreviewed code. It helped diagnose a level-timer reset bug, caught a `grid[x][y]`/`grid[y][x]` indexing bug and an unbounded gum-placement loop, contributed to the highscore data-model discussion (list vs. dict, above), and helped draft/structure this README. All AI-assisted output was read, tested, and understood by us.
