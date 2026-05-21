# ========================================================
# PATHFINDER MOUSE BRAIN & SOLVER LOGIC
# ========================================================

solver_stack = Stack()
solver_visited = set()
dead_ends = set()
solver_current = start_cell

solver_stack.push(solver_current)
solver_visited.add(solver_current)
goal_found = False


def solver_step():
    """Calculates path movements and logs backtracking sequences"""
    global solver_current, goal_found
    if solver_stack.is_empty() or goal_found:
        return

    r, c = solver_current
    if (r, c) == end_cell:
        goal_found = True
        return

    possible_moves = []
    # Verify open paths by ensuring wall layout flags equal 0 (No wall exists)
    if r + 1 < R and northWall[r + 1][c] == 0:
        possible_moves.append((r + 1, c))
    if r - 1 >= 0 and northWall[r][c] == 0:
        possible_moves.append((r - 1, c))
    if c + 1 < C and eastWall[r][c + 1] == 0:
        possible_moves.append((r, c + 1))
    if c - 1 >= 0 and eastWall[r][c] == 0:
        possible_moves.append((r, c - 1))

    valid_moves = [
        m for m in possible_moves if m not in solver_visited and m not in dead_ends]

    if valid_moves:
        next_cell = random.choice(valid_moves)
        solver_stack.push(next_cell)
        solver_visited.add(next_cell)
        solver_current = next_cell
    else:
        # Backtracking Logic: If stuck, add to dead ends, pop stack, and step back
        dead_ends.add((r, c))
        solver_stack.pop()
        if not solver_stack.is_empty():
            solver_current = solver_stack.peek()
