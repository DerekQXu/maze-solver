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
        self._recursive_maze_generation()
        # for i in range(self.N-4):
            # self.maze_dict[(self.N-3,i)].is_wall = True
        # for i in range(self.N-7, self.N-2):
            # self.maze_dict[(i,self.N-4)].is_wall = True
        
        # link cells
        self._link_cells()
        
        self.entrance_cell = self.maze_dict[(0,0)]
        self.end_cell = self.maze_dict[(self.N-1,self.N-1)]
    
    def _recursive_maze_generation(self):
        split_stack = [Surface((0,0), (self.N, self.N), 'vert')]
        while split_stack:
            # split the surface
            cur_surface = split_stack.pop()
            if cur_surface.min_dim() < 3:
                continue
            split_idx, path_idx, new_surfaces = cur_surface.split()
            split_stack.extend(new_surfaces)
            
            # add the walls
            if cur_surface.direction == 'vert':
                for i in range(cur_surface.height):
                    if i == path_idx:
                        continue
                    self.maze_dict[
                            (
                                cur_surface.x_offset + split_idx, 
                                cur_surface.y_offset + i
                            )
                        ].is_wall = True
                    
            elif cur_surface.direction == 'hori':
                for i in range(cur_surface.width):
                    if i == path_idx:
                        continue
                    self.maze_dict[
                            (
                                cur_surface.x_offset + i, 
                                cur_surface.y_offset + split_idx
                            )
                        ].is_wall = True
            else:
                assert False
                
    
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

class Surface:
    def __init__(self, offset_coord, dimensions, direction):
        self.x_offset, self.y_offset = offset_coord
        self.width, self.height = dimensions
        self.direction = direction
        
    def split(self):
        if self.direction == 'vert':
            dim_primary = self.width
            dim_secondary = self.height
            offset_primary = self.x_offset
            offset_secondary = self.y_offset
        elif self.direction == 'hori':
            dim_primary = self.height
            dim_secondary = self.width
            offset_primary = self.y_offset
            offset_secondary = self.x_offset
        else:
            assert False
        
        split_idx = int(random.random() * (dim_primary-2)) + 1
        path_idx = int(random.random() * dim_secondary)
        
        primary_axis_split_L = (offset_primary, split_idx)
        primary_axis_split_R = (offset_primary+split_idx+1, dim_primary-split_idx-1)
        secondary_axis_split_L = (offset_secondary, path_idx)
        secondary_axis_split_R = (offset_secondary+path_idx+1, dim_secondary-path_idx-1)
        
        new_split_direction = self._get_inv_direction()
        
        if self.direction == 'vert':
            x_L, w_L = primary_axis_split_L
            x_R, w_R = primary_axis_split_R
            y_D, h_D = secondary_axis_split_L
            y_U, h_U = secondary_axis_split_R
            LU = Surface((x_L, y_U), (w_L, h_U), new_split_direction)
            RU = Surface((x_R, y_U), (w_R, h_U), new_split_direction)
            LD = Surface((x_L, y_D), (w_L, h_D), new_split_direction)
            RD = Surface((x_R, y_D), (w_R, h_D), new_split_direction)
        elif self.direction == 'hori':
            x_L, w_L = secondary_axis_split_L
            x_R, w_R = secondary_axis_split_R
            y_D, h_D = primary_axis_split_L
            y_U, h_U = primary_axis_split_R
            LU = Surface((x_L, y_U), (w_L, h_U), new_split_direction)
            RU = Surface((x_R, y_U), (w_R, h_U), new_split_direction)
            LD = Surface((x_L, y_D), (w_L, h_D), new_split_direction)
            RD = Surface((x_R, y_D), (w_R, h_D), new_split_direction)
        else:
            assert False
        
        return split_idx, path_idx, [LU, RU, LD, RD]
    
    def min_dim(self):
        return min([self.width, self.height])
    
    def _get_inv_direction(self):
        if self.direction == 'hori':
            return 'vert'
        elif self.direction == 'vert':
            return 'hori'
        else:
            assert False