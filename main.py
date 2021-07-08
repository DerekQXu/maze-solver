import os
from os.path import join
from pathlib import Path
import subprocess

from agent import Agent
from config import ANIMATION_FLAG, MAX_COST, MAX_ITER, MIN_COST, ROOT_DIR, TICK_SPEED, NO_LIB
from maze import Maze
from utils import PathTracker, compute_score

if NO_LIB:
    tqdm = lambda x: x
    ANIMATION_FLAG = False
else:
    from visualizer import visualize
    from tqdm import tqdm

def main():
    score_li = []
    for N in [5, 10, 20, 30, 40, 50]:
        n_mazes_per_size = 1
        for i in range(n_mazes_per_size):
            print(f"generating maze of size {N} ({i+1}/{n_mazes_per_size})")

            # init maze and agent
            maze = Maze(N, seed=(int((i + N) * 3.141592653) % 2021))
            print(f"maze generated!")
            agent = Agent(N)

            mid = f"{N}x{N}-run{i}"
            shortest_path_cost = get_shortest_path_cost(maze)
            score_li.append(run_simulation(mid, maze, agent, shortest_path_cost))
    print(f"final score: {sum(score_li)/len(score_li)}")


def run_simulation(mid, maze, agent, shortest_path_cost):
    next_cell_sanitized = None
    next_adjacent_cells_sanitized = [get_sanitized_cell(maze.entrance_cell)]
    path_tracker = PathTracker(maze.entrance_cell)
    candidate_cells = {maze.entrance_cell}
    candidate_cells_sanitized = {get_sanitized_cell(maze.entrance_cell)}
    explored_cells = set()

    animation_li = []
    found_end = False
    number_iterations = 1
    for _ in tqdm(range(MAX_ITER)):
        # time.sleep(0.1)
        next_cell_sanitized = agent.select_action(
            list(candidate_cells_sanitized),
            next_adjacent_cells_sanitized,
            next_cell_sanitized,
        )

        # get next action
        next_cell = get_unsanitized_cell(next_cell_sanitized, maze)
        assert next_cell in candidate_cells.union(explored_cells)

        # get next adjacent_cells
        next_adjacent_cells_sanitized = [
            get_sanitized_cell(cell) for cell in next_cell.adj_set
        ]

        # get next candidate_cells
        explored_cells.add(next_cell)
        candidate_cells.update(next_cell.adj_set)
        candidate_cells = candidate_cells - explored_cells
        candidate_cells_sanitized = {
            get_sanitized_cell(cell) for cell in candidate_cells
        }

        # update backtracking
        if next_cell != maze.entrance_cell:
            path_tracker.add_cell(next_cell)

        # update animation
        if ANIMATION_FLAG:
            mat = cvt_to_matrix(maze, candidate_cells, explored_cells, next_cell)
            animation_li.append(mat)

        # exit condition
        if agent.done:
            if path_tracker.is_tracked(maze.end_cell):
                found_end = True
            break
        number_iterations += 1

    score, breakdown = compute_score(
        found_end,
        explored_cells,
        maze.end_cell.cost_to_cell,
        maze.N,
        shortest_path_cost,
    )
    print(
        f'score: {score}\n\tbreakdown: {",".join(f"{key}:{val}" for key, val in breakdown.items())}'
    )

    if ANIMATION_FLAG:
        print("\tanimating...")
        visualize(
            animation_li,
            Path(join(ROOT_DIR, "results", f"{mid}.gif")),
            delay=TICK_SPEED,
            scale=5,
        )
    print("============================")

    return score


def get_shortest_path_cost(maze):
    path_tracker = PathTracker(maze.entrance_cell)
    candidate_cells = {maze.entrance_cell}
    explored_cells = set()

    while candidate_cells:
        next_cell = candidate_cells.pop()

        # get next candidate_cells
        explored_cells.add(next_cell)
        candidate_cells.update(next_cell.adj_set)
        candidate_cells = candidate_cells - explored_cells

        # update backtracking
        if next_cell != maze.entrance_cell:
            path_tracker.add_cell(next_cell)

    # compute shortest path and clean up cells
    shortest_path = maze.end_cell.cost_to_cell
    for cell in maze.maze_dict.values():
        cell.cost_to_cell = None

    return shortest_path


def cvt_to_matrix(maze, explored_cells, next_adjacent_cells, cur_cell):
    matrix = [[0.1 for _ in range(maze.N)] for _ in range(maze.N)]
    e_keys = [cell.get_loc() for cell in explored_cells]
    n_keys = [cell.get_loc() for cell in next_adjacent_cells]
    for (i, j), cell in maze.maze_dict.items():
        if cell.get_loc() == cur_cell.get_loc():
            matrix[i][j] = "C"
        elif cell.get_loc() in n_keys:
            matrix[i][j] = "N"
        elif cell.get_loc() in e_keys:
            matrix[i][j] = "T"
        elif cell.is_wall:
            matrix[i][j] = "W"
        else:
            matrix[i][j] = (float(cell.terrain) - MIN_COST) / MAX_COST
    return matrix


def get_sanitized_cell(cell):
    return cell.x, cell.y, cell.terrain


def get_unsanitized_cell(sanitized_cell, maze):
    x, y, _ = sanitized_cell
    cell = maze.maze_dict[(x, y)]
    return cell


if __name__ == "__main__":
    blocked = ["main.py", "maze.py", "perlin.py", "utils.py"] * (os.name == "posix")

    for file in blocked:
        subprocess.call(["chmod", "000", Path(ROOT_DIR) / file])

    main()

    for file in blocked:
        subprocess.call(["chmod", "644", Path(ROOT_DIR) / file])
