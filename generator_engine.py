# ========================================================
# STEP-BY-STEP MAZE GENERATION ENGINE
# ========================================================

gen_stack = Stack()
current_gen_cell = (random.randint(0, R - 1), random.randint(0, C - 1))
visited[current_gen_cell[0]][current_gen_cell[1]] = True
gen_stack.push(current_gen_cell)
generation_complete = False

def generation_step():
    """Executes a single step of the randomized maze generation animation"""
    global current_gen_cell, generation_complete
    if gen_stack.is_empty():
        generation_complete = True
        return

    r, c = current_gen_cell
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C and not visited[nr][nc]:
            neighbors.append((nr, nc))

    if neighbors:
        next_r, next_c = random.choice(neighbors)
        
        # Addendum Challenge: 1 out of 20 times (5%), eat into an already visited neighbor to create cycles
        if random.random() < 0.05:
            visited_neighbors = []
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                v_r, v_c = r + dr, c + dc
                if 0 <= v_r < R and 0 <= v_c < C and visited[v_r][v_c]:
                    visited_neighbors.append((v_r, v_c))
            if visited_neighbors:
                cycle_r, cycle_c = random.choice(visited_neighbors)
                eat_wall_between(r, c, cycle_r, cycle_c)

        # Flawless wall removal logic and coordinate movement tracking
        eat_wall_between(r, c, next_r, next_c)
        visited[next_r][next_c] = True
        gen_stack.push((next_r, next_c))
        current_gen_cell = (next_r, next_c)
    else:
        gen_stack.pop()
        if not gen_stack.is_empty():
            current_gen_cell = gen_stack.peek()

# final suubmission