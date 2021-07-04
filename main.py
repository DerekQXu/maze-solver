from maze import Maze
from agent import Agent
from utils import PathTracker
from config import MAX_COST, MIN_COST, ROOT_DIR, TICK_SPEED

from os.path import join
from tqdm import tqdm
from visualizer import visualize
from pathlib import Path
import time

MAX_ITERATIONS = 1000

def main():
    for N in [3,5,10,20,50,100]:
        n_mazes_per_size = 2
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
    # next_cell_sanitized = None
    # next_adjacent_cells = [get_sanitized_cell(maze.entrance_cell)]
    path_tracker = PathTracker(maze.entrance_cell)
    candidate_cells = {maze.entrance_cell}
    candidate_cells_sanitized = {get_sanitized_cell(maze.entrance_cell)}
    explored_cells = set()

    animation_li = []
    for _ in tqdm(range(MAX_ITERATIONS)):
        # time.sleep(0.1)
        next_cell_sanitized = agent.select_action(candidate_cells_sanitized)

        next_cell = get_unsanitized_cell(next_cell_sanitized, maze)
        
        # check if valid action
        assert next_cell in candidate_cells.union(explored_cells)
        explored_cells.add(next_cell)
        candidate_cells.update(next_cell.adj_set)
        candidate_cells = candidate_cells - explored_cells
        
        # get newly reachable cells
        # next_adjacent_cells = [get_sanitized_cell(cell) for cell in next_cell.adj_set]
        # agent.update_backtracking_path(
        #     [get_sanitized_cell(cell) for cell in next_cell.adj_set],
        #     get_sanitized_cell(next_cell)
        # )
        if next_cell != maze.entrance_cell:
            path_tracker.add_cell(next_cell)
        candidate_cells_sanitized = {get_sanitized_cell(cell) for cell in candidate_cells}

        mat = cvt_to_matrix(maze, candidate_cells, explored_cells, next_cell)
        animation_li.append(mat)

        # exit condition
        if agent.done:
            assert path_tracker.is_tracked(maze.end_cell) # maze.end_cell.get_loc() in agent.backtracking_path
            break

    path, path_score = path_tracker.get_best_path_wrapper(maze.entrance_cell, maze.end_cell), maze.end_cell.cost_to_cell
    print('animating...')
    visualize(animation_li, Path(join(ROOT_DIR,'results',f'{mid}.gif')), delay=TICK_SPEED, scale=5)

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
    return (cell.x, cell.y, cell.terrain)

def get_unsanitized_cell(sanitized_cell, maze):
    x,y,_ = sanitized_cell
    cell = maze.maze_dict[(x,y)]
    return cell

if __name__ == '__main__':
    main()