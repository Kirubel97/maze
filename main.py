import pygame
import sys

from maze_core import (
    R, C, CELL_SIZE, WIDTH, HEIGHT, 
    northWall, eastWall, start_cell, end_cell
)
import generator_engine
import solver

BG_COLOR = (255, 255, 255)       
WALL_COLOR = (20, 20, 20)        
GENERATOR_COLOR = (255, 51, 102) 
PATH_COLOR = (255, 0, 0)         
DEAD_END_COLOR = (0, 120, 255)   

START_PAD_COLOR = (46, 204, 113) 
GOAL_PAD_COLOR = (155, 89, 182)  

START_FINISH_COLOR = (241, 196, 15) 
GOAL_FINISH_COLOR = (52, 152, 219) 

pygame.init()
pygame.font.init()

try:
    label_font = pygame.font.SysFont("Arial", 11, bold=True)
except:
    label_font = pygame.font.Font(None, 18)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Assignment 1: Generator And Solver Simulation")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not generator_engine.generation_complete:
        generator_engine.generation_step()
    else:
        solver.solver_step()

    screen.fill(BG_COLOR)

    sr, sc = start_cell
    start_x = sc * CELL_SIZE
    start_y = (R - 1 - sr) * CELL_SIZE
    current_start_color = START_FINISH_COLOR if solver.goal_found else START_PAD_COLOR
    pygame.draw.rect(screen, current_start_color, (start_x + 2, start_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

    er, ec = end_cell
    end_x = ec * CELL_SIZE
    end_y = (R - 1 - er) * CELL_SIZE
    current_goal_color = GOAL_FINISH_COLOR if solver.goal_found else GOAL_PAD_COLOR
    pygame.draw.rect(screen, current_goal_color, (end_x + 2, end_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

    if generator_engine.generation_complete:
        for r, c in solver.dead_ends:
            if (r, c) != start_cell and (r, c) != end_cell:
                pygame.draw.rect(screen, DEAD_END_COLOR, (c * CELL_SIZE + 8, (R - 1 - r) * CELL_SIZE + 8, CELL_SIZE - 16, CELL_SIZE - 16))
        for r, c in solver.solver_stack.items:
            if (r, c) != start_cell and (r, c) != end_cell:
                pygame.draw.rect(screen, PATH_COLOR, (c * CELL_SIZE + 9, (R - 1 - r) * CELL_SIZE + 9, CELL_SIZE - 18, CELL_SIZE - 18))

    
    for r in range(R):
        for c in range(C):
            x = c * CELL_SIZE
            y = (R - 1 - r) * CELL_SIZE
            if northWall[r + 1][c] == 1:
                pygame.draw.line(screen, WALL_COLOR, (x, y), (x + CELL_SIZE, y), 3)
            if eastWall[r][c + 1] == 1:
                pygame.draw.line(screen, WALL_COLOR, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 3)


    for c in range(C):
        if northWall[0][c] == 1:
            pygame.draw.line(screen, WALL_COLOR, (c * CELL_SIZE, HEIGHT - 2), ((c + 1) * CELL_SIZE, HEIGHT - 2), 3)
        if northWall[R][c] == 1:
            pygame.draw.line(screen, WALL_COLOR, (c * CELL_SIZE, 2), ((c + 1) * CELL_SIZE, 2), 3)
            
    for r in range(R):
        if eastWall[r][0] == 1:
            pygame.draw.line(screen, WALL_COLOR, (2, (R - 1 - r) * CELL_SIZE), (2, (R - r) * CELL_SIZE), 3)
        if eastWall[r][C] == 1:
            pygame.draw.line(screen, WALL_COLOR, (WIDTH - 2, (R - 1 - r) * CELL_SIZE), (WIDTH - 2, (R - r) * CELL_SIZE), 3)

    
    if not generator_engine.generation_complete:
        gr, gc = generator_engine.current_gen_cell
        if (gr, gc) != start_cell and (gr, gc) != end_cell:
            pygame.draw.rect(screen, GENERATOR_COLOR, (gc * CELL_SIZE + 6, (R - 1 - gr) * CELL_SIZE + 6, CELL_SIZE - 12, CELL_SIZE - 12))

    start_text_color = (40, 40, 40) if solver.goal_found else (20, 20, 20)
    text_start = label_font.render("START", True, start_text_color)
    screen.blit(text_start, (start_x + (CELL_SIZE - text_start.get_width()) // 2, start_y + (CELL_SIZE - text_start.get_height()) // 2))
    
    end_text_color = (255, 255, 255)
    text_end = label_font.render("END", True, end_text_color)
    screen.blit(text_end, (end_x + (CELL_SIZE - text_end.get_width()) // 2, end_y + (CELL_SIZE - text_end.get_height()) // 2))

    pygame.display.flip()
    clock.tick(15)

pygame.quit()
sys.exit()