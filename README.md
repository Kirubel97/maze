# 🐭 Maze Generator & Solver (Pygame)

A visual simulation of **randomized maze generation and solving**, built with Python and Pygame. Watch an invisible "mouse" carve a solvable maze from a solid grid, then follow a second mouse as it finds the exit using backtracking.

## 🗺️ How the Maze is Generated

### Starting State

The maze begins as a complete grid, every cell is surrounded by four walls (north, south, east, west). No passages exist.

### The Generator Mouse (Stack-Based DFS)

An invisible **"mouse"** is placed in an arbitrarily chosen cell. Its job is to **eat through walls** to connect adjacent cells, carving a spanning tree through the grid using **iterative depth-first search (DFS)** with an explicit stack.

At each step, the mouse:

1. Checks its four neighbors.
2. Identifies which neighbors still have **all four walls intact** .
3. **Randomly picks one** unvisited neighbor, saves the others onto a stack, erases the connecting wall, and moves into the chosen cell.
4. Repeats until it reaches a **dead end** where all the neighbors are visited.
5. At a dead end, it **pops the stack** to backtrack to the most recent cell that still has unvisited neighbors, and continues from there.
6. When the **stack is empty**, every cell has been visited. The maze is complete.

> **💡 Why a stack and not a queue?**
> A stack enforces last-in, first-out backtracking, which means the mouse always continues from the *most recently reached* cell. This produces **long, winding corridors** with relatively few branches.
>
> A **queue** would produce breadth-first generation instead. Rather than carving deep passages, it would expand the frontier evenly in all directions, creating **shorter, more branching corridors** that feel busier and less "tunnellike." The overall maze structure would look fundamentally different, it's wider but shallower paths, with many more branches near the start.

### Cycle Creation

Normally, a DFS-generated maze is a tree with no loops. This means it can always be solved using the *shoulder-to-the-wall* rule: simply keep one hand on the left-hand wall and you will always reach the exit, since there are no encircling loops to trap you.

To defeat this strategy, **with roughly 1-in-20 probability** at each step, the mouse eats an *extra* wall into an already-visited neighbor. This creates **cycles** in the graph, forming enclosed loops that can surround the goal cell and break the shoulder-to-the-wall method.

> **📐 Why does the shoulder-to-the-wall rule still work without cycles?**
> Because a cycle-free maze is a **tree**, and a tree is a connected graph with no loops. Every path between two cells is unique. Tracing a wall continuously will follow that unique path without ever circling back on itself, so as long as start and end are both on the outer boundary, you are guaranteed to reach the end. Add cycles, and this guarantee breaks down.

## 🔴 How the Maze is Solved

Once generation is complete, a **second mouse** starts at the `START` cell and searches for the `END` cell using **iterative DFS with backtracking** the same as generation.

At each step, the solver:

1. Tries to move in a random valid direction.
2. If a move is possible, it pushes the new cell onto the solver stack, marks it visited, and moves there. This cell is drawn with a **red dot**.
3. If no moves are possible (dead end): marks the current cell **blue** (a dead end), pops it from the stack, and backtracks to the previous cell. A "wall" is logically raised to prevent revisiting.
4. Continues until the `END` cell is reached.


## 🎮 Features

- **Randomized Maze Generation** via stack-based DFS with occasional extra wall-eating for cycles.
- **Live Solver Visualization:**
  - 🔴 **Red cells** — the current active solving path (solver stack contents).
  - 🔵 **Blue cells** — backtracked dead ends (never revisited).
- **Random Start & End Cells** chosen along maze boundaries.
- **Dynamic Wall Rendering** — walls are drawn only where they still exist.
- **Animated Phase Transition** — generation runs first; solving begins automatically once every cell is carved.
- **Highlighted Cells** — start (green → gold on finish) and end (purple → blue on finish).


## ⚙️ Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/)

```bash
pip install pygame
```



## ▶️ Running the Simulation

```bash
python maze.py
```

The window will open and immediately begin the generation phase. Once the maze is fully carved, the solver mouse will start automatically.


## 🔧 Configuration

At the top of `maze.py`, you can adjust the following constants:

| Constant    | Default | Description                        |
|-------------|---------|------------------------------------|
| `R`         | `15`    | Number of rows                     |
| `C`         | `15`    | Number of columns                  |
| `CELL_SIZE` | `42`    | Pixel size of each cell            |
| `clock.tick(15)` | `15` | Simulation speed (frames/second) |



## 📚 Concepts Demonstrated

- **Iterative DFS** using an explicit `Stack` class 
- **Graph representation** via wall arrays (`northWall`, `eastWall`) 
- **Backtracking** for both generation and solving
- **Cycle injection** to defeat simple maze-solving heuristics
- **Coordinate system mapping** between grid logic and Pygame screen space
