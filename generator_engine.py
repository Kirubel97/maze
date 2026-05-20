import pygame
import random
import sys

from maze_core import eat_wall_between

# GLOBAL CONFIGURATION & GRAPHICS ENGINE
R = 20  
C = 20  
CELL_SIZE = 30
WIDTH, HEIGHT = C * CELL_SIZE, R * CELL_SIZE

# Color Palette (High-Contrast Settings)
BG_COLOR = (255, 255, 255)       
WALL_COLOR = (20, 20, 20)        
GENERATOR_COLOR = (255, 51, 102) 
PATH_COLOR = (255, 0, 0)         
DEAD_END_COLOR = (0, 120, 255)   
START_PAD_COLOR = (46, 204, 113) 
GOAL_PAD_COLOR = (155, 89, 182)  

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

# 5% CYCLE GENERATION CHALLENGE LOGIC
def handle_cycle_generation(r, c):
    """Executes the 1-in-20 chance bonus to break into an already visited room"""
    if random.random() < 0.05:
        visited_neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            v_r, v_c = r + dr, c + dc
            if 0 <= v_r < R and 0 <= v_c < C and visited[v_r][v_c]:
                visited_neighbors.append((v_r, v_c))
        if visited_neighbors:
            cycle_r, cycle_c = random.choice(visited_neighbors)
            eat_wall_between(r, c, cycle_r, cycle_c)

# PYGAME UI RENDER LAYER
def run_graphics_loop():
    pygame.init()
    pygame.font.init()
    try:
        label_font = pygame.font.SysFont("Arial", 10, bold=True)
    except:
        label_font = pygame.font.Font(None, 18)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Assignment 1: Generator And Solver Simulation")
    clock = pygame.time.Clock()
    
    