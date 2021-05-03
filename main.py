from maze import Maze, Cell
from drawer import Animator
from agent import Agent

import time
import copy

def main():
    for N in [10]:
        n_mazes_per_size = 1
        for i in range(n_mazes_per_size):
            print(f'generating maze of size {N} ({i+1}/{n_mazes_per_size})')
            
            # init maze and agent
            maze = Maze(N, seed=(int((i+N)*3.141592653)%2021))
            agent = Agent(N)
            animator = Animator(maze)
            
            run_simulation(maze, agent, animator)
            
            del maze
            del agent
            del animator
            
def run_simulation(maze, agent, animator):
    next_cell_sanitzed = None
    next_adjacent_cells = [maze.entrance_cell]
    candidate_cells = {maze.entrance_cell}
    explored_cells = set()
    
    iteration_count = 0
    while True:
        time.sleep(0.1)
        next_cell_sanitzed = agent.select_action(next_adjacent_cells, next_cell_sanitzed)
        next_cell = get_unsanitized_cell(next_cell_sanitzed, maze)
        
        # check if valid action
        assert next_cell in candidate_cells.union(explored_cells)
        explored_cells.add(next_cell)
        candidate_cells.update(next_cell.adj_set)
        candidate_cells = candidate_cells - explored_cells
        
        # get newly reachable cells
        next_adjacent_cells = [get_sanitized_cell(cell) for cell in next_cell.adj_set]
        
        animator.draw_frame(next_cell, explored_cells, candidate_cells)
        
        # exit condition
        if agent.done:
            assert maze.end_cell.get_loc() in agent.backtracking_path
            break
        
        iteration_count += 1
    
    print('getting path')
    path, path_score = get_path(maze, agent.backtracking_path)
    print(path)
    print('drawing path')
    animator.draw_path(path)
    print(f'statistics:\n explored {len(explored_cells)} cells\n path score: {path_score}\n--------------------')
    time.sleep(0.1)
 
def get_sanitized_cell(cell):
    sanitized_cell = Cell(cell.x, cell.y, cell.terrain, cell.is_wall)
    return sanitized_cell

def get_unsanitized_cell(sanitized_cell, maze):
    x,y = sanitized_cell.x, sanitized_cell.y
    cell = maze.maze_dict[(x,y)]
    return cell
 
def get_path(maze, backtrack_dict):
    path = [maze.end_cell.get_loc()]
    path_score = maze.end_cell.terrain
    while maze.entrance_cell.get_loc() not in path:
        cur_loc = path[-1]
        last_loc = backtrack_dict[cur_loc]
        assert last_loc in [cell.get_loc() for cell in maze.maze_dict[cur_loc].adj_set]
        path.append(last_loc)
        path_score += maze.maze_dict[last_loc].terrain
    path = path[::-1]
    return path, path_score

def pause(secs):
    init_time = time.time()
    while time.time() < init_time+secs: pass

if __name__ == '__main__':
    main()
# mz = Maze(30)
# draw_maze(mz)
# time.sleep(3)