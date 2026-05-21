# ========================================================
# DATA STRUCTURES & GRID INITIALIZATION
# ========================================================
import random

# Core Grid Dimensions
R = 15  
C = 15  
CELL_SIZE = 42
WIDTH, HEIGHT = C * CELL_SIZE, R * CELL_SIZE

# Data Structures (northWall includes the extra phantom row at R index)
northWall = [[1] * C for _ in range(R + 1)]   
eastWall = [[1] * (C + 1) for _ in range(R)]  
visited = [[False] * C for _ in range(R)]

class Stack:
    def __init__(self):
        self.items = []
    def push(self, val):
        self.items.append(val)
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    def peek(self):
        return self.items[-1] if not self.is_empty() else None
    def is_empty(self):
        return len(self.items) == 0

def eat_wall_between(r1, c1, r2, c2):
    """Removes a wall between two cells cleanly"""
    if r2 > r1:       northWall[r2][c2] = 0        # Move North
    elif r1 > r2:     northWall[r1][c1] = 0        # Move South
    elif c2 > c1:     eastWall[r1][c1 + 1] = 0     # Move East
    elif c1 > c2:     eastWall[r2][c2 + 1] = 0     # Move West

def choose_boundary_cells():
    """Selects distinct start and end cells on the outer perimeter"""
    boundaries = []
    for c in range(C):
        boundaries.append((R - 1, c, 'N')) 
        boundaries.append((0, c, 'S'))     
    for r in range(R):
        boundaries.append((r, 0, 'W'))     
        boundaries.append((r, C - 1, 'E')) 
        
    start_choice = random.choice(boundaries)
    boundaries = [b for b in boundaries if (b[0], b[1]) != (start_choice[0], start_choice[1])]
    end_choice = random.choice(boundaries)
    
    return (start_choice[0], start_choice[1]), (end_choice[0], end_choice[1]), start_choice[2], end_choice[2]

start_cell, end_cell, start_wall, end_wall = choose_boundary_cells()