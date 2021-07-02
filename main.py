from maze import Maze, Cell
from agent import Agent
from config import MAX_COST, MIN_COST, ROOT_DIR, TICK_SPEED
from os.path import join

from visualizer import visualize
from pathlib import Path
import time

def main():
    for N in [5,7,9]:
        n_mazes_per_size = 1
        for i in range(n_mazes_per_size):
            print(f'generating maze of size {N} ({i+1}/{n_mazes_per_size})')
            
            # init maze and agent
            maze = Maze(N, seed=(int((i+N)*3.141592653)%2021))
            print(f'maze generated!')
            # animator.reset(maze)
            agent = Agent(N)

            mid = f'{N}x{N}-run{i}'
            run_simulation(mid, maze, agent)

def run_simulation(mid, maze, agent):
    next_cell_sanitized = None
    next_adjacent_cells = [maze.entrance_cell]
    candidate_cells = {maze.entrance_cell}
    explored_cells = set()

    animation_li = []
    iteration_count = 0
    while True:
        # time.sleep(0.1)
        next_cell_sanitized = agent.select_action(next_adjacent_cells, next_cell_sanitized)
        next_cell = get_unsanitized_cell(next_cell_sanitized, maze)
        
        # check if valid action
        assert next_cell in candidate_cells.union(explored_cells)
        explored_cells.add(next_cell)
        candidate_cells.update(next_cell.adj_set)
        candidate_cells = candidate_cells - explored_cells
        
        # get newly reachable cells
        next_adjacent_cells = [get_sanitized_cell(cell) for cell in next_cell.adj_set]

        mat = cvt_to_matrix(maze, candidate_cells, explored_cells, next_cell_sanitized)
        animation_li.append(mat)

        # exit condition
        if agent.done:
            assert maze.end_cell.get_loc() in agent.backtracking_path
            break
        
        iteration_count += 1

    path, path_score = get_path(maze, agent.backtracking_path)
    print('animating...')
    visualize(animation_li, Path(join(ROOT_DIR,'results',f'{mid}.gif')), delay=TICK_SPEED)

    print(f'statistics:\n explored {len(explored_cells)} cells\n path score: {path_score}\n--------------------')
    time.sleep(0.1)

def cvt_to_matrix(maze, explored_cells, next_adjacent_cells, cur_cell):
    matrix = [[0.1 for _ in range(maze.N)] for _ in range(maze.N)]
    e_keys = [cell.get_loc() for cell in explored_cells]
    n_keys = [cell.get_loc() for cell in next_adjacent_cells]
    for (i,j), cell in maze.maze_dict.items():
        if cell.get_loc() == cur_cell.get_loc():
            matrix[i][j] = 'C'
        elif cell.get_loc() in n_keys:
            matrix[i][j] = 'N'
        elif cell.get_loc() in e_keys:
            matrix[i][j] = 'T'
        elif cell.is_wall:
            matrix[i][j] = 'W'
        else:
            matrix[i][j] = (float(cell.terrain) - MIN_COST) / MAX_COST
    return matrix

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