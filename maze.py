from perlin import perlin_noise
from config import MAX_COST, MIN_COST, SCALE, BIAS

import random


class Cell:
    def __init__(self, x: int, y: int, terrain: float, is_wall: bool):
        assert x >= 0 and y >= 0 and terrain > 0, print(x,y,terrain)
        self.x = x
        self.y = y
        self.terrain = terrain
        self.is_wall = is_wall
        self.adj_set = set()
     
    def get_loc(self):
        return self.x, self.y

class Maze:
    def __init__(self, N: int, seed: int):
        random.seed(seed)
        offset = random.random()
        self.maze_dict = {}
        self.N = N
        # make empty maze with terrain
        for i in range(self.N):
            for j in range(self.N):
                terrain = \
                    max(
                        min(
                            abs(
                                SCALE*perlin_noise(
                                    offset + i/self.N, offset + j/self.N, 0
                                )
                            ) + BIAS, 
                            MAX_COST
                        ),
                        MIN_COST
                    )
                self.maze_dict[(i,j)] = Cell(i, j, terrain, False)
        
        # add walls
        for i in range(self.N-4):
            self.maze_dict[(self.N-3,i)].is_wall = True
        for i in range(self.N-7, self.N-2):
            self.maze_dict[(i,self.N-4)].is_wall = True
        
        # link cells
        self._link_cells()
        
        self.entrance_cell = self.maze_dict[(0,0)]
        self.end_cell = self.maze_dict[(self.N-1,self.N-1)]
    
    def _link_cells(self):
        for (i,j), cell in self.maze_dict.items():
            up_key = (i,j+1)
            down_key = (i,j-1)
            right_key = (i+1,j)
            left_key = (i-1,j)
            adjacent_cells = \
                [
                    self.maze_dict[key] \
                    for key in [up_key, down_key, right_key, left_key] \
                    if key in self.maze_dict and not self.maze_dict[key].is_wall
                ]
            cell.adj_set.update(adjacent_cells)